# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Notebook Name: Employee Engagement Cleaned
# MAGIC **Medallion Layer: Silver**  
# MAGIC
# MAGIC **Purpose:** Does Data Validation, ensuring that the values of attributes are within the appropiate ranges
# MAGIC
# MAGIC **Author:** Matthew Kristanto  
# MAGIC
# MAGIC **Date Created:** 26/03/26  
# MAGIC
# MAGIC **Last Modified:**  
# MAGIC
# MAGIC **Source Table:** [bronze_employee_engagement_injest](https://adb-7405605014654402.2.azuredatabricks.net/editor/notebooks/1864960029131489?o=7405605014654402#command/8176478096240519) 
# MAGIC
# MAGIC
# MAGIC **Notes:**
# MAGIC - Remove the Employee ID
# MAGIC - Removes any Non Alphabetical Character from the Column Titles
# MAGIC - Use Snake Case for the Column Title
# MAGIC - Range Check for Engagement Score, Satisfaction Score and Work Life Balance Score to be between 1-5 (Inclusive)
# MAGIC

# COMMAND ----------

df_bronze = spark.read.table("bronze.bronze_employee_engagement_survey")

display(df_bronze.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Remove Employee ID

# COMMAND ----------

df_bronze = df_bronze.drop("Employee ID")

display(df_bronze.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Character Cleaning

# COMMAND ----------

from pyspark.sql.functions import regexp_replace
import re

df_bronze = df_bronze.toDF(*[
    re.sub(r'[^a-zA-Z]', ' ', c)
    for c in df_bronze.columns
])


display(df_bronze.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Column Title Snake Case

# COMMAND ----------



def to_snake_case(col):
    col = re.sub(r'(?<!^)(?<=[a-zA-Z])(?=[A-Z])', ' ', col).replace(" ", "_")

    return col

columns_snake_case = [to_snake_case(col) for col in df_bronze.columns]

df_silver = df_bronze.toDF(*columns_snake_case)

display(df_silver)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Score Range Check
# MAGIC Removes the Entire Record if its Range is not valid

# COMMAND ----------

from pyspark.sql.functions import col

df_silver = df_silver.filter(
    (col("Engagement_Score").between(1, 5)) &
    (col("Satisfaction_Score").between(1, 5)) &
    (col("Work_Life_Balance_Score").between(1, 5))
)

display(df_silver)

# COMMAND ----------

### Create Silver Schema if not exist
spark.sql("CREATE SCHEMA IF NOT EXISTS silver")

# COMMAND ----------

### Save the Silver Table to the Catalog
(df_silver.write
    .format("delta")  
    .mode("overwrite")  
    .saveAsTable("silver.silver_employee_engagement_cleaned"))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM silver.silver_employee_engagement_cleaned