# Databricks notebook source
# MAGIC %md
# MAGIC ## Notebook Name: Date Dim
# MAGIC **Medallion Layer: Gold**  
# MAGIC
# MAGIC **Purpose:** Creates a Dimension Table that gives the contextual information regarding a specific date.
# MAGIC
# MAGIC **Author:** Matthew Kristanto  
# MAGIC
# MAGIC **Date Created:** 2/04/26  
# MAGIC
# MAGIC **Last Modified:**  
# MAGIC
# MAGIC **Source Table:** 
# MAGIC [silver_employee_payroll_transformed](https://adb-7405605014654402.2.azuredatabricks.net/editor/notebooks/3775063119320221?o=7405605014654402) 
# MAGIC
# MAGIC [silver_employee_engagement_transformed](https://adb-7405605014654402.2.azuredatabricks.net/editor/notebooks/2684211816196212?o=7405605014654402) 
# MAGIC
# MAGIC
# MAGIC **Notes:**
# MAGIC - The Starting Date, we assume would be 10 years ago from the creation of the Notebook.
# MAGIC - The End Date would be 10 years in the future from the creation of the notebook
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS gold

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS gold.gold_date_dim (
# MAGIC   date_key                  INT,
# MAGIC   date                      DATE,
# MAGIC   day_of_the_month          INT,
# MAGIC   day_of_the_week           INT,
# MAGIC   weekday                   STRING,
# MAGIC   month                     INT,
# MAGIC   month_name                STRING,
# MAGIC   year                      INT,
# MAGIC   quarter                   INT,
# MAGIC   is_weekend                BOOLEAN
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Create CTE Temporary Table
# MAGIC INSERT OVERWRITE gold.gold_date_dim
# MAGIC WITH date_range AS (
# MAGIC   -- Make into Rows
# MAGIC   SELECT explode(
# MAGIC     -- Create an Array of Dates
# MAGIC     sequence(
# MAGIC       DATE '2016-01-01',
# MAGIC       DATE '2026-12-31',
# MAGIC       INTERVAL 1 DAY
# MAGIC     )
# MAGIC   ) AS date
# MAGIC )
# MAGIC SELECT
# MAGIC   CAST(date_format(date, 'yyyyMMdd') AS INT) AS date_key,
# MAGIC   date,
# MAGIC   day(date) AS day_of_the_month,
# MAGIC   dayofweek(date) AS day_of_the_week,
# MAGIC   date_format(date, 'EEEE') AS weekday,
# MAGIC   month(date) AS month,
# MAGIC   date_format(date, 'MMMM') AS month_name,
# MAGIC   year(date) AS year,
# MAGIC   quarter(date) AS quarter,
# MAGIC   CASE
# MAGIC     WHEN dayofweek(date) IN (1,7) THEN TRUE
# MAGIC     ELSE FALSE
# MAGIC   END AS is_weekend
# MAGIC FROM date_range;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Do the Check
# MAGIC SELECT COUNT(*) FROM gold.gold_date_dim

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM gold.gold_date_dim