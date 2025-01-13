from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):
    """
    Airflow Operator for performing data quality checks on tables in Redshift.

    :param redshift_conn_id: Airflow connection ID for Redshift database
    :param tables: List of table names to perform data quality checks on
    """
    @apply_defaults
    def __init__(
        self,
        redshift_conn_id: str,
        tables: list,
        *args, **kwargs
    ):
        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.redshift_conn_id = redshift_conn_id
        self.tables = tables or []  # Ensuring tables is a list to avoid TypeError if None

    def execute(self, context):
        self.log.info('Starting Data Quality Checks...')
        redshift_hook = PostgresHook(self.redshift_conn_id)
        
        failed_checks = []
        for table in self.tables:
            records = redshift_hook.get_records(f"SELECT COUNT(*) FROM {table}")
            if len(records) < 1 or len(records[0]) < 1 or records[0][0] < 1:
                failed_checks.append(table)

        if len(failed_checks) == 0:
            raise ValueError(f"Data quality check failed for tables: {', '.join(failed_checks)}. They returned no results or 0 records.")
        
        for table in self.tables:
            self.log.info(f"Data Quality check passed for {table} with records present.")

