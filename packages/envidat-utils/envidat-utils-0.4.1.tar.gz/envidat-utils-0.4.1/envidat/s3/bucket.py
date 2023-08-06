import json
import logging
import mimetypes
import os
from io import BytesIO
from pathlib import Path
from textwrap import dedent
from typing import Any, NoReturn, Union

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from envidat.s3 import exceptions
from envidat.utils import get_url

log = logging.getLogger(__name__)


class Bucket:
    """Class to handle S3 bucket transactions.
    Handles boto3 exceptions with custom exception classes.
    """

    _AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY")
    _AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_KEY")
    _AWS_ENDPOINT = os.getenv("AWS_ENDPOINT")
    _AWS_REGION = os.getenv("AWS_REGION", default="")

    def __init__(
        self,
        bucket_name: str = None,
        is_new: bool = False,
        is_public: bool = False,
    ) -> NoReturn:
        """Init the Bucket object.

        Args:
            bucket_name (str): Name of the bucket.
                If AWS_BUCKET_NAME is set in the environment, this is overriden.
            is_new (bool): If true, creates a new bucket.
            is_public (bool): If true, makes the bucket public on creation.
        """

        if None in [Bucket._AWS_ACCESS_KEY_ID, Bucket._AWS_SECRET_ACCESS_KEY]:
            missing_vars = {"AWS_ACCESS_KEY", "AWS_SECRET_KEY"} - set(os.environ)
            if not missing_vars:
                log.info(
                    "Environment variables set after Bucket class import. "
                    "Re-configuring Bucket with specified environment variables."
                )
                Bucket.config(
                    os.getenv("AWS_ACCESS_KEY"),
                    os.getenv("AWS_SECRET_KEY"),
                    endpoint=os.getenv("AWS_ENDPOINT"),
                    region=os.getenv("AWS_REGION", default=""),
                )

        log.debug(
            "S3 Bucket object instantiated. "
            f"Access key: {True if Bucket._AWS_ACCESS_KEY_ID else False} | "
            f"Secret key: {True if Bucket._AWS_SECRET_ACCESS_KEY else False} | "
            f"Endpoint: {Bucket._AWS_ENDPOINT} | "
            f"Region: {Bucket._AWS_REGION} | "
            f"is_new: {is_new} | "
            f"is_public: {is_public}"
        )
        # Ensure credentials are configured
        if not Bucket._AWS_ACCESS_KEY_ID or not Bucket._AWS_SECRET_ACCESS_KEY:
            log.error("Bucket instantiated without access key and secret key set.")
            raise TypeError(
                "AWS Access Key ID and AWS Secret Access Key must be configured. "
                "Set them with environment variables AWS_ACCESS_KEY and AWS_ACCESS_KEY "
                "or with Bucket.config(access_key, secret_key, endpoint, region)"
            )
        if "AWS_BUCKET_NAME" in os.environ:
            log.debug("Getting bucket name from environment variable.")
            self.bucket_name = os.getenv("AWS_BUCKET_NAME")
        else:
            self.bucket_name = bucket_name

        self.is_public = is_public

        if is_new:
            self.create()

    @classmethod
    def config(
        cls, access_key: str, secret_key: str, endpoint: str = None, region: str = ""
    ) -> NoReturn:
        """Config the bucket connection parameters before init.

        Args:
            access_key (str): AWS_ACCESS_KEY_ID.
            secret_key (str): AWS_SECRET_ACCESS_KEY.
            endpoint (str): Endpoint for the S3, if not AWS.
                Defaults to None.
            region (str): AWS_REGION.
                Defaults to empty string "".
        """
        cls._AWS_ACCESS_KEY_ID = access_key
        cls._AWS_SECRET_ACCESS_KEY = secret_key
        cls._AWS_ENDPOINT = endpoint
        cls._AWS_REGION = region

    @staticmethod
    def get_boto3_resource() -> NoReturn:
        """Configure boto3 resource object."""

        log.debug("Accessing boto3 resource.")
        return boto3.resource(
            "s3",
            aws_access_key_id=Bucket._AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Bucket._AWS_SECRET_ACCESS_KEY,
            endpoint_url=Bucket._AWS_ENDPOINT,
            region_name=Bucket._AWS_REGION,
            config=Config(signature_version="s3v4"),
        )

    @staticmethod
    def get_boto3_client() -> NoReturn:
        """Cofigure boto3 client object."""

        log.debug("Accessing boto3 client.")
        return boto3.client(
            "s3",
            aws_access_key_id=Bucket._AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Bucket._AWS_SECRET_ACCESS_KEY,
            endpoint_url=Bucket._AWS_ENDPOINT,
            region_name=Bucket._AWS_REGION,
            config=Config(signature_version="s3v4"),
        )

    def _handle_boto3_client_error(self, e: ClientError, key: str = None) -> NoReturn:
        """Handle boto3 ClientError.
        The exception type returned from the server is nested here.
        Refer to exceptions.py

        Args:
            e (ClientError): The ClientError to handle
            key (str): The S3 object key. Defaults to None.
        """
        error_code: str = e.response.get("Error").get("Code")

        log.debug(e.response)

        if error_code == "AccessDenied":
            raise exceptions.BucketAccessDenied(self.bucket_name)
        elif error_code == "NoSuchBucket":
            raise exceptions.NoSuchBucket(self.bucket_name)
        elif error_code == "NoSuchKey":
            raise exceptions.NoSuchKey(key, self.bucket_name)
        elif error_code == "BucketAlreadyExists":
            raise exceptions.BucketAlreadyExists(self.bucket_name)
        elif error_code == "NoSuchCORSConfiguration":
            raise exceptions.NoSuchCORSConfiguration(self.bucket_name)
        else:
            raise exceptions.UnknownBucketException(self.bucket_name, e)

    def _raise_file_not_found(self, file_path: str, is_dir: bool = False) -> NoReturn:
        """Raise error if expected file not found on disk.

        Args:
            file_path (str): The path to the expected file.
            is_dir (bool): True if path is a directory.
                Defaults to False.
        """

        msg = (
            f"Referenced {'directory' if is_dir else 'file'} "
            f"not found on disk: {file_path}"
        )
        log.error(msg)
        raise FileNotFoundError(msg)

    def _raise_parameter_error(self, param_name: str, value: str) -> NoReturn:
        """Raise error if incorrect parameters are provided.

        Args:
            param_name (str): The parameter name.
            value (str): The parameter value.
        """

        if value is None:
            msg = f"A value must be set for parameter {param_name}"
        else:
            msg = f"Invalid value for parameter {param_name}: {value}"
        log.error(msg)
        raise ValueError(msg)

    def create(self) -> "boto3.resource.Bucket":
        """Create the S3 bucket on the endpoint.
        Method may be called directly to manipulate the boto3 Bucket object.

        Returns:
            "boto3.resource.Bucket": A boto3 S3 Bucket object.
        """

        resource = Bucket.get_boto3_resource()

        try:
            log.info(f"Creating bucket named {self.bucket_name}")
            bucket = resource.create_bucket(
                ACL="public-read" if self.is_public else "private",
                Bucket=self.bucket_name,
                CreateBucketConfiguration={
                    "LocationConstraint": f"{Bucket._AWS_REGION}"
                },
                ObjectLockEnabledForBucket=False,
            )
            log.debug("Bucket created successfully")
            return bucket
        except ClientError as e:
            self._handle_boto3_client_error(e)

    def get(
        self,
        key: str,
        response_content_type: str = None,
        decode: bool = False,
    ) -> (Any, dict):
        """Get an object from the bucket into a memory object.
        Defaults to utf-8 decode, unless specified.

        Args:
            key (str): The key, i.e. path within the bucket to get.
            response_content_type (str): Content type to enforce on the response.
                Defaults to None.
            decode (bool): Decodes using utf-8 if set. Useful for text based files.
                Defaults to None.

        Returns:
            tuple: (data, S3 Metadata dict).
        """

        resource = Bucket.get_boto3_resource()
        s3_object = resource.Object(self.bucket_name, key)

        try:
            log.info(f"Getting S3 object with key {key}")
            if response_content_type:
                response = s3_object.get(ResponseContentType=response_content_type)
            else:
                response = s3_object.get()

            log.debug("Reading returned data into Python object")
            data = response.get("Body").read()
            metadata: dict = response.get("Metadata")

            if decode:
                log.debug("Decoding object with utf-8")
                data = data.decode("utf-8")

            return data, metadata

        except ClientError as e:
            self._handle_boto3_client_error(e, key=key)

    def put(
        self,
        key: str,
        data: Union[str, bytes],
        content_type: str = None,
        metadata: dict = {},
    ) -> dict:
        """Put an in memory object into the bucket.

        Args:
            key (str): The key, i.e. path within the bucket to store as.
            data (Union[str, bytes]): The data to store, can be bytes or string.
            content_type (str): The mime type to store the data as.
                E.g. important for binary data or html text.
                Defaults to None.
            metadata (dict): Dictionary of metadata.
                E.g. timestamp or organisation details as string type.
                Defaults to None.

        Returns:
            dict: Response dictionary from S3.
        """

        resource = Bucket.get_boto3_resource()
        s3_object = resource.Object(self.bucket_name, key)

        try:
            log.info(
                "Uploading S3 object with: "
                f"Key: {key} | "
                f"ContentType: {content_type} | "
                f"Metadata: {metadata}"
            )
            if content_type:
                response = s3_object.put(
                    Body=data, ContentType=content_type, Key=key, Metadata=metadata
                )
            else:
                response = s3_object.put(Body=data, Key=key, Metadata=metadata)
            return response

        except ClientError as e:
            self._handle_boto3_client_error(e, key=key)

    def delete(self, key: str) -> dict:
        """Delete specified object of a given key.

        Args:
            key (str): The key, i.e. path within the bucket to delete.

        Returns:
            dict: Response dictionary from S3.
        """

        client = Bucket.get_boto3_client()

        try:
            log.info(f"Deleting S3 object with key: {key}")
            response = client.delete_object(Bucket=self.bucket_name, Key=key)
            return response

        except ClientError as e:
            self._handle_boto3_client_error(e, key=key)

    def upload_file(self, key: str, local_filepath: Union[str, Path]) -> bool:
        """Upload a local file to the bucket.
        Transparently manages multipart uploads.

        Args:
            key (str): The key, i.e. path within the bucket to store as.
            local_filepath (Union[str, Path]): Path string or Pathlib path to upload.

        Returns:
            bool: True if success, False is failure.
        """

        resource = Bucket.get_boto3_resource()
        s3_object = resource.Object(self.bucket_name, key)

        file_path = Path(local_filepath).resolve()
        if not file_path.is_file():
            self._raise_file_not_found(file_path)
        else:
            file_path = str(file_path)
        log.debug(f"File to upload: {file_path}")

        log.debug("Guessing file mimetype")
        mimetype, _ = mimetypes.guess_type(file_path)
        if mimetype is None:
            log.debug("Failed to guess mimetype, setting to application/octet-stream")
            mimetype = "application/octet-stream"

        try:
            log.info(f"Uploading to S3 from file: File Path: {file_path} | Key: {key}")
            s3_object.upload_file(file_path, ExtraArgs={"ContentType": mimetype})
            return True

        except ClientError as e:
            self._handle_boto3_client_error(e, key=key)

        return False

    def download_file(self, key: str, local_filepath: Union[str, Path]) -> bool:
        """Download S3 object to a local file.
        Transparently manages multipart downloads.

        Args:
            key (str): The key, i.e. path within the bucket to download from.
            local_filepath (Union[str, Path]): Path string or Pathlib path
                to download to.

        Returns:
            bool: True if success, False is failure.
        """

        resource = Bucket.get_boto3_resource()
        s3_object = resource.Object(self.bucket_name, key)

        file_path = Path(local_filepath).resolve()
        if not file_path.parent.is_dir():
            self._raise_file_not_found(file_path, is_dir=True)
        else:
            file_path = str(file_path)

        try:
            log.info(
                f"Downloading from S3 to file: Key: {key} | File Path: {file_path}"
            )
            s3_object.download_file(file_path)
            return True

        except ClientError as e:
            self._handle_boto3_client_error(e, key=key)

        return False

    def list_all(self) -> list:
        """Get a list of all objects in the bucket.

        Returns:
            list: List of s3.ObjectSummary dicts, containing object metadata.
        """

        resource = Bucket.get_boto3_resource()

        try:
            log.debug(f"Getting bucket named: {self.bucket_name}")
            bucket = resource.Bucket(self.bucket_name)

            log.debug("Listing all objects in bucket")
            objects = bucket.objects.all()

            file_names = [os.path.splitext(file.key)[0] for file in objects]
            log.info(
                f"Returned {len(file_names)} objects from "
                f"bucket named {self.bucket_name}"
            )

            return file_names

        except ClientError as e:
            self._handle_boto3_client_error(e)

    def list_dir(
        self,
        path: str = "",
        recursive: bool = False,
        file_type: str = "",
        names_only: bool = False,
    ) -> list:
        """Get a list of all objects in a specific directory (s3 path).
        Returns up to a max of 1000 values.

        Args:
            path (str): The directory in the bucket.
                Defaults to root ("").
            recursive (bool): To list all objects and subdirectory objects recursively.
                Defaults to False.
            file_type (str): File extension to filter by, e.g. 'txt'
                Defaults to blank string ("").
            names_only (bool): Remove file extensions and path,
                giving only the file name.
                Defaults to False.

        Returns:
            list: List of s3.ObjectSummary dicts, containing object metadata.
        """

        resource = Bucket.get_boto3_resource()

        if path:
            path = path[1:] if path.startswith("/") else path
            path = (path + "/") if not path.endswith("/") else path

        try:
            log.debug(f"Getting bucket named: {self.bucket_name}")
            bucket = resource.Bucket(self.bucket_name)

            log.debug(
                "Filtering objects in bucket with params: "
                f"path: {path} | recursive: {recursive} | file_type: {file_type}"
            )
            filtered_objects = bucket.objects.filter(
                Delimiter="/" if not recursive else "",
                # EncodingType='url',
                # Marker='string',
                # MaxKeys=123,
                Prefix=path,
            )

        except ClientError as e:
            self._handle_boto3_client_error(e)

        # Test if a match is made, else function will return [False]
        if not isinstance(
            filtered_objects, boto3.resources.collection.ResourceCollection
        ):
            log.info("No matching files for bucket filter parameters.")
            return []

        if file_type:
            log.debug(f"Further filtering return by file extension: {file_type}")
            file_names = [
                obj.key for obj in filtered_objects if obj.key.endswith(file_type)
            ]
        else:
            file_names = [obj.key for obj in filtered_objects]

        if names_only:
            log.debug("Removing extensions from file names")
            file_paths = [Path(file_name) for file_name in file_names]
            file_names = [str(file_path.stem) for file_path in file_paths]

        log.info(
            f"Returned {len(file_names)} filtered objects from "
            f"bucket named {self.bucket_name}"
        )

        return file_names

    def download_dir(
        self,
        s3_path: str,
        local_dir: Union[str, Path],
        file_type: str = "",
    ) -> bool:
        """
        Download an entire S3 path, including subpaths, to a local directory.

        Args:
            s3_path (str): The path within the bucket to download.
            local_dir (Union[str, Path]): Directory to download files into.
            file_type (str): Download files with extension only, e.g. txt.

        Returns:
            dict: key:value pair of s3_key:download_status.
                download_status True if downloaded, False if failed.
        """

        status_dict = {}

        local_dir_path = Path(local_dir)
        log.debug(f"Top level directory to download to: {local_dir_path}")

        s3_keys = self.list_dir(path=s3_path, recursive=True, file_type=file_type)

        for key in s3_keys:
            log.debug(f"S3 key to download: {key}")

            file_path = local_dir_path / key.replace("/", "", 1)
            log.debug(f"Creating parent download directory: {file_path.parent}")
            file_path.parent.mkdir(parents=True, exist_ok=True)

            status_dict[key] = self.download_file(key, file_path)

        return status_dict

    def upload_dir(
        self,
        s3_path: str,
        local_dir: Union[str, Path],
        file_type: str = "",
    ) -> bool:
        """
        Upload an entire local directory to a bucket path.

        Args:
            s3_path (str): The path within the bucket to upload to.
            local_dir (Union[str, Path]): Directory to upload files from.
            file_type (str): Upload files with extension only, e.g. txt.

        Returns:
            dict: key:value pair of file_name:upload_status.
                upload_status True if uploaded, False if failed.
        """

        status_dict = {}

        local_dir_path = Path(local_dir).resolve()
        log.debug(f"Full directory path to upload: {local_dir_path}")

        parent_parts = local_dir_path.parent.parts
        log.debug(f"Part directory parts: {parent_parts}")
        num_parents = len(parent_parts)

        all_subdirs = list(local_dir_path.glob("**"))

        for dir_path in all_subdirs:
            log.debug(f"Searching for files in directory: {dir_path}")

            file_names = dir_path.glob(f"*{('.' + file_type) if file_type else ''}")

            # Only return valid files
            file_names = [f for f in file_names if f.is_file()]
            log.debug(f"Files found: {list(file_names)}")

            for i, file_name in enumerate(file_names):
                s3_key = str(Path(s3_path) / Path(*file_name.parts[num_parents:]))
                log.debug(f"S3 key to upload: {s3_key}")
                status_dict[str(file_name)] = self.upload_file(s3_key, file_name)

        return status_dict

    def clean_multiparts(self) -> bool:
        """
        Clean up failed multipart uploads in a bucket.

        Returns:
            dict: key:value pair of s3_multipart_key:clean_status.
                clean_status True if removed, False if failed.
        """

        status_dict = {}
        success_counter = 0
        failure_counter = 0

        client = Bucket.get_boto3_client()

        try:
            log.debug(f"Getting multipart uploads for bucket {self.bucket_name}")
            response = client.list_multipart_uploads(Bucket=self.bucket_name)

            files = response["Uploads"]
            log.info(
                f"Returned {len(files)} objects from "
                f"bucket named {self.bucket_name}"
            )

            log.info("Cleaning multipart parts if present")
            for file in files:
                response = client.abort_multipart_upload(
                    Bucket=self.bucket_name,
                    Key=file["Key"],
                    UploadId=file["UploadId"],
                )

                if response["ResponseMetadata"]["HTTPStatusCode"] == 204:
                    log.debug(f"Multipart successfully deleted: {file}")
                    success_counter += 1
                    status_dict[file["Key"]] = True
                else:
                    log.debug(f"Multipart deletion failed: {file}")
                    failure_counter += 1
                    status_dict[file["Key"]] = False

            log.info(f"Successful: {success_counter} | Failed: {failure_counter}")

            return status_dict

        except ClientError as e:
            self._handle_boto3_client_error(e)

    def configure_static_website(
        self,
        index_file: str = "index.html",
        error_file: str = "error.html",
        include_icon: bool = True,
    ) -> bool:
        """Add static website hosting config to an S3 bucket.

        Note:
            WARNING this will set all data to public read policy.

        Args:
            index_file (str): Name of index html file displaying page content.
                Defaults to 'index.html'.
            error_file (str): Name of error html file displaying error content.
                Defaults to 'error.html'.
            include_icon (bool): Include the envidat favicon.ico for the bucket.
                Defaults to True.

        Returns:
            bool: True if success, False is failure.
        """

        client = Bucket.get_boto3_client()

        try:
            log.debug("Setting public read access policy for static website.")
            public_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "PublicRead",
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "s3:GetObject",
                        "Resource": f"arn:aws:s3:::{self.bucket_name}/*",
                    }
                ],
            }
            bucket_policy = json.dumps(public_policy)
            client.put_bucket_policy(Bucket=self.bucket_name, Policy=bucket_policy)
            log.info("Public read access policy set for static website.")

            log.debug("Setting S3 static website configuration...")
            client.put_bucket_website(
                Bucket=self.bucket_name,
                WebsiteConfiguration={
                    "ErrorDocument": {
                        "Key": error_file,
                    },
                    "IndexDocument": {
                        "Suffix": index_file,
                    },
                },
            )

            if include_icon:
                log.debug("Adding envidat favicon.ico to bucket root")
                icon = get_url("https://envidat.ch/favicon.ico").content
                self.put("favicon.ico", icon, content_type="image/x-icon")

            log.info(f"Static website configured for bucket: {self.bucket_name}")

            return True

        except ClientError as e:
            self._handle_boto3_client_error(e)

        return False

    def generate_index_html(
        self, title: str, file_list: Union[list, str], index_file: str = "index.html"
    ) -> BytesIO:
        """Write index file to root of S3 bucket, with embedded S3 download links.

        Args:
            title (str): HTML title tag for page.
            file_list (Union[list, str]): List of file name to generate access urls for.
            index_file (str): Name of index html file displaying page content.
                Defaults to 'index.html'.

        Returns:
            dict: Response dictionary from index file upload.
        """

        if isinstance(file_list, str):
            log.debug(f"Converting string file_list into list: {file_list}")
            file_list = [file_list]

        buf = BytesIO()

        # Start HTML
        html_block = dedent(
            f"""
            <html>
            <head>
            <meta charset="utf-8">
            <title>{title}</title>
            </head>
            <body>
            """
        ).strip()
        log.debug(f"Writing start HTML block to buffer: {html_block}")
        buf.write(html_block.encode("utf_8"))

        # Files
        log.info("Iterating file list to write S3 links to index.")
        for file_name in file_list:
            log.debug(f"File name: {file_name}")
            html_block = dedent(
                f"""
                <div class='flex py-2 xs6'>
                <a href='https://{self.bucket_name}.s3-zh.os.switch.ch/{file_name}'>
                    https://{self.bucket_name}.s3-zh.os.switch.ch/{file_name}
                </a>
                </div>"""
            )
            log.debug(f"Writing file link HTML to buffer: {html_block}")
            buf.write(html_block.encode("utf_8"))

        # Close
        html_block = dedent(
            """
            </body>
            </html>"""
        )
        log.debug(f"Writing end HTML block to buffer: {html_block}")
        buf.write(html_block.encode("utf_8"))

        buf.seek(0)
        decoded_html = buf.read().decode("utf_8")

        response = self.put(index_file, decoded_html, content_type="text/html")
        return response

    def get_cors_config(self) -> dict:
        """Get the CORS config for a bucket.

        Returns:
            dict: Response dictionary containing CORS config.
        """

        client = Bucket.get_boto3_client()

        try:
            log.info(f"Getting CORS config for bucket named {self.bucket_name}")
            response = client.get_bucket_cors(Bucket=self.bucket_name)
            cors_rules = (
                response["CORSRules"][0] if len(response["CORSRules"]) > 0 else None
            )
            return cors_rules

        except ClientError as e:
            self._handle_boto3_client_error(e)

        return None

    def set_cors_config(self, origins: list = None, allow_all: bool = False) -> dict:
        """Set the CORS config for a bucket.

        Args:
            origins (list): List of allowed origins in CORS headers.
                Defaults to None.
            allow_all (bool): Allow all origins, set to wildcard *.
                Defaults to False

        Returns:
            bool: True if success, False is failure.
        """

        client = Bucket.get_boto3_client()

        if allow_all is False and origins is None:
            log.debug("No origins provided for param allow_all")
            self._raise_parameter_error("allow_all", allow_all)

        if allow_all:
            origins = ["*"]

        cors_configuration = {
            "CORSRules": [
                {
                    "AllowedHeaders": ["Authorization"],
                    "AllowedMethods": ["GET", "PUT"],
                    "AllowedOrigins": origins,
                    "ExposeHeaders": ["ETag", "x-amz-request-id"],
                    "MaxAgeSeconds": 3000,
                }
            ]
        }

        try:
            log.info(
                "Setting CORS config for bucket named "
                f"{self.bucket_name} to origins {origins}"
            )
            client.put_bucket_cors(
                Bucket=self.bucket_name, CORSConfiguration=cors_configuration
            )
            return True

        except ClientError as e:
            self._handle_boto3_client_error(e)

        return False
