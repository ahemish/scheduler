from flask import Flask, jsonify, render_template, request, url_for,redirect
from sqlalchemy import create_engine
import json
import datetime
import sqlite3
import pandas as pd
import random
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_pyfile('config.cfg')


db = sqlite3.connect('sqlite/schedule.db')
db_session = SQLAlchemy(app)
from models import *


cursor = db.cursor()

def getAppoinments():
    
    df = pd.read_sql('SELECT * FROM appointments', db)
    appointmentsJson = df.to_json(orient='records')
    appointments = json.loads(appointmentsJson)
    

    for i in appointments:
        if i["appointment_colour"] != None:
            i["appointment_colour"] = i.get("appointment_colour", "").split(" ")
    return appointments


    
    



@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    #query = db_session.session.query(Appointment.title).filter(Appointment.title.like('%' + str(search) + '%'))
    #results = [p[0] for p in query.all()]
    return jsonify({'d':'d'})#jsonify(matching_results=results)



@app.route('/getPatient', methods=['POST'])
def getPatient():
    
    patientDf = pd.read_sql('SELECT * FROM appointments where title = (?) ', db , params=(request.form["data"],))
    
    patientAppointmentJson = patientDf.to_json(orient='records')
    patientAppointment = json.loads(patientAppointmentJson)
    
    return jsonify(patientAppointment)


@app.route('/addAppointment', methods=['POST'])
def addAppointment():
    data=json.loads(request.data)
    patient_name=data['patientName']
    patient_phone_number=data['phoneNumber']
    patient_notes=data['notes']
    start=data['start']
    end=data['end']
    all_day=data['allDay']
    appointment_colour=data['appointmentColour']
    patient_email=data['email']
    appointment_type=data['appointmentType']
    canceled=data['canceled']
    
    #Does Patient already exist
    patient_id = db_session.session.query(Patient.id).filter_by(name=patient_name).scalar()
    if patient_id is  None:
        new_patient = Patient(name=patient_name,email=patient_email,phone_number=patient_phone_number,notes=patient_notes)
        db_session.session.add(new_patient)
        db_session.session.commit()
        patient_id = Patient.query.filter_by(name=patient_name).first().id

    new_appointment = Appointment(
        start =start ,
        end =end ,
        all_day =all_day ,
        appointment_colour =appointment_colour ,
        patient_id =patient_id ,
        appointment_type=appointment_type,
        canceled =canceled
    )
    db_session.session.add(new_appointment)
    db_session.session.commit()

        
    
    return ""
    


@app.route('/updateAppointment', methods=['POST'])
def updateAppointment():
    
    appointment = json.loads(request.data)
    appointments = db_session.session.query(Appointment,Patient).join(Appointment.patient_id == Patient.id ).all()

    #appointment['className'] = "".join(appointment.get("className"))
    cursor.execute(''' DELETE FROM appointments WHERE id = ? and title = ? ''',(appointment.get("id"), appointment.get("oldTitle", appointment.get("title"))))
    db.commit()
    df = pd.DataFrame(appointment,index=[0])
    if(appointment.get("oldTitle") != None):
        
        df = df.drop(["oldTitle"],axis=1)
    df.to_sql('appointments', con=db, if_exists='append', index=False)
    
    
    
    
    return ""

    

@app.route('/deleteAppointment', methods=['POST'])
def deleteAppointment():
    req = json.loads(request.data)
    cursor.execute(''' DELETE FROM appointments WHERE id = ? and title = ? ''',(req.get("id"), req.get("title")))
    db.commit()
    
    print(req.get("id"), req.get("title"))
    return ""

@app.route('/')
def homepage():

    #cursor.execute('select name from photos where tag like "" ')
    #results = cursor.fetchall()
    return render_template('dashboard/pages/AJAX_Full_Version/index.html')

	
@app.route('/dashboard')
def dashboard():

	render_template('dashboard/pages/AJAX_Full_Version/dashboard.html')
	
@app.route('/login')
def login():
    
    return render_template('dashboard/pages/AJAX_Full_Version/login.html')

@app.route('/overview')
def overview():
    
    return render_template('dashboard/pages/AJAX_Full_Version/overview.html')

	
	

@app.route('/calendar')
def calendar():

    
	event= getAppoinments()
	print(event)
	return render_template('dashboard/pages/AJAX_Full_Version/calendar.html' , event=event)




@app.route('/todolist')
def todolist():

   
	
	return render_template('dashboard/pages/AJAX_Full_Version/todolist.html')


@app.route('/patientappointment')
def patientappointment():

   
	
	return render_template('dashboard/pages/AJAX_Full_Version/patientappointment.html')






if __name__ == "__main__":
    app.run("0.0.0.0")

