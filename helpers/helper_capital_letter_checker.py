# Databricks notebook source
# MAGIC %md
# MAGIC ## Notebook Name: Capital Letter Checker
# MAGIC **Helper**  
# MAGIC
# MAGIC **Purpose:** Checks that each word in the values of a Column begins with a Capital Letter
# MAGIC
# MAGIC **Author:** Matthew Kristanto  
# MAGIC
# MAGIC **Date Created:** 30/03/26  
# MAGIC
# MAGIC **Last Modified:**
# MAGIC
# MAGIC **Notes:**
# MAGIC - If there are records that have the words not in Capital Letters, than create a JSON Object that would be passed to ADF
# MAGIC

# COMMAND ----------

from pyspark.sql.functions import col
import json

def capital_letter_checker(df, col_name):
  the_invalid_records = df.filter(~col(col_name).rlike(r"^[A-Z]"))

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

  CreatingNonCapitalLetterRecords(the_invalid_records)
