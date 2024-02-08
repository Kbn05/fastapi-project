import mysql.connector
import time

while True:
    try:
        mydbConnect = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Zot10175",
            database="fastapi"
        )
        cursor = mydbConnect.cursor()
        print("Connected to database")
        break
    except:
        print("Error connecting to database")
        time.sleep(5)
