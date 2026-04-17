# Databricks notebook source
# MAGIC %md
# MAGIC ## Notebook Name: Valid Values Checker
# MAGIC **Helper**  
# MAGIC
# MAGIC **Purpose:** Checks that each value in a specified column belongs to a value from a specified valid list
# MAGIC
# MAGIC **Author:** Matthew Kristanto  
# MAGIC
# MAGIC **Date Created:** 30/03/26  
# MAGIC
# MAGIC **Last Modified:**
# MAGIC
# MAGIC **Notes:**
# MAGIC N/A
# MAGIC
# MAGIC

# COMMAND ----------


def valid_values_checker(df, column_name, valid_values):
  invalid_records = df.filter(~df[column_name].isin(valid_values))

  invalid_count = invalid_records.count()

  if invalid_count == 0:
      print("All Values Valid")
  else:
      display(invalid_records)
      raise ValueError("Values not Valid")