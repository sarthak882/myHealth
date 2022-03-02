# from re import DEBUG
from flask import Flask, render_template, request
import pymongoFlask

app = Flask(__name__)

@app.route('/drlogin',methods=['POST','GET'])
def dr_login():
    print("Inside dr_login()")
    if request.method == 'POST':
        print("Inside dr POST")
        # do stuff when the form is submitted
        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        try:
            print("Taking input")
            #inputID = request.args.get('loginID')
            inputID = request.form['loginID']
            print(inputID)
            try:
                print("Searching Doctor ID")
                name = pymongoFlask.getDrName(inputID)
                # print(profile)
                try:                
                    patients = pymongoFlask.patientsByDR(inputID)            
                except:
                    print("Couldn't find patients")
                    patients = ""
                
                print("Rendering doctor page")
                #return ("Doctor is here"+name)
                return render_template('drprofile.html', ID=inputID, name=name, patients=patients)

            except:
                print("Couldn't find Dr")
                return render_template('404.html', ID=inputID)
                # return("Somewhere, something went wrong.")
        except(ValueError):
            print("DR Value error")
            return render_template('404value.html')

    # show the form, it wasn't submitted
    else:
        print("Rendering Doctor Login")
        return render_template('drlogin.html')

@app.route('/',methods=['POST','GET'])
def index():
    print("Inside index")
    if request.method == 'POST':
        print("Inside index POST")
        # pass
        try:
            inputID = int(request.form['loginID'])
            try:
                print("Searching for patient")
                profile = pymongoFlask.findPatient(inputID)
                # print(profile)
                firstName = profile['name']
                lastName = ""
                if ' ' in profile['name']:
                    firstName, lastName = profile['name'].split(None, 1)

                try:                
                    records = pymongoFlask.findReports(inputID)            
                except:
                    records = ""
                print("Found patient")
                return render_template('profile.html', ID=inputID, age=profile['age'], name=profile['name'], location=profile['location'], 
                                                        bloodGroup=profile['bloodGroup'], recordCount=profile['recordCount'],
                                                        firstName=firstName, lastName=lastName, records=records)

            except:
                print("Couldn't find patient")
                return render_template('404.html', ID=inputID)
                # return("Somewhere, something went wrong.")
        except(ValueError):
            print("INDEX Value error")
            return render_template('404value.html')
    else:
        print("Rendering Index login")
        return render_template ('index.html')


if __name__ == '__main__':
    app.run(debug=True)
