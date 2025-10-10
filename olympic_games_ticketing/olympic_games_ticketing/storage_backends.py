from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    """
    S3 storage backend for public media files.

    Stores uploaded files in the 'media/' prefix of the S3 bucket,
    with no ACLs and no overwriting of existing files.
    """

    location = "media"
    default_acl = None
    file_overwrite = False
