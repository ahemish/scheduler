from flask import Flask, jsonify, render_template, request, url_for,redirect,session,flash
from sqlalchemy import create_engine
import json
import datetime
from datetime import timedelta
import sqlite3
import flask_login
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from gcal import gcal_events,gcal_delete_event,gcal_add_event
import os


app = Flask(__name__)
app.config.from_pyfile('config.cfg')
app.secret_key = 'super secret string'  # Change this!
cred_file_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','..', 'credentials.json'))

db = SQLAlchemy(app)
from models import *

#flask_login setup
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.needs_refresh_message_category = "info"

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))

#Set session length
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)


def getAppoinments():
    
    all_appointments = [{
        "id" : i[0].id,
        "start" : i[0].start,
        "end" : i[0].end,
        "allDay" : i[0].all_day,
        "className" : i[0].appointment_colour,
        "patient_id" : i[0].patient_id,
        "appointmentType" : i[0].appointment_type,
        "canceled" : i[0].canceled,
        "gcalId": i[0].gcal_id,
        "title" : i[1].name,
        "email" : i[1].email,
        "phoneNumber" : i[1].phone_number,
        "dob" : i[1].dob,
        "notes" : i[1].notes,
        "addressLine" : i[1].address_line,
        "city" : i[1].city,
        "county" : i[1].county,
        "postCode" : i[1].post_code,
        "howDidYouHearAboutUs" : i[1].how_did_you_hear_about_us
    } for i in db.session.query(Appointment,Patient).join(Patient, Appointment.patient_id == Patient.id).all()]

    return all_appointments

def get_evnet_ids():
    return[i.gcal_id for i in db.session.query(Appointment).all()]

def get_patients_name():
    return [i.name for i in db.session.query(Patient).all()]

def patient(patient_name):
    patient_appointment = [{
        "id" : i.id,
        "title" : i.name,
        "email" : i.email,
        "phoneNumber" : i.phone_number,
        "dob" : i.dob,
        "notes" : i.notes,
        "addressLine" : i.address_line,
        "city" : i.city,
        "county" : i.county,
        "postCode" : i.post_code,
        "howDidYouHearAboutUs" : i.how_did_you_hear_about_us
    } for i in Patient.query.filter_by(name=patient_name).all()]
    return patient_appointment

def totalPatientsSeen():
    date = datetime.datetime.now()
    month = date.strftime('%m')
    year = date.strftime('%Y')
    patients_seen_month = db.engine.execute("select count(id) from appointments where strftime('%m', start) = '" + str(month) + "'")
    patients_seen_year = db.engine.execute("select count(id) from appointments where strftime('%Y', start) = '" + str(year) + "'")
    return {"month" : [i[0] for i in patients_seen_month][0],
            "year"  : [i[0] for i in patients_seen_year][0]
            }



@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    query = db.session.query(Patient.name).filter(Patient.name.like('%' + str(search) + '%'))
    results = [p[0] for p in query.all()]
    if len(results) == 0:
        return jsonify(matching_results=['No Results'])
    return jsonify(matching_results=results)



@app.route('/getPatient', methods=['POST'])
def getPatient():
    patient_name = request.form["data"]
    return jsonify(patient(name))


@app.route('/addAppointment', methods=['POST'])
def addAppointment():
    data=json.loads(request.data)
    patient_name=data['patientName']
    patient_phone_number=data['phoneNumber']
    patient_dob =data['dob']
    patient_notes=data['notes']
    start=data['start']
    end=data['end']
    all_day=data['allDay']
    appointment_colour=data['appointmentColour']
    patient_email=data['email']
    appointment_type=data['appointmentType']
    canceled=data['canceled']
    address_line = data['addressLine']
    city = data['city']
    county = data['county']
    post_code = data['postCode']
    how_did_you_hear_about_us =data['howDidYouHearAboutUs']
    
    #Does Patient already exist add if not
    patient_id = db.session.query(Patient.id).filter_by(name=patient_name).scalar()
    if patient_id is  None:
        new_patient = Patient(name=patient_name,
        email=patient_email,
        phone_number=patient_phone_number,
        dob=patient_dob,
        notes=patient_notes,
        address_line=address_line,
        city=city,
        county=county,
        post_code=post_code,
        how_did_you_hear_about_us=how_did_you_hear_about_us)

        db.session.add(new_patient)
        db.session.commit()
        patient_id = new_patient.id
    gcal_event_id = gcal_add_event(patient_name,start,end,cred_file_path)
    new_appointment = Appointment(
        start =start ,
        end =end ,
        all_day =all_day ,
        appointment_colour =appointment_colour ,
        patient_id =patient_id ,
        appointment_type=appointment_type,
        canceled =canceled,
        gcal_id=gcal_event_id
    )
    db.session.add(new_appointment)
    db.session.commit()

    return jsonify({'id' : new_appointment.id , 'gcalId': gcal_event_id})
    


@app.route('/updateAppointment', methods=['POST'])
def updateAppointment():
    
    data = json.loads(request.data)
    appointment_id = data['id']
    patient_name=data['patientName']
    patient_phone_number=data['phoneNumber']
    patient_dob=data['dob']
    patient_notes=data['notes']
    start=data['start']
    end=data['end']
    all_day=data['allDay']
    appointment_colour=data['appointmentColour']
    patient_email=data['email']
    how_did_you_hear_about_us=data["howDidYouHearAboutUs"]
    appointment_type=data['appointmentType']
    canceled=data['canceled']
    address_line = data['addressLine']
    city = data['city']
    county = data['county']
    post_code = data['postCode']

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
    patient.dob = patient_dob
    patient.notes = patient_notes
    patient.address_line=address_line
    patient.city=city
    patient.county=county
    patient.post_code=post_code
    patient.how_did_you_hear_about_us = how_did_you_hear_about_us
    db.session.commit()
    return jsonify({'status' : 'Success' })

    

@app.route('/deleteAppointment', methods=['POST'])
def deleteAppointment():
    data = json.loads(request.data)
    print(data)
    if data.get('gcal'):
        print(gcal_delete_event(data['id'],cred_file_path))
    else:
        id = data["id"]
        if data.get('gcalId'):
            gcal_delete_event(data['gcalId'],cred_file_path)
        appointment = Appointment.query.filter_by(id=id).delete()
        db.session.commit()

    return jsonify({'status' : 'Success'})

@app.route('/')
@flask_login.login_required
def homepage():

    return render_template('dashboard/pages/AJAX_Full_Version/index.html')

	
@app.route('/dashboard')
@flask_login.login_required
def dashboard():

	render_template('dashboard/pages/AJAX_Full_Version/dashboard.html')
	
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('dashboard/pages/AJAX_Full_Version/login.html')
    
    email = request.form['email']
    password= request.form['password']
    registered_user = User.query.filter_by(email_address=email).first()
    if registered_user is None:
            flash('Username or Password is invalid' , 'error')
            return redirect(url_for('login'))
    if check_password_hash(registered_user.password, password) == True:
        flask_login.login_user(registered_user)
        flash('Logged in successfully')
        session['fullName'] = registered_user.full_name
        print(session['fullName'])
        return redirect(url_for('homepage'))
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))

@app.route('/overview')
def overview():
    
    return render_template('dashboard/pages/AJAX_Full_Version/overview.html')

	
	

@app.route('/calendar')
@flask_login.login_required
def calendar():
    patients_seen = totalPatientsSeen()
    event= getAppoinments()
    patients = get_patients_name()
    event_ids = get_evnet_ids()
    days = {'SU' : 0 ,'MO' : 1, 'TU' : 2 , 'WE' : 3, 'TH' : 4 , 'FR' : 5, 'SA' : 6}
    gcal = []
    for i in gcal_events(cred_file_path):
        appointment = {
            'id' : i['id'], 
            'title' : i['summary'] + ' (gcal)' ,
            'start': i['start']['dateTime'] ,
            'end' : i['end']['dateTime'],
            "className" : 'bg-color-blueLight txt-color-white',
            'gcal' : True}
        if i['id'] not in event_ids:
            for name in patients:
                if name.lower() in i['summary'].lower():
                    appointment.update(patient(name)[0])
                if i.get('recurrence'):
                    recurrence_days = i['recurrence'][0].split(';')[-1].split('=')[-1].split(',')
                    recurrence_days = [days[i] for i in recurrence_days]
                    appointment['start']=i['start']['dateTime'].split('T')[-1].split('+')[0] ,
                    appointment['end']=i['end']['dateTime'].split('T')[-1].split('+')[0],
                    appointment['dow']=recurrence_days
        gcal.append(appointment)

    # gcal = [{
    #     'id' : i['id'], 
    #     'title' : i['summary'] + ' (gcal)' ,
    #     'start': i['start']['dateTime'] ,
    #     'end' : i['end']['dateTime'],
    #     "className" : 'bg-color-blueLight txt-color-white',
    #     'gcal' : True}
    #     for i in gcal_events(cred_file_path) if i['id'] not in event_ids]
    events = event + gcal
    return render_template('dashboard/pages/AJAX_Full_Version/calendar.html' , event=events, monthPatientsSeen=patients_seen['month'] ,yearPatientsSeen=patients_seen['year'])




@app.route('/todolist')
@flask_login.login_required
def todolist():
	return render_template('dashboard/pages/AJAX_Full_Version/todolist.html')


@app.route('/patientappointment')
@flask_login.login_required
def patientappointment():
	return render_template('dashboard/pages/AJAX_Full_Version/patientappointment.html')






if __name__ == "__main__":
    app.run("0.0.0.0",debug=True)

