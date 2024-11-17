#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, os, json

with open('secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCredentials']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/showStudents', methods=['GET'])
def showStudents():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    # mycursor2 = connection.cursor()

    # If there is a section_id 'GET' variable, use this to refine the query
    SalesOrderID = request.args.get('salesorder_orderid')
    if SalesOrderID is not None:
        mycursor.execute("""SELECT Product.ProductID, ProductName, ProductType, FirstName, LastName from Product 
                         join OrderProduct on Product.ProductID=OrderProduct.ProductID
                         join SalesOrder on SalesOrder.OrderID=OrderProduct.OrderID
                         join Person on Person.PersonID=SalesOrder.PersonID
                         where SalesOrder.OrderID=%s""", (SalesOrderID,))
        myresult = mycursor.fetchall()
        if len(myresult) >= 1:
            courseName = myresult[0][3]
            courseNumber = myresult[0][4]
        else:
            courseName = courseNumber = "Unknown"
        pageTitle = f"Showing all products in order {SalesOrderID}, {courseName} ({courseNumber})"
    else:
        mycursor.execute("SELECT ProductID, ProductName, ProductType from Product")
        pageTitle = "Showing all products"
        myresult = mycursor.fetchall()

    mycursor.close()
    connection.close()
    return render_template('students.html', studentList=myresult, pageTitle=pageTitle)

@app.route('/showSections', methods=['GET'])
def showSections():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # If there is a student_id 'GET' variable, use this to refine the query
    productid = request.args.get('Product_ProductID')
    if productid is not None:
        # Check if the student is registering for a new class
        registerSectionId = request.args.get('register_section_id')
        if registerSectionId is not None:
            mycursor.execute("""INSERT into OrderProduct (ProductID, OrderID) values (%s, %s)
                             """, (productid, registerSectionId))
            connection.commit()

        mycursor.execute("""SELECT SalesOrder.OrderID, FirstName, LastName, ProductName, ProductType
                         from Product
                         join OrderProduct on Product.ProductID=OrderProduct.ProductID
                         join SalesOrder on SalesOrder.OrderID=OrderProduct.OrderID
                         join Person on PersonID=SalesOrder.PersonID
                         where Product.ProductID=%s""", (productid,))
        sections = mycursor.fetchall()
        print(sections)
        if len(sections) >= 1:
            studentName = sections[0][3] + " " + sections[0][4]
            mycursor.execute("""SELECT SalesOrder.OrderID, FirstName, LastName
                                FROM SalesOrder
                                Join Person on Person.PersonID=SalesOrder.PersonID
                                WHERE SalesOrder.OrderID not in (
                                    SELECT SalesOrderID
                                    from OrderProduct
                                    where OrderProduct.ProductID=%s
                                )
                             """, (productid,))
            othersections = mycursor.fetchall()
            print(othersections)
        else:
            studentName = "Unknown"
            othersections = None
        pageTitle = f"Showing all orders for products: {studentName})"
    else:
        mycursor.execute("""SELECT SalesOrder.OrderID, FirstName, LastName from SalesOrder
                         join Person on SalesOrder.PersonID=Person.PersonID""")
        pageTitle = "Showing all orders"
        sections = mycursor.fetchall()
        othersections = None

    mycursor.close()
    connection.close()
    print(f"{productid=}")
    return render_template('sections.html', 
                           sectionList=sections, 
                           pageTitle=pageTitle, 
                           othersections=othersections, 
                           studentId=productid 
                           )


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")