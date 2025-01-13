from airflow.models import BaseOperator
from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook
from airflow.hooks.postgres_hook import PostgresHook

class StageToRedshiftOperator(BaseOperator):
    ui_color = '#358140'
    def __init__(self,
                connection_id=None,
                table="",
                s3=None,
                region = "",
                 *args, **kwargs):
        super(StageToRedshiftOperator, self).__init__(*args, **kwargs)
        self.connection_id = connection_id
        self.table = table
        self.s3 = s3
        self.region = region

    def execute(self, context):
        aws_hook = AwsBaseHook(self.connection_id["credentials"], client_type='redshift')
        credentials = aws_hook.get_credentials()
        redshift_hook = PostgresHook(postgres_conn_id=self.connection_id["redshift"])
        
        # Updated to use s3_bucket and prefix
        s3_path = f"s3://{self.s3['bucket_name']}/{self.s3['prefix']}"

        self.log.info(f"Copying data from {s3_path} to Redshift table {self.table}")

        copy_query = f"""
            COPY {self.table}
            FROM '{s3_path}'
            ACCESS_KEY_ID '{credentials.access_key}'
            SECRET_ACCESS_KEY '{credentials.secret_key}'
            FORMAT AS JSON 'auto'
            TIMEFORMAT AS 'auto';
        """

        try:
            redshift_hook.run(copy_query)
            self.log.info("Copy to Redshift completed successfully.")
        except Exception as e:
            self.log.error(f"Error copying data to Redshift: {e}")
            raise