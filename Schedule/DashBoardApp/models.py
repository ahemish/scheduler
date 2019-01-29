from main import db_session
from flask_login import UserMixin

class Appointment(db_session.Model ,UserMixin):
    __tablename__ = 'appointments'
    id = db_session.Column(db_session.Integer, primary_key=True)
    start = db_session.Column(db_session.String(255))
    end = db_session.Column(db_session.String(255))
    all_day = db_session.Column(db_session.String(255))
    appointment_colour = db_session.Column(db_session.String(255),nullable=False)
    patient_id = db_session.Column(db_session.String(255))
    appointment_type = db_session.Column(db_session.String(255))
    canceled = db_session.Column(db_session.String(255))

class Employee(db_session.Model ,UserMixin):
    __tablename__ = 'employee'
    id = db_session.Column(db_session.Integer, primary_key=True)
    email = db_session.Column(db_session.String(120), unique=True, nullable=False)
    employee_id = db_session.Column(db_session.String(120), unique=True, nullable=False)
    first_name = db_session.Column(db_session.String(255))
    last_name = db_session.Column(db_session.String(255))
    full_name = db_session.Column(db_session.String(255))


class Patient(db_session.Model ,UserMixin):
     __tablename__ = 'patients'
     id = db_session.Column(db_session.Integer, primary_key=True)
     name = db_session.Column(db_session.String(255),nullable=False)
     email = db_session.Column(db_session.String(120), nullable=False)
     phone_number = db_session.Column(db_session.String(255))
     notes = db_session.Column(db_session.String(255))

# class Event(db_session.Model):
    
#     __tablename__ = 'appointments'
#     id = db_session.Column(db_session.String(100), primary_key=True)
#     title = db_session.Column(db_session.String(80), unique=True, nullable=False)
#     email = db_session.Column(db_session.String(120), unique=True, nullable=False)

#     def __repr__(self):
#         return '{} | {}  | {}'.format(self.id , self.title , self.email)
