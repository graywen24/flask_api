#update in https://www.cnblogs.com/gray13/p/10977375.html

#!flask/bin/python

#coding:utf-8
from flask import Flask, jsonify
import json
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)



try:
    connection = mysql.connector.connect(host='127.0.0.1',database='bms_1',user='root',password='P@ssw0rd')
    if connection.is_connected():
        SQL = "select id,guid,tag,path,name,node_type,space_type,parent_guid,time from space;"
        cursor = connection.cursor()
        cursor.execute(SQL)
        result_list = cursor.fetchall()      #return sql result
        print("fetch result-->",type(result_list))  #is s list type, need to be a dict

        fields_list = cursor.description   # sql key name
        print("fields result -->",fields_list)
        #print("header--->",fields)
        cursor.close()
        connection.close()



        # main part
    column_list = []
    for i in fields_list:
        column_list.append(i[0])
    print("print final colume_list",column_list)

        # print("colume list  -->", column_list)

    jsonData_list = []
    for row in result_list:
        data_dict = {}
        for i in range(len(column_list)):
            data_dict[column_list[i]] = row[i]
        jsonData_list.append(data_dict)



    @app.route('/north/getSpace', methods=['GET'])
    def get_space():
        return jsonify({'space': jsonData_list})


    if __name__ == '__main__':
        app.run(debug=True)


except Error as e:
    print("Error while connection to Mysql", e)
finally:
    connection.close()
    print "==== mysql closed==="