"""
Mapping from WI fields to DwC terms for the Darwin Core Measurement or
Facts dataframe creation.
"""
import numpy as np

mapping = [
    {
        "type": "camera make",
        "value": "make",
        "unit": np.nan,
        "remarks": None,
    },
    {
        "type": "camera serial number",
        "value": "serial_number",
        "unit": np.nan,
        "remarks": None,
    },
    {
        "type": "camera year purchased",
        "value": "year_purchased",
        "unit": np.nan,
        "remarks": None,
    },
    {
        "type": "bait type",
        "value": "bait_type",
        "unit": np.nan,
        "remarks": "bait_description",
    },
    {
        "type": "quiet period",
        "value": "quiet_period",
        "unit": "seconds",
        "remarks": None,
    },
    {
        "type": "camera functioning",
        "value": "camera_functioning",
        "unit": np.nan,
        "remarks": None,
    },
    {
        "type": "sensor height",
        "value": "sensor_height",
        "unit": np.nan,
        "remarks": "height_other",
    },
    {
        "type": "sensor orientation",
        "value": "sensor_orientation",
        "unit": np.nan,
        "remarks": "orientation_other",
    },
    {
        "type": "plot treatment",
        "value": "plot_treatment",
        "unit": np.nan,
        "remarks": "plot_treatment_description",
    },
    {
        "type": "detection distance",
        "value": "detection_distance",
        "unit": "meters",
        "remarks": None,
    },
]
