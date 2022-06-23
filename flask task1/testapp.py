import json
from flask import Flask, g, redirect, render_template, flash, url_for
from flask_oidc import OpenIDConnect
from keycloak import KeycloakOpenID, KeycloakAdmin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

app = Flask(__name__)

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
