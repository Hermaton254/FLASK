#  import flask 
from flask import *
import pymysql
import os
#initialize the app

app=Flask(__name__)

# configure the upload folder 
app.config["UPLOAD_FOLDER"] ="static/images"

# define your route/endpoint 
@app.route("/api/adminadds",methods=["POST"])

# define function to sign up 
def adminadds():
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
    connection =pymysql.connect(host="localhost",user="root",password="",database="Isabu")

    # define your cursor 
    cursor=connection.cursor()

    # define sql to insert 
    sql ="insert into adminadds(username,email,password ,phone) values (%s,%s,%s,%s)"

    # define your data 
    # NB: its the user inputs from step 3 
    data = (username ,email ,password,phone)

    # execute/run query 
    cursor.execute(sql,data)

    # commit/save changes 
    connection.commit()

    # return response  to the user 
    return jsonify ({"message":"Added successful"})

    # singin/login 
    # 1.define your route 
@app.route("/api/admins",methods=["POST"])
# 2.define function 
def admins():
    # 3 get user input form 
    username=request.form["username"]
    password=request.form["password"]
    # 4.establish connection to database 
    connection=pymysql.connect(host="localhost",user="root",database="Isabu",password="")
    # 5.define your cursor 
    cursor=connection.cursor(pymysql.cursors.DictCursor)
    # 6.sql to select 
    sql=("select * from adminadds where username=%s and password=%s")
    # 7.define your data 
    data=(username,password)
    # 8.run query 
    cursor.execute (sql,data)
    # 9.check if user exist 
    if cursor.rowcount==0:
        return jsonify ({"message":"login failed"})
    else:
        #fetch the user
        user=cursor.fetchone()
        return jsonify ({"message":"login successful","admins":user})
@app.route("/api/registration",methods=["POST"])
def registration():
    # get user inputs from the form 
    admision= request.form["admision"]
    username= request.form["username"]
    password = request.form["password"]
    

    # print the user info in terminal 
    print("our admision is",admision)
    print("our username is",username)
    print("our password is",password)
    

    # establish connection in database 
    connection =pymysql.connect(host="localhost",user="root",password="",database="Isabu")

    # define your cursor 
    cursor=connection.cursor()

    # define sql to insert 
    sql ="insert into registration(admision,username,password) values (%s,%s,%s)"

    # define your data 
    # NB: its the user inputs from step 3 
    data = (admision,username,password)

    # execute/run query 
    cursor.execute(sql,data)

    # commit/save changes 
    connection.commit()

    # return response  to the user 
    return jsonify ({"message":"Added successful"})

    # singin/login 
    # 1.define your route 
@app.route("/api/login",methods=["POST"])
# 2.define function 
def login():
    # 3 get user input form 
    admision=request.form["admision"]
    password=request.form["password"]
    # 4.establish connection to database 
    connection=pymysql.connect(host="localhost",user="root",database="Isabu",password="")
    # 5.define your cursor 
    cursor=connection.cursor(pymysql.cursors.DictCursor)
    # 6.sql to select 
    sql=("select * from registration where admision=%s and password=%s")
    # 7.define your data 
    data=(admision,password)
    # 8.run query 
    cursor.execute (sql,data)
    # 9.check if user exist 
    user=cursor.fetchone()
    if user is None:
        return jsonify ({"message":"login failed"})
    else:
        #fetch the user
        user=cursor.fetchone()
        return jsonify ({"message":"login successful","registration":user})
   
#add product
# define your route 
@app.route("/api/announcements",methods=["POST"])
def announcements ():
    # get product information 
    title=request.form["title"]
    description=request.form["description"]
    photo=request.files["photo"]

    # get filename 
    filename=photo.filename

    # specify where image will be saved 
    photopath=os.path.join(app.config["UPLOAD_FOLDER"],filename)
    # save the photo 
    photo.save(photopath)


    # establish connection in database 
    connection=pymysql.connect(host="localhost",user="root",password="",database="Isabu")
    # define cursor 
    cursor=connection.cursor()
    # define sql insert 
    sql="insert into announcements(title,description,photo)values(%s,%s,%s)"
    # define your data 
    data=(title,description,filename)
    # execute query 
    cursor.execute(sql,data)
    # save changes 
    connection.commit()
    # return response to the user 
    return jsonify ({"message":"product added successful"})


# get/fetch products 
# define your route/endpoints 
@app.route("/api/homepage")
# define your function 
def homepage ():
    # connection to database 
    connection=pymysql.connect(host="localhost",user="root",database="Isabu",password="") 
    # define cursor 
    cursor=connection.cursor(pymysql.cursors.DictCursor)
    # define sql 
    sql="select * from announcements"

    # execute query 
    cursor.execute(sql)
    # fetch all products 
    annuoncements=cursor.fetchall()
    return jsonify(annuoncements)
# run the app 
app.run(debug=True)