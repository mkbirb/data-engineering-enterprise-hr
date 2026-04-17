# Databricks notebook source
# MAGIC %md
# MAGIC ## Notebook Name: Email Valid Checker
# MAGIC **Helper**  
# MAGIC
# MAGIC **Purpose:** Checks that Email Address is in proper format
# MAGIC
# MAGIC **Author:** Matthew Kristanto  
# MAGIC
# MAGIC **Date Created:** 27/03/26  
# MAGIC
# MAGIC **Last Modified:**
# MAGIC
# MAGIC **Notes:**
# MAGIC - Ensures Email has "@" symbol
# MAGIC - Ensures that Email Address contains either ".com", ".net" or ".org" at the end of the Email Address
# MAGIC
# MAGIC

# COMMAND ----------

from pyspark.sql.functions import col

def validate_email_column(df, column_name):
    invalid_emails = df.filter(
        ~((col(column_name).contains("@")) &
        (
            col(column_name).endswith(".com") |
            col(column_name).endswith(".net") |
            col(column_name).endswith(".org")
        )
    ))
    display(invalid_emails)

    if invalid_emails.count() > 0:
        print(f"Invalid emails found in column '{column_name}':")
        display(invalid_emails)
    else:
        print(f"No invalid emails found in column '{column_name}'.")
