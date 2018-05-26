from flask import Flask

from flask import jsonify
from flask import render_template , request, url_for
from flask import Flask
from flask import Flask, render_template, request , redirect,url_for
from sqlalchemy import create_engine
from flask import jsonify
import json
import datetime 
import sqlite3
import pandas as pd
import random
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)


db = sqlite3.connect('/Volumes/Disk 2/Users/arranhemish/sqlite/schedule.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Volumes/Disk 2/Users/arranhemish/sqlite/schedule.db'
db_session = SQLAlchemy(app)


class Event(db_session.Model):
    
    __tablename__ = 'appointments'
    id = db_session.Column(db_session.String(100), primary_key=True)
    title = db_session.Column(db_session.String(80), unique=True, nullable=False)
    email = db_session.Column(db_session.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '{} | {}  | {}'.format(self.id , self.title , self.email)

cursor = db.cursor()

def getAppoinments():
    
    df = pd.read_sql('SELECT * FROM appointments', db)
    
    appointmentsJson = df.to_json(orient='records')
    appointments = json.loads(appointmentsJson)
    
        
    for i in appointments:
        if i["className"] != None:
            i["className"] = i.get("className", "").split(" ")
        
           
    print(appointments)
    
   
    
    
    return appointments


    
    
def addPatient(aAppointment):
    
    dfRename = aAppointment.rename(index=str, columns={"title": "name", "description": "appointmentType"})
    
    patientDetails = dfRename[['id','name','appointmentType' , 'email' , 'phoneNumber', 'notes','start','end']]
    
    patientDetails.to_sql('patients', con=db, if_exists='append',index=False)
    print(patientDetails)



@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    query = db_session.session.query(Event.title).filter(Event.title.like('%' + str(search) + '%'))
    results = [mv[0] for mv in query.all()]
    return jsonify(matching_results=results)



@app.route('/getPatient', methods=['POST'])
def getPatient():
    
    patientDf = pd.read_sql('SELECT * FROM appointments where title = (?) ', db , params=(request.form["data"],))
    
    patientAppointmentJson = patientDf.to_json(orient='records')
    patientAppointment = json.loads(patientAppointmentJson)
    
    return jsonify(patientAppointment)


@app.route('/addAppointment', methods=['POST'])
def addAppointment():
    
    df = pd.DataFrame(json.loads(request.data),index=[0])
    
    df.to_sql('appointments', con=db, if_exists='append', index=False)
    
    addPatient(df)
    
    
    return ""
    


@app.route('/updateAppointment', methods=['POST'])
def updateAppointment():
    
    appointment = json.loads(request.data)
    
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
	
	return render_template('dashboard/pages/AJAX_Full_Version/calendar.html' , event=event)




@app.route('/todolist')
def todolist():

   
	
	return render_template('dashboard/pages/AJAX_Full_Version/todolist.html')


@app.route('/patientappointment')
def patientappointment():

   
	
	return render_template('dashboard/pages/AJAX_Full_Version/patientappointment.html')






if __name__ == "__main__":
    app.run("0.0.0.0")

