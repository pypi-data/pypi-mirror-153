# utils.py
# functions to help out with procedures on an AWS account

# All of these require a aws configuration file.

from zipfile import ZipFile
import boto3
import io
import pickle
import numpy as np
import pandas as pd

## __all__ file determines what a user can import from utils
__all__ = ["s3_zip_download"]

#### Utility functions for the Utility module. #####
# Reuse these as much as you can
def __setup_session():
    """Sets up the aws boto3 session and returns error if credentials
    are invalid.

    returns session
    """
    try:
        alias = boto3.client("iam").list_account_aliases()["AccountAliases"][0]
        print(f"Using: '{alias}' AWS Account")
        session = boto3.session.Session()
        return session
    except:
        raise Exception(
            "AWS credentials invalid, configure these by running 'aws configure'"
        )


#### Actual functionality utilities #####
def s3_zip_download(bucket_name: str, key: str):
    """Extracts the contents of a zip file in S3 into the current directory of the file.

    Args:
        bucket_name (str): S3 bucket that contains the zip file
        key (str): S3 key of the zip file within the bucket
    """

    # Initialise session get s3 resource
    session = __setup_session()
    s3_resource = session.resource("s3")

    # Get the zip file in s3 as an object
    bucket = s3_resource.Bucket(bucket_name)
    zip_obj = s3_resource.Object(bucket_name=bucket_name, key=key)

    # Pull the file from s3 and get zip object
    data = io.BytesIO(zip_obj.get()["Body"].read())

    # Metadata object
    file_info = {}

    # Iterate through files create metadata and extract to current dir
    with ZipFile(data) as z:
        for filename in z.namelist():
            file_info[filename] = z.getinfo(filename)
        zfile.extractall()

    return file_info
