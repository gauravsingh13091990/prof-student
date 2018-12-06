import os
import sqlite3
from flask import *
from flask_sqlalchemy import *
from datetime import datetime
from flask import send_from_directory
from werkzeug.utils import secure_filename
from sqlalchemy import update
from sqlalchemy import desc


app = Flask(__name__) # create the application instance :)
app.config.from_object(__name__) # load config from this file , flaskr.py

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///confessions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.secret_key = 'random string'

UPLOAD_FOLDER = 'static'

ALLOWED_EXTENSIONS = set(['jpeg', 'jpg', 'png', 'gif','txt','pdf','JPG'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

class Users(db.Model):
	__tablename__='users'
	password = db.Column(db.String(255))
	email = db.Column(db.String(255),primary_key=True)
	name = db.Column(db.String(255))
	phone = db.Column(db.String(255))
	gender = db.Column(db.String(255))
	Birthday = db.Column(db.String(255))

class Image(db.Model):
	__tablename__='images'
	title = db.Column(db.String(255))
	desc =  db.Column(db.String(255))
	id =db.Column(db.Integer,primary_key=True)
	imagename = db.Column(db.String(255))
	upvotes =db.Column(db.Integer)
	downvotes =db.Column(db.Integer)
	comment = db.Column(db.String(255))

class Like(db.Model):
	__tablename__='votes'
	likes_id =db.Column(db.String(255),primary_key=True)


class student(db.Model):
	__tablename__='student'
	password = db.Column(db.String(255))
	email = db.Column(db.String(255),primary_key=True)
	name = db.Column(db.String(255))
	phone = db.Column(db.String(255))
	gender = db.Column(db.String(255))
	Birthday = db.Column(db.String(255))

class Image1(db.Model):
	__tablename__='images1'
	title = db.Column(db.String(255))
	desc =  db.Column(db.String(255))
	id =db.Column(db.Integer,primary_key=True)
	imagename = db.Column(db.String(255))
	upvotes =db.Column(db.Integer)
	downvotes =db.Column(db.Integer)
	comment = db.Column(db.String(255))

class Like1(db.Model):
	__tablename__='votes1'
	likes_id =db.Column(db.String(255),primary_key=True)
db.create_all()

#done
@app.route("/register",methods = ['GET','POST'])
def registers():
	if request.method =='POST':
		password = request.form['password']
		password1= request.form['password1']
		email = request.form['email']
		name = request.form['name']
		gender = request.form['gender']
		Birthday = request.form['Birthday']
		phone = request.form['phone']
		if(password == password1):
			try:
				user = Users(password=password,email=email,name=name,gender=gender,Birthday=Birthday,phone=phone)
				db.session.add(user)
				db.session.commit()
				msg="registered successfully"
			except:
				db.session.rollback()
				msg="error occured"
		else:
			return render_template("layout.html",error1="password doesnot match")
	db.session.close()
	return render_template("layout.html",msg=msg)
# done
@app.route("/toprof")
def loginForm():
		return render_template('layout.html', error='')


@app.route('/')
def layout():	
	return render_template("home.html")

@app.route("/registerationForm")
def registrationForm():
	return render_template("layout.html")


@app.route("/login", methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		if is_valid(email, password):
			session['email'] = email
			session['logged_in'] = True
			global x
			x = email
			return redirect(url_for('index'))
		else:
			error = 'Invalid UserId / Password'
			return render_template('layout.html', error=error)
x=""		
@app.route('/index')
def index():
	if 'email' in session:
		email = session['email']
		image1 = "SELECT * FROM images"
		data1 = db.engine.execute(image1).fetchall()
		data2=reversed(data1)
		return render_template('main.html',email=email,name=data2)
	return render_template('home.html')
# done
def is_valid(email,password):
	stmt = "SELECT email, password FROM users"
	data = db.engine.execute(stmt).fetchall()
	for row in data:
		if row[0] == email and row[1] == password:
			return True
	return False
# done
@app.route("/write")
def write():
	return render_template('post.html')

# Done
@app.route("/About")
def about():
	stmt = "SELECT * FROM users"
	data = db.engine.execute(stmt).fetchall()
	for confession1 in data:
		if(confession1.email==x):
			Name=confession1.name
			Email=confession1.email
			Birthday=confession1.Birthday
			gender=confession1.gender
			mobile=confession1.phone
			return render_template('about.html',Name=Name,Email=Email,Birthday=Birthday,gender=gender,mobile=mobile)

# done
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	
	if request.method == 'POST':
		title = request.form['title']
		desc =  request.form['text']
	
		# check if post request has file path
		if 'file' not in request.files:
			print ("return.............")
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		print (file)
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		print("path doesn't know....")
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			MYDIR = os.path.dirname(__file__)
			print ("Is saving.....", MYDIR)
			file.save(os.path.join(MYDIR + "/" + app.config['UPLOAD_FOLDER'] + "/" + filename))
			return redirect(url_for('uploaded_file',filename=file.filename,title=title,desc=desc))
	error="error occured"
	return render_template("post.html",error=error)
	
def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# done
@app.route('/uploads/<filename>/<title>/<desc>',methods=['GET', 'POST'])
def uploaded_file(filename,title,desc):
	print (filename)
	ImagesAll = Image(imagename=filename,title=title,desc=desc,upvotes=0,downvotes=0,comment="comments goes here \n")
	db.session.add(ImagesAll)
	db.session.commit()
	return redirect(url_for('index'))
# done
@app.route('/votes/<xid>', methods=['GET', 'POST'])
def votes(xid):
	xid=int(xid)
	s=x+str(xid)
	if request.method == 'POST':
		name = request.form['voted']
		stmt=Image.query.filter_by(id=xid).all()[0]
		stmt2=Like.query.filter_by(likes_id=s).all()
		if(len(stmt2)==0):
			if(name =="like"):
				liked=Like(likes_id=s)
				db.session.add(liked)
				# db.session.commit()
				stmt.upvotes+=1
				db.session.commit()
				return redirect(url_for('index'))
			else:
				liked=Like(likes_id=s)
				db.session.add(liked)
				stmt.downvotes+=1
				db.session.commit()
				return redirect(url_for('index'))
		return redirect(url_for('index'))

	return render_template("home.html")
# done
@app.route('/comment/<xid>', methods=['GET', 'POST'])
def comment(xid):
	xid=int(xid)
	if request.method == 'POST':
		name = request.form['text']
		if(len(name)>0):
			stmt=Image.query.filter_by(id=xid).all()[0]
			z=stmt.comment.replace('\n','<br>')
			s=z+"\n"+name
			s=s.replace('\n','<br>')
			stmt.comment=s
			db.session.commit()
			return redirect(url_for('index'))
		return redirect(url_for('index'))

@app.route('/sign/<name>/<email>')
def sign(name,email):
	try:
		user = Users(password=None,email=email,name=name,gender=None,Birthday=None,phone=None)
		db.session.add(user)
		db.session.commit()
		msg="registered successfully"
	except:
		db.session.rollback()
		msg="error occured"
	session['email'] = email
	session['logged_in'] = True
	global y
	y=email
	return redirect(url_for('index'))
# done
@app.route('/logout')
def logout():
	session['logged_in'] = False
	session.pop('email',None)
	x=''
	return redirect(url_for('index'))
# STUDENT CODE
# ===================================================================================
@app.route("/jdhome")
def loginForm1():
		return render_template('layout1.html', error='')

@app.route("/register1",methods = ['GET','POST'])
def registers1():
	if request.method =='POST':
		password = request.form['password']
		password1= request.form['password1']
		email = request.form['email']
		name = request.form['name']
		gender = request.form['gender']
		Birthday = request.form['Birthday']
		phone = request.form['phone']
		if(password == password1):
			try:
				user = student(password=password,email=email,name=name,gender=gender,Birthday=Birthday,phone=phone)
				db.session.add(user)
				db.session.commit()
				msg="registered successfully"
			except:
				db.session.rollback()
				msg="error occured"
		else:
			return render_template("layout1.html",error1="password doesnot match")
	db.session.close()
	return render_template("layout1.html",msg=msg)

@app.route("/login1", methods = ['POST', 'GET'])
def login1():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		if is_valid1(email, password):
			session['email'] = email
			session['logged_in'] = True
			global k
			k = email
			return redirect(url_for('index1'))
		else:
			error = 'Invalid UserId / Password'
			return render_template('layout1.html', error=error)

@app.route('/index1')
def index1():
	if 'email' in session:
		email = session['email']
		image1 = "SELECT * FROM images1"
		data1 = db.engine.execute(image1).fetchall()
		data2=reversed(data1)
		return render_template('main1.html',email=email,name=data2)
	return render_template('home.html')

k=''
def is_valid1(email,password):
	stmt = "SELECT email, password FROM student"
	data = db.engine.execute(stmt).fetchall()
	for row in data:
		if row[0] == email and row[1] == password:
			return True
	return False

@app.route("/write1")
def write1():
	return render_template('post1.html')

@app.route("/About1")
def about1():
	stmt = "SELECT * FROM student"
	data = db.engine.execute(stmt).fetchall()
	for confession1 in data:
		if(confession1.email==k):
			Name=confession1.name
			Email=confession1.email
			Birthday=confession1.Birthday
			gender=confession1.gender
			mobile=confession1.phone
			return render_template('about1.html',Name=Name,Email=Email,Birthday=Birthday,gender=gender,mobile=mobile)

@app.route('/upload1', methods=['GET', 'POST'])
def upload_file1():
	
	if request.method == 'POST':
		title = request.form['title']
		desc =  request.form['text']
	
		# check if post request has file path
		if 'file' not in request.files:
			print ("return.............")
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		print (file)
		# if user does not select file, browser also
		# submit a empty part without filename
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		print("path doesn't know....")
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			MYDIR = os.path.dirname(__file__)
			print ("Is saving.....", MYDIR)
			file.save(os.path.join(MYDIR + "/" + app.config['UPLOAD_FOLDER'] + "/" + filename))
			return redirect(url_for('uploaded_file1',filename=file.filename,title=title,desc=desc))
	error="error occured"
	return render_template("post1.html",error=error)

@app.route('/uploads1/<filename>/<title>/<desc>',methods=['GET', 'POST'])
def uploaded_file1(filename,title,desc):
	print (filename)
	ImagesAll = Image1(imagename=filename,title=title,desc=desc,upvotes=0,downvotes=0,comment="comments goes here \n")
	db.session.add(ImagesAll)
	db.session.commit()
	return redirect(url_for('index1'))

@app.route('/votes1/<xid>', methods=['GET', 'POST'])
def votes1(xid):
	xid=int(xid)
	s=x+str(xid)
	if request.method == 'POST':
		name = request.form['voted']
		stmt=Image1.query.filter_by(id=xid).all()[0]
		stmt2=Like1.query.filter_by(likes_id=s).all()
		if(len(stmt2)==0):
			if(name =="like"):
				liked=Like1(likes_id=s)
				db.session.add(liked)
				# db.session.commit()
				stmt.upvotes+=1
				db.session.commit()
				return redirect(url_for('index1'))
			else:
				liked=Like1(likes_id=s)
				db.session.add(liked)
				stmt.downvotes+=1
				db.session.commit()
				return redirect(url_for('index1'))
		return redirect(url_for('index1'))

	return render_template("home.html")

@app.route('/comment1/<xid>', methods=['GET', 'POST'])
def comment1(xid):
	xid=int(xid)
	if request.method == 'POST':
		name = request.form['text']
		if(len(name)>0):
			stmt=Image1.query.filter_by(id=xid).all()[0]
			z=stmt.comment.replace('\n','<br>')
			s=z+"\n"+name
			s=s.replace('\n','<br>')
			stmt.comment=s
			db.session.commit()
			return redirect(url_for('index1'))
		return redirect(url_for('index1'))

@app.route('/logout1')
def logout1():
	session['logged_in'] = False
	session.pop('email',None)
	k=''
	return redirect(url_for('index1'))

@app.route('/CCNSB.html', methods=['GET', 'POST'])  
def CCNSB():
    return render_template('CCNSB.html')
@app.route('/CVIT.html', methods=['GET', 'POST'])  
def CVIT():
    return render_template('CVIT.html')
@app.route('/CogSci.html', methods=['GET', 'POST'])  
def CogSci():
    return render_template('CogSci.html')
@app.route('/DSAC.html', methods=['GET', 'POST'])  
def DSAC():
    return render_template('DSAC.html')
@app.route('/LTRC.html', methods=['GET', 'POST'])  
def LTRC():
    return render_template('LTRC.html')
@app.route('/LSI.html', methods=['GET', 'POST'])  
def LSI():
    return render_template('LSI.html')
@app.route('/SPCRC.html', methods=['GET', 'POST'])  
def SPCRC():
    return render_template('SPCRC.html')

@app.route('/profblog.html', methods=['GET', 'POST'])  
def profblog():
    return render_template('profblog.html')

@app.route('/abhijit.html', methods=['GET', 'POST'])  
def abhijit():
    return render_template('abhijit.html')

@app.route('/nita.html', methods=['GET', 'POST'])  
def nita():
    return render_template('nita.html')

@app.route('/vinod.html', methods=['GET', 'POST'])  
def vinod():
    return render_template('vinod.html')

@app.route('/deva.html', methods=['GET', 'POST'])  
def deva():
    return render_template('deva.html')

@app.route('/harjinder.html', methods=['GET', 'POST'])  
def harjinder():
    return render_template('harjinder.html')

@app.route('/vineet.html', methods=['GET', 'POST'])  
def vineet():
    return render_template('vineet.html')

@app.route('/jawahar.html', methods=['GET', 'POST'])  
def jawahar():
    return render_template('jawahar.html')

@app.route('/deb.html', methods=['GET', 'POST'])  
def deb():
    return render_template('deb.html')

@app.route('/kamalakar.html', methods=['GET', 'POST'])  
def kamalakar():
    return render_template('kamalakar.html')

@app.route('/kishore.html', methods=['GET', 'POST'])  
def kishore():
    return render_template('kishore.html')

@app.route('/rajeev.html', methods=['GET', 'POST'])  
def rajeev():
    return render_template('rajeev.html')

@app.route('/abhishek.html', methods=['GET', 'POST'])  
def abhishek():
    return render_template('abhishek.html')

@app.route('/rama.html', methods=['GET', 'POST'])  
def rama():
    return render_template('rama.html')

@app.route('/shaik.html', methods=['GET', 'POST'])  
def shaik():
    return render_template('shaik.html')

@app.route('/garimella.html', methods=['GET', 'POST'])  
def garimella():
    return render_template('garimella.html')

@app.route('/anil.html', methods=['GET', 'POST'])  
def anil():
    return render_template('anil.html')

@app.errorhandler(404)
def http_404_handler(error):
	return render_template('error404.html')
	
if __name__ =='__main__':
	app.run()

