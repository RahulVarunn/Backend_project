import time
from flask import Flask, redirect, request, render_template, session, url_for
from flask_caching import Cache
from flask_restful import Resource, Api, reqparse
from flask import jsonify
from werkzeug.utils import secure_filename
import os
import pymysql
from flaskext.mysql import MySQL
from authlib.integrations.flask_client import OAuth


from flask_caching import Cache



app=Flask(__name__)


app.secret_key='random'
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='648212973492-krl5m9p2gnp11hdo1kvve1fdmagje1ig.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid profile email'},
)





api=Api(app)
app.config['MYSQL_DATABASE_HOST']="localhost"
app.config['MYSQL_DATABASE_USER']="root"
app.config['MYSQL_DATABASE_PASSWORD']=""
app.config['MYSQL_DATABASE_DB']="project_video"
mysql=MySQL(app)



config = {
    "DEBUG": True,          # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}
app.config.from_mapping(config)
cache = Cache(app)


app.config['UPLOAD_FOLDER'] = './static/image/' 



@app.route("/")
def hello():
     return render_template('login.html')


@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method =='POST':
        google=oauth.create_client('google')
        redirect_uri = url_for('authorize', _external=True)
        return google.authorize_redirect(redirect_uri)
    else:
         return render_template('login.html')


@app.route('/authorize')
def authorize():
    google=oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    print(user_info)
    session['email']=user_info
    conn=mysql.connect()
    cursor=conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * from users where user_id='{}'".format(user_info['id']))
    data=cursor.fetchall()
    if data:
        print('exist')
        for i in data:
            session['id']=i['id']  

    else:
        email=dict(session).get('email',None)
        cursor.execute("insert into users(user_id,user_name,user_profile) values('{}','{}','{}')".format(int(email['id']),email['name'],email['picture']))
        conn.commit()
        cursor.execute("SELECT * from users where user_id='{}'".format(user_info['id']))
        data=cursor.fetchall()
        for i in data:
            session['id']=i['id']  
    return redirect('/home')













@app.route('/upload',methods = ['GET','POST'])
def upload_file():
    if request.method =='POST':
        file = request.files['file']
        cmt=request.form.get('comments')
        tag=request.form.get('tags')

        if file:
            filename = secure_filename(file.filename)
            name="rahul"+"10"+filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],name))

            conn=mysql.connect()
            cursor=conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("insert into uploads(user_id,filename,captions,tags) values('{}','{}','{}','{}')".format(session.get('id'),name,cmt,tag))
            conn.commit()
            return "DONE"
    return render_template('folder.html')





@app.route('/home')
@cache.cached(key_prefix='MyCachedList',timeout=5)
def upload_f():
    conn=mysql.connect()
    cursor=conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT uploads.upload_id,uploads.filename,uploads.captions,uploads.tags,uploads.uplaod_date,users.id,users.`user_name`,users.user_profile FROM uploads INNER JOIN users ON uploads.user_id=users.id;")
    data=cursor.fetchall()  
    cursor.execute("SELECT * from users")
    data2=cursor.fetchall()  
    print(cache.get('MyCachedList'))
    return render_template('home.html',details=data,all=data2)







@app.route('/Personal_details',methods = ['GET','POST'])
def account():
    if request.method =='POST':
        id=request.form.get('id')
        conn=mysql.connect()
        cursor=conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT users.user_name,users_details.name,users_details.bio,users_details.user_id FROM users INNER JOIN users_details ON users.id=users_details.user_id WHERE users.id='{}';".format(id))
        data=cursor.fetchall()  


        return str(data)

        # return render_template('personal_acc.html')







@app.route('/add_comment',methods = ['GET','POST'])
def asi():
    if request.method =='POST':

        id=request.form.get('media_id')
        cmt=request.form.get('cmt')
        conn=mysql.connect()
        cursor=conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("insert into comments(comments,commented_usr_id,media_id) values('{}','{}','{}')".format(cmt,session.get('id'),id))
        conn.commit()
        return redirect('/home')



if __name__ == '__main__':
	app.run(debug=True,port=5000, host='localhost')