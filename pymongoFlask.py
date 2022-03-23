from time import strftime
from flask import Flask, jsonify, abort
from flask_pymongo import PyMongo
import datetime
import ssl
from pprint import pprint

IST = datetime.timedelta(hours=5, minutes=30)

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://Sarthak:sarthak-1234@cluster0.ugso6.mongodb.net/test2"
cluster = PyMongo(app, ssl_cert_reqs=ssl.CERT_NONE)
db = cluster.db
patients = db.Patients
reports = db.Reports
doctors = db.Doctors

## 

def findAllPatients():
    for patient in patients.find():
        pprint(patient)

def findPatient(ID):
    patient = patients.find_one_or_404({'_id':ID})
    return patient

def addRecord(ID, hospital, category, description, drID, currentTime = datetime.datetime.now()):
    # Inserting New Record
    # currentTime = datetime.datetime.now()
    newRecord = reports.insert_one({'hospitalName': hospital, 'category': category, 'description': description, 'drID': drID, 'date': currentTime})
    patients.update_one({'_id': ID}, {'$inc': {'recordCount': 1}, '$push': {'records': newRecord.inserted_id}}, upsert=True)
    # Time from created object
    # currentTime = newRecord['_id'].generation_time + IST
    return newRecord.inserted_id

def findReports(ID):
    recData = patients.find_one_or_404({'_id':ID})['records']  #array
    reportz = []
    for reportID in recData:
        reportz.append(reports.find_one_or_404({'_id': reportID}))
    for i in reportz:
        drName = getDrName(i['drID'])
        i['drName']=drName
        
    #print(type(reportz))
    return reportz
    #    pprint(reports.find_one_or_404({'_id': reportID}))
    #    pprint(reports.find_one_or_404({'_id': reportID}, {'_id':0}))

def getDrName(_id):
    try:
        return doctors.find_one({"_id":_id})["name"]
    except:
        #print(_id)
        return "Couldn't find"

def createPatient(_id, name, age, location, bloodGroup):
    # ID and Age must be INT32
    # Check for ID must not be already existing
    patients.insert_one({"_id": _id, "name": name, "age": age, "location": location, "bloodGroup": bloodGroup, "recordCount": 0})


def deletePatient(_id):
    # Delete reports
    patients.delete_one({"_id":_id})

def patientsByDR(_id):
    
    #drReports = []
    drReports = reports.find({"drID": _id})
    patientss = []
    for report in drReports:
        #pprint(report)
        rID = report['_id']
        #pprint(patients.find_one({"records": rID}))
        p = patients.find_one({"records": rID})
        patientss.append(dict([ ('_id', p['_id']), ('name', p['name']), ('date', report['date']) ]))
        #patientss.append((patients.find_one({"records": rID})['_id']))
    
    return(patientss)

def patient(_id):
    profile = dict()
    #ID, Name, Age, BloodGroup, Location, RecordCount, firstName, lastName, Records
    profile['id'] = _id
    try:
        # print("Finding patient...")
        p = findPatient(_id)
        print("Found patient")
        profile['age'] = p['age']
        # print("Age")
        profile['recordCount'] = p['recordCount']
        profile['location'] = p['location']
        profile['bloodGroup'] = p['bloodGroup']
        profile['name'] = profile['firstName'] = p['name']
        profile['lastName'] = ""
        if ' ' in profile['name']:
            profile['firstName'], profile['lastName'] = p['name'].split(None, 1)
        
        # print("Assigned variables to p")

        try:
            print("Looking for reports..")
            profile['records'] = findReports(_id)
        except:
            profile['records'] = ""

        print("Returning Patient")
        # pprint(profile)
        return(profile)
    except:
        print("EXCEPTION 404")
        abort(404)

def doctor(_id):
    profile = dict()
    profile['id'] = _id
    try:
        print("Searching Doctor ID")
        profile['name'] = getDrName(_id)
        try:
            profile['patients'] = patientsByDR(_id)
        except:
            print("Couldn't find patients")
            profile['patients'] = ""
        
        print("Found doctor")
        # pprint(profile)
        return (profile)
    except:
        print("ABORTING")
        abort(404)

# <td> <a href="{{url_for('index', id= pat['_id'])}}"> {{pat['_id']}}</td>


# profile = pymongoFlask.findPatient(inputID)
# # print(profile)
# firstName = profile['name']
# lastName = ""
# if ' ' in profile['name']:
#     firstName, lastName = profile['name'].split(None, 1)

# try:                
#     records = pymongoFlask.findReports(inputID)            
# except:
#     records = ""
# print("Found patient")
# return render_template('profile.html', ID=inputID, age=profile['age'], name=profile['name'], location=profile['location'], 
#                                         bloodGroup=profile['bloodGroup'], recordCount=profile['recordCount'],
#                                         firstName=firstName, lastName=lastName, records=records)


def main():
    #pprint(findReports(882))
    print("hellooooo")
    # xy = findPatient()
    # print(xy['name'])
    pprint(patient(882))
    # pprint(patientsByDR("DR001"))

if __name__ == "__main__":
    main()
    pass

##
## JUST USE strftime('%Y/%m/%d %I:%M:%S %p')
##

def dDate(dtime):
    return str(dtime.date())
def dTime(dtime):
    return str(dtime.time())


def dtime():
    strftime('%Y-%m-%d')


def getName(ID):
    vari = dict(findPatient(ID))
    name = vari['name']
    pprint(name)