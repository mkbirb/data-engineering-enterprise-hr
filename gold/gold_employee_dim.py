# Databricks notebook source
# MAGIC %md
# MAGIC ## Notebook Name: Employee Dim
# MAGIC **Medallion Layer: Gold**  
# MAGIC
# MAGIC **Purpose:** Creates a Dimension Table that gives the contextual information regarding a specific employee.
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
# MAGIC - This uses the Slowly Changing Dimensions (SCD) Type 2, where the historical records are kept to track how attributes change over time.
# MAGIC - Performance is also optimized by speeding up the values of searching of the is_current column
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE SCHEMA IF NOT EXISTS gold

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Determine the Schema
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS gold.gold_employee_dim (
# MAGIC     employee_key        INT,
# MAGIC     employee_id         STRING,
# MAGIC     first_name          STRING,
# MAGIC     last_name           STRING,
# MAGIC     hire_date           DATE,
# MAGIC     department          STRING,
# MAGIC     salary              DOUBLE,
# MAGIC     employment_status   STRING,
# MAGIC     is_current          BOOLEAN,
# MAGIC     -- Identifies the time period where this version of the Employee Record was valid, done for historical tracking.
# MAGIC     effective_from      DATE,
# MAGIC     effective_to        DATE
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# %sql
# DROP TABLE IF EXISTS gold.gold_employee_dim

# COMMAND ----------

# MAGIC %sql
# MAGIC -- DO THE INITIAL LOAD OF THE TABLE
# MAGIC INSERT INTO gold.gold_employee_dim 
# MAGIC SELECT
# MAGIC   monotonically_increasing_id() AS employee_key,
# MAGIC   employee_id,
# MAGIC   first_name,
# MAGIC   last_name,
# MAGIC   hire_date,
# MAGIC   department,
# MAGIC   salary,
# MAGIC   employment_status,
# MAGIC   CASE 
# MAGIC     WHEN employment_status IN ('Terminated') THEN FALSE
# MAGIC     ELSE TRUE
# MAGIC   END AS is_current,
# MAGIC   current_date() AS effective_from,
# MAGIC   -- SET A MAXIMUM TIME DATE
# MAGIC   DATE '9999-12-31' AS effective_to
# MAGIC FROM
# MAGIC   silver.silver_employee_payroll_transformed;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM gold.gold_employee_dim

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Handles the Incremental Changes, where if any of the tracked attributes changes then the current row would be closed
# MAGIC
# MAGIC MERGE INTO gold.gold_employee_dim trgt
# MAGIC USING silver.silver_employee_payroll_transformed src
# MAGIC ON trgt.employee_id = src.employee_id
# MAGIC AND trgt.is_current = true
# MAGIC -- Only set an update, when there is a difference between the Source and the Target Tables
# MAGIC WHEN MATCHED AND (
# MAGIC   trgt.department IS DISTINCT FROM src.department OR
# MAGIC   trgt.salary IS DISTINCT FROM src.salary OR
# MAGIC   trgt.employment_status IS DISTINCT FROM src.employment_status OR
# MAGIC   trgt.last_name IS DISTINCT FROM src.last_name
# MAGIC )
# MAGIC THEN UPDATE SET
# MAGIC   trgt.effective_to = current_date() - 1,
# MAGIC   trgt.is_current = false;
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Insert new versions for employees that have been changed or are new
# MAGIC INSERT INTO gold.gold_employee_dim
# MAGIC SELECT
# MAGIC   monotonically_increasing_id() AS employee_key,
# MAGIC   src.employee_id,
# MAGIC   src.first_name,
# MAGIC   src.last_name,
# MAGIC   src.hire_date,
# MAGIC   src.department,
# MAGIC   src.salary,
# MAGIC   src.employment_status,
# MAGIC   true  AS  is_current,
# MAGIC   current_date() AS effective_from,
# MAGIC   -- SET A MAXIMUM TIME DATE
# MAGIC   DATE '9999-12-31' AS effective_to
# MAGIC   FROM silver.silver_employee_payroll_transformed src
# MAGIC   -- Record gets inserted when cannot find matching is_current meaning new employee
# MAGIC   LEFT JOIN gold.gold_employee_dim AS trgt
# MAGIC   ON src.employee_id = trgt.employee_id
# MAGIC   AND trgt.is_current = true
# MAGIC   WHERE (
# MAGIC           trgt.employee_id IS NULL
# MAGIC     OR    trgt.department IS DISTINCT FROM src.department
# MAGIC     OR    trgt.salary IS DISTINCT FROM src.salary
# MAGIC     OR    trgt.employment_status IS DISTINCT FROM src.employment_status
# MAGIC     OR    trgt.last_name IS DISTINCT FROM src.last_name
# MAGIC   )
# MAGIC   AND NOT (
# MAGIC     trgt.employee_id IS NULL
# MAGIC     AND src.employment_status = 'Terminated'
# MAGIC   )
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM gold.gold_employee_dim

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Speeds up the performance by speeding up the is current filters
# MAGIC OPTIMIZE gold.gold_employee_dim
# MAGIC ZORDER BY (employee_id, is_current)