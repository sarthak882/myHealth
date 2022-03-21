# from cProfile import Profile
from email import message
import pprint
from flask import Flask, render_template, jsonify, request
import pymongoFlask

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def index():
    print("In index")
    if request.method == 'POST':
        print("In index POST")
        try:
            inputID = int(request.form['loginID'])
            try:                
                profile = pymongoFlask.patient(inputID)
                return render_template('profile.html', profile = profile)
            except:
                print("Couldn't find patient")
                return render_template('404.html', ID=inputID)
        except(ValueError):
            print("INDEX Value error")
            return render_template('404value.html')
    else:
        print("Rendering Index login")
        return render_template ('index.html')

@app.route('/drlogin',methods=['POST','GET'])
def dr_login():
    print("In dr_login()")
    if request.method == 'POST':
        print("In doctor POST")
        try:
            print("Taking input")
            inputID = request.form['loginID']
            print(inputID)
            try:
                profile = pymongoFlask.doctor(inputID)
                # pprint(profile)
                print("Rendering Template")
                return render_template('drprofile.html', profile = profile)  
            except:
                print("Couldn't find Dr")
                return render_template('404.html', ID=inputID)
        except(ValueError):
            print("DR Value error")
            return render_template('404value.html')
    else:
        print("Rendering Doctor Login")
        return render_template('drlogin.html')

@app.route('/pprofile',methods=['POST','GET'])
def pprofile():
    id = request.args['id']
    print(id)
    print(type(id))
    intID =int(id)
    try:
        profile = pymongoFlask.patient(intID)
    except:
        print("Couldn't find patient")
        return render_template('404.html', ID=id)
    print(type(profile))
    print("Rendering Template")
    return render_template('profile.html', profile = profile)

if __name__ == '__main__':
    app.run(debug=True)
