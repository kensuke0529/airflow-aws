from airflow.providers.amazon.aws.hooks.s3 import S3Hook
import os


def upload_to_s3(file_path: str, bucket_name: str, object_key: str, aws_conn_id: str = 'aws_default') -> None:
    """
    Upload a file to an S3 bucket using Airflow's S3Hook.

    Args:
        file_path (str): Local path to the file.
        bucket_name (str): Name of the S3 bucket.
        object_key (str): S3 object key (folder/filename in S3).
        aws_conn_id (str): Airflow connection ID for AWS credentials.

    Raises:
        FileNotFoundError: If the local file doesn't exist.
        Exception: For other upload errors.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"{file_path} does not exist")

    s3_hook = S3Hook(aws_conn_id=aws_conn_id)

    try:
        s3_hook.load_file(filename=file_path, key=object_key,
                          bucket_name=bucket_name, replace=True)
        print(f"Uploaded {file_path} to s3://{bucket_name}/{object_key}")

    except Exception as e:
        print(f"Upload failed: {e}")
        raise
