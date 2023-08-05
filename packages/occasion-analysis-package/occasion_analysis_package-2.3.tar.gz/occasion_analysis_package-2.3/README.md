**Installation:**

pip install occasion-analysis-package


**Get started:**

**Description:** Python package to do analysis on Occasion.

**Long Description:** This package consist of 3 functions: export sql data to csv(export_data_to_csv), create word cloud(create_word_cloud), create emoji chart(create_emoji_chart).

1. **export_data_to_csv(credential_file_path, export_file_path):**
The function will export data based on SQL query into csv file.
For data loading, create a file named: "credentials.env" which has database credential details in following format:

DATABASE = 'database_name'

USER = 'user_name'

PASSWORD = 'password'

HOST = 'host'

PORT = 'port_number'


***Parameters:***

**credential_file_path (string):** File Path for Credential File without file name (as it is set to credentials.env). Please enter file path with double backslash "\\\\".

**export_file_path (string):** File Path to export the data(as it is set to occasion.csv). Please enter file path with double backslash "\\\\".

***Package Import:*** psycopg2, os, csv, io, pandas, dotenv


2. **create_word_cloud(import_file_path,stop_words):**
The function will create Word Cloud using Document Term Matrix.

***Parameters:***

**import_file_path (string):** File Path to export the data. Please enter file path with double backslash "\\\\" with file name. There should be two columns in the file: "use_case", "all_text". File name should be .csv extension.

**stop_words (list/string):** Enter the list of stop words, which should be avoided while creating word cloud. Example: "mother, mom, mum".

***Package Import:*** numpy, pandas, matplotlib, re, string, spacy, sklearn 


3. **create_emoji_chart(import_file_path):**
The function will create Emoji Frequency Chart.

***Parameters:***

**import_file_path (string):** File Path to export the data. Please enter file path with double backslash "\\\\" with file name. There should be two columns in the file: "use_case", "all_text". File name should be .csv extension.

***Package Import:*** pandas, plotly, advertools

**Example:**
from occasion_analysis_package import export_data_to_csv, create_word_cloud, create_emoji_chart

export_data_to_csv("D:\\\\Analysis\\\\Occassion Analysis","D:\\\\Analysis\\\\Occassion Analysis\\\\test")

create_word_cloud("D:\\\\Analysis\\\\Occassion Analysis\\\\test\\\\occasion.csv","mother, mom, mum, mummy, grandmother, grand mother, grand ma, grandma, step mom, stepmom") --Stop words for Mother''s Day

create_emoji_chart("D:\\\\Analysis\\\\Occassion Analysis\\\\test\\\\occasion.csv")
             