# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Contains helper methods for mltable apis."""
import re
from enum import Enum


def _download_mltable_yaml(path: str):
    from azureml.dataprep.rslex import Copier, PyLocationInfo, PyIfDestinationExists
    from azureml.exceptions import UserErrorException
    from azureml.exceptions import AzureMLException

    # normalize path to MLTable yaml path
    normalized_path = "{}/MLTable".format(path.rstrip("/"))
    if_destination_exists = PyIfDestinationExists.MERGE_WITH_OVERWRITE
    try:

        from tempfile import mkdtemp
        local_path = mkdtemp()
        Copier.copy_uri(PyLocationInfo('Local', local_path, {}),
                        normalized_path, if_destination_exists, "")

        return local_path
    except Exception as e:
        if "InvalidUriScheme" in e.args[0] or \
            "StreamError(NotFound)" in e.args[0] or \
                "DataAccessError(NotFound)" in e.args[0]:
            raise UserErrorException(e.args[0])
        else:
            raise AzureMLException(e.args[0])


def _is_tabular(mltable_yaml):
    if mltable_yaml is None:
        return False

    transformations_key = "transformations"
    if transformations_key not in mltable_yaml.keys():
        return False

    tabular_transformations = [
        "read_delimited",
        "read_parquet",
        "read_json_lines"
    ]

    if mltable_yaml['transformations'] and all(isinstance(e, dict) for e in mltable_yaml['transformations']):
        list_of_transformations = [k for d in mltable_yaml['transformations'] for k, v in d.items()]
    else:
        # case where transformations section is a list[str], not a list[dict].
        list_of_transformations = mltable_yaml['transformations']
    return any(key in tabular_transformations for key in list_of_transformations)


class _PathType(Enum):
    local = 1
    cloud = 2
    legacy_dataset = 3


def _parse_path_format(path: str, workspace=None):
    regular_cloud_uri_patterns = re.compile(r'^https?://|adl://|wasbs?://|abfss?://|azureml://subscriptions',
                                            re.IGNORECASE)
    if regular_cloud_uri_patterns.match(path):
        return _PathType.cloud, path, None

    dataset_uri_pattern = re.compile(
        r'^azureml://locations/(.*)/workspaces/(.*)/data/([0-9a-z_-]+)/versions/([0-9a-z_-]+)',
        re.IGNORECASE)
    dataset_uri_match = dataset_uri_pattern.match(path)
    if dataset_uri_match:
        return _PathType.legacy_dataset, dataset_uri_match.group(3), dataset_uri_match.group(4)

    return _PathType.local, path, None
