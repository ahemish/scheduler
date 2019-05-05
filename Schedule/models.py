from main import db
from flask_login import UserMixin
class Appointment(db.Model ,UserMixin):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String(255))
    end = db.Column(db.String(255))
    all_day = db.Column(db.Boolean(255))
    appointment_colour = db.Column(db.String(255),nullable=False)
    patient_id = db.Column(db.String(255))
    appointment_type = db.Column(db.String(255))
    canceled = db.Column(db.Boolean(255))
    gcal_id = db.Column(db.String(255),nullable=True)
    

class Employee(db.Model ,UserMixin):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    employee_id = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    full_name = db.Column(db.String(255))


class Patient(db.Model ,UserMixin):
     __tablename__ = 'patients'
     id = db.Column(db.Integer, primary_key=True)
     name = db.Column(db.String(255),nullable=False)
     email = db.Column(db.String(120), nullable=False)
     phone_number = db.Column(db.String(255))
     dob = db.Column(db.String(255), nullable=False)
     notes = db.Column(db.String(255))
     address_line = db.Column(db.String(255))
     city = db.Column(db.String(255))
     county = db.Column(db.String(255))
     post_code = db.Column(db.String(255))
     how_did_you_hear_about_us  = db.Column(db.String(255))

class User(db.Model ,UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(200))
    full_name = db.Column(db.String(30))
    email_address = db.Column(db.String(200), unique=True)
    created_at = db.Column(db.DateTime())
