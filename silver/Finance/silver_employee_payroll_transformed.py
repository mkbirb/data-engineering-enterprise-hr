# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Notebook Name: Employee Payroll Transformed
# MAGIC **Medallion Layer: Silver**  
# MAGIC
# MAGIC **Purpose:** Transforms the Data to the appropiate Data Types
# MAGIC
# MAGIC **Author:** Matthew Kristanto  
# MAGIC
# MAGIC **Date Created:** 27/03/26  
# MAGIC
# MAGIC **Last Modified:**  
# MAGIC
# MAGIC **Source Table:** [silver_employee_engagement_cleaned](https://adb-7405605014654402.2.azuredatabricks.net/editor/notebooks/688206018208305?o=7405605014654402#command/8953292221246996) 
# MAGIC
# MAGIC
# MAGIC **Notes:**
# MAGIC - Hire_Date changed from String to Date
# MAGIC - Salary changed from String to Double

# COMMAND ----------

df_silver = spark.read.table("silver.silver_employee_payroll_cleaned")

display(df_silver.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Hire Date: String Type to Date Type

# COMMAND ----------

from pyspark.sql.functions import to_date, date_format, col

### Converts to Day, Month and Year Format first
df_silver = df_silver.withColumn(
    "Hire_Date",
    to_date(col("Hire_Date"), "yyyy-MM-dd")
)


display(df_silver.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Salary: String Type to Double Type

# COMMAND ----------

df_silver = df_silver.withColumn("Salary", col("Salary").cast("double"))

display(df_silver.limit(5))

# COMMAND ----------

### Save the Silver Table to the Catalog
(df_silver.write
    .format("delta")  
    .mode("overwrite")  
    .saveAsTable("silver.silver_employee_payroll_transformed"))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM silver.silver_employee_payroll_transformed