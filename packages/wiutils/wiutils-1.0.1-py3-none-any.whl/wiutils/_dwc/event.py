"""
Mapping from WI fields to DwC terms, constant values and term order for
the Darwin Core Event dataframe creation.
"""
constants = {
    "samplingProtocol": "camera trap",
    "sampleSizeValue": 1,
    "sampleSizeUnit": "camera",
    "geodeticDatum": "WGS84",
}

mapping = {
    "deployment_id": "eventID",
    "placename": "parentEventID",
    "event_description": "eventRemarks",
    "country_code": "countryCode",
    "feature_type": "locationRemarks",
    "latitude": "decimalLatitude",
    "longitude": "decimalLongitude",
    "project_admin_organization": "institutionCode",
}

order = [
    "eventID",
    "parentEventID",
    "samplingProtocol",
    "sampleSizeValue",
    "sampleSizeUnit",
    "samplingEffort",
    "eventDate",
    "eventRemarks",
    "countryCode",
    "locationRemarks",
    "decimalLatitude",
    "decimalLongitude",
    "geodeticDatum",
    "institutionCode",
]
