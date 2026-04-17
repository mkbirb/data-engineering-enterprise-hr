# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Notebook Name: Employee Engagement Transformed
# MAGIC **Medallion Layer: Silver**  
# MAGIC
# MAGIC **Purpose:** Transforms the Data to the appropiate Data Types
# MAGIC
# MAGIC **Author:** Matthew Kristanto  
# MAGIC
# MAGIC **Date Created:** 26/03/26  
# MAGIC
# MAGIC **Last Modified:**  
# MAGIC
# MAGIC **Source Table:** [silver_employee_engagement_cleaned](https://adb-7405605014654402.2.azuredatabricks.net/editor/notebooks/688206018208305?o=7405605014654402#command/8953292221246996) 
# MAGIC
# MAGIC
# MAGIC **Notes:**
# MAGIC - Survey_Date changed from String Data Type to Column Data Type
# MAGIC - Engagement_Score, Satisfaction_Score and Work_Life_Balance_Score changed from String Data Type to Integer Data Type

# COMMAND ----------

df_silver = spark.read.table("silver.silver_employee_engagement_cleaned")

display(df_silver.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Survey Date: String Type to Date Type

# COMMAND ----------

from pyspark.sql.functions import to_date

df_silver = df_silver.withColumn("Survey_Date", to_date("Survey_Date", "dd-MM-yyyy"))

display(df_silver.limit(5))

# COMMAND ----------

### Save the Silver Table to the Catalog
(df_silver.write
    .format("delta")  
    .mode("overwrite")  
    .saveAsTable("silver.silver_employee_engagement_transformed"))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM silver.silver_employee_engagement_transformed