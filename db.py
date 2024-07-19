import mysql.connector

dataBase = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="]+X6£nGgSRD4<X9weB",
)

# Prepare a cursor object
cursorObject = dataBase.cursor()

# Create the database
cursorObject.execute("CREATE DATABASE dojoco")
print("Complete")

