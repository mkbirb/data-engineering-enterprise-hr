-- Databricks notebook source
-- MAGIC %md
-- MAGIC ## Notebook Name: Applicant Dim
-- MAGIC **Medallion Layer: Gold**  
-- MAGIC
-- MAGIC **Purpose:** Creates a Dimension Table that gives the contextual information regarding a specific applicant.
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

-- Determine the Schema
CREATE TABLE IF NOT EXISTS gold.gold_applicant_dim (
    Applicant_key           INT,
    Applicant_id            STRING,
    First_name              STRING,
    Last_name               STRING,
    Gender                  STRING,
    Date_of_birth           DATE,
    Phone_e164              STRING,
    Is_valid_phone_number   BOOLEAN,
    Address                 STRING,
    City                    STRING,
    State                   STRING,
    Zip_code                STRING,
    Country                 STRING,
    Education_level         STRING,
    Years_of_experience     STRING
)
USING DELTA;

-- COMMAND ----------

-- Do the Initial Load
INSERT INTO gold.gold_applicant_dim
SELECT
monotonically_increasing_id() AS Applicant_key,
Applicant_id,
First_name,
Last_name,
Gender,
Date_of_birth,
Phone_e164,
Is_valid_phone_number,
Address,
City,
State,
Zip_code,
Country,
Education_level,
Years_of_experience
FROM
  silver.silver_recruitment_data_transformed

-- COMMAND ----------

-- DROP TABLE IF EXISTS gold.gold_applicant_dim

-- COMMAND ----------

SELECT * FROM gold.gold_applicant_dim

-- COMMAND ----------

-- Only have and keep the current record
MERGE INTO gold.gold_applicant_dim as trgt
USING silver.silver_recruitment_data_transformed as src
ON trgt.applicant_id = src.applicant_id

WHEN MATCHED THEN
  UPDATE SET
    trgt.First_name = src.First_name,
    trgt.Last_name = src.Last_name,
    trgt.Gender = src.Gender,
    trgt.Date_of_birth = src.Date_of_birth,
    trgt.Phone_e164 = src.Phone_e164,
    trgt.Is_valid_phone_number = src.Is_valid_phone_number,
    trgt.Address = src.Address,
    trgt.City = src.City,
    trgt.State = src.State,
    trgt.Zip_code = src.Zip_code,
    trgt.Country = src.Country,
    trgt.Education_level = src.Education_level,
    trgt.Years_of_experience = src.Years_of_experience
    
WHEN NOT MATCHED THEN
  INSERT (
    Applicant_key,
    Applicant_id,
    First_name,
    Last_name,
    Gender,
    Date_of_birth,
    Phone_e164,
    Is_valid_phone_number,
    Address,
    City,
    State,
    Zip_code,
    Country,
    Education_level,
    Years_of_experience
  )
  VALUES (
    monotonically_increasing_id(),
    src.Applicant_id,
    src.First_name,
    src.Last_name,
    src.Gender,
    src.Date_of_birth,
    src.Phone_e164,
    src.Is_valid_phone_number,
    src.Address,
    src.City,
    src.State,
    src.Zip_code,
    src.Country,
    src.Education_level,
    src.Years_of_experience
  )

-- COMMAND ----------

SELECT * FROM gold.gold_applicant_dim