"""
Functions to read information from WI projects.
"""
import pathlib
import zipfile
from typing import Union

import pandas as pd

from . import _labels


def _read_file(path: Union[str, pathlib.Path], name, **kwargs) -> pd.DataFrame:
    if not isinstance(path, pathlib.Path):
        path = pathlib.Path(path)

    if path.is_file():
        if not path.suffix == ".zip":
            raise ValueError("path must be either a folder or a .zip file.")
        with zipfile.ZipFile(path) as z:
            path = z.open(f"{path.stem}/{name}.csv")
    else:
        path = path.joinpath(f"{name}.csv")

    return pd.read_csv(path, **kwargs)


def load_demo(name) -> tuple:
    """
    Loads the cameras, deployments, images and projects tables from a
    demo dataset.

    Parameters
    ----------
    name : str
        Demo dataset name. Can be one of:

            - 'cajambre'
            - 'cristales'

    Returns
    -------
    DataFrame
        Demo cameras dataframe
    DataFrame
        Demo deployments dataframe
    DataFrame
        Demo images dataframe
    DataFrame
        Demo projects dataframe

    """
    root = pathlib.Path(__file__).parents[0]
    if name == "cajambre":
        path = root.joinpath("data/cajambre.zip")
    elif name == "cristales":
        path = root.joinpath("data/cristales.zip")
    else:
        raise ValueError("name must be of one ['cajambre', 'cristales']")

    return read_bundle(path)


def read_bundle(path: Union[str, pathlib.Path]) -> tuple:
    """
    Reads the cameras, deployments, images and projects tables from a
    specific Wildlife Insights project bundle.

    Parameters
    ----------
    path : str or Path
        Absolute or relative path of the project bundle. Can be a folder
        with all the respective csv files inside or a zip file.

    Returns
    -------
    DataFrame
        Bundle cameras dataframe
    DataFrame
        Bundle deployments dataframe
    DataFrame
        Bundle images dataframe
    DataFrame
        Bundle projects dataframe

    """
    cameras = read_cameras(path)
    deployments = read_deployments(path)
    images = read_images(path)
    projects = read_projects(path)

    return cameras, deployments, images, projects


def read_cameras(path: Union[str, pathlib.Path], **kwargs) -> pd.DataFrame:
    """
    Reads the cameras' table from a specific Wildlife Insights project bundle.

    Parameters
    ----------
    path : str or Path
        Absolute or relative path of the project bundle. Can be a folder
        with all the respective csv files inside or a zip file.
    kwargs
        Keyword arguments passed to the pd.read_csv function.

    Returns
    -------
    DataFrame
        Bundle cameras dataframe

    """
    return _read_file(path, "cameras", **kwargs)


def read_deployments(path: Union[str, pathlib.Path], **kwargs) -> pd.DataFrame:
    """
    Reads the deployments' table from a specific Wildlife Insights project
    bundle. Start and end column values are automatically parsed as dates.

    Parameters
    ----------
    path : str or Path
        Absolute or relative path of the project bundle. Can be a folder
        with all the respective csv files inside or a zip file.
    kwargs
        Keyword arguments passed to the pd.read_csv function.

    Returns
    -------
    DataFrame
        Bundle deployments dataframe

    """
    kwargs.update(
        dict(parse_dates=[_labels.deployments.start, _labels.deployments.end])
    )
    return _read_file(path, "deployments", **kwargs)


def read_images(path: Union[str, pathlib.Path], **kwargs) -> pd.DataFrame:
    """
    Reads the images' table from a specific Wildlife Insights project
    bundle. Timestamp column values are automatically parsed as dates.

    Parameters
    ----------
    path : str or Path
        Absolute or relative path of the project bundle. Can be a folder
        with all the respective csv files inside or a zip file.
    kwargs
        Keyword arguments passed to the pd.read_csv function.

    Returns
    -------
    DataFrame
        Bundle images dataframe

    """
    kwargs.update(dict(parse_dates=[_labels.images.date]))
    return _read_file(path, "images", **kwargs)


def read_projects(path: Union[str, pathlib.Path], **kwargs) -> pd.DataFrame:
    """
    Reads projects table from a specific Wildlife Insights project bundle.

    Parameters
    ----------
    path : str or Path
        Absolute or relative path of the project bundle. Can be a folder
        with all the respective csv files inside or a zip file.
    kwargs
        Keyword arguments passed to the pd.read_csv function.

    Returns
    -------
    DataFrame
        Bundle projects dataframe

    """
    return _read_file(path, "projects", **kwargs)
