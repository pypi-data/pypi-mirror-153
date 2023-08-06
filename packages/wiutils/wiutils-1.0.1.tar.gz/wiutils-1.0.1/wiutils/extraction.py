"""
Functions for extracting information from WI tables.
"""
from typing import Union

import numpy as np
import pandas as pd

from . import _labels, _utils


def get_date_ranges(
    images: pd.DataFrame = None,
    deployments: pd.DataFrame = None,
    source: str = "both",
    compute_delta: bool = False,
    pivot: bool = False,
) -> pd.DataFrame:
    """
    Gets deployment date ranges using information from either images,
    deployments or both.

    Parameters
    ----------
    images : DataFrame
        DataFrame with the project's images.
    deployments : DataFrame
        DataFrame with the project's deployments.
    source : bool
        Source to plot date ranges from: Values can be:

            - 'images' to plot date ranges from images (i.e. first image
            to last image taken).
            - 'deployments' to plot date ranges from deployments
            information (i.e. start date and end date).
            - 'both' to plot both sources in two different subplots.
    compute_delta : bool
        Whether to compute the delta (in days) between the start and end
        dates.
    pivot : bool
        Whether to pivot (reshape from long to wide format) the resulting
        DataFrame.

    Returns
    -------
    DataFrame
        DataFrame with date ranges.

    """
    df = pd.DataFrame()

    if source == "images" or source == "both":
        if images is None:
            raise ValueError("images DataFrame must be provided.")
        images = images.copy()
        images[_labels.images.date] = pd.to_datetime(images[_labels.images.date])
        images[_labels.images.date] = pd.to_datetime(
            images[_labels.images.date].dt.date
        )
        dates = images.groupby(_labels.images.deployment_id)[_labels.images.date].agg(
            start_date="min", end_date="max"
        )
        dates["source"] = "images"
        df = pd.concat([df, dates.reset_index()], ignore_index=True)

    if source == "deployments" or source == "both":
        if deployments is None:
            raise ValueError("deployments DataFrame must be provided.")
        deployments = deployments.copy()
        deployments[_labels.deployments.start] = pd.to_datetime(
            deployments[_labels.deployments.start]
        )
        deployments[_labels.deployments.end] = pd.to_datetime(
            deployments[_labels.deployments.end]
        )
        dates = deployments.loc[
            :,
            [
                _labels.deployments.deployment_id,
                _labels.deployments.start,
                _labels.deployments.end,
            ],
        ]
        dates["source"] = "deployments"
        df = pd.concat([df, dates], ignore_index=True)

    if source not in ("images", "deployments", "both"):
        raise ValueError("source must be one of ['images', 'deployments', 'both']")

    if compute_delta:
        delta = df["end_date"] - df["start_date"]
        df["delta"] = delta.dt.days

    if pivot:
        df = df.pivot(index="deployment_id", columns="source")

    return df


def get_lowest_taxon(
    images: pd.DataFrame, return_rank: bool = False
) -> Union[pd.Series, tuple]:
    """
    Gets the lowest identified taxa and ranks.

    Parameters
    ----------
    images : DataFrame
        DataFrame with the project's images.
    return_rank : bool
        Whether to return the lowest identified ranks.

    Returns
    -------
    Series
        Lowest identified taxon for each image.
    Series
        Lowest identified rank for each image.

    """
    ranks = _utils.taxonomy.compute_taxonomic_rank(images)
    taxa = get_scientific_name(images, keep_genus=False, add_qualifier=False)

    mask = (taxa.isna()) & (ranks.notna())
    sorted_columns = np.argsort(images.columns)
    column_indices = np.searchsorted(images.columns[sorted_columns], ranks.loc[mask])
    indices = sorted_columns[column_indices]
    taxa.loc[mask] = images.loc[mask].values[np.arange(mask.sum()), indices]

    if return_rank:
        return taxa, ranks
    else:
        return taxa


def get_scientific_name(
    images: pd.DataFrame,
    keep_genus: bool = False,
    add_qualifier: bool = False,
) -> pd.Series:
    """
    Gets the scientific name of each image by concatenating their
    respective genus and specific epithet.

    Parameters
    ----------
    images : DataFrame
        DataFrame with the project's images.
    keep_genus: bool
        Whether to keep the genus as the scientific name in images where
        only the genus was identified. If False, the scientific name for
        those cases will be emtpy.
    add_qualifier
        Whether to add an open nomenclature qualifier (sp.) to the
        scientific name of those cases where only the genus was
        identified. Only has effect if keep_genus is True.

    Returns
    -------
    Series
        Series with the corresponding scientific names.

    """
    names = pd.Series(np.nan, index=images.index, dtype=str)

    exclude = ["No CV Result", "Unknown"]
    has_genus = (
        ~images[_labels.images.genus].isin(exclude)
        & images[_labels.images.genus].notna()
    )
    has_epithet = (
        ~images[_labels.images.species].isin(exclude)
        & images[_labels.images.species].notna()
    )

    mask = has_genus & has_epithet
    names.loc[mask] = (
        images.loc[mask, _labels.images.genus]
        + " "
        + images.loc[mask, _labels.images.species]
    )

    if keep_genus:
        mask = has_genus & ~has_epithet
        names.loc[mask] = images.loc[mask, _labels.images.genus]
        if add_qualifier:
            names.loc[mask] += " sp."

    return names
