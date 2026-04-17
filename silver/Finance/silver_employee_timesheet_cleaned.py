# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Notebook Name: Employee Timesheet Cleaned
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
# MAGIC **Source Table:** [bronze_injest](https://adb-7405605014654402.2.azuredatabricks.net/editor/notebooks/1864960029131489?o=7405605014654402#command/8176478096240519) 
# MAGIC
# MAGIC
# MAGIC **Notes:**
# MAGIC - Check that the Employee ID starts with EMP and then ends with 4 digit numbers
# MAGIC - Ensure that the Department Values are only Sales, HR, Operations and Marketing.
# MAGIC - Checks if there is a first name and/or a last name, it starts with a capital letter
# MAGIC - Check that the Project Code starts with PROJ and then ends with 4 digit numbers
# MAGIC

# COMMAND ----------

df_bronze = spark.read.table("bronze.bronze_employee_timesheet")

display(df_bronze.limit(5))

# COMMAND ----------

# MAGIC %run /Workspace/Users/matthew.kristanto@exposedata.com.au/superhero_enterprise_hr/helpers/helper_snake_case_column_convertor

# COMMAND ----------


for col_name in df_bronze.columns:
    df_silver = snake_case_column_title_convertor(
        df_silver
    )


display(df_silver.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Employee ID Value Validation
# MAGIC

# COMMAND ----------

from pyspark.sql.functions import col

desired_employee_id_pattern = r"^EMP\d{3}$"

invalid_desired_employee_id_records = df_silver.filter(~col("Employee_Id").rlike(desired_employee_id_pattern))


if invalid_desired_employee_id_records.count() > 0:
    display(invalid_desired_employee_id_records)
    raise ValueError("Invalid EmployeeID format found (expected EMP####)")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Department Values Range Check

# COMMAND ----------

department_values_allowed_values = ["Sales", "HR", "Marketing", "Operations", "Engineering", "Finance"]

invalid_department_values_records = df_silver.filter(~col("Department").isin(department_values_allowed_values))

if invalid_department_values_records.count() > 0:
    display(invalid_department_values_records)
    raise ValueError("Invalid Department_Values found (expected Sales, HR, Marketing, Operations, Engineering, Finance)")



# COMMAND ----------

# MAGIC %md
# MAGIC ### First Name Capital Checking

# COMMAND ----------

from pyspark.sql.functions import col
import json

invalid_first_name_records = df_silver.filter(~col("First_Name").rlike(r"^[A-Z]"))

def CreatingNonCapitalLetterRecords(invalid_records):
  if invalid_records.count() > 0:
    display(invalid_records)

    ### Convert to Dictionary to pass to ADF
    invalid_records_list = invalid_records.toPandas().to_dict(orient='records')

    ### Build the JSON Object
    invalid_records_json = {
      "error_type": "FIRST_NAME_VALIDATION_FAILED",
      "message": "Invalid First_Name format found (expected to begin with a capital letter)",
      "invalid_first_name_records": invalid_records_list
    }


    dbutils.notebook.exit(json.dumps(invalid_records_json))

CreatingNonCapitalLetterRecords(invalid_first_name_records)


# COMMAND ----------

# MAGIC %md
# MAGIC ### Last Name Capital Checking

# COMMAND ----------

invalid_last_name_records = df_silver.filter(~col("Last_Name").rlike(r"^[A-Z]"))

CreatingNonCapitalLetterRecords(invalid_last_name_records)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Project Code Value Validation

# COMMAND ----------

desired_employee_id_pattern = r"^PROJ\d{3}$"

invalid_desired_employee_id_records = df_silver.filter(~col("Employee_Id").rlike(desired_employee_id_pattern))


if invalid_desired_employee_id_records.count() > 0:
    display(invalid_desired_employee_id_records)
    raise ValueError("Invalid ProjectID format found (expected PROJ###)")

# COMMAND ----------

### Create Silver Schema if not exist
spark.sql("CREATE SCHEMA IF NOT EXISTS silver")

# COMMAND ----------

### Save the Silver Table to the Catalog
(df_silver.write
    .format("delta")  
    .mode("overwrite")  
    .saveAsTable("silver.silver_employee_timesheet_cleaned"))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM silver.silver_employee_timesheet_cleaned