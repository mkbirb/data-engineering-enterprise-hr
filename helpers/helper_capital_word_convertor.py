# Databricks notebook source
# MAGIC %md
# MAGIC ## Notebook Name: Capital Word Convertor
# MAGIC **Helper**  
# MAGIC
# MAGIC **Purpose:** Capitalizes each individual word that is given
# MAGIC
# MAGIC **Author:** Matthew Kristanto  
# MAGIC
# MAGIC **Date Created:** 27/03/26  
# MAGIC
# MAGIC **Last Modified:**
# MAGIC
# MAGIC **Notes:**
# MAGIC - Gets the Invalid Records that are not capitalized yet, that are passed from JSON from ADF
# MAGIC
# MAGIC

# COMMAND ----------


import json

invalid_records = json.loads(dbutils.widgets.get("invalid_records"))

display(invalid_records)


# COMMAND ----------

from pyspark.sql.functions import initcap

# Convert invalid_records (list of dicts) to Spark DataFrame
invalid_records_df = spark.createDataFrame(invalid_records)

# Capitalize each word in 'first name' and 'last name' columns
capitalized_df = invalid_records_df.withColumn(
    "first name", initcap("First Name")
).withColumn(
    "last name", initcap("Last Name")
)

display(capitalized_df)

# COMMAND ----------

### Get the "table_name" Parameter from ADF

dbutils.widgets.text("table_name", "")
table_name = dbutils.widgets.get("table_name")

display(table_name)

# COMMAND ----------

### Get the "column_name" Parameter from ADF

dbutils.widgets.text("column_name", "")
column_name = dbutils.widgets.get("column_name")

display(column_name)

# COMMAND ----------

# Retrieve the table using the table_name parameter
source_table_df = spark.table(table_name)

# Update the specified column_name in source_table_df with capitalized values from capitalized_df
# Assuming column_name exists in both DataFrames and is a unique identifier

from pyspark.sql.functions import col

### Join the Source Table from the Capitalized Dataframe that has the Invalid Records
updated_df = source_table_df.join(
    capitalized_df.select(col(column_name), col("first name"), col("last name")),
    on=column_name,
    how="left"    
).withColumn(
    ### Replace the Joined Column with the Capitalized Version
    column_name,
    initcap(col(column_name))
).withColumn(
    ### Overwrite the Joined Columns with the Capitalized Versions
    "first name",
    col("first name")
).withColumn(
    "last name",
    col("last name")
)

display(updated_df)