# Databricks notebook source
# MAGIC %md
# MAGIC ## Notebook Name: Four Digit Format Checker
# MAGIC **Helper**  
# MAGIC
# MAGIC **Purpose:** Checks that each value in a specified format has Four Digits
# MAGIC
# MAGIC **Author:** Matthew Kristanto  
# MAGIC
# MAGIC **Date Created:** 30/03/26  
# MAGIC
# MAGIC **Last Modified:**
# MAGIC
# MAGIC **Notes:**
# MAGIC - Also displays the Dataframe of Records that are not in Four Digit Format
# MAGIC
# MAGIC

# COMMAND ----------

from pyspark.sql.functions import col, length

def four_digit_format_checker(df, column_name):

    df_not_4_digits = df.filter(length(col(column_name)) != 4)
    display(df_not_4_digits)

    if df_not_4_digits.count() > 0:
        print(f"Found {df_not_4_digits.count()} records with non-4-digit {column_name} values.")
    else:
        print(f"All {column_name} values are 4 digits.")