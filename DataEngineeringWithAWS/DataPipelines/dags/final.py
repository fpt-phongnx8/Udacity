import pendulum
from datetime import timedelta
from airflow import DAG

from common.create_table import CreateTableOperator
from common.drop_table import DropTableOperator
from common.stage_redshift import StageToRedshiftOperator
from common.load_fact import LoadFactOperator
from common.sql_queries import SqlQueries
from common.load_dimension import LoadDimensionOperator
from common.data_quality import DataQualityOperator

default_args = {
    'owner': 'niannguyen',
    'depends_on_past': False,
    'start_date': pendulum.now(),
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

dag = DAG('final-dag',
        default_args=default_args,
        description='Load and transform data in Redshift with Airflow',
        schedule_interval='0 * * * *'
        )

start_operator = CreateTableOperator(
    task_id='Begin_execution',
    dag=dag,
    connection_id="redshift",
    sql_file="/home/workspace/airflow/dags/common/sql/create.sql"
)

stage_events_to_redshift = StageToRedshiftOperator(
    task_id='Stage_events',
    dag=dag,
    table="staging_events",
    region="us-east-1",
    s3={
        "bucket_name": "udacity-datapepline",
        "prefix": "log-data"
    },
    connection_id={
        "credentials": "aws_credentials",
        "redshift": "redshift"
    }
)

stage_songs_to_redshift = StageToRedshiftOperator(
    task_id='song_events',
    dag=dag,
    table="staging_songs",
    region="us-east-1",
    s3={
        "bucket_name": "udacity-datapepline",
        "prefix": "song-data"
    },
    connection_id={
        "credentials": "aws_credentials",
        "redshift": "redshift"
    }
)

load_songplays_table = LoadFactOperator(
    task_id='Load_songplays_fact_table',
    dag=dag,
    connection_id="redshift",
    table="songplays",
    sql_query=SqlQueries.songplay_table_insert
)

load_user_dimension_table = LoadDimensionOperator(
    task_id='Load_user_dim_table',
    dag=dag,
    connection_id="redshift",
    table="users",
    sql_query=SqlQueries.user_table_insert
)

load_song_dimension_table = LoadDimensionOperator(
    task_id='Insert_song_dim_table',
    dag=dag,
    connection_id="redshift",
    table="songs",
    sql_query=SqlQueries.song_table_insert
)

load_artist_dimension_table = LoadDimensionOperator(
    task_id='Load_artist_dim_table',
    dag=dag,
    connection_id="redshift",
    table="artists",
    sql_query=SqlQueries.artist_table_insert
)

load_time_dimension_table = LoadDimensionOperator(
    task_id='Load_time_dim_table',
    dag=dag,
    connection_id="redshift",
    table="time",
    sql_query=SqlQueries.time_table_insert
)

run_quality_checks = DataQualityOperator(
    task_id='Run_data_quality_checks',
    dag=dag,
    redshift_conn_id="redshift",
    tables=["songplays", "artists", "time", "songs", "users"]
)

end_operator = DropTableOperator(task_id='Stop_execution', dag=dag, connection_id="redshift",
                                tables=["artists", "songplays", "songs", "time", "users"])

start_operator >> [ stage_events_to_redshift, stage_songs_to_redshift ] >> load_songplays_table >> [
    load_user_dimension_table,
    load_song_dimension_table,
    load_artist_dimension_table,
    load_time_dimension_table
] >> run_quality_checks >> end_operator

