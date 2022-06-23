import json
import requests
from flask import Flask, g, redirect, render_template, flash, url_for, session
from flask_oidc import OpenIDConnect
from keycloak import KeycloakOpenID, KeycloakAdmin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


url = "http://localhost:8080/auth/realms/demo-realm/protocol/openid-connect/token"
 
header = {    
    "Content-Type":"application/x-www-form-urlencoded"    
    }
 
rr ="grant_type=client_credentials&client_id=client1&client_secret=f720daa4-059b-4ba6-b34d-e898fab1e6ae"
response = requests.post(url, data=rr, headers=header, verify=False)
 
print("Status Code", response.status_code)
print("JSON Response ", response.json())

class LoginForm(FlaskForm):
  username = StringField(validators=[InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

  password = PasswordField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

  submit = SubmitField('Login')

app.config.update({
    'SECRET_KEY': 'goktuggoktuggoktuggoktuggoktuggoktuggoktuggoktug',
    'TESTING': True,
    'DEBUG': True,    
})

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
          
        return render_template('login.html',form=form)

    return render_template('login.html',form=form)


if __name__ == '__main__':
    app.run('localhost', port=5000)
