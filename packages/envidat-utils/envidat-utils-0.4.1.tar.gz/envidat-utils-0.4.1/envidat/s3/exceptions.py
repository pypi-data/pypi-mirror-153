import logging

from botocore.exceptions import ClientError

log = logging.getLogger(__name__)


class BucketException(Exception):
    """Parent class to be inherited for consistency."""

    def __init__(self, message, bucket):
        log.error(message)
        self.bucket = bucket
        self.message = f"{message}"
        super().__init__(self.message)


class NoSuchKey(BucketException):
    """Exception for if bucket key does not exist."""

    def __init__(self, key, bucket):
        self.key = key
        self.bucket = bucket
        self.message = f"Object not found in bucket {bucket} matching {key}"
        super().__init__(self.message, self.bucket)


class NoSuchBucket(BucketException):
    """Exception for if bucket does not exist."""

    def __init__(self, bucket_name):
        self.bucket = bucket_name
        self.message = f"Bucket named '{bucket_name}' does not exist!"
        super().__init__(self.message, self.bucket)


class BucketAlreadyExists(BucketException):
    """Exception for if bucket already exists."""

    def __init__(self, bucket_name):
        self.bucket = bucket_name
        self.message = f"Bucket named '{bucket_name}' already exists. Creation failed."
        super().__init__(self.message, self.bucket)


class BucketAccessDenied(BucketException):
    """Exception for if bucket access is denied."""

    def __init__(self, bucket_name):
        self.bucket = bucket_name
        self.message = f"Unable to access bucket {self.bucket}. Does it exist?"
        super().__init__(self.message, self.bucket)


class NoSuchCORSConfiguration(BucketException):
    """Exception for if the bucket does not have a CORS configuration."""

    def __init__(self, bucket_name):
        self.bucket = bucket_name
        self.message = f"Bucket {self.bucket} does not have CORS configured."
        super().__init__(self.message, self.bucket)


class UnknownBucketException(BucketException):
    """Exception to catch all other unknown errors."""

    def __init__(self, bucket_name, e: ClientError):
        self.bucket = bucket_name
        error_code: str = e.response.get("Error").get("Code")
        error_message: str = e.response.get("Error").get("Message")
        self.message = f"Unknown bucket exception {error_code}: {error_message}"
        super().__init__(self.message, self.bucket)
