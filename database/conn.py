import mysql.connector
import time
from app.schema.config import setting

while True:
    try:
        mydbConnect = mysql.connector.connect(
            host=setting.DB_HOSTNAME,
            user=setting.DB_USER,
            password=setting.DB_PASSWORD,
            database=setting.DB_NAME,
        )
        cursor = mydbConnect.cursor()
        print("Connected to database")
        break
    except:
        print("Error connecting to database")
        time.sleep(5)
