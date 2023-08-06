"""
Taxonomy utilities.
"""
import numpy as np
import pandas as pd

from .. import _labels

taxonomy_columns = [
    _labels.images.class_,
    _labels.images.order,
    _labels.images.family,
    _labels.images.genus,
    _labels.images.species,
]


def compute_taxonomic_rank(images: pd.DataFrame) -> pd.Series:
    """
    Computes the taxonomic rank of the most specific identification for
    each image.

    Parameters
    ----------
    images : DataFrame
        DataFrame with records.

    Returns
    -------
    Series
        Series with the corresponding taxonomic ranks.

    """
    images = replace_unidentified(images)

    ranks = pd.Series(np.nan, index=images.index)
    for column in reversed(taxonomy_columns):
        has_rank = ranks.notna()
        has_identification = images[column].notna()
        ranks.loc[(~has_rank & has_identification)] = column

    # Because there is no column for infraspecific epithet, it is assumed
    # that all the records with two words on the species column has
    # a subspecies rank.
    words = images[_labels.images.species].str.split(" ").str.len()
    ranks.loc[words == 2] = "subspecies"

    return ranks


def get_taxonomy_columns(rank: str) -> list:
    """
    Gets a list of columns for a specific rank along with all the
    inferior taxonomic ranks.

    Parameters
    ----------
    rank : str
        Taxonomic rank.

    Returns
    -------
    list
        List with columns names for the taxonomic ranks.

    """
    if rank == "species":
        columns = taxonomy_columns[-1:]
    elif rank == "genus":
        columns = taxonomy_columns[-2:]
    elif rank == "family":
        columns = taxonomy_columns[-3:]
    elif rank == "order":
        columns = taxonomy_columns[-4:]
    elif rank == "class":
        columns = taxonomy_columns[-5:]
    else:
        raise ValueError(
            "min_rank must be one of: ['species', 'genus', 'family', 'order', 'class']."
        )

    return columns


def replace_unidentified(images: pd.DataFrame) -> pd.DataFrame:
    """
    Replaces unidentified taxa with NaN.

    Parameters
    ----------
    images : DataFrame
        DataFrame with records.

    Returns
    -------
    DataFrame
        Copy of images with replaced unidentified values.

    """
    images = images.copy()
    unidentified_values = ["No CV Result", "Unknown"]
    images.loc[:, taxonomy_columns] = images.loc[:, taxonomy_columns].replace(
        unidentified_values, np.nan
    )

    return images
