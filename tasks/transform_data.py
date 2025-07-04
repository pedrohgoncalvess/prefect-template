import polars as pl
from prefect import task
import s3fs
from datetime import datetime

from utils import get_env_var
from log import logger


@task(
    name="transform_and_save_parquet",
    description="Transforms a DataFrame and saves it back to MinIO/S3",
    retries=2,
    retry_delay_seconds=20
)
async def transform_and_save_parquet(
        df: pl.DataFrame,
        bucket_name: str,
        output_path: str
) -> bool:
    """
    Performs simple transformations on a DataFrame and saves it as Parquet to MinIO/S3.

    Args:
        df: Input Polars DataFrame to transform
        bucket_name: Name of the bucket in MinIO/S3
        output_path: Path where to save the file within the bucket

    Returns:
        Boolean indicating success or failure
    """
    if df is None or df.is_empty():
        await logger.warning("Transform", "Process", "Empty DataFrame provided, nothing to transform")
        return False

    try:
        transformed_df = df.with_columns([
            pl.col("*").fill_null(0),
            pl.lit(datetime.now()).alias("processed_at")
        ])

        if "amount" in transformed_df.columns:
            transformed_df = transformed_df.with_columns([
                pl.col("amount").sum().over("category").alias("category_total")
            ])

        s3 = s3fs.S3FileSystem(
            key=get_env_var("S3_USER"),
            secret=get_env_var("S3_PASSWORD"),
            endpoint_url=get_env_var("S3_HOST"),
        )

        full_path = f"{bucket_name}/{output_path}"

        with s3.open(full_path, "wb") as f:
            transformed_df.write_parquet(f)

        await logger.info("Transform", "Save", f"Successfully saved transformed data to {full_path}")
        return True

    except Exception as e:
        await logger.error("Transform", "Process", f"Error transforming or saving data: {str(e)}")
        return False