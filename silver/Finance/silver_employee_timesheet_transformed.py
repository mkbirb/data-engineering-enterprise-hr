# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Notebook Name: Employee Timesheet Transformed
# MAGIC **Medallion Layer: Silver**  
# MAGIC
# MAGIC **Purpose:** Transforms the Data to the appropiate Data Types
# MAGIC
# MAGIC **Author:** Matthew Kristanto  
# MAGIC
# MAGIC **Date Created:** 30/03/26  
# MAGIC
# MAGIC **Last Modified:**  
# MAGIC
# MAGIC **Source Table:** [silver_employee_engagement_transformed](https://adb-7405605014654402.2.azuredatabricks.net/editor/notebooks/3775063119320227?o=7405605014654402) 
# MAGIC
# MAGIC
# MAGIC **Notes:**
# MAGIC - Work_Date changed from String to Date
# MAGIC - Hours_Worked changed from String to Double

# COMMAND ----------

df_silver = spark.read.table("silver.silver_employee_timesheet_cleaned")

display(df_silver.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Work Date: String Type to Date Type

# COMMAND ----------

from pyspark.sql.functions import to_date, date_format, col

### Converts to Day, Month and Year Format first
df_silver = df_silver.withColumn(
    "Work_Date",
    to_date(col("Work_Date"), "yyyy-MM-dd")
)

display(df_silver.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Hours Worked: String Type to Double Type

# COMMAND ----------

df_silver = df_silver.withColumn("Hours_Worked", col("Hours_Worked").cast("double"))

display(df_silver.limit(5))

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS silver

# COMMAND ----------

### Save the Silver Table to the Catalog
(df_silver.write
    .format("delta")  
    .mode("overwrite")  
    .saveAsTable("silver.silver_employee_timesheet_transformed"))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM silver.silver_employee_timesheet_transformed