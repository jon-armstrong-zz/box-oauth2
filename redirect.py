import flask
from flask import Flask, request, render_template, session
from flask.ext.session import Session
from boxsdk import OAuth2, Client
from boxsdk.exception import BoxOAuthException
from datetime import timedelta
from ConfigParser import ConfigParser

"""
Handles OAuth2 authorization flow with Box.
"""

app = Flask(__name__)

SESSION_TYPE = 'redis'
app.config.from_object(__name__)
Session(app)

config = None
oauth = None

def store_tokens(access, refresh):
    global session
    session['access_token'] = access
    session['refresh_token'] = refresh

def get_oauth():
    global session
    global config

    return OAuth2(
        client_id=config.get('main', 'CLIENT_ID'),
        client_secret=config.get('main', 'CLIENT_SECRET'),
        store_tokens=store_tokens,
        access_token=session.get('access_token'),
        refresh_token=session.get('refresh_token')
    )

@app.route('/redirect', methods=['GET'])
def redirect():
    global session

    code = request.args.get('code')

    if request.args.get('state') != session.get('csrf_token'):
        return 'Bad Request: Missing CSRF token', 400
    else:
        get_oauth().authenticate(code)
        return flask.redirect('/', code=302)

@app.route('/', methods=['GET'])
def index():
    global session

    try:
        client = Client(get_oauth())
        me = client.user(user_id='me').get()
        data = me['login']
        return render_template('authorized.html', data=data)
    except BoxOAuthException, e:
        auth_url, csrf_token = get_oauth().get_authorization_url(config.get('main', 'AUTH_URL'))
        session['csrf_token'] = csrf_token
        return render_template('index.html', auth_url=auth_url)
        


if __name__ == '__main__':
    config = ConfigParser()
    config.readfp(open('./config.cfg'))

    app.run(host='0.0.0.0', debug=False)
