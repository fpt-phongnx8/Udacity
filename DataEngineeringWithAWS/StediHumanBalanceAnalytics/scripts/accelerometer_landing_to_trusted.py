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
customer_trusted_node1709396357218 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="customer_trusted",
    transformation_ctx="customer_trusted_node1709396357218",
)

# Script generated for node accelerometer_landing
accelerometer_landing_node1709396388933 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="accelerometer_landing",
    transformation_ctx="accelerometer_landing_node1709396388933",
)

# Script generated for node join query
SqlQuery449 = """
select accelerometer_landing.* from accelerometer_landing join customer_trusted on customer_trusted.email = accelerometer_landing.user;
"""
joinquery_node1709396430588 = sparkSqlQuery(
    glueContext,
    query=SqlQuery449,
    mapping={
        "customer_trusted": customer_trusted_node1709396357218,
        "accelerometer_landing": accelerometer_landing_node1709396388933,
    },
    transformation_ctx="joinquery_node1709396430588",
)

# Script generated for node accelerometer_trusted
accelerometer_trusted_node1709396858671 = glueContext.getSink(
    path="s3://udacity-sdi-lakehouses/accelerometer/trusted/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="accelerometer_trusted_node1709396858671",
)
accelerometer_trusted_node1709396858671.setCatalogInfo(
    catalogDatabase="stedi", catalogTableName="accelerometer_trusted"
)
accelerometer_trusted_node1709396858671.setFormat("json")
accelerometer_trusted_node1709396858671.writeFrame(joinquery_node1709396430588)
job.commit()
