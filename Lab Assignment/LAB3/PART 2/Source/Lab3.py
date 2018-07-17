from pyspark.sql import SparkSession
import pyspark.sql.functions as f
from pyspark.sql.types import StructType, StructField, IntegerType, DateType, StringType, TimestampType

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

df1 = spark.read.format("csv").option("header","true").load("WorldCups.csv")
df1.createOrReplaceTempView("t1")

    q1 = spark.sql("select Winner,collect_set(Year),count(Country) from t1 GROUP BY Winner").show()


