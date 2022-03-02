from time import strftime
from flask import Flask, jsonify
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

def addNewRecord(ID, hospital, category, description, currentTime = datetime.datetime.now()):
    # Inserting New Record
    # currentTime = datetime.datetime.now()
    newRecord = reports.insert_one({'hospitalName': hospital, 'category': category, 'description': description, 'date': currentTime})
    patients.update_one({'_id': ID}, {'$inc': {'recordCount': 1}, '$push': {'records': newRecord.inserted_id}}, upsert=True)
    # Time from created object
    # currentTime = newRecord['_id'].generation_time + IST
    return newRecord.inserted_id

def findReports(ID):
    data = patients.find_one_or_404({'_id':ID})['records']  #array
    reportz = []
    for reportID in data:
        reportz.append(reports.find_one_or_404({'_id': reportID}))
    for i in reportz:
        drName = getDrName(i['drID'])
        i['drName']=drName
        #i.append({'dName':dName})
        pass
        
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

def deleteReport(ID):
    pass

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



def main():
    #pprint(findReports(882))
    print("hellooooo")
    # xy = findPatient()
    # print(xy['name'])
    pprint(patientsByDR("DR001"))

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