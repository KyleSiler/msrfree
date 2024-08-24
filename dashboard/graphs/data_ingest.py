from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as sf


class DataIngest:
    def __init__(self):
        self.spark = SparkSession.builder.master("spark://oasis:7077").getOrCreate()
        self.spark.conf.set("spark.sql.session.timeZone", "America/Los_Angeles")
        df_autonation = self.createAutonationDataFrame()
        df_elkgrove = self.createElkGroveDataFrame()
        self.df_all_dealerships = df_autonation.union(df_elkgrove)

    def createAutonationDataFrame(self) -> DataFrame:
        df_autonation = self.spark.read.json(
            [
                "/home/ksiler/msrfree/data/roseville**.json",
                "/home/ksiler/msrfree/data/sacramento**.json",
                "/home/ksiler/msrfree/data/folsom**.json",
            ]
        )
        df_autonation = df_autonation.select(sf.explode("inventory").alias("inventory"))
        df_autonation = df_autonation.withColumn("fileName", sf.input_file_name())
        df_autonation = df_autonation.withColumn(
            "dealership",
            sf.regexp_extract(sf.col("fileName"), r"(\w*)-\d{4}\d{2}\d{2}", 1),
        )
        df_autonation = df_autonation.withColumn(
            "date", sf.regexp_extract(sf.col("fileName"), r"(\d{4}\d{2}\d{2})", 1)
        ).drop("fileName")
        df_autonation = df_autonation.withColumn(
            "date", sf.to_date(sf.col("date"), "yyyyMMdd")
        )
        return df_autonation.select(
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
        )

    def createElkGroveDataFrame(self) -> DataFrame:
        self.spark.conf.set("spark.sql.caseSensitive", True)

        df_elkgrove = self.spark.read.json(
            [
                "/home/ksiler/msrfree/data/elkgrove**.json",
                "/home/ksiler/msrfree/data/placerville**.json",
            ],
            mode="DROPMALFORMED",
        )

        df_elkgrove = df_elkgrove.withColumn("fileName", sf.input_file_name())
        df_elkgrove = df_elkgrove.withColumn(
            "dealership",
            sf.regexp_extract(sf.col("fileName"), r"(\w*)-\d{4}\d{2}\d{2}", 1),
        )
        df_elkgrove = df_elkgrove.withColumn(
            "date", sf.regexp_extract(sf.col("fileName"), r"(\d{4}\d{2}\d{2})", 1)
        ).drop("fileName")
        df_elkgrove = df_elkgrove.withColumn(
            "date", sf.to_date(sf.col("date"), "yyyyMMdd")
        )

        return (
            df_elkgrove.withColumn("first_result", sf.element_at("results", 1))
            .drop("results")
            .withColumn("hit", sf.explode("first_result.hits"))
            .drop("first_result")
            .select(
                "date",
                "hit.vin",
                "dealership",
                "hit.year",
                "hit.trim",
                sf.expr("ucase(split_part(hit.trim, ' ', 1))").alias("s_trim"),
                sf.col("hit.ext_color_generic").alias("color"),
                sf.col("hit.msrp").alias("retail_price"),
                sf.col("hit.our_price").alias("final_price"),
                sf.expr("(final_price / retail_price) * 100").alias("final_percent"),
            )
        )
