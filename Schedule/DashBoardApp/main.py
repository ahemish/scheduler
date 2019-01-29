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

db = SQLAlchemy(app)
from models import *



def getAppoinments():
    
    all_appointments = [{
        "id" : i[0].id,
        "start" : i[0].start,
        "end" : i[0].end,
        "allDay" : i[0].all_day,
        "className" : i[0].appointment_colour,
        "patient_id" : i[0].patient_id,
        "appointment_type" : i[0].appointment_type,
        "cancelled" : i[0].canceled,
        "title" : i[1].name,
        "email" : i[1].email,
        "phoneNumber" : i[1].phone_number,
        "notes" : i[1].notes
    } for i in db.session.query(Appointment,Patient).join(Patient, Appointment.patient_id == Patient.id).all()]

    return all_appointments


@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    query = db.session.query(Patient.name).filter(Patient.name.like('%' + str(search) + '%'))
    results = [p[0] for p in query.all()]
    return jsonify(matching_results=results)



@app.route('/getPatient', methods=['POST'])
def getPatient():

    patient_name = request.form["data"]
    patient_appointment = [{
        "id" : i.id,
        "title" : i.name,
        "email" : i.email,
        "phoneNumber" : i.phone_number,
        "notes" : i.notes
    } for i in Patient.query.filter_by(name=patient_name).all()]
    return jsonify(patient_appointment)


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
    
    #Does Patient already exist add if not
    patient_id = db.session.query(Patient.id).filter_by(name=patient_name).scalar()
    if patient_id is  None:
        new_patient = Patient(name=patient_name,email=patient_email,phone_number=patient_phone_number,notes=patient_notes)
        db.session.add(new_patient)
        db.session.commit()
        patient_id = new_patient.id #Patient.query.filter_by(name=patient_name).first().id

    new_appointment = Appointment(
        start =start ,
        end =end ,
        all_day =all_day ,
        appointment_colour =appointment_colour ,
        patient_id =patient_id ,
        appointment_type=appointment_type,
        canceled =canceled
    )
    db.session.add(new_appointment)
    db.session.commit()

    return jsonify({'id' : new_appointment.id})
    


@app.route('/updateAppointment', methods=['POST'])
def updateAppointment():
    
    data = json.loads(request.data)
    appointment_id = data['id']
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

    appointment = Appointment.query.filter_by(id=appointment_id).first()
    appointment.start = start
    appointment.end = end
    appointment.all_day = all_day
    appointment.appointment_colour = appointment_colour
    appointment.appointment_type = appointment_type
    appointment.canceled = canceled
    
    patient = Patient.query.filter_by(id=appointment.patient_id).first()
    patient.name = patient_name
    patient.email = patient_email
    patient.phone_number = patient_phone_number
    patient.notes = patient_notes
    db.session.commit()
    return jsonify({'status' : 'Success' })

    

@app.route('/deleteAppointment', methods=['POST'])
def deleteAppointment():
    data = json.loads(request.data)
    id = data["id"] 
    appointment = Appointment.query.filter_by(id=id).delete()
    db.session.commit()

    return jsonify({'status' : 'Success'})

@app.route('/')
def homepage():

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
	return render_template('dashboard/pages/AJAX_Full_Version/calendar.html' , event=event)




@app.route('/todolist')
def todolist():

   
	
	return render_template('dashboard/pages/AJAX_Full_Version/todolist.html')


@app.route('/patientappointment')
def patientappointment():

   
	
	return render_template('dashboard/pages/AJAX_Full_Version/patientappointment.html')






if __name__ == "__main__":
    app.run("0.0.0.0",debug=True)

