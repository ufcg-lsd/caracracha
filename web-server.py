import json
from flask import Flask, flash, request, render_template, session
from wtforms import Form, BooleanField, StringField, PasswordField, validators

app = Flask(__name__)
app.secret_key = "super secret key"

class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    mac = StringField('MAC Address', [validators.Length(min=17, max=17)])

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        form = RegistrationForm(request.form)
        form.msg = ''
        with open('users.json') as f:
            registered_users = json.load(f)
        
        if request.method == 'POST' and form.validate():
            registered_users[form.name.data] = form.mac.data
            with open('users.json', 'w') as f:
                f.write(json.dumps(registered_users))
            form.msg = 'Thanks for registering :)'
        
        form.users = []
        for user in registered_users:
            form.users.append(user)

        return render_template('index.html', form=form)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    app.debug = True
    app.run("0.0.0.0", 80)
