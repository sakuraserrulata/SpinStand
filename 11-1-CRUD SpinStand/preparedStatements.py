#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, os, json


with open('/home/kristen/SpinStand/10-1-preparedStatements/secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCredentials']

connection = mysql.connector.connect(**creds)


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def showActors():
    mycursor = connection.cursor()

    # Handle POST creating a new entry
    if request.method == 'POST':
        # FirstName, LastName, PhoneNumber, Email, Company
        newPersonData = request.form
        if newPersonData["FirstName"] == '' or newPersonData["LastName"] == '':
            return "Invalid form, first name and last name must be filled out"
        dataUnpacked = (
            newPersonData["FirstName"],
            newPersonData["LastName"],
            newPersonData["PhoneNumber"],
            newPersonData["Email"],
            newPersonData["Company"]
        )
        mycursor.execute("INSERT into Person (FirstName, LastName, PhoneNumber, Email, Company) values (%s, %s, %s, %s, %s)", dataUnpacked)
        connection.commit()

    # Delete entries
    if request.args.get('delete') == 'true':
        deleteID = request.args.get('PersonID')
        mycursor.execute("DELETE from Person where PersonID=%s", (deleteID,))
        connection.commit()

    # Fetch the current values of the speaker table
    mycursor.execute("Select * from Person")
    myresult = mycursor.fetchall()
    mycursor.close()
    return render_template('PersonTable.html', collection=myresult)

@app.route("/updateperson", methods=["GET", "POST"])
def updateActor():
    mycursor = connection.cursor()
    if request.method == 'POST':
        # PersonID, FirstName, LastName, PhoneNumber, Email, Company
        personData = request.form
        if personData["FirstName"] == '' or personData["LastName"] == '' or personData["PersonID"] == '':
            return "Invalid form, first name and last name must be filled out"
        person = (
            personData["PersonID"],
            personData["FirstName"],
            personData["LastName"],
            personData["PhoneNumber"],
            personData["Email"],
            personData["Company"],
            personData["PersonID"]
        )
        mycursor.execute("UPDATE Person set PersonID=%s, FirstName=%s, LastName=%s, PhoneNumber=%s, Email=%s, Company=%s where PersonID=%s", person)
        mycursor.close()
        connection.commit()
        return redirect('/')

    PersonID = request.args.get('PersonID')

    if PersonID is None:
        return "Error, id not specified"

    mycursor = connection.cursor()
    mycursor.execute("select * from Person where PersonID=%s;", (PersonID,))
    personFromDB = mycursor.fetchone()
    mycursor.close()
    return render_template('UpdatePerson.html', person=personFromDB)


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")