# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Notebook Name: Training and Development Cleaned
# MAGIC **Medallion Layer: Silver**  
# MAGIC
# MAGIC **Purpose:** Does Data Validation, ensuring that the values of attributes are within the appropiate ranges
# MAGIC
# MAGIC **Author:** Matthew Kristanto  
# MAGIC
# MAGIC **Date Created:** 31/03/26  
# MAGIC
# MAGIC **Last Modified:**  
# MAGIC
# MAGIC **Source Table:** [bronze_injest](https://adb-7405605014654402.2.azuredatabricks.net/editor/notebooks/1864960029131489?o=7405605014654402#command/8176478096240519) 
# MAGIC
# MAGIC
# MAGIC **Notes:**
# MAGIC - Convert the Column Title into Snake Case
# MAGIC - Ensure that the Training_Program_Name values are either "Leadership Development", "Customer Service", "Technical Skills", "Communication Skills" and "Project Management"
# MAGIC - Ensure that the Training_Type values are either "Internal" or "External"
# MAGIC - Ensure that the Training_Outcome values are "Passed" or "Failed" or "Completed" or "Incomplete"
# MAGIC
# MAGIC

# COMMAND ----------

df_bronze = spark.read.table("bronze.bronze_training_and_development")

display(df_bronze.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Column Title Snake Case

# COMMAND ----------

# MAGIC %run /Workspace/Users/matthew.kristanto@exposedata.com.au/superhero_enterprise_hr/helpers/helper_snake_case_column_convertor

# COMMAND ----------

df_silver = snake_case_column_title_convertor(df_bronze)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Training Program Name Valid Values

# COMMAND ----------

# MAGIC %run /Workspace/Users/matthew.kristanto@exposedata.com.au/superhero_enterprise_hr/helpers/helper_valid_values_checker

# COMMAND ----------



valid_values_checker(df_silver, "Training_Program_Name", ["Leadership Development","Customer Service","Technical Skills", "Communication Skills","Project Management"])


# COMMAND ----------

# MAGIC %md
# MAGIC ### Training Type Valid Values

# COMMAND ----------

valid_values_checker(df_silver, "Training_Type", ["Internal", "External"])

# COMMAND ----------

# MAGIC %md
# MAGIC ### Training Outcome Valid Values

# COMMAND ----------

valid_values_checker(df_silver, "Training_Outcome", ["Passed", "Failed", "Completed", "Incomplete"])

# COMMAND ----------

### Save the Silver Table to the Catalog
(df_silver.write
    .format("delta")  
    .mode("overwrite")  
    .saveAsTable("silver.silver_training_and_development_cleaned"))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM silver.silver_training_and_development_cleaned