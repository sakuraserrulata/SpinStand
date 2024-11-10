#!/usr/bin/python3

from flask import Flask, render_template, request
import mysql.connector, os
import json


app = Flask(__name__)


@app.route('/', methods=['GET'])
def showPerson():
    with open('/home/kristen/SpinStand/10-1-preparedStatements/secrets.json', 'r') as secretFile:
        creds = json.load(secretFile)['mysqlCredentials']

    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # If there is a name and desc 'GET' variable, insert the new value into the database
    First_Name = request.args.get('FirstName')
    Last_Name = request.args.get('LastName')
    Phone_Number = request.args.get('PhoneNumber')
    
    if First_Name:
        mycursor.execute("INSERT INTO Person (FirstName,LastName, PhoneNumber) values (%s, %s, %s)", (First_Name, Last_Name, Phone_Number))
        connection.commit()

    # Fetch the current values of the speaker table
    mycursor.execute("Select FirstName, LastName, PhoneNumber from Person")
    myresult = mycursor.fetchall()
    mycursor.close()
    connection.close()
    return render_template('AddToPersonTable.html', collection=myresult)
    #return "Hello world"


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")