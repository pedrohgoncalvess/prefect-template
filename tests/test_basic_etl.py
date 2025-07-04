"""
Testing Prefect Flows: Best Practices

- Mock external dependencies (APIs, databases, file systems)
- Test both happy paths and error scenarios
- Verify task interactions and parameter passing
- Check logging for proper monitoring
- Focus on behavior, not implementation details
"""
import pytest
import polars as pl
from unittest.mock import patch, AsyncMock

from flows import etl_template_flow


@pytest.mark.asyncio
async def test_etl_template_flow_success():
    """Test successful execution of the ETL flow."""
    test_df = pl.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})

    with patch('tasks.read_parquet_from_minio', new_callable=AsyncMock) as mock_read, \
            patch('tasks.transform_and_save_parquet', new_callable=AsyncMock) as mock_transform, \
            patch('log.logger', new_callable=AsyncMock) as mock_logger:
        mock_read.return_value = test_df
        mock_transform.return_value = True

        result = await etl_template_flow(
            source_bucket="test",
            source_file="test/input.parquet",
            target_bucket="test-target",
            target_file="test/output.parquet"
        )

        assert result is True

        mock_read.assert_called_once_with(
            bucket_name="test",
            file_path="test/test.parquet"
        )

        mock_transform.assert_called_once_with(
            df=test_df,
            bucket_name="test-target",
            output_path="test/output.parquet"
        )

        assert mock_logger.info.call_count == 3
        assert mock_logger.error.call_count == 0