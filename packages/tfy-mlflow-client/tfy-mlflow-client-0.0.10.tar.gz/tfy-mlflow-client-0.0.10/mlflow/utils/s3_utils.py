import os
from datetime import datetime
from functools import lru_cache

import boto3
from botocore.client import Config

from mlflow.data import parse_s3_uri
from mlflow.exceptions import MlflowException
from mlflow.protos.databricks_pb2 import INTERNAL, PERMISSION_DENIED

_MAX_CACHE_SECONDS = 300


def _get_utcnow_timestamp():
    return datetime.utcnow().timestamp()


@lru_cache(maxsize=64)
def _cached_get_s3_client(
    timestamp,
):  # pylint: disable=unused-argument
    signature_version = os.environ.get("MLFLOW_EXPERIMENTAL_S3_SIGNATURE_VERSION", "s3v4")
    return boto3.client(
        "s3",
        config=Config(signature_version=signature_version),
    )


def get_s3_client():
    timestamp = int(_get_utcnow_timestamp() / _MAX_CACHE_SECONDS)
    return _cached_get_s3_client(timestamp)


def validate_run_id(run_id, s3_uri, tracking_store):

    response_message = tracking_store.get_run(run_id).to_proto()
    uri = response_message.info.artifact_uri
    if s3_uri.startswith(uri + "/"):
        return
    else:
        raise MlflowException(
            f"Not authorized to access the uri: {s3_uri} with the run_id: {run_id}",
            error_code=PERMISSION_DENIED,
        )


def get_presigned_s3_url(_type, path, run_id, tracking_store):
    s3_client = get_s3_client()
    bucket, key = parse_s3_uri(path)

    validate_run_id(run_id, path, tracking_store)

    if _type == "write":
        method = "put_object"
    elif _type == "read":
        method = "get_object"
    else:
        raise MlflowException("Could not identify type", error_code=INTERNAL)
    return s3_client.generate_presigned_url(
        method,
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=1800,
    )
