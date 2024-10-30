#! /usr/bin/python3

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("InputFormPersonTable.html")


@app.route('/PersonTable.html', methods=['GET'])
def renderTableGet():
    firstname = request.args.get('fname')
    lastname = request.args.get('lname')
    phonenumber = request.args.get('phonenumber')
    output = render_template('PersonTable.html', fname=firstname, lname=lastname, phonenumber=phonenumber)
    return output 


if __name__ == '__main__':
    app.run(port=8000, debug=True, host="0.0.0.0")