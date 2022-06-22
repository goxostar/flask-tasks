import json
from flask import Flask, g, redirect, render_template, flash, url_for
from flask_oidc import OpenIDConnect

app = Flask(__name__)

app.config.update({
    'SECRET_KEY': 'goktuggoktuggoktuggoktuggoktuggoktuggoktuggoktug',
    'TESTING': True,
    'DEBUG': True,
    'OIDC_CLIENT_SECRETS': 'client_secrets.json',
    'OIDC_ID_TOKEN_COOKIE_SECURE': False,
    'OIDC_REQUIRE_VERIFIED_EMAIL': False,
    'OIDC_VALID_ISSUERS': ['http://localhost:8080/auth/realms/demo-realm'],
    'OIDC_OPENID_REALM': 'http://localhost:5000/oidc_callback'
})
oidc = OpenIDConnect(app)


@app.route('/', methods=['GET','POST'])
def hello_world():
    if oidc.user_loggedin:
        return ('Hi, %s, <a href="/dashboard">See dashboard</a> '
                '<a href="/logout">Log out</a>') % \
            oidc.user_getfield('email')
    else:   
        return render_template('home.html')
        #return 'Welcome Newcomer, <a href="/dashboard">Log in</a>'


@app.route('/dashboard', methods=['GET','POST'])
@oidc.require_login
def dashboard():
    info = oidc.user_getinfo(['email', 'openid_id'])
    return ('Hello, your email is %s ! <a href="/">Go Back</a>' %
            (info.get('email')))


@app.route('/api', methods=['GET','POST'])
@oidc.accept_token(True, ['openid'])
def hello_api():
    return json.dumps({'hello': 'Welcome %s' % g.oidc_token_info['sub']})


@app.route('/logout', methods=['GET','POST'])
def logout():
    oidc.logout()
    return 'You have been logged out! <a href="/">Home</a>'


if __name__ == '__main__':
    app.run('localhost', port=5000)
