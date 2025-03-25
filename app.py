from flask import Flask, flash, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime
from sqlalchemy import  DateTime
from sqlalchemy.sql import func
from mysql import connector

#creating the app
app=Flask(__name__)
app.secret_key="secret"

class Base(DeclarativeBase):
    pass

# creating the db 
db=SQLAlchemy(model_class=Base)


#define the db tables
class Users(db.Model):
    __tablename__ = 'Users'
    uid = db.Column(db.Integer, primary_key=True)
    uname = db.Column(db.String(50))
    email = db.Column(db.String(20), unique= True)
    password= db.Column(db.String(16))
    created_date=db.Column(DateTime(timezone=True), default=func.now()) 
    

class Todos(db.Model):
    __tablename__ = 'Todos'
    id=db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(50),unique=True, nullable=False)
    completed = db.Column(db.Boolean)
    date  = db.Column(DateTime(timezone=True), default=func.now())
    uid= db.Column(db.Integer, db.ForeignKey('Users.uid'))
    user = db.relationship('Users', backref='todo')


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:@localhost/todoapp"
db.init_app(app)

#default signup page
@app.route("/")
def check():
    return render_template('signup.html')

# fetch all existing todos and send to client on js file
@app.route("/allTodos/<string:user>")
def allTodos(user):
    #find the uid of the current user
    curr_user=Users.query.filter_by(uname=user).first()
    the_uid=curr_user.uid
    
    #get all the todos for the logged in user
    activities=Todos.query.filter_by(uid=the_uid).all()
    todos={}
    
    for i in activities:
        a=i.activity
        b=i.completed
        todos[a]=b
    
    return jsonify(todos)

# Create a new todo
@app.route("/newTodo", methods=['POST', 'GET'])
def addTodo():
    if request.method=='POST':
        todo=request.get_json().get('activity')
        date=datetime.now()
        user=request.get_json().get('user')

        #get the user details and add a new todo for him
        user_id=Users.query.filter_by(uname=user).first()
        new=Todos(activity=todo, completed=False, date=date, uid=user_id.uid)
        db.session.add(new)
        db.session.commit()
        return "todo added successfully"
    
# updates an existing todo
@app.route("/updateTodo",methods=['POST', 'GET'])
def updateTodo():
    if request.method=="POST":
        todo=request.get_json().get('activity')
        action=request.get_json().get('action')
        user=request.get_json().get('user')
        
        #get the user details and update the todo for him
        this_user=Users.query.filter_by(uname=user).first()
        todoRecord=Todos.query.filter_by(activity=todo, uid=this_user.uid).first()
        if action=="delete":
            db.session.delete(todoRecord)
        elif action=="complete":
            if todoRecord.completed==True:
                todoRecord.completed=False
            else:
                todoRecord.completed=True
        db.session.commit()
        return "received and updated data"

#signup page
@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method=="POST":

        name =request.form.get('name')
        email=request.form.get('email')
        password=request.form.get('password')
        date=datetime.now()

        #if blank fields are submitted
        if name=="" or password=="" or email=="":
            flash("Please enter the required fields!", "no_details")
            return redirect(url_for('check'))
        else: #the user already exists
            ex_user=Users.query.filter_by(uname=name).first()
            ex_email=Users.query.filter_by(email=email).first()
            if ex_user!=None or ex_email!=None:
                flash("This username or email already exists, please login.", "exists")
                return redirect(url_for('check'))
            else: #add user to database
                new=Users(uname=name, email=email, password=password, created_date=date)
                db.session.add(new)
                db.session.commit()

                flash("Your account was successfully created!!! PLease login.", "account created")
                return redirect(url_for('login'))
        
#login page
@app.route("/login", methods=['GET'])
def login():
    return render_template('login.html')

#check if login credentials are correct
@app.route("/checkLogin", methods=['POST'])
def checkLogin():
    if request.method=='POST':
        username=request.form.get('username')
        password=request.form.get('password')
        
        if username=="" or password=="":
            flash("Please enter the required fields!", "no_credentials")
            return redirect(url_for('login'))
        else:
            user=Users.query.filter_by(uname=username).first()
            if user!=None and user.password==password:
                return render_template('index.html', user=username)
            else:
                flash("Username or/and Password is incorrect!","wrong_credentials")
                return redirect(url_for('login'))
            
#logout 
@app.route("/logout")
def logout():
    return redirect(url_for('login'))


app.run()

