# from cProfile import Profile
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
    id = int(id)

    if (request.method=='POST'):
        add_record(id)

    try:
        profile = pymongoFlask.patient(id)
    except:
        print("Couldn't find patient")
        return render_template('404.html', ID=id)
    print("Rendering Template")
    return render_template('pprofile.html', profile = profile)
    
def add_record(id):
    print("Inside add_record() function")
    rec = pymongoFlask.addRecord(ID=id, hospital=request.form['hospitalName'], category=request.form['category'], description=request.form['description'], drID=request.form['drID'])
    print("New record added!")
    print(rec)
    pass

if __name__ == '__main__':
    app.run(debug=True)
