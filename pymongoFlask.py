from time import strftime
from flask import Flask, jsonify
from flask_pymongo import PyMongo
import datetime
import ssl
from pprint import pprint

IST = datetime.timedelta(hours=5, minutes=30)

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://Sarthak:sarthak-1234@cluster0.ugso6.mongodb.net/test2?retryWrites=true&w=majority"
cluster = PyMongo(app, ssl_cert_reqs=ssl.CERT_NONE)
db = cluster.db
patients = db.Patients
reports = db.Reports

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
    data = patients.find_one_or_404({'_id':ID})['records']
    reportz = []
    for reportID in data:
        reportz.append(reports.find_one_or_404({'_id': reportID}))

    return reportz
    #    pprint(reports.find_one_or_404({'_id': reportID}))
    #    pprint(reports.find_one_or_404({'_id': reportID}, {'_id':0}))

def createPatient(_id, name, age, location, bloodGroup):
    # ID and Age must be INT32
    # Check for ID must not be already existing
    patients.insert_one({"_id": _id, "name": name, "age": age, "location": location, "bloodGroup": bloodGroup, "recordCount": 0})

def deleteReport(ID):
    pass

def deletePatient(_id):
    # Delete reports
    patients.delete_one({"_id":_id})

def main():
    xy = findPatient()
    print(xy['name'])

if __name__ == "__main__":
    #main()
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



'''
def getName(ID):
    vari = dict(findPatient(ID))
    name = vari['name']
    pprint(name)
'''