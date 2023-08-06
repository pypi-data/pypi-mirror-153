import pytest
from moto import mock_s3

from envidat.s3.exceptions import NoSuchCORSConfiguration


@mock_s3
def test_get_s3_resource(bucket):
    resource = bucket.get_boto3_resource()
    assert resource, "No boto3 resource was returned"


@mock_s3
def test_get_s3_client(bucket):
    client = bucket.get_boto3_client()
    assert client, "No boto3 client was returned"


@mock_s3
def test_bucket_create_public(bucket):
    bucket.is_public = True
    new_bucket = bucket.create()

    response = new_bucket.meta.client.head_bucket(Bucket="testing")
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200


@mock_s3
def test_configure_static_website(bucket):
    bucket.create()

    success = bucket.configure_static_website()
    assert success is True


@mock_s3
def test_generate_index_html(bucket):
    bucket.create()

    response = bucket.generate_index_html("testing", "testing")
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200


@mock_s3
def test_get_bucket_cors_unset(bucket):
    bucket.create()

    with pytest.raises(NoSuchCORSConfiguration):
        bucket.get_cors_config()


@mock_s3
def test_set_bucket_cors(bucket):
    bucket.create()

    bucket.set_cors_config(origins=["testsite.com", "testsite2.ch"])
    response = bucket.get_cors_config()
    assert response["AllowedOrigins"] == ["testsite.com", "testsite2.ch"]


@mock_s3
def test_set_bucket_cors_allow_all(bucket):
    bucket.create()

    bucket.set_cors_config(allow_all=True)
    response = bucket.get_cors_config()
    assert response["AllowedOrigins"] == ["*"]


@mock_s3
def test_clean_multiparts(bucket, create_tempfile):
    bucket.create()

    client = bucket.get_boto3_client()
    assert client

    key = "/test.txt"

    response = client.create_multipart_upload(
        Bucket=bucket.bucket_name,
        Key=key,
    )
    assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    with create_tempfile("txt") as upload:
        upload.write(b"0" * 1024 * 1024 * 5)  # 5MB

        response = client.upload_part(
            Bucket=bucket.bucket_name,
            Key=key,
            PartNumber=1,
            UploadId=response["UploadId"],
            Body=upload,
        )
        assert response["ResponseMetadata"]["HTTPStatusCode"] == 200

    response = client.list_multipart_uploads(
        Bucket=bucket.bucket_name,
    )
    assert len(response["Uploads"]) == 1

    status_dict = bucket.clean_multiparts()
    assert status_dict[key] is True

    response = client.list_multipart_uploads(
        Bucket=bucket.bucket_name,
    )
    assert "Uploads" not in response, "The multipart clean failed."
