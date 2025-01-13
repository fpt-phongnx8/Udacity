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

# Script generated for node step_trainer_landing
step_trainer_landing_node1709398464114 = glueContext.create_dynamic_frame.from_catalog(
    database="stedi",
    table_name="step_trainer_landing",
    transformation_ctx="step_trainer_landing_node1709398464114",
)

# Script generated for node customer_trusted_to_curated
customer_trusted_to_curated_node1709398421322 = (
    glueContext.create_dynamic_frame.from_catalog(
        database="stedi",
        table_name="customer_trusted_to_curated",
        transformation_ctx="customer_trusted_to_curated_node1709398421322",
    )
)

# Script generated for node SQL Query
SqlQuery404 = """
select * 
from step_trainer_landing where serialnumber in (select serialnumber from customer_trusted_to_curated);
"""
SQLQuery_node1709430909706 = sparkSqlQuery(
    glueContext,
    query=SqlQuery404,
    mapping={
        "step_trainer_landing": step_trainer_landing_node1709398464114,
        "customer_trusted_to_curated": customer_trusted_to_curated_node1709398421322,
    },
    transformation_ctx="SQLQuery_node1709430909706",
)

# Script generated for node step_trainer_trusted
step_trainer_trusted_node1709398544454 = glueContext.getSink(
    path="s3://udacity-sdi-lakehouses/step_trainer/trusted/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    enableUpdateCatalog=True,
    transformation_ctx="step_trainer_trusted_node1709398544454",
)
step_trainer_trusted_node1709398544454.setCatalogInfo(
    catalogDatabase="stedi", catalogTableName="step_trainer_trusted"
)
step_trainer_trusted_node1709398544454.setFormat("json")
step_trainer_trusted_node1709398544454.writeFrame(SQLQuery_node1709430909706)
job.commit()
