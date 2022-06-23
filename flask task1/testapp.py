import json
from os import access
import requests
from flask import Flask, g, redirect, render_template, flash, url_for, session
from flask_oidc import OpenIDConnect
from keycloak import KeycloakOpenID, KeycloakAdmin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user

app = Flask(__name__)


# Login Request To Keycloak API - Response = Status, Access Token, Refresh Token
url = "http://localhost:8080/auth/realms/demo-realm/protocol/openid-connect/token" 
header = {    
    "Content-Type":"application/x-www-form-urlencoded"    
    }


# Login Form for User Input
class LoginForm(FlaskForm):
  username = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Username"})

  password = PasswordField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Password"})

  submit = SubmitField('Login')

app.config.update({
    'SECRET_KEY': 'goktuggoktuggoktuggoktuggoktuggoktuggoktuggoktug',
    'TESTING': True,
    'DEBUG': True,    
})

@app.route('/login', methods=['GET','POST'])
def login():

    # Access Code Variable for Authorization
    # Check if user already logged in? 
    with open('access_token.json', 'r') as f:
        access_token_from_json = json.load(f)

    if access_token_from_json['access_token']:
            return redirect(url_for('dashboard'))

    form = LoginForm()

    if form.validate_on_submit():        
            
        # Login Request with User Input
        username=form.username.data
        password=form.password.data
        rr = f"client_id=client1&username={username}&password={password}&grant_type=password&client_secret=f720daa4-059b-4ba6-b34d-e898fab1e6ae"
        response = requests.post(url, data=rr, headers=header, verify=False)
        #print("Status Code", response.status_code)
        #print("JSON Response ", response.json())

        # if status 200 (OK) -> write access token and login
        if response.status_code == 200:
            access_token = response.json()['access_token']
            dictionary ={
            "access_token" : access_token
            }
            json_object = json.dumps(dictionary, indent = 1)
            with open("access_token.json", "w") as outfile:
                outfile.write(json_object)
            return redirect(url_for('dashboard'))               
                 

    return render_template('login.html',form=form)

@app.route('/dashboard', methods=['GET','POST'])
def dashboard(): 

    # Access Code Variable for Authorization
    # Check if user logged in? or deny and direct to login page
    with open('access_token.json', 'r') as f:
        access_token_from_json = json.load(f)

    if access_token_from_json['access_token']:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))


@app.route('/', methods=['GET','POST'])
def index(): 

    return render_template('index.html')


if __name__ == '__main__':
    app.run('localhost', port=5000)
