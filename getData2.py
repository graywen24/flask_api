#!flask/bin/python
from flask import Flask, jsonify
import json
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)



try:
    connection = mysql.connector.connect(host='127.0.0.1',database='bms_1',user='root',password='P@ssw0rd')
    if connection.is_connected():
        db_info = connection.get_server_info()
        #print ("==== connect to mysql database... mysql server version is ", db_info)
        #connect to database now
        SQL = "select id,guid,tag,path,name,node_type,space_type,parent_guid,time from space;"

        cursor = connection.cursor()
        cursor.execute(SQL)
        data = cursor.fetchall()      #return sql result
        print("total how many rows: -->",cursor.rowcount)
        # will only return last record....................#
        fields = cursor.description   # sql key name
        cursor.close()

   #main part
    column_list = []
    for i in fields:
        column_list.append(i[0])
        print("colume list length -->",len(column_list))

    print("print data array detail",data)
    #
    for row in data:
# will only return last record....................#
            result = {}
            for i in range(len(column_list)):
                result[column_list[i]] = row[i]
                #result[column_list[0]] = row[0]
                #print row[0]
                #result[column_list[1]] = row[1]
                #result[column_list[2]] = row[2]
                #result[column_list[3]] = row[3]
                #result[column_list[4]] = row[4]
                #result[column_list[5]] = row[5]
                #result[column_list[6]] = row[6]
                #result[column_list[7]] = row[7]
                print("final result -->",result)
    @app.route('/north/getSpace', methods=['GET'])
    def get_result():
        return jsonify({'space': result})

    if __name__ == '__main__':
        app.run(debug=True)


except Error as e:
    print("Error while connection to Mysql", e)
finally:
    #closing the database connection
    if(connection.is_connected()):
        connection.close()
        print "==== mysql closed==="











