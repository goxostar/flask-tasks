import json
from os import access
import requests
from flask import Flask, g, redirect, render_template, flash, url_for, session
from flask_oidc import OpenIDConnect
from keycloak import KeycloakOpenID, KeycloakAdmin
from flask_wtf import FlaskForm
from sqlalchemy import null
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user

app = Flask(__name__)


# Login Request To Keycloak API - Response = Status, Access Token, Refresh Token
url = "http://localhost:8080/auth/realms/demo-realm/protocol/openid-connect/token" 
register_url = "http://localhost:8080/auth/admin/realms/demo-realm/users"
header = {    
    "Content-Type":"application/x-www-form-urlencoded"    
    }


# Login Form for User Input
class LoginForm(FlaskForm):
  username = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Username"})

  password = PasswordField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Password"})

  submit = SubmitField('Login')

# Register Form for User Input
class RegisterForm(FlaskForm):
  username = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Username"})
  firstName = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "First Name"})
  lastName = StringField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Last Name"})
  email = StringField(validators=[InputRequired(), Length(min=1, max=50)], render_kw={"placeholder": "Email"})
  password = PasswordField(validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Password"})

  submit = SubmitField('Register')

# Logout Form 
class LogoutForm(FlaskForm):  

  submit = SubmitField('Logout')

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

    form3 = LogoutForm()

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


@app.route('/register', methods=['GET','POST'])
def register(): 

    #Check if user already logged in?
    with open('access_token.json', 'r') as f:
        access_token_from_json = json.load(f)

    if access_token_from_json['access_token']:
            return redirect(url_for('dashboard'))

    form2 = RegisterForm()

    if form2.validate_on_submit():       

        # Getting Admin Access Code for User Creation
        rr = f"client_id=admin-cli&grant_type=client_credentials&client_secret=bb00d3d2-6aed-4de6-87b5-0f0c68475eba"
        response = requests.post(url, data=rr, headers=header, verify=False)
        admin_access_token = response.json()['access_token']   

        header_register = {    
        "Content-Type":"application/json",
        "Authorization": f"Bearer {admin_access_token}"    
        }


        register_data = {
            "enabled": True,
            "username": "{}".format(form2.username.data),
            "firstName": "{}".format(form2.firstName.data),
            "lastName": "{}".format(form2.lastName.data),
            "email": "{}".format(form2.email.data),
            "credentials": [
                {
                    "type": "password",
                    "value": "{}".format(form2.password.data),
                    "temporary": False
                }
            ],
            "groups": []
        }

        response_register = requests.post(register_url, headers=header_register, json=register_data, verify=False)
        return redirect(url_for('login'))   
        

    return render_template('register.html', form2=form2)


@app.route('/logout', methods=['GET','POST'])
def logout(): 

    with open('access_token.json', 'r') as f:
        access_token_from_json = json.load(f)

    if access_token_from_json['access_token']:
        dictionary ={
            "access_token" : ""
            }
        json_object = json.dumps(dictionary, indent = 1)
        with open("access_token.json", "w") as outfile:
            outfile.write(json_object)
        return redirect(url_for('index')) 


    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run('localhost', port=5000)
