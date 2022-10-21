from flask import Flask,session,redirect, url_for

from authlib.integrations.flask_client import OAuth


app=Flask(__name__)
app.secret_key='rahhndom'
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id='181667646250-v561tv2im05chpsbk3h5gsfp9c17eflm.apps.googleusercontent.com',
    client_secret='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',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid profile email'},
)

@app.route("/home")
def hello():
    email=dict(session).get('user',None)
    return 'Hello, {}'.format(email['given_name'])


@app.route('/login')
def login():
    google=oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google=oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    profile = resp.json()
    session['user']=profile
    return redirect('/home')



if __name__ == '__main__':
	app.run(debug=True,port=5000, host='localhost')