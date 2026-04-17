-- Databricks notebook source
-- MAGIC %md
-- MAGIC ## Notebook Name: Job Application Fact
-- MAGIC **Medallion Layer: Gold**  
-- MAGIC
-- MAGIC **Purpose:** Creates a Fact Table that gives the factual information regarding a specific applicant who have applied to a specific job.
-- MAGIC
-- MAGIC **Author:** Matthew Kristanto  
-- MAGIC
-- MAGIC **Date Created:** 7/04/26  
-- MAGIC
-- MAGIC **Last Modified:**  
-- MAGIC
-- MAGIC **Source Table:** 
-- MAGIC [silver_recruitment_data_transformed](https://adb-7405605014654402.2.azuredatabricks.net/editor/notebooks/1674403678266130?o=7405605014654402) 
-- MAGIC
-- MAGIC
-- MAGIC **Notes:**
-- MAGIC - This uses the Slowly Changing Dimensions (SCD) Type 1, where the existing data is overwritten, making the current data the only retained.
-- MAGIC
-- MAGIC
-- MAGIC

-- COMMAND ----------

CREATE SCHEMA IF NOT EXISTS gold

-- COMMAND ----------

-- Initial Schema
CREATE TABLE IF NOT EXISTS gold.gold_job_application_fact (
  job_application_fact_key    BIGINT,
  applicant_key               INT,
  job_title                   STRING,
  application_date_key        INT,
  status_key                  INT,
  desired_salary              DECIMAL(18,2),
  years_of_experience         INT
)
USING DELTA;

-- COMMAND ----------

-- Load the Facts
INSERT INTO gold.gold_job_application_fact
  SELECT
  monotonically_increasing_id() as job_application_fact_key,
  a.applicant_key,
  src.job_title,
  d.date_key                    as application_date_key,
  st.status_key                 as application_status,
  src.desired_salary,
  src.years_of_experience

  FROM silver.silver_recruitment_data_transformed src
  JOIN gold.gold_applicant_dim a
  ON src.applicant_Id = a.applicant_id
  JOIN gold.gold_date_dim d
  ON to_date(src.application_date, 'yyyy-MM-dd') = d.date
  JOIN gold.gold_application_status_dim st
  ON src.status = st.status_name

-- COMMAND ----------

SELECT * FROM gold.gold_job_application_fact