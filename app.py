# from re import DEBUG
from flask import Flask, render_template, request
import pymongoFlask

app = Flask(__name__)

@app.route('/',methods=['POST','GET'])
def index():

    if request.method == 'POST':
        # pass
        try:
            inputID = int(request.form['loginID'])
            try:
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
                
                return render_template('profile.html', ID=inputID, age=profile['age'], name=profile['name'], location=profile['location'], 
                                                        bloodGroup=profile['bloodGroup'], recordCount=profile['recordCount'],
                                                        firstName=firstName, lastName=lastName, records=records)

            except:
                return render_template('404.html', ID=inputID)
                # return("Somewhere, something went wrong.")
        except(ValueError):
            return render_template('404value.html')
    else:
        return render_template ('index.html')

if __name__ == '__main__':
    app.run(debug=True)
