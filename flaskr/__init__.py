from flask import Flask, session, redirect, url_for
from authlib.integrations.flask_client import OAuth
import os
import requests

# trigger deployment 

def create_app(test_config=None, *args, **kwargs):
    # create and configure app
    app = Flask(__name__)
    from . import config
    app.config.from_object(config)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.secret_key = "secret key"
    oauth = OAuth(app)

    # set up Amazon Cognito login
    oauth.register(
        name='oidc',
        authority='https://cognito-idp.us-east-2.amazonaws.com/us-east-2_uiivhIHti',
        client_id=app.config["CLIENT_ID"],
        client_secret='1q99uobg1v91rtkksi3365apnoq43n0j9u2snf6d543ub3tr6fji', # store this and client id securely later
        server_metadata_url='https://cognito-idp.us-east-2.amazonaws.com/us-east-2_uiivhIHti/.well-known/openid-configuration',
        client_kwargs={'scope': 'email openid phone'}
    )

    from . import home
    app.register_blueprint(home.bp)

    from . import dashboard
    app.register_blueprint(dashboard.bp)

    from . import db
    db.init_app(app)

    @app.route('/cognito-login')
    def login():
      print(session.get("user", None))
      nonce = os.urandom(16).hex()
      session['nonce'] = nonce

      state = os.urandom(16).hex() 
      session['state'] = state
      return oauth.oidc.authorize_redirect('https://money-mate-f79a354aaf62.herokuapp.com/callback', nonce=nonce, state=state)
      # return oauth.oidc.authorize_redirect('http://localhost:5000/callback', nonce=nonce, state=state, prompt='login')

    @app.route('/cognito-logout')
    def logout():
      session.clear()
      cognito_logout_url = f"https://cognito-idp.us-east-2.amazonaws.com/us-east-2_uiivhIHti/logout?client_id={app.config['CLIENT_ID']}&logout_uri=https://money-mate-f79a354aaf62.herokuapp.com/"
      # cognito_logout_url = f"https://us-east-2uiivhihti.auth.us-east-2.amazoncognito.com/logout?client_id={app.config['CLIENT_ID']}&logout_uri=http://localhost:5000/"
      return redirect(cognito_logout_url)
    
    @app.route('/callback')
    def callback():
        token = oauth.oidc.authorize_access_token()
        nonce = session.pop('nonce')
        user_info = oauth.oidc.parse_id_token(token, nonce=nonce) 
        session["user"] = user_info  
        return redirect("/")  

    return app
