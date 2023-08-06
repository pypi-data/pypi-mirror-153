import os
from tempfile import NamedTemporaryFile

import pytest
from moto import mock_s3

from envidat.s3.bucket import Bucket

os.environ["MOTO_ALLOW_NONEXISTENT_REGION"] = "True"


# @pytest.fixture(scope="session")
# def s3_env_vars():

#     # Disable region validation for moto
#     os.environ["MOTO_ALLOW_NONEXISTENT_REGION"] = "True"

#     # Official vars
#     os.environ["AWS_ACCESS_KEY_ID"] = "testing"
#     os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
#     os.environ["AWS_SECURITY_TOKEN"] = "testing"
#     os.environ["AWS_SESSION_TOKEN"] = "testing"
#     os.environ["AWS_DEFAULT_REGION"] = "testing"

#     # Custom vars
#     os.environ["AWS_ENDPOINT"] = "testing"
#     os.environ["AWS_ACCESS_KEY"] = "testing"
#     os.environ["AWS_SECRET_KEY"] = "testing"
#     os.environ["AWS_REGION"] = "testing"
#     os.environ["AWS_BUCKET_NAME"] = "testing"


@pytest.fixture(scope="session")
@mock_s3
def bucket():
    Bucket.config("testing", "testing", endpoint=None, region="testing")
    new_bucket = Bucket("testing")
    return new_bucket


@pytest.fixture
def create_tempfile(scope="function"):
    def nested_tempfile(file_type, temp_dir=None, delete=True):
        temp_file = NamedTemporaryFile(
            dir=temp_dir, delete=delete, suffix=f".{file_type}"
        )
        with open(temp_file.name, "w", encoding="UTF-8") as f:
            f.write("test")
        return temp_file

    return nested_tempfile
