"""
Mapping from WI fields to DwC terms, constant values and term order for
the Darwin Core Simple Multimedia dataframe creation.
"""
constants = {
    "type": "Image",
    "format": "image/jpeg",
    "publisher": "Wildlife Insights",
}

mapping = {
    "deployment_id": "eventID",
    "image_id": "identifier",
    "location": "references",
    "timestamp": "created",
    "recorded_by": "creator",
    "identified_by": "contributor",
    "license": "license",
}

order = [
    "eventID",
    "type",
    "format",
    "identifier",
    "references",
    "title",
    "created",
    "creator",
    "contributor",
    "publisher",
    "license",
]
