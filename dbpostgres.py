import os
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
import json
import sys
sys.path.insert(1, '/')

#==============================================DATABASE SET UP==============================================
try:
    load_dotenv(".env")
except:
    load_dotenv(".\.env")

host = os.environ['POSTGRES_HOST_AZURE']
dbname = os.environ['POSTGRES_DBNAME_AZURE']
user = os.environ['POSTGRES_USER_AZURE']
password = os.environ['POSTGRES_PASSWORD_AZURE']
sslmode = "disable"

class DatabaseElems():
    def __init__(self,cursor,database):
        self.cursor=cursor
        self.database=database

def closeConnection(dbelem):
    try:
        #close and return
        dbelem.cursor.close()
        dbelem.database.commit()
        dbelem.database.close()
        return"good"
    except:
        return"error"

def getDBCursor():
    try:
        conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)        
        database = psycopg2.connect(conn_string)
        # print("Connection established")
        cursor = database.cursor()
        dbelem=DatabaseElems(cursor,database)
    except Exception as e:
        cursor=None
        # print(e)
        dbelem="exception: "+str(e)
    return dbelem
#==============================================DATABASE SET UP END==============================================
#=====================================================================================================================
def get_clients():
    # Construct connection string
    dbelem=getDBCursor()
        
    select_all = """SELECT * from clients"""
                
    dbelem.cursor.execute(select_all)
    fetched_data = dbelem.cursor.fetchall()

    CONNECTION=closeConnection(dbelem)

    if CONNECTION=='good':
        return fetched_data 
    else:
        return "error"
#=====================================================================================================================
#=====================================================================================================================
def addTest(event):
    dbelem=getDBCursor()
        
    insert_test = f"""INSERT INTO tests_performed(event) VALUES('{event}') """
                
    dbelem.cursor.execute(insert_test)

    CONNECTION=closeConnection(dbelem)

    if CONNECTION=='good':
        return "Test added to table" 
    else:
        return "error"
#=====================================================================================================================
#=====================================================================================================================
def includeAlert(overdraft=False, stolen=False):
    dbelem=getDBCursor()
    
    alert_type=''

    if overdraft:
        alert_type+="Overdraft "
        alert_message="A purchase has been done with an overdraft credit card"
        alert_sent=False
    if stolen:
        alert_type+="Stolen Card"
        alert_message="A stolen Credit Card tried to purchase something. Please review."
        alert_sent=False

    insert_test = f"""INSERT INTO alerts(alert_type, alert_message, alert_sent) VALUES('{alert_type}','{alert_message}', {alert_sent}) """
                
    dbelem.cursor.execute(insert_test)

    CONNECTION=closeConnection(dbelem)

    if CONNECTION=='good':
        return "Alert added to table" 
    else:
        return "error"
#=====================================================================================================================
#=====================================================================================================================
def get_alerts():
    # Construct connection string
    dbelem=getDBCursor()
        
    select_all = """SELECT * from alerts where alert_sent=false"""
                
    dbelem.cursor.execute(select_all)
    fetched_data = dbelem.cursor.fetchall()

    CONNECTION=closeConnection(dbelem)

    if CONNECTION=='good':
        return fetched_data 
    else:
        return "error"
#=====================================================================================================================
#=====================================================================================================================
def takecareofAlert(alert_id):
    dbelem=getDBCursor()
        
    insert_test = f"""UPDATE alerts SET alert_sent=true WHERE alert_id ={alert_id}"""
                
    dbelem.cursor.execute(insert_test)

    CONNECTION=closeConnection(dbelem)

    if CONNECTION=='good':
        return f"Alert ({alert_id}) has been sent." 
    else:
        return "error"