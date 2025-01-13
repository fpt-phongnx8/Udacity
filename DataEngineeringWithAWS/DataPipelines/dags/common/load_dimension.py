from airflow.models import BaseOperator
from airflow.hooks.postgres_hook import PostgresHook

class LoadDimensionOperator(BaseOperator):
    ui_color = '#80BD9E'
    def __init__(
        self,
        connection_id: str,
        table: str,
        sql_query: str,
        is_truncated: bool = True,
        *args, **kwargs
    ):
        """
        Initialize the LoadDimensionOperator to load data into a dimension table.

        :param connection_id: The Airflow connection ID to use for the PostgreSQL database.
        :param table: The name of the target dimension table.
        :param sql_query: The SQL query to execute for loading data into the dimension table.
        :param is_truncated: Flag to determine if the dimension table should be truncated before loading new data.
        """
        super(LoadDimensionOperator, self).__init__(*args, **kwargs)
        self.connection_id = connection_id
        self.table = table
        self.sql_query = sql_query
        self.is_truncated = is_truncated

    def execute(self, context):
        postgres_hook = PostgresHook(postgres_conn_id=self.connection_id)
        self.log.info(f'Loading data into {self.table} dimension table.')

        if self.is_truncated:
            self.log.info(f"Clearing data from {self.table} table...")
            postgres_hook.run(f"TRUNCATE TABLE {self.table}")
            self.log.info(f"Table {self.table} has been cleared.")

        postgres_hook.run(f"""
            INSERT INTO {self.table}
            {self.sql_query};
        """)

        self.log.info(f'Data has been loaded into {self.table} dimension table.')
