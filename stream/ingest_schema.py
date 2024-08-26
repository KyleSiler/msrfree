from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, ArrayType

spark = (SparkSession.builder
    .master("spark://oasis:7077")
    .getOrCreate()
)

autonation_schema = StructType([StructField("inventory", ArrayType(StructType([
    StructField("vin", StringType()),
    StructField("year", StringType()),
    StructField("trim", StringType())
])))])

#json_files = spark.read.json("/home/ksiler/msrfree/data/autonation")
json_files = spark.read.schema(autonation_schema).json("/home/ksiler/msrfree/data/autonation")

json_files.printSchema()
json_files.show()
