"""
Functions to create new tables or modify existing ones from WI data.
"""
from typing import Union

import numpy as np
import pandas as pd

from . import _labels, _utils
from .extraction import get_lowest_taxon
from .filtering import remove_duplicates, remove_unidentified


def _compute_q_diversity_index(p: Union[list, tuple, np.ndarray], q: int) -> float:
    if q == 1:
        return np.exp(-np.sum(p * np.log(p)))
    else:
        return np.sum(p**q) ** (1 / (1 - q))


def _process_groupby_arg(
    images: pd.DataFrame, deployments: pd.DataFrame, groupby: str
) -> tuple:
    if groupby == "deployment":
        groupby_label = _labels.images.deployment_id
    elif groupby == "location":
        groupby_label = _labels.deployments.location
        if deployments is not None:
            images = pd.merge(
                images,
                deployments[
                    [_labels.deployments.deployment_id, _labels.deployments.location]
                ],
                left_on=_labels.images.deployment_id,
                right_on=_labels.deployments.deployment_id,
                how="left",
            )
        else:
            raise ValueError("deployments must be passed if groupby is 'location'")
    else:
        raise ValueError("groupby must be one of ['deployment', 'location']")

    return images, groupby_label


def compute_count_summary(
    images: pd.DataFrame,
    deployments: pd.DataFrame = None,
    groupby: str = "deployment",
    add_records_by_class: bool = False,
    add_species_by_class: bool = False,
    remove_unidentified_kws: dict = None,
    remove_duplicates_kws: dict = None,
) -> pd.DataFrame:
    """
    Computes a summary of images, records and taxa count by deployment.

    Parameters
    ----------
    images : DataFrame
        DataFrame with the project's images.
    deployments : DataFrame
        DataFrame with the project's deployments. Must be passed only if
        groupby is 'location'.
    groupby : str
        Level to group results by. Can be one of:

            - 'deployment' to group by deployment (deployment_id)
            - 'location' to group by location (placename)
    add_records_by_class : bool
        Whether to add number of independent records discriminated by
        taxonomic class.
    add_species_by_class : bool
        Whether to add number of species discriminated by taxonomic class.
    remove_unidentified_kws : dict
        Keyword arguments for the wiutils.remove_unidentified function.
    remove_duplicates_kws : dict
        Keyword arguments for the wiutils.remove_duplicates function.

    Returns
    -------
    DataFrame
        Summary of images, records and species count by deployment.

    """
    images = images.copy()

    if remove_unidentified_kws is None:
        remove_unidentified_kws = {"rank": "class"}
    if remove_duplicates_kws is None:
        remove_duplicates_kws = {}

    images, groupby_label = _process_groupby_arg(images, deployments, groupby)
    result = pd.DataFrame(index=sorted(images[groupby_label].unique()))
    result = result.join(images.groupby(groupby_label).size().rename("total_images"))
    images = remove_unidentified(images, **remove_unidentified_kws)
    result = result.join(
        images.groupby(groupby_label).size().rename("identified_images")
    )
    images = remove_duplicates(images, **remove_duplicates_kws)

    result = result.join(
        images.groupby(groupby_label)[_labels.images.objects].sum().rename("records")
    )
    if add_records_by_class:
        classes = images[_labels.images.class_].dropna().unique()
        for class_ in classes:
            subset = images[images[_labels.images.class_] == class_]
            result = result.join(
                subset.groupby(groupby_label)[_labels.images.objects]
                .sum()
                .rename(f"records_{class_.lower()}")
            )

    images["taxon"] = get_lowest_taxon(images, return_rank=False)
    result = result.join(
        images.groupby(groupby_label)["taxon"].nunique().rename("taxa")
    )
    if add_species_by_class:
        classes = images[_labels.images.class_].dropna().unique()
        for class_ in classes:
            subset = images[images[_labels.images.class_] == class_]
            result = result.join(
                subset.groupby(groupby_label)["taxon"]
                .nunique()
                .rename(f"taxa_{class_.lower()}")
            )

    result.index.name = groupby_label
    result = result.reset_index()
    result.iloc[:, 1:] = result.iloc[:, 1:].fillna(0).astype(int)

    return result


def compute_detection(
    images: pd.DataFrame,
    deployments: pd.DataFrame = None,
    groupby: str = "deployment",
    compute_abundance: bool = True,
    pivot: bool = False,
):
    """
    Computes the detection (in terms of abundance or presence) of each
    taxon by deployment.

    Parameters
    ----------
    images : DataFrame
        DataFrame with the project's images.
    deployments : DataFrame
        DataFrame with the project's deployments. Must be passed only if
        groupby is 'location'.
    groupby : str
        Level to group results by. Can be one of:

            - 'deployment' to group by deployment (deployment_id)
            - 'location' to group by location (placename)
    compute_abundance : bool
        Whether to compute the abundance for each deployment. If False,
        returns presence/absence for the deployments.
    pivot : bool
        Whether to pivot (reshape from long to wide format) the resulting
        DataFrame.

    Returns
    -------
    DataFrame
        DataFrame with the detection of each species by deployment.

    """
    images = images.copy()

    images, groupby_label = _process_groupby_arg(images, deployments, groupby)
    images["taxon"] = get_lowest_taxon(images, return_rank=False)
    result = images.groupby(["taxon", groupby_label])[_labels.images.objects].sum()
    taxa = images["taxon"].unique()
    sites = images[groupby_label].unique()
    idx = pd.MultiIndex.from_product([taxa, sites], names=["taxon", groupby_label])
    result = result.reindex(idx, fill_value=0)
    result.name = "value"
    result = result.reset_index()

    if not compute_abundance:
        has_observations = result["value"] > 0
        result.loc[has_observations, "value"] = 1

    result = result.sort_values(["taxon", groupby_label], ignore_index=True)

    if pivot:
        result = result.pivot(index="taxon", columns=groupby_label, values="value")
        result = result.rename_axis(None, axis=1).reset_index()

    return result


def compute_detection_history(
    images: pd.DataFrame,
    deployments: pd.DataFrame,
    date_range: str = "deployments",
    days: int = 1,
    compute_abundance: bool = True,
    pivot: bool = False,
) -> pd.DataFrame:
    """
    Computes the detection history (in terms of abundance or presence) by
    taxon and deployment, grouping observations into specific days-long
    intervals.

    Parameters
    ----------
    images : DataFrame
        DataFrame with the project's images.
    deployments : DataFrame
        DataFrame with the project's deployments.
    date_range : str
        Table to compute the date range from. Possible values are:

            - 'deployments'
            - 'images'
    days : int
        Days interval to group observations into.
    compute_abundance : bool
        Whether to compute the abundance for each interval. If False,
        returns presence/absence for the intervals.
    pivot : bool
        Whether to pivot (reshape from long to wide format) the resulting
        DataFrame.

    Returns
    -------
    DataFrame
        Detection history.

    """
    images = images.copy()
    deployments = deployments.copy()

    images[_labels.images.date] = pd.to_datetime(images[_labels.images.date])
    images[_labels.images.date] = pd.to_datetime(images[_labels.images.date].dt.date)
    deployments[_labels.deployments.start] = pd.to_datetime(
        deployments[_labels.deployments.start]
    )
    deployments[_labels.deployments.end] = pd.to_datetime(
        deployments[_labels.deployments.end]
    )
    if date_range == "deployments":
        start = deployments[_labels.deployments.start].min()
        end = deployments[_labels.deployments.end].max()
    elif date_range == "images":
        start = images[_labels.images.date].min()
        end = images[_labels.images.date].max()
    else:
        raise ValueError("date_range must be one of ['deployments', 'images'].")

    images["taxon"] = get_lowest_taxon(images, return_rank=False)
    freq = pd.Timedelta(days=days)
    groupers = [
        pd.Grouper(key="taxon"),
        pd.Grouper(key=_labels.images.deployment_id),
        pd.Grouper(key=_labels.images.date, freq=freq, origin=start),
    ]
    result = images.groupby(groupers)[_labels.images.objects].sum()

    # A new index with all the combinations of species, sites and dates
    # is created to reindex the result and to assign zeros where there
    # were no observations.
    species = images["taxon"].unique()
    sites = images[_labels.images.deployment_id].unique()
    dates = pd.date_range(start, end, freq=freq)
    idx = pd.MultiIndex.from_product(
        [species, sites, dates],
        names=["taxon", _labels.images.deployment_id, _labels.images.date],
    )
    result = result.reindex(idx, fill_value=0)
    result.name = "value"
    result = result.reset_index()

    if not compute_abundance:
        has_observations = result["value"] > 0
        result.loc[has_observations, "value"] = 1

    # Groups (i.e. days intervals) where the corresponding camera was not
    # deployed at the time are assigned NaNs.
    result = pd.merge(
        result,
        deployments[
            [
                _labels.images.deployment_id,
                _labels.deployments.start,
                _labels.deployments.end,
            ]
        ],
        on=_labels.images.deployment_id,
        how="left",
    )
    group_start = result[_labels.images.date]
    group_end = result[_labels.images.date] + pd.Timedelta(days=days - 1)
    inside_range_left = group_start.between(
        result[_labels.deployments.start], result[_labels.deployments.end]
    )
    inside_range_right = group_end.between(
        result[_labels.deployments.start], result[_labels.deployments.end]
    )
    inside_range = inside_range_left | inside_range_right
    result.loc[~inside_range, "value"] = np.nan
    result = result.drop(columns=[_labels.deployments.start, _labels.deployments.end])

    result = result.sort_values(
        ["taxon", _labels.images.deployment_id, _labels.images.date], ignore_index=True
    )

    if pivot:
        result[_labels.images.date] = result[_labels.images.date].astype(str)
        result = result.pivot(
            index=["taxon", _labels.images.deployment_id],
            columns=_labels.images.date,
            values="value",
        )
        result = result.rename_axis(None, axis=1).reset_index()

    return result


def compute_general_count(
    images: pd.DataFrame,
    deployments: pd.DataFrame = None,
    groupby: str = "deployment",
    add_taxonomy: bool = False,
    rank: str = "class",
):
    """
    Computes the general abundance and number of deployments for each
    taxon.

    Parameters
    ----------
    images : DataFrame
        DataFrame with the project's images.
    deployments : DataFrame
        DataFrame with the project's deployments. Must be passed only if
        groupby is 'location'.
    groupby : str
        Level to group results by. Can be one of:

            - 'deployment' to group by deployment (deployment_id)
            - 'location' to group by location (placename)
    add_taxonomy : bool
        Whether to add the superior taxonomy of the species to the result.
    rank : str
        Upper taxonomic rank to extract classification for. Possible
        values are:

            - 'epithet'
            - 'genus'
            - 'family'
            - 'order'
            - 'class'
        For example, if rank is 'family', the result will have the
        corresponding family (and therefore the inferior ranks - genus
        and epithet -) were not identified will be removed.

    Returns
    -------
    DataFrame
        DataFrame with abundance and number of deployments by species.

    """
    images = images.copy()

    images, groupby_label = _process_groupby_arg(images, deployments, groupby)
    images["taxon"] = get_lowest_taxon(images, return_rank=False)
    result = images.groupby("taxon").agg(
        {_labels.images.objects: "sum", groupby_label: "nunique"}
    )
    result = result.rename(
        columns={_labels.images.objects: "records", groupby_label: f"{groupby}s"}
    )
    result = result.reset_index()

    if add_taxonomy:
        taxonomy_columns = _utils.taxonomy.get_taxonomy_columns(rank)
        taxonomy = images[["taxon", *taxonomy_columns]].drop_duplicates("taxon")
        result = pd.merge(result, taxonomy, on="taxon", how="left")

    return result


def compute_hill_numbers(
    images: pd.DataFrame,
    deployments: pd.DataFrame = None,
    groupby: str = "deployment",
    q_values: Union[int, list, tuple, np.ndarray] = (0, 1, 2),
    pivot: bool = False,
) -> pd.DataFrame:
    """
    Computes the Hill numbers of order q (also called effective number of
    species) by site for some given values of q.

    Parameters
    ----------
    images : DataFrame
        DataFrame with the project's images.
    deployments : DataFrame
        DataFrame with the project's deployments. Must be passed only if
        groupby is 'location'.
    groupby : str
        Level to group results by. Can be one of:

            - 'deployment' to group by deployment (deployment_id)
            - 'location' to group by location (placename)
    q_values : int, list, tuple or array
        Value(s) of q to compute Hill numbers for.
    pivot : bool
        Whether to pivot (reshape from long to wide format) the resulting
        DataFrame.

    Returns
    -------
    DataFrame
        Computed Hill numbers by deployment.

    """
    images = images.copy()

    if isinstance(q_values, int):
        q_values = [q_values]

    result = []

    images, groupby_label = _process_groupby_arg(images, deployments, groupby)
    images["taxon"] = get_lowest_taxon(images, return_rank=False)
    abundance = images.groupby([groupby_label, "taxon"])[_labels.images.objects].sum()
    relative_abundance = abundance / abundance.groupby(level=0).sum()
    for site, group in relative_abundance.groupby(level=0):
        for q in q_values:
            row = {
                groupby_label: site,
                "q": q,
                "D": _compute_q_diversity_index(group.to_numpy(), q),
            }
            result.append(row)

    result = pd.DataFrame(result)

    if pivot:
        result["q"] = result["q"].astype(str)
        result = result.pivot(index=groupby_label, columns="q", values="D")
        result = result.rename_axis(None, axis=1).reset_index()

    return result
