from prefect import flow

from log import logger
from tasks import read_parquet_from_minio, transform_and_save_parquet


@flow(
    name="etl_template_flow",
    description="Template ETL flow demonstrating data extraction, transformation and loading",
    version="1.0.0"
)
async def etl_template_flow(
        source_bucket: str = "raw-data",
        source_file: str = "sample/data.parquet",
        target_bucket: str = "processed-data",
        target_file: str = "output/processed_data.parquet"
):
    """
    A template ETL flow that reads data from MinIO/S3, transforms it, and saves it back.

    Args:
        source_bucket: Source bucket name in MinIO/S3
        source_file: Source file path within the bucket
        target_bucket: Target bucket name in MinIO/S3
        target_file: Target file path within the bucket
    """
    await logger.info("Flow", "Start", f"Starting ETL template flow")

    df = await read_parquet_from_minio(
        bucket_name=source_bucket,
        file_path=source_file
    )

    if df is not None:
        await logger.info("Flow", "Extract", f"Successfully read {df.shape[0]} rows from source")

        success = await transform_and_save_parquet(
            df=df,
            bucket_name=target_bucket,
            output_path=target_file
        )

        if success:
            await logger.info("Flow", "Complete", "ETL process completed successfully")
        else:
            await logger.error("Flow", "Failed", "ETL process failed during transform/load phase")
    else:
        await logger.error("Flow", "Failed", "ETL process failed during extract phase")

    return df is not None and success