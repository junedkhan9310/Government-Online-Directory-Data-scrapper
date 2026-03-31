from datetime import datetime
import time
import sys,os
import os
import wx
import database
import re

import time


def print_exception_details(e):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    # Extract relevant information
    Exception_Type = exc_type.__name__
    Line_No = exc_tb.tb_lineno
    Error_Message = str(e)
    if '(Session info:' in Error_Message:
        Error_Message = Error_Message.partition('(Session info:')[0].strip()
    Error_Message = Error_Message.replace('\n',', ')
    Function_name = exc_tb.tb_frame.f_code.co_name
    File_Name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    Timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Timestamp of the error occurrence
    # Construct the error message with all relevant details
    Error_Final = (
        f"Timestamp: {Timestamp} | Error_Message: {Error_Message} | "
        f"Function: {Function_name} | Exception_Type: {Exception_Type} | "
        f"File_Name: {File_Name} | Line_No: {Line_No} "
    )
    # Print the error message
    print(Error_Final)
    # Optionally, sleep to allow for error inspection (can be removed if not needed)
    time.sleep(10)

def insert_on_table(link):
    while True:
        try:
            connection = database.DB_Connection()
            mycursor = connection.cursor()
            thread_id = connection.thread_id()

            sql = "INSERT INTO goverment_links (url) VALUES (%s);"
            mycursor.execute(sql, (link,))
            connection.commit()
            
            print(f"Inserted: {link}")
            mycursor.close()
            connection.close()
            break
        except Exception as e:
            print_exception_details(e)
            database.kill_query(thread_id)

