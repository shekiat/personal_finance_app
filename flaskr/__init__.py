from flask import Flask, session, redirect
from authlib.integrations.flask_client import OAuth
import os

def create_app(test_config=None):
    # create and configure app
    app = Flask(__name__)
    app.config.from_object('config')
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
      nonce = os.urandom(16).hex()
      session['nonce'] = nonce
      return oauth.oidc.authorize_redirect('http://localhost:5000/callback', nonce=nonce)
    
    @app.route('/logout')
    def logout():
      session.clear()
      
      cognito_logout_url = 'https://127.0.0.1/logout' 
      cognito_logout_url += f'?client_id={app.config["CLIENT_ID"]}&logout_uri=http://localhost:5000/cognito-login'
    
      return redirect(cognito_logout_url)  
    
    @app.route('/callback')
    def callback():
        token = oauth.oidc.authorize_access_token()
        nonce = session.pop('nonce')
        user_info = oauth.oidc.parse_id_token(token, nonce=nonce) 
        session["user"] = user_info  
        return redirect("/")  

    return app