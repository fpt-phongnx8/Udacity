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

# Script generated for node customer_trusted
customer_trusted_node1709397342755 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="customer_trusted",
    transformation_ctx="customer_trusted_node1709397342755",
)

# Script generated for node accelerometer_landing
accelerometer_landing_node1709397404364 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="accelerometer_landing",
    transformation_ctx="accelerometer_landing_node1709397404364",
)

# Script generated for node SQL Query
SqlQuery523 = """
select customer_trusted.* from customer_trusted join accelerometer_landing on customer_trusted.email = accelerometer_landing.user;
"""
SQLQuery_node1709397451705 = sparkSqlQuery(
    glueContext,
    query=SqlQuery523,
    mapping={
        "customer_trusted": customer_trusted_node1709397342755,
        "accelerometer_landing": accelerometer_landing_node1709397404364,
    },
    transformation_ctx="SQLQuery_node1709397451705",
)

# Script generated for node customer_trusted_to_curated
customer_trusted_to_curated_node1709397522005 = glueContext.getSink(
    path="s3://udacity-sdi-lakehouses/customer_trusted_to_curated/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="customer_trusted_to_curated_node1709397522005",
)
customer_trusted_to_curated_node1709397522005.setCatalogInfo(
    catalogDatabase="stedi", catalogTableName="customer_trusted_to_curated"
)
customer_trusted_to_curated_node1709397522005.setFormat(
    "glueparquet", compression="snappy"
)
customer_trusted_to_curated_node1709397522005.writeFrame(SQLQuery_node1709397451705)
job.commit()
