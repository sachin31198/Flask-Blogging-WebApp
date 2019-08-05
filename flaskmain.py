from flask import Flask
import pyodbc as db
from flask import Flask, flash, redirect, render_template, request, url_for
app = Flask(__name__)
#Create connection string to connect DBTest database with windows authentication
con = db.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=.;Trusted_Connection=yes;DATABASE=Blogsdb')
cur = con.cursor()

sess_running=False
user_email=None
user_password=None
Owner_id=None
Username=None

@app.route('/signup', methods=['GET','POST'])
def Signupform():
	global sess_running
	sess_running=False
	if request.method =='POST':
		if not request.form['email'] or not request.form['password']:
			return render_template("login.html")
		else:
			email = request.form['email']
			password=request.form['password']
			name=request.form['name']
			cur.execute("Insert into users values(?,?,?,GETDATE())",name,email,password)
			cur.commit()
	return render_template("signuppage.html")

@app.route('/login',methods=['GET','POST'])
def Loginform():
	global sess_running,user_email,user_password,Owner_id,Username
	sess_running=False
	if request.method =='POST':
		if not request.form['email'] or not request.form['password']:
			return render_template("loginpage.html")
		else:
			email = request.form['email']
			password=request.form['password']
			cur.execute("Select users.password,users.userid,users.Username from users where users.useremail=?",email)
			value=cur.fetchone()
			if value[0]==password:
				sess_running=True
				user_email=email
				user_password=password
				Owner_id=value[1]
				Username=value[2]
				return redirect("http://127.0.0.1:5000/blogs")
			else:
				return render_template("loginpage.html")
	return render_template("loginpage.html")

@app.route('/blogs',methods=['GET','POST'])
def blogshomepage():
	global sess_running,user_email,user_password,Owner_id,Username
	if sess_running==True:
		indx=[i for i in range(12,17)]
		l1=list()
		l2=list()
		for val in indx:
			cur.execute('select PostDetails.Posttext from Postdetails where postdetails.postdetailid=?',val)
			value=cur.fetchone()
			cur.execute('select PostDetails.PostID from Postdetails where postdetails.postdetailid=?',val)
			ids=cur.fetchone()
			cur.execute('select Posts.posttitle from posts where posts.postid=?',ids)
			title=cur.fetchone()
			l1.append(value)
			l2.append(title)
		print(l2)
		return render_template("blogspage.html",blog_content=l1,Postid=indx,title=l2)
	else:
		return redirect("http://127.0.0.1:5000/login")

@app.route('/myblogs',methods=['GET','POST'])
def myblog():
	global sess_running,user_email,user_password,Owner_id,Username
	if sess_running==True:
		l1=list()
		l2=list()
		cur.execute('select Posts.PostID from Posts where posts.ownerid=?',Owner_id)
		post_id=cur.fetchall()
		for x in post_id:
			cur.execute('select PostDetails.Posttext from Postdetails where postdetails.postid=?',x)
			value=cur.fetchone()
			cur.execute('select Posts.posttitle from posts where posts.postid=?',x)
			title=cur.fetchone()
			l1.append(value)
			l2.append(title)
		return render_template("myblogs.html",blog_content=l1,Postid=post_id,title=l2)
	else:
		return redirect("http://127.0.0.1:5000/login")

@app.route('/Compose',methods=['GET','POST'])
def compose():
	global sess_running,user_email,user_password,Owner_id,Username
	if sess_running==True:
		if request.method =='POST':
			blog_title=request.form['title']
			blog_content=request.form['content']
			length=len(blog_content)
			cur.execute('Insert into Posts values(?,GETDATE(),0,?)',blog_title,Owner_id)
			cur.commit()
			cur.execute('select Posts.PostID from Posts where Posts.Posttitle=?',blog_title)
			val=cur.fetchone()
			cur.execute('Insert into PostDetails values(?,?,?)',val[0],blog_content,length)
			cur.commit()
	return render_template("testtext.html")

@app.route('/Readmore/<PostID>',methods=['GET','POST'])
def readmore(PostID):
	global sess_running,user_email,user_password,Owner_id,Username
	if request.method =='POST':
		comment=request.form['Comment']
		cur.execute('Insert into comments values (?,?,GETDATE(),0,?)',comment,Owner_id,PostID)
		cur.commit()
		cur.execute('Select Postdetails.posttext from Postdetails where Postdetails.Postdetailid=?',PostID)
		val=cur.fetchone()
		cur.execute('select Postdetails.PostID from postdetails where postdetails.postdetailid=?',PostID)
		x=cur.fetchone()
		cur.execute('select posts.posttitle from posts where posts.postid=?',x)
		title=cur.fetchone()
		cur.execute('select comments.comment from comments where comments.PostID=?',PostID)
		comments=cur.fetchone()
		return render_template('readmore.html',blog_content=val,title=title,comments=comments)
	if request.method=='GET':
		cur.execute('Select Postdetails.posttext from Postdetails where Postdetails.Postdetailid=?',PostID)
		val=cur.fetchone()
		cur.execute('select Postdetails.PostID from postdetails where postdetails.postdetailid=?',PostID)
		x=cur.fetchone()
		cur.execute('select posts.posttitle from posts where posts.postid=?',x)
		title=cur.fetchone()
		cur.execute('select comments.comment from comments where comments.PostID=?',PostID)
		comments=cur.fetchone()
		return render_template('readmore.html',blog_content=val,title=title,comments=comments)


@app.route('/logout',methods=['GET','POST'])
def logout():
	global sess_running,user_email,user_password,Owner_id,Username
	sess_running=False
	return render_template('loginpage.html')
cur.commit() #Use this to commit the insert operation

"""cur.execute("select C_ID,C_FP from Test2")
row=cur.fetchone()
if row:
	print(row)
	print(row[1])



"""