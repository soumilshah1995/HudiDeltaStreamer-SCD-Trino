import sys
import os
os.environ['JAVA_HOME'] = '/opt/homebrew/opt/openjdk@11'

try:
    import os
    import sys
    import pyspark
    from pyspark.sql import SparkSession

    print("Imports loaded")
except Exception as e:
    print("error", e)



HUDI_VERSION = '0.14.0'
SPARK_VERSION = '3.4'

SUBMIT_ARGS = f"--packages org.apache.hadoop:hadoop-aws:3.3.2,org.apache.hudi:hudi-spark{SPARK_VERSION}-bundle_2.12:{HUDI_VERSION} pyspark-shell"
os.environ["PYSPARK_SUBMIT_ARGS"] = SUBMIT_ARGS
os.environ['PYSPARK_PYTHON'] = sys.executable

# Set Spark and Hoodie configurations
spark = SparkSession.builder \
    .config('spark.serializer', 'org.apache.spark.serializer.KryoSerializer') \
    .config('spark.sql.extensions', 'org.apache.spark.sql.hudi.HoodieSparkSessionExtension') \
    .config('spark.sql.hive.convertMetastoreParquet', 'false') \
    .config("spark.hadoop.fs.s3a.endpoint", "http://127.0.0.1:9000/") \
    .config("spark.hadoop.fs.s3a.access.key", "admin") \
    .config("spark.hadoop.fs.s3a.secret.key", "password") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
    .getOrCreate()

path = "s3a://warehouse/default/table_name=customer_dim"

# Load data and create temporary view
spark.read.format("hudi") \
    .load(path) \
    .createOrReplaceTempView("hudi_snapshot")

spark.sql("SELECT customer_dim_key,is_current,customer_id,email FROM hudi_snapshot ").show(truncate=False)
