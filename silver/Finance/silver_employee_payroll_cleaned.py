# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Notebook Name: Employee Payroll Cleaned
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
# MAGIC - Check that the Employee ID starts with EMP and then ends with 4 digit numbers
# MAGIC - Make Capital Letter Snake Case for the Column Title
# MAGIC - Range Check for Employment Status, ensuring that it can only be Active, Terminated and On Leave.
# MAGIC

# COMMAND ----------

df_bronze = spark.read.table("bronze.bronze_employee_payroll")

display(df_bronze.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Employee ID Value Validation

# COMMAND ----------

from pyspark.sql.functions import col

desired_employee_id_pattern = r"^EMP\d{4}$"

invalid_desired_employee_id_records = df_bronze.filter(~col("employee_id").rlike(desired_employee_id_pattern))



if invalid_desired_employee_id_records.count() > 0:
    display(invalid_desired_employee_id_records)
    raise ValueError("Invalid EmployeeID format found (expected EMP####)")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Capital Letter Snake Case Column Title

# COMMAND ----------

def capitalize_snake_case(col_name):
    ### Splits the Column Names into a List using "_" as the seperator
    ### Then capitalizes the first letter of each word, before joining it back again
    return '_'.join([word.capitalize() for word in col_name.split('_')])

new_column_titles = [capitalize_snake_case(col) for col in df_bronze.columns]

df_silver = df_bronze.toDF(*new_column_titles)

display(df_silver.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Employment Status Range Check

# COMMAND ----------

### Determine the valid values for "Employment Status"
employment_status_allowed_values = ["Active", "Terminated", "On Leave"]

invalid_values_in_employment_status = df_silver.filter(~col("Employment_Status").isin(employment_status_allowed_values))

### Display the Invalid Values if found
display(invalid_values_in_employment_status)

if invalid_values_in_employment_status.count() > 0:
  raise ValueError("Invalid values found in column 'Employment_Status'")

# COMMAND ----------

### Create Silver Schema if not exist
spark.sql("CREATE SCHEMA IF NOT EXISTS silver")

# COMMAND ----------

### Save the Silver Table to the Catalog
(df_silver.write
    .format("delta")  
    .mode("overwrite")  
    .saveAsTable("silver.silver_employee_payroll_cleaned"))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM silver.silver_employee_payroll_cleaned