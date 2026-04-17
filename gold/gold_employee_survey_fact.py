# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Notebook Name: Employee Survey Fact
# MAGIC **Medallion Layer: Gold**  
# MAGIC
# MAGIC **Purpose:** Creates a measurable fact table of the employee engagement survey, which references the employee master dimension table
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
# MAGIC - Has a Foreign Key referencing to the Employee Key
# MAGIC - Has a Foreign Key referencing to the Date Key
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS gold.gold_employee_survey_fact (
# MAGIC   survey_fact_key         BIGINT,
# MAGIC   employee_key            INT,
# MAGIC   survey_date_key         INT,
# MAGIC   engagement_score        INT,
# MAGIC   satisfaction_score      INT,
# MAGIC   work_life_balance_score INT
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO gold.gold_employee_survey_fact
# MAGIC SELECT
# MAGIC   monotonically_increasing_id() AS  survey_fact_key,
# MAGIC   emp.employee_key,
# MAGIC   dt.date_key                   AS  survey_date_key,
# MAGIC   s.engagement_score,
# MAGIC   s.satisfaction_score,
# MAGIC   s.work_life_balance_score
# MAGIC   FROM
# MAGIC   silver.silver_employee_engagement_transformed s
# MAGIC
# MAGIC   -- Get the correct version of the Employee Record
# MAGIC   JOIN gold.gold_employee_dim emp
# MAGIC   -- NOTE: SINCE THE MOCK DATA IS NOT CONSISTENT WITH THE EMPLOYEE ID BETWEEN THE EMPLOYEE_DIM AND THE ENGAGEMENT TABLE, WE JUST JOIN IT TO ITSELF
# MAGIC   ON emp.employee_id = emp.employee_id
# MAGIC   AND s.survey_date BETWEEN emp.effective_from  AND emp.effective_to
# MAGIC
# MAGIC   JOIN gold.gold_date_dim dt
# MAGIC     ON s.survey_date = dt.date;
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC ### Validation Checks

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Checks that for each of the survey record, there is no mismatch between the valid record effectiveness time period and the survey date.
# MAGIC -- NOTE THIS ONLY WORKS WITH CONSISTENT MOCK DATA, WHICH WE DO NOT HAVE AS THE SOURCE TABLE OF THE EMPLOYEE ENAGEMENT TRANSFORMED HAS EMPLOYEE IDS THAT ARE NOT CONSISTENT!
# MAGIC -- SELECT COUNT(*) AS unmatched_surveys
# MAGIC -- FROM silver.silver_employee_engagement_transformed s
# MAGIC -- LEFT JOIN gold.gold_employee_dim emp
# MAGIC --   ON  s.employee_id = emp.employee_id
# MAGIC --   AND s.survey_date BETWEEN emp.effective_from  AND emp.effective_to
# MAGIC -- WHERE emp.employee_key IS NULL

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Check that the Date Dimension Table covers the full range of the survey
# MAGIC
# MAGIC SELECT COUNT(*) AS unmatched_dates
# MAGIC FROM silver.silver_employee_engagement_transformed s    
# MAGIC LEFT JOIN gold.gold_date_dim d
# MAGIC   ON s.survey_date = d.date
# MAGIC WHERE d.date_key IS NULL;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Ensures that there is no duplication of Survey Data containing duplicates
# MAGIC
# MAGIC SELECT
# MAGIC   employee_key,
# MAGIC   survey_date_key,
# MAGIC   COUNT(*) AS row_count
# MAGIC FROM gold.gold_employee_survey_fact
# MAGIC GROUP BY employee_key, survey_date_key
# MAGIC HAVING COUNT(*) > 1;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC OPTIMIZE gold.gold_employee_survey_fact
# MAGIC ZORDER BY (survey_date_key, employee_key);