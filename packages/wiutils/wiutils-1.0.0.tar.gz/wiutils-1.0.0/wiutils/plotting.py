"""
Functions to plot information from the images and deployments tables.
"""
import pathlib
from typing import Union

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from . import _labels
from .extraction import get_date_ranges, get_lowest_taxon
from .summarizing import compute_detection_history

CONFIG_FILE = pathlib.Path(__file__).parents[0].joinpath("config/mplstyle")


def _plot_polar(
    df: pd.DataFrame,
    y: str,
    hue: str = None,
    density: bool = False,
    kind: str = "hist",
    fill: bool = True,
) -> plt.PolarAxes:
    unique_values = df[hue].unique()
    width = 2 * np.pi / 24
    ax = plt.subplot(polar=True)
    handles = []
    for i, value in enumerate(unique_values):
        mask = df[hue] == value
        subset = df[mask]
        hist, edges = np.histogram(subset[y], bins=np.arange(25), density=density)
        if kind == "area":
            theta = np.arange(24) * width + (width / 2)
            theta = np.append(theta, theta[0])
            hist = np.append(hist, hist[0])
            handle = ax.plot(theta, hist, label=value)
            if fill:
                plt.fill(theta, hist, alpha=0.25)
        elif kind == "hist":
            theta = np.arange(24) * width
            if fill:
                edgecolor = "black"
                linewidth = 0.75
            else:
                edgecolor = f"C{i}"
                linewidth = 1
            handle = ax.bar(
                theta,
                hist,
                width,
                fill=fill,
                align="edge",
                label=value,
                edgecolor=edgecolor,
                linewidth=linewidth,
                alpha=0.75,
                zorder=2,
            )
        handles.append(handle)

    ax.legend()

    return ax


@mpl.rc_context(fname=CONFIG_FILE)
def plot_activity_hours(
    images: pd.DataFrame,
    names: Union[list, str, pd.Series],
    kind: str = "kde",
    polar: bool = False,
    hist_kws: dict = None,
    kde_kws: dict = None,
    polar_kws: dict = None,
) -> Union[plt.Axes, plt.PolarAxes]:
    """
    Plots the activity hours of one or multiple taxa by grouping all
    observations into a 24-hour range.

    Parameters
    ----------
    images : DataFrame
        DataFrame with the project's images.
    names : list, str or Series
        List of names to plot activity hours for.
    kind : str
        Type of plot. Values can be:

        - 'hist' for histogram.
        - 'kde' for kernel density estimate plot.
    polar : bool
        Whether to use a polar (i.e. circular projection) for the plot.
        If polar is True, kind must be one of 'area' or 'hist'. Otherwise
        it must be one of 'hist' or 'kde'.
    hist_kws : dict
        Keyword arguments passed to the seaborn.histplot() function. Only
        has effect if kind is 'hist' and polar is False.
    kde_kws : dict
        Keyword arguments passed to the seaborn.kde() function. Only
        has effect if kind is 'kde'.
    polar_kws : dict
        Keyword arguments passed to a local function when polar is True,
        regardless of kind. Possible arguments are:

            - 'density': True or False. Whether to compute density or
            counts. Default is False.
            - 'fill': True or False. Whether to fill the area under the
            line (when kind is 'area') or the rectangles (when kind is
            'hist'). Default is True.

    Returns
    -------
    Axes
        Plot axes.

    """
    if isinstance(names, str):
        names = [names]

    if hist_kws is None:
        hist_kws = {}
    if kde_kws is None:
        kde_kws = {}
    if polar_kws is None:
        polar_kws = {}

    taxa = get_lowest_taxon(images, return_rank=False)
    inconsistent_names = set(names) - set(taxa)
    if len(inconsistent_names):
        raise ValueError(f"{list(inconsistent_names)} were not found in images.")

    images = images.copy()
    images["taxon"] = taxa
    images = images.loc[images["taxon"].isin(names), :].reset_index(drop=True)
    images[_labels.images.date] = pd.to_datetime(images[_labels.images.date])
    images["hour"] = images[_labels.images.date].dt.hour + (
        images[_labels.images.date].dt.minute / 60
    )

    # Each image is duplicated by its number of objects to properly
    # account for those images with more than one animal.
    images = images.loc[
        images.index.repeat(images[_labels.images.objects])
    ].reset_index(drop=True)

    if polar:
        if kind in ("area", "hist"):
            ax = _plot_polar(images, "hour", hue="taxon", kind=kind, **polar_kws)
        elif kind == "kde":
            raise ValueError("kind cannot be 'kde' when polar=True.")
        else:
            raise ValueError("kind must be one of ['area', 'hist']")

        ax.set_theta_direction(-1)
        ax.set_theta_zero_location("N")
        x_labels = [f"{h:02}:00" for h in np.arange(0, 24, 2)]
        plt.thetagrids(np.arange(0, 360, 360 // 12), x_labels)

    else:
        images = images[["taxon", "hour"]]
        if kind == "area":
            raise ValueError("kind cannot be 'area' when polar=False.")
        elif kind == "hist":
            ax = sns.histplot(
                data=images,
                x="hour",
                hue="taxon",
                binwidth=1,
                binrange=(0, 24),
                discrete=False,
                **hist_kws,
            )
        elif kind == "kde":
            ax = sns.kdeplot(data=images, x="hour", hue="taxon", **kde_kws)
        else:
            raise ValueError("kind must be one of ['hist', 'kde']")

        x_ticks = np.arange(0, 26, 2)
        x_labels = [f"{h:02}:00" for h in x_ticks]
        ax.set_xlim(-2, 26)
        ax.set_xticks(x_ticks, labels=x_labels)

    return ax


@mpl.rc_context(fname=CONFIG_FILE)
def plot_date_ranges(
    images: pd.DataFrame = None,
    deployments: pd.DataFrame = None,
    source: str = "both",
    **kwargs,
) -> plt.Axes:
    """
    Plots deployment date ranges.

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

    kwargs
        Keyword arguments passed to the sns.relplot() function.

    Returns
    -------
    Axes
        Plot axes.

    """
    df = get_date_ranges(
        images,
        deployments,
        source,
        compute_delta=False,
        pivot=False,
    )

    df = pd.melt(
        df,
        id_vars=[_labels.deployments.deployment_id, "source"],
        value_vars=[_labels.deployments.start, _labels.deployments.end],
    )
    df = df.rename(columns={"value": "date"})
    df = df.sort_values("date").reset_index(drop=True)

    g = sns.relplot(
        data=df,
        x="date",
        y=_labels.deployments.deployment_id,
        row="source",
        kind="line",
        units=_labels.deployments.deployment_id,
        estimator=None,
        facet_kws=dict(despine=False),
        **kwargs,
    )

    return g.axes


@mpl.rc_context(fname=CONFIG_FILE)
def plot_detection_history(
    images: pd.DataFrame,
    deployments: pd.DataFrame,
    name: str,
    mask: bool = False,
    compute_detection_history_kws: dict = None,
    heatmap_kws: dict = None,
) -> plt.Axes:
    """
    Plots detection history matrix for a given species.

    Parameters
    ----------
    images : DataFrame
        DataFrame with the project's images.
    deployments : DataFrame
        DataFrame with the project's deployments.
    name : str
        Scientific name of the species to plot the detection history for.
    mask : bool
        Whether to mask cells where cameras were not functioning. If True,
        those cells won't be displayed. Otherwise, they will be displayed
        as zero.
    compute_detection_history_kws : dict
        Keyword arguments for the wiutils.compute_detection_history()
        function.
    heatmap_kws : dict
        Keyword arguments for the seaborn.heatmap() function.

    Returns
    -------
    Axes
        Plot axes.

    """
    if compute_detection_history_kws is None:
        compute_detection_history_kws = {}
    if heatmap_kws is None:
        heatmap_kws = {}

    taxa = get_lowest_taxon(images, return_rank=False)
    if name not in taxa.unique():
        raise ValueError(f"{name} was not found in images.")

    result = compute_detection_history(
        images, deployments, pivot=True, **compute_detection_history_kws
    )
    result = result[result["taxon"] == name]
    result = result.drop(columns="taxon")
    result = result.set_index(_labels.images.deployment_id)

    if not mask:
        result = result.fillna(0)

    ax = sns.heatmap(data=result, **heatmap_kws)

    return ax
