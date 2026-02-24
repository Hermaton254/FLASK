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

# Mpesa Payment Route/Endpoint 
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth
 
@app.route('/api/mpesa_payment', methods=['POST'])
def mpesa_payment():
    if request.method == 'POST':
        amount = request.form['amount']
        phone = request.form['phone']
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"
 
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
 
        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']
 
        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')
 
        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/api/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }
 
        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }
 
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL
 
        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return jsonify({"message": "Please Complete Payment in Your Phone and we will deliver in minutes"})




















# run the app 
app.run(debug=True)