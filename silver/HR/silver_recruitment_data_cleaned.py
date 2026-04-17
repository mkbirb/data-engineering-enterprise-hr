# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Notebook Name: Recruitment Data Cleaned
# MAGIC **Medallion Layer: Silver**  
# MAGIC
# MAGIC **Purpose:** Does Data Validation, ensuring that the values of attributes are within the appropiate ranges
# MAGIC
# MAGIC **Author:** Matthew Kristanto  
# MAGIC
# MAGIC **Date Created:** 30/03/26  
# MAGIC
# MAGIC **Last Modified:**  
# MAGIC
# MAGIC **Source Table:** [bronze_injest](https://adb-7405605014654402.2.azuredatabricks.net/editor/notebooks/1864960029131489?o=7405605014654402#command/8176478096240519) 
# MAGIC
# MAGIC
# MAGIC **Notes:**
# MAGIC - Use Snake Case for Column Title
# MAGIC - Ensure that Applicant_ID is in four digit format
# MAGIC - Ensure that First_Name Values start with a capital letter
# MAGIC - Ensure that Last_Name Values start with a capital letter
# MAGIC - Ensure that Gender Values are either Male, Female or Other
# MAGIC - Ensure that the Phone_Number Column is split into Phone_e164 (Stores the Cleaned Phone Number in Global Format), Phone_Extension (Seperated from the Main Phone Number) and Is_Valid_Phone_Number (Determines whether the Phone Number is usable or not)
# MAGIC - Ensure that the Email has a "@" symbol and a ".com", ".net" or ".org"
# MAGIC - Ensure that Education_Level is only High School, Bachelor's Degree, Master's Degree or PHD
# MAGIC - Ensure that the Status is only Interviewing, Rejected, In Review or Offered
# MAGIC
# MAGIC

# COMMAND ----------

df_bronze = spark.read.table("bronze.bronze_recruitment_data")

display(df_bronze.limit(5))

# COMMAND ----------

df_silver = df_bronze

# COMMAND ----------

# MAGIC %md
# MAGIC ### Column Title Snake Case

# COMMAND ----------

# MAGIC %run /Workspace/Users/matthew.kristanto@exposedata.com.au/superhero_enterprise_hr/helpers/helper_snake_case_column_convertor

# COMMAND ----------

# DBTITLE 1,Apply snake case conversion

for col_name in df_bronze.columns:
    df_silver = snake_case_column_title_convertor(
        df_silver
    )


display(df_silver.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Applicant ID Format Value Validation

# COMMAND ----------

# MAGIC %run /Workspace/Users/matthew.kristanto@exposedata.com.au/superhero_enterprise_hr/helpers/helper_four_digit_format_checker

# COMMAND ----------

four_digit_format_checker(df_silver, "Applicant_ID")

# COMMAND ----------

# MAGIC %md
# MAGIC ### First Name Capital Checking

# COMMAND ----------

# MAGIC %run /Workspace/Users/matthew.kristanto@exposedata.com.au/superhero_enterprise_hr/helpers/helper_capital_letter_checker

# COMMAND ----------

capital_letter_checker(df_silver, "First_Name")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Last Name Capital Checking

# COMMAND ----------

capital_letter_checker(df_silver, "Last_Name")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Gender Values Validation

# COMMAND ----------

# MAGIC %run /Workspace/Users/matthew.kristanto@exposedata.com.au/superhero_enterprise_hr/helpers/helper_valid_values_checker

# COMMAND ----------

valid_values_checker(df_silver, "Gender", ["Male", "Female", "Other"])

# COMMAND ----------

# MAGIC %md
# MAGIC ### Phone Number Column Splitting

# COMMAND ----------

from pyspark.sql.functions import col, regexp_extract, regexp_replace, when, length, lit, concat


### Extract the Extension from the Phone Number
df_silver = df_silver.withColumn(
    "Phone_Extension",
    regexp_extract(
        col("Phone_Number"),
        r"(?:x|ext|extension)\s*(\d+)",
        1
    )
)

### Remove the Extension from the Phone Number
df_silver = df_silver.withColumn(
    "Phone_Clean",
    regexp_replace(
        col("Phone_Number"),
        r"(?:x|ext|extension)\s*(\d+)",
        ""
    )
)

### Keep the Digits and the Plus Symbol
df_silver = df_silver.withColumn(
    "Phone_Digits",
    regexp_replace(col("phone_clean"), r"[^\d+]", "")
)


### Create the Phone_e164 Column
df_silver = df_silver.withColumn(
    "Phone_e164",
    ### Checks that the Digits are in the Global Format, for which
    ### It would assume that the Phone Number already includes the Country Code
    when(col("Phone_Digits").startswith("+"), col("Phone_Digits"))
    ### Checks that Phone Number is in 10 Digits, if so, then assume its from US
    .when(length(col("Phone_Digits")) == 10, concat(lit("+1"), col("Phone_Digits")))
    ### Checks if the Phone Number is in 11 Digits starting with 1, if so, then just add Plus Symbol
    .when(length(col("Phone_Digits")) == 11, concat(lit("+"), col("Phone_Digits")))
    .otherwise(None)
)

# COMMAND ----------

### Flag whether the Phone Number is usable or not
df_silver = df_silver.withColumn(
    "Is_Valid_Phone_Number",
    col("Phone_e164").isNotNull()
)

### Remove the Helper Functions that were used
df_silver = df_silver.drop("Phone_Clean", "Phone_Digits")

### Drop the Original Phone Number Column
df_silver = df_silver.drop("Phone_Number")

display(df_silver.limit(5))


# COMMAND ----------

# MAGIC %md
# MAGIC ### Email Valid Validation

# COMMAND ----------

# MAGIC %run /Workspace/Users/matthew.kristanto@exposedata.com.au/superhero_enterprise_hr/helpers/helper_email_valid_checker

# COMMAND ----------

validate_email_column(df_silver, "Email")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Education Levels Values Validation

# COMMAND ----------

valid_values_checker(df_silver, "Education_Level", ["High School", "Bachelor's Degree", "Master's Degree" ,"PhD"])

# COMMAND ----------

# MAGIC %md
# MAGIC ### Status Values Validation

# COMMAND ----------

valid_values_checker(df_silver, "Status", ["Applied", "Interviewing", "Rejected", "In Review", "Offered"])

# COMMAND ----------

### Save the Silver Table to the Catalog
(df_silver.write
    .format("delta")  
    .mode("overwrite")  
    .saveAsTable("silver.silver_recruitment_data_cleaned"))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM silver.silver_recruitment_data_cleaned