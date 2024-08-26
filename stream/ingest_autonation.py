from pyspark.sql import SparkSession
from pyspark.sql import functions as sf

spark = (
    SparkSession.builder.appName("IngestAutonation")
    .master("spark://oasis:7077")
    .getOrCreate()
)

spark.conf.set("spark.sql.session.timeZone", "America/Los_Angeles")

# Need to create a schema that will be used on read
json_stream = spark.readStream.json(
        "/home/ksiler/msrfree/data/autonation"
)

df_autonation = json_stream.select(sf.explode("inventory").alias("inventory"))
df_autonation = df_autonation.withColumn("fileName", sf.input_file_name())
df_autonation = df_autonation.withColumn(
    "dealership",
    sf.regexp_extract(sf.col("fileName"), r"(\w*)-\d{4}\d{2}\d{2}", 1),
)
df_autonation = df_autonation.withColumn(
    "date", sf.regexp_extract(sf.col("fileName"), r"(\d{4}\d{2}\d{2})", 1)
).drop("fileName")
df_autonation = df_autonation.withColumn("date", sf.to_date(sf.col("date"), "yyyyMMdd"))
df_autonation.select(
    "date",
    "inventory.vin",
    "dealership",
    "inventory.year",
    "inventory.trim",
    sf.expr("ucase(split_part(inventory.trim, ' ', 1))").alias("s_trim"),
    sf.expr("filter(inventory.attributes, x -> x.name = 'exteriorColor')")
    .getItem(0)["normalizedValue"]
    .alias("color"),
    # sf.col("inventory.attributes").getItem(2)["normalizedValue"],\
    sf.regexp_replace(sf.col("inventory.pricing.retailPrice"), "[$,]", "")
    .cast("double")
    .alias("retail_price"),
    sf.expr(
        "regexp_replace((filter(inventory.pricing.dPrice, x -> x.type = 'TOTAL'))[0].value, '[$,]', '')"
    )
    .cast("double")
    .alias("final_price"),
    sf.expr("(final_price / retail_price) * 100").alias("final_percent"),
).writeStream.toTable("autonation_gladiators", outputMode="append", format="parquet")


# TODO: Go through all selects. At the end need to create df.writeStream.format("parquet").start()
# TODO: try executing the stream and see if it outputs a file, and where
