"""
Functions to preprocess information before uploading it to WI.
"""
import datetime
import pathlib
from typing import Union

import cv2
import ffmpeg
import pandas as pd
from PIL import ExifTags, Image


def _get_exif_code(tag: str) -> int:
    for key, value in ExifTags.TAGS.items():
        if value == tag:
            return key


def change_image_timestamp(
    image_path: Union[str, pathlib.Path],
    output_path: Union[str, pathlib.Path],
    timestamp: Union[str, datetime.datetime, pd.Timestamp] = None,
    offset: Union[pd.DateOffset, pd.Timedelta] = None,
) -> None:
    """
    Changes an image's associated timestamp metadata for a new timestamp.
    This can be a new arbitrary timestamp or a computed new timestamp from
    an offset and the original timestamp.

    Parameters
    ----------
    image_path : str or Path
        Relative or absolute path of the image to resample.
    output_path : str or Path
        Relative or absolute path of the output image.
    timestamp : str, datetime.datetime or pd.Timestamp
        New timestamp to write to the image's metadata.
    offset : DateOffset or Timedelta
        Offset or Timedelta to add to (if positive) or subtract from (if
        negative) the original image's timestamp. This argument only has
         effect when no timestamp is specified.

    Returns
    -------
    None

    """
    if not isinstance(image_path, pathlib.Path):
        image_path = pathlib.Path(image_path)
    if not isinstance(output_path, pathlib.Path):
        output_path = pathlib.Path(output_path)

    image = Image.open(image_path.as_posix())
    exif = image.getexif()

    if timestamp is not None:
        if not isinstance(timestamp, pd.Timestamp):
            timestamp = pd.Timestamp(timestamp)
    else:
        timestamp = exif[_get_exif_code("DateTime")]
        timestamp = pd.Timestamp(timestamp.replace(":", "-", 2))
        timestamp += offset

    exif[_get_exif_code("DateTime")] = timestamp.strftime("%Y:%m:%d %H:%M:%S")
    exif[_get_exif_code("DateTimeOriginal")] = timestamp.strftime("%Y:%m:%d %H:%M:%S")

    image.save(output_path.as_posix(), format=image.format, exif=exif)


def convert_video_to_images(
    video_path: Union[str, pathlib.Path],
    output_path: Union[str, pathlib.Path],
    timestamp: Union[str, datetime.datetime, pd.Timestamp] = None,
    image_format: str = "jpeg",
    offset: int = None,
) -> None:
    """
    Converts a video to images with an associated timestamp.

    Parameters
    ----------
    video_path : str or Path
        Relative or absolute path of the video to convert.
    output_path : str or Path
        Relative or absolute path of the folder to save the images to. If
        the folder does not exist, it will be created.
    timestamp : str, datetime.datetime or pd.Timestamp
        Timestamp of the beginning of the video. If no timestamp is
        provided, it will be automatically extracted from the metadata.
    image_format : str
        Image format of the output images. Possible values are:

            - 'jpeg'
            - 'png'
    offset : int
        Offset (in seconds) to convert frames to images. For example, if
        offset is 1, the output images will correspond to 1 second-separated
        frames of the video. If offset is None, all the frames in the video
        will be converted to images.

    Returns
    -------
    None

    """
    if not isinstance(video_path, pathlib.Path):
        video_path = pathlib.Path(video_path)
    if not isinstance(output_path, pathlib.Path):
        output_path = pathlib.Path(output_path)

    if image_format not in ("jpeg", "png"):
        raise ValueError("image_format must be one of ['jpeg', 'png'].")

    ext = "jpg" if image_format == "jpeg" else image_format

    if timestamp is not None:
        start = pd.Timestamp(timestamp)
    else:
        info = ffmpeg.probe(video_path.as_posix())
        try:
            start = info["format"]["tags"]["creation_time"]
        except KeyError:
            raise KeyError(f"{video_path.as_posix()} does not have a creation date.")
        start = pd.Timestamp(start)

    video = cv2.VideoCapture(video_path.as_posix())
    frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    width = len(str(frames))
    datetime_code = _get_exif_code("DateTimeOriginal")

    output_path.mkdir(parents=True, exist_ok=True)

    count = 1
    flag, arr = video.read()
    while flag:
        image = Image.fromarray(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR))
        exif = image.getexif()
        timestamp = start + pd.Timedelta(milliseconds=video.get(cv2.CAP_PROP_POS_MSEC))
        exif[datetime_code] = timestamp.strftime("%Y:%m:%d %H:%M:%S")
        name = video_path.stem + "_" + str(count).zfill(width) + f".{ext}"
        image.save(
            output_path.joinpath(name).as_posix(), format=image_format, exif=exif
        )
        if offset:
            video.set(cv2.CAP_PROP_POS_MSEC, count * (offset * 1e3))
        flag, arr = video.read()
        count += 1


def reduce_image_size(
    image_path: Union[str, pathlib.Path],
    output_path: Union[str, pathlib.Path],
    factor: float = 0.9,
    method: int = 1,
) -> None:
    """
    Reduces image file size by resampling using a given factor.

    Parameters
    ----------
    image_path : str or Path
        Relative or absolute path of the image to resample.
    output_path : str or Path
        Relative or absolute path of the output image.
    factor : float
        Resampling factor.
    method : int
        Image resizing method used by PIL. Possible values are:

            - 0: PIL.Image.Resampling.NEAREST
            - 1: PIL.Image.Resampling.LANCZOS
            - 2: PIL.Image.Resampling.BILINEAR
            - 3: PIL.Image.Resampling.BICUBIC

    Returns
    -------
    None

    """
    if not isinstance(image_path, pathlib.Path):
        image_path = pathlib.Path(image_path)
    if not isinstance(output_path, pathlib.Path):
        output_path = pathlib.Path(output_path)

    image = Image.open(image_path.as_posix())
    exif = image.getexif()
    new_width = round(image.width * factor)
    new_height = round(image.height * factor)
    result = image.resize((new_width, new_height), method)

    result.save(output_path.as_posix(), format=image.format, exif=exif)
