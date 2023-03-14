# import the necessary packages
from flask import Flask, render_template, redirect, url_for, request,session,Response
from werkzeug import secure_filename
import sqlite3
import pandas as pd
from datetime import datetime
from autocorrect import Speller
from supportFile import *

spell = Speller(lang='en')

symptoms = ''
r = 0
l = 0
tstamp1=''
tstamp2=''

app = Flask(__name__)

app.secret_key = '1234'
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=['GET', 'POST'])
def landing():
	return redirect(url_for('login'))

@app.route('/home', methods=['GET', 'POST'])
def home():
	return render_template('home.html')

@app.route('/input', methods=['GET', 'POST'])
def input():
	
	if request.method == 'POST':
		if request.form['sub']=='Submit':
			num = request.form['num']
			
			users = {'Name':request.form['name'],'Email':request.form['email'],'Contact':request.form['num']}
			df = pd.DataFrame(users,index=[0])
			df.to_csv('users.csv',mode='a',header=False)

			sec = {'num':num}
			df = pd.DataFrame(sec,index=[0])
			df.to_csv('secrets.csv')

			name = request.form['name']
			num = request.form['num']
			email = request.form['email']
			password = request.form['password']
			age = request.form['age']
			gender = request.form['gender']

			now = datetime.now()
			dt_string = now.strftime("%d/%m/%Y %H:%M:%S")			
			con = sqlite3.connect('mydatabase.db')
			cursorObj = con.cursor()
			cursorObj.execute("CREATE TABLE IF NOT EXISTS Users (Date text,Name text,Contact text,Email text,password text,age text,gender text)")
			cursorObj.execute("INSERT INTO Users VALUES(?,?,?,?,?,?,?)",(dt_string,name,num,email,password,age,gender))
			con.commit()

			return redirect(url_for('login'))

	return render_template('input.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	global video
	global name
	if request.method == 'POST':
		name = request.form['name']
		password = request.form['password']
		con = sqlite3.connect('mydatabase.db')
		cursorObj = con.cursor()
		cursorObj.execute(f"SELECT Name from Users WHERE Name='{name}' AND password = '{password}';")

	
		if(cursorObj.fetchone()):
			return redirect(url_for('home'))
		else:
			error = "Invalid Credentials Please try again..!!!"
	return render_template('login.html',error=error)


@app.route('/textmining',methods=['GET', 'POST'])
def textmining():
	global symptoms
	global r
	global l
	global tstamp1,tstamp2
	count = 0
	if request.method == 'POST':
		if request.form['sub']=='Start':
			now = datetime.now()
			dt_string = now.strftime('%Y-%m-%d %H:%M:%S')			
			fmt = '%Y-%m-%d %H:%M:%S'
			tstamp1 = datetime.strptime(dt_string,fmt)
			print(tstamp1)

		if request.form['sub']=='Stop':
			now = datetime.now()
			dt_string = now.strftime('%Y-%m-%d %H:%M:%S')			
			fmt = '%Y-%m-%d %H:%M:%S'
			tstamp2 = datetime.strptime(dt_string,fmt)
			print(tstamp2)

			mins = timeDiff(tstamp1,tstamp2)
			if(mins == 0):
				mins = 1

			#username = request.form["name"]
			#email = request.form["email"]
			#num = request.form["num"]
			symptoms = request.form["symptoms"]
			words = symptoms.split()
			l = len(words)/mins
			text = '''In publishing and graphic design, Lorem ipsum is a 
			placeholder text commonly used to demonstrate the visual form of a 
			document or a typeface without relying on meaningful content. Lorem 
			ipsum may be used as a placeholder before final copy is available'''
			words1 = text.split()

			for word in words:
				cword = spell(word)
				print(cword,word)
				if(cword != word):
					count = count + 1
			r = count
			return redirect(url_for('stress'))		    
	return render_template('textmining.html')

@app.route('/stress',methods=['GET', 'POST'])
def stress():
	global symptoms
	global r
	global l
	if(request.method=='POST'):
		l = request.form['l']
		r = float(request.form['r'])
		temp = int(request.form['temp'])
		bph = int(request.form['bph'])
		bpl = int(request.form['bpl'])
		hr = int(request.form['hr'])
		test_sample = [[l,r,temp,bph,bpl,hr]]
		result,feedback = predictStress(test_sample)
		return render_template('stress.html',temp=temp,bph=bph,bpl=bpl,r=r,l=l,hr=hr,result=result,feedback=feedback)
	return render_template('stress.html',r=r,l=l)


# No caching at all for API endpoints.
@app.after_request
def add_header(response):
	# response.cache_control.no_store = True
	response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Expires'] = '-1'
	return response


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, threaded=True)
