import pymysql

db = pymysql.connect(host='192.168.0.102',port=3306,user='luser',password='456123789',database='python')
cursor = db.cursor()

cursor.execule("show tables")

db.commit()
db.close()
