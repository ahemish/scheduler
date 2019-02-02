CREATE TABLE IF NOT EXISTS appointments
(
id integer primary key AUTOINCREMENT,
start VARCHAR(255),
end VARCHAR(255) ,
all_day boolean,
appointment_colour VARCHAR(255),
patient_id int,
appointment_type VARCHAR(255),
canceled boolean


);


CREATE TABLE IF NOT EXISTS employees (
  id integer primary key AUTOINCREMENT,
  email VARCHAR(255),
  employee_id VARCHAR(255),
  first_name VARCHAR(255),
  last_name VARCHAR(255),
  full_name VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS patients (
  id integer primary key AUTOINCREMENT,
  name VARCHAR(255),
  email VARCHAR(255),
  phone_number VARCHAR(255),
  notes VARCHAR(255)
);
