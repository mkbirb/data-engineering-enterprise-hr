# Databricks notebook source
# MAGIC %md
# MAGIC ## Notebook Name: Training and Development Transformed
# MAGIC **Medallion Layer: Silver**  
# MAGIC
# MAGIC **Purpose:** Transforms the Data to the appropiate Data Types
# MAGIC
# MAGIC **Author:** Matthew Kristanto  
# MAGIC
# MAGIC **Date Created:** 31/03/26  
# MAGIC
# MAGIC **Last Modified:**  
# MAGIC
# MAGIC **Source Table:** [silver_training_and_development_cleaned](https://adb-7405605014654402.2.azuredatabricks.net/editor/notebooks/4362505560230414?o=7405605014654402) 
# MAGIC
# MAGIC
# MAGIC **Notes:**
# MAGIC - Convert Training_Date from String to Date
# MAGIC - Convert Training_Duration from String to Integer
# MAGIC - Convert Training_Cost from String to Double
# MAGIC

# COMMAND ----------

df_silver = spark.read.table("silver.silver_training_and_development_cleaned")

display(df_silver.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Training Date: String Type to Date Type

# COMMAND ----------

from pyspark.sql.functions import upper, col, try_to_date


df_silver = df_silver.withColumn(
    "Training_Date",
    ### Triple M is for textual month name
    to_date(upper(col("Training_Date")), "dd-MMM-yy")
)


display(df_silver.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Training Duration: String Type to Integer Type

# COMMAND ----------

df_silver = df_silver.withColumn("Training_Durationdays", df_silver["Training_Durationdays"].cast("int"))

display(df_silver.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Training Cost: String Type to Double Type

# COMMAND ----------

df_silver = df_silver.withColumn("Training_Cost", df_silver["Training_Cost"].cast("Double"))

# COMMAND ----------

### Save the Silver Table to the Catalog
(df_silver.write
    .format("delta")  
    .mode("overwrite")  
    .saveAsTable("silver.silver_training_and_development_transformed"))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM silver.silver_training_and_development_transformed