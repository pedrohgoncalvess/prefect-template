import polars as pl
from prefect import task
import s3fs

from utils import get_env_var
from log import logger


@task(
    name="read_parquet_from_minio",
    description="Reads a Parquet file from MinIO/S3 using Polars",
    retries=3,
    retry_delay_seconds=30
)
async def read_parquet_from_minio(
        bucket_name: str,
        file_path: str
) -> pl.DataFrame | None:
    """
    Reads a Parquet file stored in MinIO/S3 using Polars.

    Args:
        bucket_name: Name of the bucket in MinIO/S3
        file_path: Path to the file within the bucket

    Returns:
        Polars DataFrame with the read data
    """

    s3 = s3fs.S3FileSystem(
        key=get_env_var("S3_USER"),
        secret=get_env_var("S3_PASSWORD"),
        endpoint_url=f"http://{get_env_var('S3_HOST')}:{get_env_var('S3_PORT')}",
    )

    full_path = f"{bucket_name}/{file_path}"

    if not s3.exists(full_path):
        await logger.error("S3", "Read", f"File not found: {full_path}")
        return None

    with s3.open(full_path, "rb") as f:
        df = pl.scan_parquet(f).collect()

    return df