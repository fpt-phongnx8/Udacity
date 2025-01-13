from airflow.models import BaseOperator
from airflow.hooks.postgres_hook import PostgresHook

class DropTableOperator(BaseOperator):
    ui_color = '#358140'
    def __init__(
        self,
        tables=None,
        connection_id="redshift",
        *args, **kwargs
    ):
        """
        Initializes the operator to drop tables in a Redshift database.

        :param tables: A list of table names to be dropped.
        :param connection_id: Airflow connection ID for the Redshift database.
        """
        super().__init__(*args, **kwargs)
        self.connection_id = connection_id
        self.tables = tables or []  # Simplified default parameter handling

    def execute(self, context):
        """
        Executes the table dropping process.
        """
        if self.tables:
            postgres_hook = PostgresHook(postgres_conn_id=self.connection_id)
            self.log.info(f"Dropping all tables including public.{self.tables}")

            for table in self.tables:
                drop_query = f"DROP TABLE IF EXISTS public.{table};"
                postgres_hook.run(drop_query)
                self.log.info(f"Table public.{table} dropped successfully.")
        else:
            self.log.info("No tables to delete")
