import os
from flask import Flask, session, render_template,request, url_for,redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
DATABASE_URL="postgres://dnlwaxlradcjor:65c6399c0ddf92b6648364d98c1cece55b184bf8050278f9b2d07522e85fc61e@ec2-50-17-246-114.compute-1.amazonaws.com:5432/d3fg403272h3as"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def index():
	return render_template('welcome.html')

@app.route("/post")
def post():
	return render_template('post.html')

@app.route("/home")
def home():
	return render_template('home.html')	

@app.route("/login")
def login():
	return render_template('login.html')

@app.route("/vlogin",methods=['POST','GET'])
def vlogin():
	email=request.form.get("email")
	password=request.form.get("password")
	query=db.execute("SELECT * FROM signup WHERE email=:email AND password=:password",
	{"email":email,"password":password}).fetchall()
	for q in query:
		if q.email==email and q.password==password:
			return redirect(url_for('home'))
	return redirect(url_for('login'))		

@app.route("/signup")
def signup():
	return render_template('signup.html')

@app.route("/register", methods=['POST'])
def register():
	firstName=request.form.get("firstName")
	lastName=request.form.get("lastName")
	email=request.form.get("email")
	if request.form.get("password") == request.form.get("c_password"):
		password=request.form.get("password")
	else:
		flash('Password does not match')
		return redirect(url_for('signup'))
	db.execute("INSERT INTO signup(firstName,lastName,email,password) VALUES(:firstName,:lastName,:email,:password)",
	{"firstName":firstName,"lastName":lastName,"email":email,"password":password})
	db.commit()
	db.close()
	return render_template('login.html')
