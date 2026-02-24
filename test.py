# import flask 
from flask import *
# initialize the app 
app=Flask(__name__)
# define your route/endpoint 
@app.route("/api/home")
# define a function 
def home():
    return jsonify({"message":"welcome to home"})

# products 
@app.route("/api/products")
def products() :
    return jsonify({"message" :"welcome to products"})

# services 
@app.route("/api/services")
def services() :
    return jsonify({"message" :"welcome to services"})

#contact
@app.route("/api/contact")
def contact () :
    return jsonify({"message":"welcome to contact"})

#shopping
@app.route("/api/shopping")
def shopping () :
    return jsonify({"message" :"welcome to shopping"})

#groceries
@app.route("/api/groceries")
def groceries () :
    return jsonify({"message" : "welcome to groceries"})

@app.route ("/api/addition",methods =["POST"])
def addition ():
    num1=request.form["num1"]
    num2=request.form["num2"]
    answer=int(num1)+int (num2)
    return jsonify({"sum":answer}) 
    

#substracton
@app.route ("/api/substraction",methods=["POST"])
def substraction () :
    num1=request.form["num1"]
    num2=request.form["num2"]
    answer=int(num1)-int(num2)
    return jsonify({"difference":answer})

#multiplication
@app.route("/api/multiplication",methods=["POST"])
def multiplication():
    num1=request.form["num1"]
    num2=request.form["num2"]
    answer=int(num1)*int(num2)
    return jsonify({"answer":answer})

#division
@app.route("/api/division",methods=["POST"])
def division ():
    num1=request.form["num1"]
    num2=request.form["num2"]
    answer=int(num1)/int(num2)
    return jsonify({"answer":answer})

#simple interest
@app.route("/api/simpleinterest",methods=["POST"])
def simpleinterest():
    num1=request.form["num1"]
    num2=request.form["num2"]
    num3=request.form["num3"]
    answer=int(num1)*int(num2)/int(num3)
    return jsonify({"answer":answer})












# run the app 
app.run(debug=True)