# Code for ETL operations on Country-GDP data

# Importing the required libraries
import pandas as pd
import requests
import numpy as np
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime

url = 'https://web.archive.org/web/20230908091635%20/https://en.wikipedia.org/wiki/List_of_largest_banks'
exchange_csv_path = './exchange_rate.csv'
table_attribs =['Name','MC_USD_Billion']
final_table_attribs=['Name', 'MC_USD_Billion', 'MC_GBP_Billion', 'MC_EUR_Billion', 'MC_INR_Billion']
csv_path ='./Largest_banks_data.csv'
db_name='Banks.db'
table_name ='Largest_banks'
log_path='./code_log.txt'

def log_progress(message):
    ''' This function logs the mentioned message of a given stage of the
    code execution to a log file. Function returns nothing'''
    timestamp_format ='%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)

    with open(log_path, 'a') as f:
        f.write(f"{timestamp}, {message} \n")
    


def extract(url, table_attribs):
    ''' This function aims to extract the required
    information from the website and save it to a data frame. The
    function returns the data frame for further processing. '''
    html_page = requests.get(url).text
    data = BeautifulSoup(html_page,'html.parser')
    df= pd.DataFrame(columns=table_attribs)
    tables = data.find_all('tbody')
    rows = tables[0].find_all('tr')
    
    for row in rows:
        col = row.find_all('td')
        if len(col)!=0:
            # if col[1].find('a') is not None and '\n' not in col[2]:
                data_dic={

                    "Name": col[1].contents[2],
                    "MC_USD_Billion": col[2].contents[0]
                }
                df1 = pd.DataFrame(data_dic, index=[0])
                df1['MC_USD_Billion']= df1['MC_USD_Billion'].str.strip()
                MC_USD_list= df1["MC_USD_Billion"].tolist()
                MC_USD_list = [float("".join(x.split(','))) for x in MC_USD_list]
                df1["MC_USD_Billion"] = MC_USD_list
                df = pd.concat([df,df1], ignore_index=True)

    return df

def transform(df, csv_path):
    ''' This function accesses the CSV file for exchange rate[]
    information, and adds three columns to the data frame, each
    containing the transformed version of Market Cap column to
    respective currencies'''
    df_csv=pd.read_csv(csv_path)
    exchange_rate = df_csv.set_index('Currency').to_dict()['Rate']
    df['MC_GBP_Billion'] = [np.round(x*exchange_rate['GBP'],2) for x in df['MC_USD_Billion']]
    df['MC_EUR_Billion'] = [np.round(x*exchange_rate['EUR'],2) for x in df['MC_USD_Billion']]
    df['MC_INR_Billion'] = [np.round(x*exchange_rate['INR'],2) for x in df['MC_USD_Billion']]
    

    return df

def load_to_csv(df, output_path):
    ''' This function saves the final data frame as a CSV file in
    the provided path. Function returns nothing.'''
    df.to_csv(output_path)

def load_to_db(df, sql_connection, table_name):
    ''' This function saves the final data frame to a database
    table with the provided name. Function returns nothing.'''

def run_query(query_statement, sql_connection):
    ''' This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing. '''

''' Here, you define the required entities and call the relevant
functions in the correct order to complete the project. Note that this
portion is not inside any function.'''

