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

# Script generated for node Amazon S3
AmazonS3_node1709394577994 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="customer_landing",
    transformation_ctx="AmazonS3_node1709394577994",
)

# Script generated for node SQL Query
SqlQuery464 = """
select * from myDataSource where sharewithresearchasofdate is not null;
"""
SQLQuery_node1709394632580 = sparkSqlQuery(
    glueContext,
    query=SqlQuery464,
    mapping={"myDataSource": AmazonS3_node1709394577994},
    transformation_ctx="SQLQuery_node1709394632580",
)

# Script generated for node Amazon S3
AmazonS3_node1709394690606 = glueContext.getSink(
    path="s3://udacity-sdi-lakehouses/customer/trusted/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="AmazonS3_node1709394690606",
)
AmazonS3_node1709394690606.setCatalogInfo(
    catalogDatabase="stedi", catalogTableName="customer_trusted"
)
AmazonS3_node1709394690606.setFormat("json")
AmazonS3_node1709394690606.writeFrame(SQLQuery_node1709394632580)
job.commit()
