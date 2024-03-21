import mysql.connector
cnx = mysql.connector.connect(
    host="LUNCHBOX",
    user="root",
    password="admin",
    database="dbms_project"
)
cursor = cnx.cursor()
query = "SELECT * FROM items"
cursor.execute(query)
items = cursor.fetchall()