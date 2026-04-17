# Databricks notebook source
# MAGIC %md
# MAGIC ## Notebook Name: Snake Case Column Convertor
# MAGIC **Helper**  
# MAGIC
# MAGIC **Purpose:** Converts the Column Titles into Snake Case
# MAGIC
# MAGIC **Author:** Matthew Kristanto  
# MAGIC
# MAGIC **Date Created:** 30/03/26  
# MAGIC
# MAGIC **Last Modified:**
# MAGIC
# MAGIC **Notes:**
# MAGIC - Gets the Column Titles from a Table and converts them to Snake Case, to make sure they are in Snake Case format.
# MAGIC
# MAGIC

# COMMAND ----------


import re

def snake_case_column_title_convertor(df):
    def to_snake_case(col_name):
        col_name = col_name.strip().lower()
        ### Remove Punctuation
        col_name = re.sub(r"[^\w\s]", "", col_name)  
        ### Make spaces into Underscores
        col_name = re.sub(r"\s+", "_", col_name)      
        ### Replaces any sequence of one or more underscores with just a single underscore
        col_name = re.sub(r"_+", "_", col_name)     

        ### Capitalize each word 
        return "_".join(word.capitalize() for word in col_name.split("_"))

    new_column_titles = [to_snake_case(col) for col in df.columns]


    return df.toDF(*new_column_titles)

