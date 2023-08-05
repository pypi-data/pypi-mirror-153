"""
Functions to filter WI images based on different conditions.
"""
import numpy as np
import pandas as pd

from . import _domestic, _labels, _utils
from .extraction import get_lowest_taxon


def remove_domestic(images: pd.DataFrame, reset_index: bool = True) -> pd.DataFrame:
    """
    Removes images where the identification corresponds to a domestic
    species. See wiutils/_domestic for a list of the genera considered
    as domestic.

    Parameters
    ----------
    images : DataFrame
        DataFrame with the project's images.
    reset_index : bool
        Whether to reset the index of the resulting DataFrame. If True,
        the index will be numeric from 0 to the length of the result.

    Returns
    -------
    DataFrame
        Copy of images with removed domestic species.

    """
    images = images.copy()
    images = images[~images[_labels.images.genus].isin(_domestic.genera)]

    if reset_index:
        images = images.reset_index(drop=True)

    return images


def remove_duplicates(
    images: pd.DataFrame,
    interval: int = 30,
    unit: str = "minutes",
    reset_index: bool = True,
) -> pd.DataFrame:
    """
    Removes duplicate records (images) from the same taxon in the same
    deployment given a time interval.

    Parameters
    ----------
    images : DataFrame
        DataFrame with the project's images.
    interval : int
        Time interval (for a specific time unit).
    unit : str
        Time unit. Possible values are:

            - 'weeks'
            - 'days'
            - 'hours'
            - 'minutes'
            - 'seconds'
    reset_index : bool
        Whether to reset the index of the resulting DataFrame. If True,
        the index will be numeric from 0 to the length of the result.

    Returns
    -------
    DataFrame
        Copy of images with removed duplicates.

    """
    if unit not in ("weeks", "days", "hours", "minutes", "seconds"):
        raise ValueError(
            "unit must be one of ['weeks', 'days', 'hours', 'minutes', 'seconds']"
        )

    images = images.copy()
    images["taxon"] = get_lowest_taxon(images, return_rank=False)

    df = images.copy()
    df[_labels.images.date] = pd.to_datetime(df[_labels.images.date])

    df = df.sort_values([_labels.images.deployment_id, "taxon", _labels.images.date])
    delta = df.groupby([_labels.images.deployment_id, "taxon"])[
        _labels.images.date
    ].diff()
    mask = (delta >= pd.Timedelta(**{unit: interval})) | (delta.isna())

    images_reference = images.dropna(subset=["taxon"])
    images_reference = images_reference.sort_values(
        [_labels.images.deployment_id, "taxon", _labels.images.date]
    )
    df = images_reference.loc[mask]
    df = pd.concat([df, images[images["taxon"].isna()]])
    df = df.sort_index()

    if reset_index:
        df = df.reset_index(drop=True)

    df = df.drop(columns="taxon")

    return df


def remove_inconsistent_dates(
    images: pd.DataFrame, deployments: pd.DataFrame, reset_index: bool = True
) -> pd.DataFrame:
    """
    Removes images where the timestamp is outside the date range of the
    corresponding deployment.

    Parameters
    ----------
    images : DataFrame
        DataFrame with the project's images.
    deployments : pd.DataFrame
        DataFrame with the project's deployments.
    reset_index : bool
        Whether to reset the index of the resulting DataFrame. If True,
        the index will be numeric from 0 to the length of the result.

    Returns
    -------
    DataFrame
        Images DataFrame with removed inconsistent images.

    """
    df = images.copy()
    deployments = deployments.copy()

    df[_labels.images.date] = pd.to_datetime(df[_labels.images.date])
    deployments[_labels.deployments.start] = pd.to_datetime(
        deployments[_labels.deployments.start]
    )
    deployments[_labels.deployments.end] = pd.to_datetime(
        deployments[_labels.deployments.end]
    )

    df[_labels.images.date] = pd.to_datetime(df[_labels.images.date].dt.date)
    df = pd.merge(
        df,
        deployments[
            [
                _labels.deployments.deployment_id,
                _labels.deployments.start,
                _labels.deployments.end,
            ]
        ],
        on=_labels.images.deployment_id,
        how="left",
    )
    df["__is_between"] = df[_labels.images.date].between(
        df[_labels.deployments.start], df[_labels.deployments.end]
    )
    df = images[df["__is_between"]]

    if reset_index:
        df = df.reset_index(drop=True)

    return df


def remove_unidentified(
    images: pd.DataFrame, rank: str = "genus", reset_index: bool = True
) -> pd.DataFrame:
    """
    Removes unidentified (up to a specific taxonomic rank) images.

    Parameters
    ----------
    images : DataFrame
        DataFrame with the project's images.
    rank : str
        Taxonomic rank for which images that do not have an identification
        will be removed. Possible values are:

            - 'species'
            - 'genus'
            - 'family'
            - 'order'
            - 'class'
        For example, if rank is 'family', all images where the family
        (and therefore the inferior ranks - genus and epithet -) were
        not identified will be removed.
    reset_index : bool
        Whether to reset the index of the resulting DataFrame. If True,
        the index will be numeric from 0 to the length of the result.

    Returns
    -------
    DataFrame
        Images DataFrame with removed unidentified images.

    """
    images = images.copy()

    taxonomy_columns = _utils.taxonomy.get_taxonomy_columns(rank)
    exclude = ["No CV Result", "Unknown"]
    images[taxonomy_columns] = images[taxonomy_columns].replace(exclude, np.nan)
    images = images.dropna(subset=taxonomy_columns, how="all")

    if reset_index:
        images = images.reset_index(drop=True)

    return images
