"""
Functions to create different core and extension tables following the
Darwin Core (DwC) standard from a Wildlife Insights data.
"""
import json
import pathlib

import numpy as np
import pandas as pd

from . import _dwc, _labels
from .extraction import get_lowest_taxon
from .filtering import remove_duplicates, remove_unidentified


def _gs_to_https(location: pd.Series) -> pd.Series:
    base_url = "https://console.cloud.google.com/storage/browser/"
    bucket = location.str.split("/").str[2]
    uri = location.str.split("/").str[3:].str.join("/")

    return base_url + bucket + "/" + uri


def create_dwc_archive(
    cameras: pd.DataFrame,
    deployments: pd.DataFrame,
    images: pd.DataFrame,
    projects: pd.DataFrame,
    remove_duplicate_kws: dict = None,
) -> tuple:
    """
    Creates a Darwin Core Archive consisting of four different cores and
    extensions: Event, Occurrence, Measurement or Facts and Simple
    Multimedia.

    Parameters
    ----------
    cameras : DataFrame
        Dataframe with the bundle's cameras.
    deployments : DataFrame
        Dataframe with the bundle's deployments.
    images : DataFrame
        Dataframe with the bundle's cameras.
    projects : DataFrame
        Dataframe with the bundle's projects.
    remove_duplicate_kws : dict
        Keyword arguments passed to the wiutils.remove_duplicate function.
        Used for the creation of the Occurrence Core.

    Returns
    -------
    DataFrame
        Darwin Core Event dataframe.
    DataFrame
        Darwin Core Occurrence dataframe.
    DataFrame
        Darwin Core Measurement or Facts dataframe.
    DataFrame
        Darwin Core Simple Multimedia dataframe.

    """
    event = create_dwc_event(deployments, projects)
    occurrence = create_dwc_occurrence(
        images, deployments, projects, remove_duplicate_kws
    )
    measurement = create_dwc_measurement(cameras, deployments)
    multimedia = create_dwc_multimedia(images, deployments)

    return event, occurrence, measurement, multimedia


def create_dwc_event(
    deployments: pd.DataFrame,
    projects: pd.DataFrame,
) -> pd.DataFrame:
    """
    Creates a Darwin Core Event dataframe from deployments and projects
    information. See https://rs.gbif.org/core/dwc_event_2022-02-02.xml
    for more information about this core.

    Parameters
    ----------
    deployments : DataFrame
        Dataframe with the bundle's deployments.
    projects : DataFrame
        Dataframe with the bundle's projects.

    Returns
    -------
    DataFrame
        Darwin Core Event dataframe.

    """
    df = pd.merge(deployments, projects, on=_labels.deployments.project_id, how="left")
    df[_labels.deployments.start] = pd.to_datetime(df[_labels.deployments.start])
    df[_labels.deployments.end] = pd.to_datetime(df[_labels.deployments.end])

    core = df.rename(columns=_dwc.event.mapping)
    core = core[core.columns[core.columns.isin(_dwc.event.order)]]

    for term, value in _dwc.event.constants.items():
        core[term] = value

    delta = df[_labels.deployments.end] - df[_labels.deployments.start]
    core["samplingEffort"] = delta.dt.days.astype(str) + " trap-nights"

    core["eventDate"] = (
        df[_labels.deployments.start].dt.strftime("%Y-%m-%d")
        + "/"
        + df[_labels.deployments.end].dt.strftime("%Y-%m-%d")
    )

    with open(pathlib.Path(__file__).parent.joinpath("_dwc/countries.json")) as f:
        countries = pd.DataFrame(json.load(f))
        core["countryCode"] = core["countryCode"].map(
            countries.set_index("alpha-3")["alpha-2"]
        )

    core = core.reindex(columns=_dwc.event.order)

    return core


def create_dwc_measurement(
    deployments: pd.DataFrame,
    cameras: pd.DataFrame,
) -> pd.DataFrame:
    """
    Creates a Darwin Core Measurement or Facts dataframe from cameras and
    deployments information. See https://rs.gbif.org/extension/dwc/measurements_or_facts_2022-02-02.xml
    for more information about this extension.

    Parameters
    ----------
    deployments : DataFrame
        Dataframe with the bundle's deployments.
    cameras : DataFrame
        Dataframe with the bundle's cameras.

    Returns
    -------
    DataFrame
        Darwin Core Measurement or Facts dataframe.

    """
    df = pd.merge(deployments, cameras, on=_labels.deployments.camera_id, how="left")

    extension = pd.DataFrame()
    for item in _dwc.measurement.mapping:
        temp = pd.DataFrame()
        temp["eventID"] = df.loc[:, _labels.deployments.deployment_id]
        temp["measurementType"] = item["type"]
        temp["measurementValue"] = df.loc[:, item["value"]]
        temp["measurementUnit"] = item["unit"]
        if item["remarks"]:
            temp["measurementRemarks"] = df.loc[:, item["remarks"]]
        else:
            temp["measurementRemarks"] = np.nan
        extension = pd.concat([extension, temp], ignore_index=True)

    extension = extension.dropna(subset=["measurementValue"]).reset_index(drop=True)

    return extension


def create_dwc_multimedia(
    images: pd.DataFrame, deployments: pd.DataFrame
) -> pd.DataFrame:
    """
    Creates a Darwin Core Simple Multimedia dataframe from images and
    deployments information. See https://rs.gbif.org/extension/gbif/1.0/multimedia.xml
    for more information about this extension. The result includes
    information from all the bundle's images.

    Parameters
    ----------
    images : DataFrame
        Dataframe with the bundle's images.
    deployments : DataFrame
        Dataframe with the bundle's deployments.

    Returns
    -------
    DataFrame
        Darwin Core Simple Multimedia dataframe.

    """
    df = pd.merge(images, deployments, on=_labels.images.deployment_id, how="left")
    df[_labels.images.url] = _gs_to_https(df[_labels.images.url])

    extension = df.rename(columns=_dwc.multimedia.mapping)
    extension = extension[
        extension.columns[extension.columns.isin(_dwc.multimedia.order)]
    ]

    for term, value in _dwc.multimedia.constants.items():
        extension[term] = value

    extension["title"] = get_lowest_taxon(images, return_rank=False).fillna(
        "Blank or unidentified"
    )

    extension = extension.reindex(columns=_dwc.multimedia.order)

    return extension


def create_dwc_occurrence(
    images: pd.DataFrame,
    deployments: pd.DataFrame,
    projects: pd.DataFrame,
    remove_duplicate_kws: dict = None,
) -> pd.DataFrame:
    """
    Creates a Darwin Core Occurrence dataframe from images, deployments
    and projects information. See https://rs.gbif.org/core/dwc_occurrence_2022-02-02.xml
    for more information about this core. The result includes only
    wildlife records (i.e. unidentified and duplicate images are removed).

    Parameters
    ----------
    images : DataFrame
        Dataframe with the bundle's images.
    deployments : DataFrame
        Dataframe with the bundle's deployments.
    projects : DataFrame
        Dataframe with the bundle's projects.
    remove_duplicate_kws : dict
        Keyword arguments passed to the wiutils.remove_duplicate function.

    Returns
    -------
    DataFrame
        Darwin Core Occurrence dataframe.

    """
    if remove_duplicate_kws is None:
        remove_duplicate_kws = {}
    remove_duplicate_kws.update(dict(reset_index=False))

    images = images.copy()
    images = remove_unidentified(images, rank="class")
    filtered = remove_duplicates(images, **remove_duplicate_kws)

    df = pd.merge(
        filtered,
        deployments.drop(columns=_labels.deployments.project_id),
        on=_labels.images.deployment_id,
        how="left",
    )
    df = pd.merge(df, projects, on=_labels.images.project_id, how="left")
    df[_labels.images.date] = pd.to_datetime(df[_labels.images.date])

    core = df.rename(columns=_dwc.occurrence.mapping)
    core = core[core.columns[core.columns.isin(_dwc.occurrence.order)]]

    for term, value in _dwc.occurrence.constants.items():
        core[term] = value

    core["eventDate"] = df[_labels.images.date].dt.strftime("%Y-%m-%d")
    core["eventTime"] = df[_labels.images.date].dt.strftime("%H:%M:%S")

    images.loc[filtered.index, "__seq"] = np.arange(len(filtered))
    images["__seq"] = images["__seq"].fillna(method="ffill")
    images[_labels.images.url] = _gs_to_https(images[_labels.images.url])
    core["associatedMedia"] = images.groupby("__seq").agg(
        {_labels.images.url: "|".join}
    )

    filtered = filtered.reset_index(drop=True)
    taxa, ranks = get_lowest_taxon(filtered, return_rank=True)
    epithets = filtered[_labels.images.species].str.split(" ", expand=True)
    core["scientificName"] = taxa
    core["taxonRank"] = ranks
    core["specificEpithet"] = epithets[0]
    core["infraspecificEpithet"] = epithets.get(1, np.nan)

    core = core.reindex(columns=_dwc.occurrence.order)

    return core
