from flask import *
import pickle
import numpy as np
from flask_mysqldb import MySQL
from functools import wraps
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import *
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import warnings
import pickle
import matplotlib.pyplot as  plt
app = Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_DB']='crop_recommendation'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql=MySQL(app)
model=pickle.load(open('model.pkl','rb'))
global district



@app.route('/login',methods=['POST','GET'])
def login():
    status=True
    if request.method=='POST':
        email=request.form["email"]
        pwd=request.form["upass"]
        cur=mysql.connection.cursor()
        cur.execute("select * from user where email=%s and password=%s",(email,pwd))
        data=cur.fetchone()
        if data:
            session['logged_in']=True
            session['username']=data["username"]
            flash('Login Successfully','success')
            return redirect('home')
        else:
            flash('Invalid Login. Try Again','danger')
    return render_template("login.html")
@app.route('/adminlogin',methods=['POST','GET'])
def adminlogin():
    status=True
    if request.method=='POST':
        uname=request.form["uname"]
        pwd=request.form["upass"]
        cur=mysql.connection.cursor()
        cur.execute("select * from admin where username=%s and password=%s",(uname,pwd))
        data=cur.fetchone()
        if data:
            print('gg')
            session['logged_in']=True
            session['username']=data["username"]
            flash('Login Successfully','success')
            return redirect('home')
        else:
            flash('Invalid Login. Try Again','danger')
    return render_template("adminlogin.html")
@app.route('/predict', methods=['GET', 'POST'])
def upload():
    global res
    global district
    if request.method == 'POST':
        # Get the file from post request
        district=request.form["district"]
        
        rainfall=request.form["rainfall"]
        
        humidity=request.form["humidity"]
       
        mintemp=request.form["mintemp"]
        
        maxtemp=request.form["maxtemp"]
        
        moisture=request.form["moisture"]
        
        minph=request.form["minph"]
        
        maxph=request.form["maxph"]
        
        df = pd.read_csv('train.csv')
        dist = df['Location'].unique()
        distdict = {}
        num = 1
        for i in dist:
                        distdict[i] = num
                        num = num+1
        
        model=pickle.load(open('model.pkl','rb'))
        
        int_features=[distdict[district],rainfall,humidity,mintemp,maxtemp,moisture,minph,maxph]
        
        final = [np.array(list(int_features))]
        
        prediction = model.predict(final)
        result = "The recommended Crop is " + prediction[0]
        return result
    return None  
from flask import send_file


@app.route('/')
def index():
    return render_template('login.html')

def is_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorized, Please Login','danger')
			return redirect(url_for('login'))
	return wrap
  
#Registration  
@app.route('/reg',methods=['POST','GET'])
def reg():
    status=False
    if request.method=='POST':
        name=request.form["uname"]
        email=request.form["email"]
        pwd=request.form["upass"]
        cur=mysql.connection.cursor()
        cur.execute("insert into user(username,password,email) values(%s,%s,%s)",(name,pwd,email))
        mysql.connection.commit()
        cur.close()
        flash('Registration Successfully. Login Here...','success')
        return redirect('login')
    return render_template("reg.html",status=status)

#Home page
@app.route("/home",methods=['POST','GET'])
@is_logged_in
def home():
    if request.method=='POST':
        if request.form.get("submit") == "Demo":
            df = pd.read_csv('train.csv')
            dist = df['Location'].unique()
            print('Demo Selected')
            return render_template('demo.html',data=dist)
        if request.form.get("submit") == "Train":
            
            warnings.filterwarnings("ignore")

            df = pd.read_csv('train.csv')
            dist = df['Location'].unique()
            distdict = {}
            num = 1
            for i in dist:
                            distdict[i] = num
                            num = num+1
            x = df[['Location','rain','Humidity', 'Min Temperature', 'Max Temperature', 'Moisture level', 'Min Ph','Max Ph']]
            x = np.array(x)
            for i in x:
                            i[0] = int(distdict[i[0]])
                            print(i)
            y = df['Crop']
            y = np.array(y)
            X_train,X_test,y_train,y_test = train_test_split(x,y,test_size = 0.2,random_state = 0)
            clf = RandomForestClassifier(n_estimators=230,criterion='entropy',max_depth=6,max_features=1,min_samples_leaf=1).fit(X_train,y_train)
            pickle.dump(clf,open('model.pkl','wb'))
            model=pickle.load(open('model.pkl','rb'))

    return render_template('home.html')
@app.route("/logout")
def logout():
	session.clear()
	flash('You are now logged out','success')
	return redirect(url_for('login'))

@app.route("/graph")
def graph():
    global district
    df = pd.read_csv('train.csv')
    df = df[df['Location'] == district]
    dataa = df['Crop'].unique()
    print(dataa)
    cropp = df['Crop'].value_counts()
    values = []
    for i in dataa:
        values.append(cropp[i])
        i = str(i) + " " + str(cropp[i]/len(df.index)) + "%" 
    print(dataa)
    plt.clf()
    plt.pie(values, labels = dataa,autopct='%.2f') 
    plt.savefig('outt.png')
    filename = 'outt.png'
    return send_file(filename, mimetype='image/gif')
if __name__ ==  '__main__':
    app.secret_key='secret123'
    app.run(debug=False, host = '0.0.0.0')
