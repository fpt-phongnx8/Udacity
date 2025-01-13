from airflow.models import BaseOperator
from airflow.hooks.postgres_hook import PostgresHook

class CreateTableOperator(BaseOperator):
    ui_color = '#358140'
    def __init__(self, connection_id="redshift", sql_file="", *args, **kwargs):
        """
        Initialize the operator.

        :param connection_id: ID of the Airflow connection to use.
        :param sql_file: Path to the SQL file containing the commands to be executed.
        """
        super().__init__(*args, **kwargs)
        self.connection_id = connection_id
        self.sql_file = sql_file

    def execute(self, context):
        """
        Execute the SQL commands in the specified file.
        """
        postgres_hook = PostgresHook(postgres_conn_id=self.connection_id)

        with open(self.sql_file, 'r') as file:
            sql_commands = file.read().split(';')

        # Filter out any empty or whitespace-only commands
        sql_commands = [cmd.strip() for cmd in sql_commands if cmd.strip()]

        for command in sql_commands:
            self.log.info(f"Executing SQL command: {command}")
            postgres_hook.run(command)
