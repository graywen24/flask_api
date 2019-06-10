#!flask/bin/python
from flask import Flask, jsonify
import json
import mysql.connector
from mysql.connector import Error
try:
    connection = mysql.connector.connect(host='127.0.0.1',database='bms_1',user='root',password='P@ssw0rd')
    if connection.is_connected():
        db_info = connection.get_server_info()
        print ("==== connect to mysql database... mysql server version is ", db_info)
        #connect to database now
        SQL = "select guid,tag,path,name,node_type,space_type,parent_guid,TIME from space;"

        cursor = connection.cursor()
        cursor.execute(SQL)
        records = cursor.fetchall()
        print("total number of rows in -->", cursor.rowcount)
        print("print records===",records)
        for row in records:
            print("guid:",row[0])
            print("tag:", row[1])
            print("path:", row[2])
            print("name:", row[3])
            print("node_type:", row[4])
            print("space_type:", row[5])
            print("parent_guid:", row[6])
        #cursor.close()


except Error as e:
    print("Error while connection to Mysql", e)
finally:
    # close database
    if (connection.is_connected()):
        cursor.close()
        connection.close()
        print("Mysql connection closed")

    app = Flask(__name__)

    @app.route('/north/getSpace', methods=['GET'])
    def get_result():
        return jsonify(records)





    if __name__ == '__main__':
     app.run(debug=True)










