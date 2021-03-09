import pymsteams
import pandas as pd
import numpy as np
import pyodbc
import mysql.connector
from tabulate import tabulate

#server = ‘localhost’
#database = ‘recipes_database’
#username = ‘root’
#password = ‘’
conn = mysql.connector.connect(host='localhost',database='recipes_database',user='root',password='')
#pyodbc.connect(‘DRIVER={ODBC Driver 17 for SQL Server};SERVER=’+server+’;DATABASE=’+database+’;UID=’+username+’;PWD=’+ password)

cursor = conn.cursor()

sql_query = """select * from recipes_database.recipes"""

df = pd.read_sql(sql_query, conn)

#print(tabulate(sql_query))
def sleeve(df):
#df.to_html()

myTeamsMessage = pymsteams.connectorcard("my webhook url ")
myTeamsMessage.title(“List Of Booking Status”)
#myTeamsMessage.text(“Test Mail”)
myTeamsMessage.text(df.to_string())
myTeamsMessage.send()