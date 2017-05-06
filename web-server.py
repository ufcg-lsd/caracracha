import json
import requests
import sched, time
from flask import Flask, flash, request, render_template, session
from wtforms import Form, BooleanField, StringField, PasswordField, validators

app = Flask(__name__)
app.secret_key = "super secret key"
s_macs = sched.scheduler(time.time, time.sleep)
previousMacs = []

class RegistrationForm(Form):
    name = StringField('Name', [validators.Length(min=4, max=25)])
    mac = StringField('MAC Address', [validators.Length(min=17, max=17)])

@app.route('/openconnection', methods=['GET', 'POST'])
def openconnection():
    r = requests.get('http://10.30.100.69:5001')
    return str(r.status_code)

@app.route('/jquery-3.2.1.js', methods=['GET'])
def jquery():
    return open('templates/jquery-3.2.1.js').read()

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        form = RegistrationForm(request.form)
        form.msg = ''
        with open('macs.json') as f:
            registered_macs = json.load(f)
        
        if request.method == 'POST' and form.validate():
            registered_macs[form.mac.data] = form.name.data
            with open('macs.json', 'w') as f:
                f.write(json.dumps(registered_macs))
            form.msg = 'Thanks for registering :)'
        
        #TODO: make API request to present only the present users.
        form.users = []
        for mac in previousMacs:
            form.users.append(registered_macs[mac])

        return render_template('index.html', form=form)
    except Exception as e:
        print(e)

def update_users():
    r = requests.get("http://150.165.85.12:41205/get_number_of_macs?identifier=LSD&m=2")
    macs = json.loads(r.text)["Macs"]
    currentMacs = []
    for mac in macs:
        if mac not in previousMacs:
            currentMacs.append(mac)
    previousMacs = currentMacs
    s_macs.enter(60, 1, update_users, (s_macs,))

if __name__ == '__main__':
    #TODO: create assynchronous function to monitor when a new user appears
   
    app.debug = True
    app.run("0.0.0.0", 80)
    s_macs.enter(60, 1, update_users, (s_macs,))
    s_macs.run()
 
