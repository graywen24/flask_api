#!flask/bin/python
# coding=utf-8
from flask import Flask, jsonify
import json
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)



try:
    connection = mysql.connector.connect(host='127.0.0.1',database='bms_1',user='root',password='P@ssw0rd')
    if connection.is_connected():
        SQL = "select id,guid,tag,path,name,node_type,space_type,parent_guid from space;"
        cursor = connection.cursor()
        cursor.execute(SQL)
        result = cursor.fetchall()      #return sql result
        for data in result:
            print("here is select result from db--->", data)
        print("total how many rows: -->",cursor.rowcount)

        fields = cursor.description   # sql key name
        #print("header--->",fields)
        cursor.close()
        connection.close()

   #main part
    column_list = []
    for i in fields:
        column_list.append(i[0])
    #print("colume list  -->", column_list)

 #start to read data
    for row in result:
        datadict = {}
        for i in range(len(column_list)):
            datadict[column_list[i]] = row[i]
            print("datadicstion--->", datadict)


    @app.route('/north/getSpace', methods=['GET'])
    def get_result():

            return jsonify({'space': datadict})


    if __name__ == '__main__':
        app.run(debug=True)


except Error as e:
    print("Error while connection to Mysql", e)
finally:
    connection.close()
    print "==== mysql closed==="











