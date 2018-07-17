from pyspark.sql import Row
from pyspark.sql.types import *
from pyspark.sql import SparkSession
spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()
sc = spark.sparkContext
# Load a text file and convert each line to a Row.
lines = sc.textFile("WorldCupMatches.txt")
parts = lines.map(lambda l: l.split(","))
# Each line is converted to a tuple.
matches = parts.map(lambda p: (p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], p[13], p[14], p[15], p[16], p[17], p[18], p[19] .strip()))
# The schema is encoded in a string.
schemaString = "Year Datetime Stage Stadium City Home_Team_Name Home_Team_Goals Away_Team_Goals Away_Team_Name Win_conditions Attendance Half-time_Home_Goals Half-time_Away_Goals Referee Assistant_1 Assistant_2 RoundID MatchID Home_Team_Initials Away_Team_Initials"
fields = [StructField(field_name, StringType(), True) for field_name in schemaString.split()]
schema = StructType(fields)
# Apply the schema to the RDD
schemaMatches = spark.createDataFrame(matches, schema)
# Creates a temporary view using the DataFrame
schemaMatches.createOrReplaceTempView("matches")
#query5 = spark.sql("SELECT Home_Team_Name As COUNTRY,COUNT(Home_Team_Goals) AS No_of_Times FROM matches where Home_Team_Goals >=4 GROUP BY Home_Team_Name ORDER BY 2 DESC").show()


#query1 = spark.sql("SELECT Stage,Stadium,City,Home_Team_Name FROM matches WHERE Home_Team_Goals >= 3 AND Home_Team_Goals <= 10").show()

#q9 = spark.sql("SELECT Home_Team_Name, MAX(Home_Team_Goals) from matches where Year BETWEEN 2000 AND 2010 GROUP BY Home_Team_Name ORDER BY 2 DESC").show()

q10= spark.sql("SELECT collect_set(Home_Team_Name) from matches").show()
