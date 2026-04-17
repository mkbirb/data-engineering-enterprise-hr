# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Notebook Name: Recruitment Data Transformed
# MAGIC **Medallion Layer: Silver**  
# MAGIC
# MAGIC **Purpose:** Transforms the Data to the appropiate Data Types
# MAGIC
# MAGIC **Author:** Matthew Kristanto  
# MAGIC
# MAGIC **Date Created:** 30/03/26  
# MAGIC
# MAGIC **Last Modified:**  
# MAGIC
# MAGIC **Source Table:** [silver_recruitment_data_cleaned](https://adb-7405605014654402.2.azuredatabricks.net/editor/notebooks/3562120461079026?o=7405605014654402) 
# MAGIC
# MAGIC
# MAGIC **Notes:**
# MAGIC - Application_Date changed from String to Date
# MAGIC - Date_Of_Birth changed from String to Date
# MAGIC - Years_Of_Experience changed from String to Integer
# MAGIC - Desired_Salary changed from String to Double
# MAGIC

# COMMAND ----------

df_silver = spark.read.table("silver.silver_recruitment_data_cleaned")

display(df_silver.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Application Date: String Type to Date Type

# COMMAND ----------

from pyspark.sql.functions import to_date, col, expr

df_silver = df_silver.withColumn(
    "Application_Date",
    expr("""
        coalesce(
            try_to_date(trim(Application_Date), 'dd-MMM-yy'),
            try_to_date(trim(Application_Date), 'dd-MM-yyyy'),
            try_to_date(trim(Application_Date), 'yyyy-MM-dd')
        )
    """)
)

display(df_silver.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Date Of Birth: String Type to Date Type

# COMMAND ----------

from pyspark.sql.functions import to_date
df_silver = df_silver.withColumn("Date_Of_Birth", to_date("Date_Of_Birth", "dd-MM-yyyy"))


display(df_silver.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Years Of Experience: String Type to Integer Type

# COMMAND ----------

from pyspark.sql.functions import col

df_silver = df_silver.withColumn("Years_Of_Experience", col("Years_Of_Experience").cast("integer"))

display(df_silver.limit(5))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Desired Salary: String Type to Double Type

# COMMAND ----------

df_silver = df_silver.withColumn("Desired_Salary", col("Desired_Salary").cast("double"))

display(df_silver.limit(5))

# COMMAND ----------

### Save the Silver Table to the Catalog
(df_silver.write
    .format("delta")  
    .mode("overwrite")  
    .saveAsTable("silver.silver_recruitment_data_transformed"))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM silver.silver_recruitment_data_transformed