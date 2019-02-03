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
     notes = db.Column(db.String(255))

# class Event(db.Model):
    
#     __tablename__ = 'appointments'
#     id = db.Column(db.String(100), primary_key=True)
#     title = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return '{} | {}  | {}'.format(self.id , self.title , self.email)
