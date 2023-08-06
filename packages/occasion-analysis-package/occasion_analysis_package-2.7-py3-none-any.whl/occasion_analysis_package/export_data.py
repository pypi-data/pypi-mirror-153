import psycopg2
from psycopg2 import sql
import os
import csv
import io
from dotenv import load_dotenv

def export_data_to_csv(credential_file_path, export_file_path):
    """
    The function will export data based on SQL query into csv file.
    For data loading, create a file named: "credentials.env" which has database credential details in following format:
        DATABASE = 'database_name'
        USER = 'user_name'
        PASSWORD = 'password'
        HOST = 'host'
        PORT = 'port_number'
  
    Parameters:
        credential_file_path (string): File Path for Credential File with file name.
        export_file_path (string): File Path to export the data with file name.
    Example:
        export_data_to_csv("D:\\\\Analysis\\\\Occassion Analysis\\\\credentials.env","C:\\\\Analysis\\\\Occassion Analysis\\\\test\\\\occasion.csv")
    """
    load_dotenv(credential_file_path)

    #this section is for converting text/symbolic emoticons
    def  emoji_converter(message):
            words = message.split(" ")
            emojis = {
            ":)" : "😀",
            ":(" : "😞",
            ":-)" : "😀",
            ":-(" : "😞",
            ":D":"😄",
            ":-D":"😄",
            ":*":"😘",
            ":-*":"😘",
            ":x":"😘",
            ":P":"😛",
            ":-P":"😛",
            ":p":"😛",
            ":-p":"😛"
            }
            outcome = " "
            for word in words:
                outcome += emojis.get(word, word) + " "
            return outcome


    dbname = os.getenv('DATABASE')
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    user = os.getenv('USER')
    password = os.getenv('PASSWORD')

    try:
    #establishing the connection
        conn = psycopg2.connect(
            database = dbname, user = user, password = password, host = host, port = port
        )
        print("Connection successful")
    except psycopg2.DatabaseError as e:
        # Confirm unsuccessful connection and stop program execution.
            print("Database connection unsuccessful.",e)
            quit()

    #Creating a cursor object using the cursor() method
    cursor = conn.cursor()

    #Get Occasion List
    sql_query = ("SELECT DISTINCT tier_2_use_case from looker.tiered_attributes_new")
    cursor.execute(sql_query)
    occasion_list = cursor.fetchall()
    o_list = list()
    occasion_list.sort()
    i = 0
    for o_name in occasion_list:
        i = i+1
        print((i,o_name[0]))
        o_list.append((i,o_name[0]))
    
    #Creating Export File
    t_path_n_file = export_file_path 
    occasion_input = input("Enter Occasion Number from the list (Only enter number): ")
    if occasion_input == '' or int(occasion_input) < 1 or int(occasion_input) > i:
        print('Null Input,quiting')
        quit()
    else:
        occ = o_list[int(occasion_input)-1]
        occ_name = occ[1]
        occ_name = occ_name.replace("'","''")
        sql_query = ("SELECT tier_2_use_case as use_case, COALESCE(all_message_text(messages),'') as all_text_new from orders.ordered_products op "
                    f"JOIN (SELECT tier_2_use_case, ordered_product_id from looker.tiered_attributes_new where UPPER(tier_2_use_case) = UPPER('{occ_name}') GROUP BY 1,2)uc ON op.ordered_product_id = uc.ordered_product_id "
                    "GROUP BY 1,2")
        print(sql_query)
        cursor.execute(sql_query)

        export_list = cursor.fetchall()

        try:
            with  io.open(t_path_n_file, "w",encoding = 'utf-8-sig') as file:
                writer = csv.writer(file, delimiter=',')
                writer.writerow(['use_case','all_text'])
                #adding set of code to convert text emoji into unicode emoji
                for row in export_list:
                    row_list = list(row)
                    text_to_encode = emoji_converter(row[1])
                    row_list.append(text_to_encode)
                    row_1 = list()
                    row_1.append(row_list[0])
                    row_1.append(row_list[2])
                    row_final = tuple(row_1)
                    writer.writerow(row_final)
            print("Query executed successfully")
        except psycopg2.databaseerror as e:
            print("Error is: ",e)
            quit()
    cursor.close()
    conn.close()
