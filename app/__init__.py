import os
import pathlib

import requests
from flask import Flask, session, abort, redirect, request, render_template, url_for


from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow


from pip._vendor import cachecontrol
import google.auth.transport.requests

from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user



os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "549086998736-neu819sgnn6aiu1hm2j30ui72fa41s76.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


app = Flask(__name__)
app.secret_key = "SuperPower2022"

login_menager = LoginManager(app)

class User(UserMixin):
    def __init__(self, user_id, user_name):
        self.id = user_id
        self.name = user_name
        
        
@login_menager.user_loader
def load_user(user_id):
    return User(user_id=user_id, user_name=session.get('google_name', ''))

from app import routes

