-- Databricks notebook source
-- MAGIC %md
-- MAGIC ## Notebook Name: Application Status Dim
-- MAGIC **Medallion Layer: Gold**  
-- MAGIC
-- MAGIC **Purpose:** Creates a Dimension Table that gives the contextual information regarding the recruitment status of an applicant
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
-- MAGIC - N/A
-- MAGIC
-- MAGIC
-- MAGIC

-- COMMAND ----------

CREATE TABLE gold.gold_application_status_dim (
  status_key      INT,
  status_name     STRING
)
USING DELTA;

-- COMMAND ----------

INSERT INTO gold.gold_application_status_dim (status_key, status_name)
VALUES
  (1, 'Applied'),
  (2, 'In Review'),
  (3, 'Interviewing'),
  (4, 'Offered'),
  (5, 'Rejected');
