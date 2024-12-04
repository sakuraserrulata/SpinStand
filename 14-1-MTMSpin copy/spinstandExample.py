#!/usr/bin/python3

from flask import Flask, render_template, request, redirect, url_for
import mysql.connector, os, json

with open('/home/kristen/SpinStand/14-1-MTMSpin/secrets.json', 'r') as secretFile:
    creds = json.load(secretFile)['mysqlCredentials']

app = Flask(__name__)

@app.route('/')
def default():
    return render_template('base.html')

@app.route('/salesorder-info', methods=['GET'])
def get_salesorder_info():
    OrderID = request.args.get('OrderID')
    
    # redirect to all products if no id was provided
    if OrderID is None:
        return redirect(url_for("get_salesorders"))

    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # update salesorder information if necessary
    salesorder_info = (
        request.args.get('OrderDate'),
        request.args.get('TotalCost'),
        request.args.get('PersonID'),
        OrderID
    )
    if not None in salesorder_info:
        mycursor.execute("UPDATE salesorder set OrderDate=%s, TotalCost=%s, PersonID=%s where OrderID=%s", salesorder_info)
        connection.commit()

    # check to see if a product needs to be dropped from Person
    remove_ProductID = request.args.get('remove_ProductID')
    if remove_ProductID is not None:
        mycursor.execute("DELETE from OrderProduct where ProductId=%s and OrderID=%s", (remove_ProductID, OrderID))
        connection.commit()

    # retrive basic information for the salesorder
    mycursor.execute("SELECT FirstName, LastName, OrderDate, TotalCost, SalesOrder.PersonID from SalesOrder join Person on SalesOrder.PersonID=Person.PersonID where SalesOrder.OrderID=%s", (OrderID,))
    try:
        FirstName, LastName, OrderDate, TotalCost, PersonID = mycursor.fetchall()[0]
    except:
        return render_template("error.html", message="Error retrieving SalesOrder")
    
    # retrieve registration info
    mycursor.execute("""SELECT Product.ProductID, ProductName, ProductType from Product 
                     join OrderProduct on OrderProduct.ProductID=Product.ProductID 
                     join SalesOrder on OrderProduct.OrderID=SalesOrder.OrderID 
                     where SalesOrder.OrderID=%s
                     order by ProductName""", (OrderID,)
                     )
    registeredproducts = mycursor.fetchall()

    mycursor.close()
    connection.close()
    return render_template("salesorder-info.html",
                           OrderID=OrderID,
                           FirstName=FirstName,
                           LastName=LastName,
                           OrderDate=OrderDate,
                           TotalCost=TotalCost,
                           PersonID=PersonID,
                           registered_Products=registeredproducts
                           )

@app.route('/product-info', methods=['GET'])
def get_product_info():
    ProductID = request.args.get('ProductID')
    
    # redirect to all products if no id was provided
    if ProductID is None:
        return redirect(url_for("get_products"))

    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()
    
    # check to see if the product needs to be updated
    new_ProductName = request.args.get('ProductName')
    new_ProductType = request.args.get('ProductType')
    if new_ProductName is not None and new_ProductType is not None:
        mycursor.execute("""UPDATE Product set ProductName=%s, ProductType=%s where ProductID=%s""", (new_ProductName, new_ProductType, ProductID))
        connection.commit()

    # check to see if a SalesOrder needs to be dropped
    drop_SalesOrder_OrderID = request.args.get('drop_OrderID')
    if drop_SalesOrder_OrderID is not None:
        mycursor.execute("""DELETE from OrderProduct where ProductId=%s and OrderID=%s""", (ProductID, drop_SalesOrder_OrderID))
        connection.commit()

    # check to see if a salesOrder needs to be added
    add_SalesOrder_OrderID = request.args.get('add_SalesOrder_OrderID')
    if add_SalesOrder_OrderID is not None:
        mycursor.execute("""INSERT into OrderProduct (ProductID, OrderID) values (%s, %s)""", (ProductID, add_SalesOrder_OrderID))
        connection.commit()

    # retreve the product information from the database
    mycursor.execute("Select ProductName, ProductType from Product where ProductID=%s", (ProductID,))
    ProductName_first, ProductType_last = mycursor.fetchone()
    if ProductName_first is None or ProductType_last is None:
        return """Error - unable to find product. <a href="/products">Return to the product list</a>"""
    
    # retrieve the products's person from the database
    mycursor.execute("""SELECT OrderProduct.OrderID, FirstName, LastName, OrderDate, TotalCost, Person.PersonID from OrderProduct
                         join SalesOrder on SalesOrder.OrderID=OrderProduct.OrderID
                         join Person on Person.PersonID=SalesOrder.PersonID
                         where OrderProduct.ProductID=%s""", (ProductID,))
    registered_SalesOrders = mycursor.fetchall()
    

    # retrieve a list of other Person the Product can register for
    mycursor.execute("""SELECT SalesOrder.OrderID, FirstName, LastName
                     from (
                         select OrderID as OrderID from SalesOrder
                         except
                         select OrderID from OrderProduct where ProductID=%s) as remainingSalesOrders
                     join SalesOrder on remainingSalesOrders.OrderID=SalesOrder.OrderID
                     join Person on Person.PersonID=SalesOrder.PersonID""", (ProductID,))
    all_sections = mycursor.fetchall()

    mycursor.close()
    connection.close()

    return render_template(
        "product-info.html", 
        ProductID=ProductID, 
        ProductName=ProductName_first, 
        ProductType=ProductType_last,
        registered_SalesOrders=registered_SalesOrders,
        unregistered_sections=all_sections
        )

@app.route('/products', methods=['GET'])
def get_products():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # check to see if a new product needs to be added
    new_ProductID = request.args.get('new_ProductID')
    new_ProductName = request.args.get('new_ProductName')
    new_ProductType = request.args.get('new_ProductType')
    if new_ProductID is not None and new_ProductName is not None and new_ProductType is not None:
        mycursor.execute("INSERT INTO Product (ProductID, ProductName, ProductType) values (%s, %s, %s)", (new_ProductID, new_ProductName, new_ProductType))
        connection.commit()

    # check to see if a product needs to be deleted
    delete_ProductID = request.args.get('delete_ProductID')
    if delete_ProductID is not None:
        try:
            mycursor.execute("delete from Product where ProductID=%s",(delete_ProductID,))
            connection.commit()
        except:
            return render_template("error.html", message="Error deleting product, maybe the product is in an existing order")
        
    # retrieve all Product
    mycursor.execute("SELECT ProductID, ProductName, ProductType from Product")
    pageTitle = "Showing all products"
    allproducts = mycursor.fetchall()

    mycursor.close()
    connection.close()
    return render_template('products.html', productList=allproducts, pageTitle=pageTitle)



@app.route('/salesorders', methods=['GET'])
def get_salesorders():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # check to see if a new section needs to be added
    new_SalesOrder_info = (
        request.args.get('new_OrderID'), 
        request.args.get('new_OrderDate'), 
        request.args.get('new_TotalCost'), 
        request.args.get('PersonID')
    )
    
    if not None in (new_SalesOrder_info):
        mycursor.execute("INSERT INTO SalesOrder (OrderID, OrderDate, TotalCost, PersonID) values (%s, %s, %s, %s)", new_SalesOrder_info)
        connection.commit()

    # check to see if a SalesOrder needs to be deleted
    delete_SalesOrderID = request.args.get('delete_SalesOrderID')
    if delete_SalesOrderID is not None:
        try:
            mycursor.execute("delete from SalesOrder where OrderID=%s",(delete_SalesOrderID,))
            connection.commit()
        except:
            return render_template("error.html", message="Error deleting Sales Order, perhaps there are products registered in it")

    # retrieve all SalesOrders
    mycursor.execute("SELECT SalesOrder.OrderID, FirstName, LastName, OrderDate, TotalCost from SalesOrder join Person on SalesOrder.PersonID=Person.PersonID")
    allSalesOrders = mycursor.fetchall()
    pageTitle = "Showing all sales orders"
    mycursor.execute("SELECT PersonID, FirstName, LastName from Person")
    allPersons = mycursor.fetchall()

    mycursor.close()
    connection.close()
    return render_template('salesorders.html', salesorderList=allSalesOrders, pageTitle=pageTitle, allPersons=allPersons)

@app.route('/persons', methods=['GET'])
def get_persons():
    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # look to see if a new Person should be added
    new_person_info = (
        request.args.get('new_PersonID'),
        request.args.get('new_FirstName'),
        request.args.get('new_LastName'),
        request.args.get('new_PhoneNumber'),
        request.args.get('new_Email'),
        request.args.get('new_Company')
    )
    if not None in new_person_info:
        mycursor.execute("INSERT INTO Person (PersonID, FirstName, LastName, PhoneNumber, Email, Company) values (%s, %s, %s, %s, %s, %s)", new_person_info)
        connection.commit()

    # look to see if a Person should be deleted
    delete_PersonID = request.args.get('delete_PersonID')
    if delete_PersonID is not None:
        try:
            mycursor.execute("DELETE from Person where PersonID=%s", (delete_PersonID,))
            connection.commit()
        except:
            return render_template("error.html", message="Error deleting Person, perhaps it has sections")

    # retrieve a list of all persons
    mycursor.execute("SELECT PersonID, FirstName, LastName, PhoneNumber, Email, Company from Person")
    allPersons = mycursor.fetchall()
    pageTitle = "Showing all people"
    
    mycursor.close()
    connection.close()
    return render_template('persons.html', pageTitle=pageTitle, allPersons=allPersons)
    #pageTitle=pageTitle

@app.route('/person-info', methods=['GET'])
def get_person_info():
    PersonID = request.args.get('PersonID')
    
    # redirect to all persons if no id was provided
    if PersonID is None:
        return redirect(url_for("get_persons"))

    connection = mysql.connector.connect(**creds)
    mycursor = connection.cursor()

    # update Person information
    FirstName = request.args.get('FirstName')
    LastName = request.args.get('LastName')
    PhoneNumber = request.args.get('PhoneNumber')
    Email = request.args.get('Email')
    Company = request.args.get('Company')

    if FirstName is not None and LastName is not None:
        mycursor.execute("UPDATE Person set FirstName=%s, LastName=%s, PhoneNumber=%s, Email=%s, Company=%s where PersonID=%s", (FirstName, LastName, PhoneNumber, Email, Company, PersonID))
        connection.commit()

    # retrieve Person information
    mycursor.execute("SELECT FirstName, LastName, PhoneNumber, Email, Company from Person where PersonID=%s", (PersonID,))
    try:
        FirstName, LastName, PhoneNumber, Email, Company = mycursor.fetchall()[0]
    except:
        return render_template("error.html", message="Error retrieving Person")
    
    # retrieve existing salesorder of Person
    mycursor.execute("SELECT OrderID, OrderDate, TotalCost from SalesOrder where PersonID=%s", (PersonID,))
    existingSalesOrders = mycursor.fetchall()
    
    mycursor.close()
    connection.close()

    return render_template("person-info.html",
                           PersonID=PersonID,
                           FirstName=FirstName,
                           LastName=LastName,
                           PhoneNumber=PhoneNumber,
                           Email=Email,
                           Company=Company,
                           existingSalesOrders=existingSalesOrders
                           )

if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")