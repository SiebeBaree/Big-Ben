import mysql.connector
from settings import host, user, passwd, database

db = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
cursor = db.cursor()

cursor.execute("CREATE TABLE guildSettings (guild BIGINT PRIMARY KEY, prefix VARCHAR(5))")

db.commit()
db.close()
