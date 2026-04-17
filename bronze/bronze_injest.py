# Databricks notebook source
# MAGIC %md
# MAGIC ## Notebook Name: Injest
# MAGIC **Medallion Layer: Bronze**  
# MAGIC
# MAGIC **Purpose:** Ingest the Raw Data of the Employee Engagement for the Workplace 
# MAGIC
# MAGIC **Author:** Matthew Kristanto  
# MAGIC
# MAGIC **Date Created:** 20/03/26  
# MAGIC
# MAGIC **Last Modified:**
# MAGIC
# MAGIC **Notes:**
# MAGIC - Injesting the raw CSV Files from Microsoft Azure Data Lake Storage of the Bronze Folder
# MAGIC - Does not handle missing or Null Values
# MAGIC

# COMMAND ----------

# COMMAND ----------

### ---------- THIS USES THE WIDGETS---------
# ### Create Widgets that would allow for the selection of the desired date by user
# from datetime import datetime, timedelta

# dates = []

# for i in range(30):
#     date_value = datetime.today() - timedelta(days=i)
#     formatted_date = date_value.strftime("%Y-%m-%d")
#     dates.append(formatted_date)

# dbutils.widgets.dropdown("process_date", dates[0], dates)

# selected_date = dbutils.widgets.get("process_date")

# csv_file = "employee_engagement_survey"

# COMMAND ----------

### --- THIS USES ADF PARAMETERS
selected_year = dbutils.widgets.get("process_date_year")
selected_month = dbutils.widgets.get("process_date_month")
selected_date = dbutils.widgets.get("process_date_date")
csv_file = dbutils.widgets.get("csv_file")

# COMMAND ----------

### Read the CSV

df_bronze = (
    spark.read
         .format("csv")
         .option("header", "true")
         .option("multiline", "true")
         .load(
             f"wasbs://bronze@{storage_account_name}.blob.core.windows.net/"
             f"{selected_year}/{selected_month}/{selected_date}/{csv_file}/{csv_file}.csv" 
         )
)

# COMMAND ----------

### Inspect that the data has been retrieved.
print(f"Reading from path: wasbs://bronze@{storage_account_name}.blob.core.windows.net/"f"{selected_year}/{selected_month}/{selected_date}/{csv_file}/{csv_file}.csv")

display(df_bronze)

# COMMAND ----------

spark.sql("CREATE SCHEMA IF NOT EXISTS bronze")

# COMMAND ----------

(df_bronze.write
    .format("delta")
    .mode("overwrite")
    .option("delta.columnMapping.mode", "name")
    .saveAsTable(f"bronze.bronze_{csv_file}"))

# COMMAND ----------

df = spark.sql(f"SELECT * FROM bronze.bronze_{csv_file}")

df.show()