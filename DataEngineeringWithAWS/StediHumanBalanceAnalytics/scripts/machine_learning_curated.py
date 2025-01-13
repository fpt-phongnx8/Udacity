import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame


def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)


args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node step_trainer_trusted
step_trainer_trusted_node1709431756453 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="step_trainer_trusted",
    transformation_ctx="step_trainer_trusted_node1709431756453",
)

# Script generated for node accelerometer_trusted
accelerometer_trusted_node1709431786236 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="accelerometer_trusted",
    transformation_ctx="accelerometer_trusted_node1709431786236",
)

# Script generated for node SQL Query
SqlQuery522 = """
select * 
from step_trainer_trusted join accelerometer_trusted on accelerometer_trusted.timestamp = step_trainer_trusted.sensorreadingtime
"""
SQLQuery_node1709431814904 = sparkSqlQuery(
    glueContext,
    query=SqlQuery522,
    mapping={
        "step_trainer_trusted": step_trainer_trusted_node1709431756453,
        "accelerometer_trusted": accelerometer_trusted_node1709431786236,
    },
    transformation_ctx="SQLQuery_node1709431814904",
)

# Script generated for node Amazon S3
AmazonS3_node1709432601661 = glueContext.getSink(
    path="s3://udacity-sdi-lakehouses/step_trainer/curated/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    compression="snappy",
    enableUpdateCatalog=True,
    transformation_ctx="AmazonS3_node1709432601661",
)
AmazonS3_node1709432601661.setCatalogInfo(
    catalogDatabase="stedi", catalogTableName="machine_learning_curated"
)
AmazonS3_node1709432601661.setFormat("json")
AmazonS3_node1709432601661.writeFrame(SQLQuery_node1709431814904)
job.commit()
