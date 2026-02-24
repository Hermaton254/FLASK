# import flask 
from flask import *
import pymysql
import os
#initialize the app

app=Flask(__name__)

# configure the upload folder 
app.config["UPLOAD_FOLDER"] ="static/images"

# define your route/endpoint 
@app.route("/api/signup",methods=["POST"])

# define function to sign up 
def signup():
    # get user inputs from the form 
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    phone = request.form["phone"]

    # print the user info in terminal 
    print("our username is",username)
    print("our email is",email)
    print("our password is",password)
    print("our phone is",phone)

    # establish connection in database 
    connection =pymysql.connect(host="localhost",user="root",password="",database="higgssokogarden")

    # define your cursor 
    cursor=connection.cursor()

    # define sql to insert 
    sql ="insert into users(username,email,password ,phone) values (%s,%s,%s,%s)"

    # define your data 
    # NB: its the user inputs from step 3 
    data = (username ,email ,password,phone)

    # execute/run query 
    cursor.execute(sql,data)

    # commit/save changes 
    connection.commit()

    # return response  to the user 
    return jsonify ({"message":"signup successful"})

    # singin/login 
    # 1.define your route 
@app.route("/api/signin",methods=["POST"])
# 2.define function 
def login():
    # 3 get user input form 
    email=request.form["email"]
    password=request.form["password"]
    # 4.establish connection to database 
    connection=pymysql.connect(host="localhost",user="root",database="higgssokogarden",password="")
    # 5.define your cursor 
    cursor=connection.cursor(pymysql.cursors.DictCursor)
    # 6.sql to select 
    sql=("select * from users where email=%s and password=%s")
    # 7.define your data 
    data=(email,password)
    # 8.run query 
    cursor.execute (sql,data)
    # 9.check if user exist 
    if cursor.rowcount==0:
        return jsonify ({"message":"login failed"})
    else:
        #fetch the user
        user=cursor.fetchone()
        return jsonify ({"message":"login successful","user":user})
#add product
# define your route 
@app.route("/api/addproduct",methods=["POST"])
def product_details ():
    # get product information 
    product_name=request.form["product_name"]
    product_description=request.form["product_description"]
    product_cost=request.form["product_cost"]
    product_photo=request.files["product_photo"]

    # get filename 
    filename=product_photo.filename

    # specify where image will be saved 
    photopath=os.path.join(app.config["UPLOAD_FOLDER"],filename)
    # save the photo 
    product_photo.save(photopath)


    # establish connection in database 
    connection=pymysql.connect(host="localhost",user="root",password="",database="higgssokogarden")
    # define cursor 
    cursor=connection.cursor()
    # define sql insert 
    sql="insert into product_details (product_name,product_description,product_cost,product_photo)values(%s,%s,%s,%s)"
    # define your data 
    data=(product_name,product_description,product_cost,filename)
    # execute query 
    cursor.execute(sql,data)
    # save changes 
    connection.commit()
    # return response to the user 
    return jsonify ({"message":"product added successful"})


# get/fetch products 
# define your route/endpoints 
@app.route("/api/getproducts")
# define your function 
def getproducts ():
    # connection to database 
    connection=pymysql.connect(host="localhost",user="root",database="higgssokogarden",password="") 
    # define cursor 
    cursor=connection.cursor(pymysql.cursors.DictCursor)
    # define sql 
    sql="select * from product_details"

    # execute query 
    cursor.execute(sql)
    # fetch all products 
    allproducts=cursor.fetchall()
    return jsonify(allproducts)


# add caraccesories 
# define your route 
@app.route("/api/caraccesories",methods=["POST"])
def caraccesories ():
     # get product information 
     name=request.form["name"]
     brand=request.form["brand"]
     compatibility=request.form["compatibility"]
     material=request.form["material"]
     price=request.form["price"]
     photo=request.files["photo"]

     filename=photo.filename
     photopath=os.path.join(app.config["UPLOAD_FOLDER"],filename)
     photo.save(photopath)

     connection=pymysql.connect(host="localhost",user="root",password="",database="higgssokogarden")

     cursor=connection.cursor()

     sql="insert into caraccesories(name,brand,compatibility,material,price,photo)values (%s,%s,%s,%s,%s,%s)"

     data=(name,brand,compatibility,material,price,photo)

     cursor.execute(sql,data)

     connection.commit()

     return jsonify ({"message":"accesories added successful"})


#  get/fetch products 
# define your route/endpoints 
@app.route("/api/getcaraccesories")
# define your function 
def getcaraccesories ():
    # connection to database 
    connection=pymysql.connect(host="localhost",user="root",database="higgssokogarden",password="") 
    # define cursor 
    cursor=connection.cursor(pymysql.cursors.DictCursor)
    # define sql 
    sql="select * from caraccesories"

    # execute query 
    cursor.execute(sql)
    # fetch  
    allcaraccesories=cursor.fetchall()
    return jsonify( allcaraccesories)

    





   





























# run the app 
app.run(debug=True)