import uuid
from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import UUID, String
from wtforms.fields.datetime import DateField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, Length

db = SQLAlchemy()

hospital_patient = db.Table("hospital_patient",
    db.Column('hospital_id', UUID(as_uuid=True), db.ForeignKey("hospital.id"), primary_key=True),
    db.Column('patient_id', db.String(), db.ForeignKey("patient.id"), primary_key=True),
    db.Column("enrollment_date", db.DateTime, default=datetime.utcnow),
                            )

class Hospital(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    reader_uuid = db.Column(UUID(as_uuid=True), unique=True, nullable=False)
    patients = db.relationship('Patient',
                               secondary=hospital_patient,
                               backref=db.backref('students', lazy="dynamic"), lazy="dynamic")
    uuid_used = db.Column(db.Boolean, unique=False, nullable=False)

class Staff(db.Model, UserMixin):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(), unique=True, nullable=False)
    role = db.Column(db.String(120), unique=False, nullable=False)
    hospital_id = db.Column(UUID(as_uuid=True), db.ForeignKey("hospital.id"), nullable=False)
    hospital = db.relationship('Hospital', backref="staves")
    is_admin = db.Column(db.Boolean, unique=False, nullable=False)

class Specialist(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    speciality = db.Column(db.String(120), unique=False, nullable=False)
    phone_number = db.Column(db.String(120), unique=False, nullable=False)
    hospital_id = db.Column(UUID(as_uuid=True), db.ForeignKey("hospital.id"), nullable=False)
    hospital = db.relationship('Hospital', backref="specialist")
    gender = db.Column(db.String(120), unique=False, nullable=False)


class Patient(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    phone_number = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(120), unique=False, nullable=False)
    city = db.Column(db.String(120), unique=False, nullable=False)
    zip_code = db.Column(db.String(120), unique=False, nullable=False)
    registered_date = db.Column(db.Date, nullable=False)
    profile_url = db.Column(db.String(), nullable=True)

class File(db.Model):
    id= db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    name = db.Column(db.String(300), nullable=False)
    url = db.Column(db.String(500),  nullable=False)
    size = db.Column(db.Float, nullable=False)
    patient_id = db.Column(db.String(), db.ForeignKey("patient.id"), nullable=False)
    patient = db.relationship('Patient', backref='files')


class LoginForm(FlaskForm):
    email = StringField('Username', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    reader_uuid = StringField('Reader UUID', validators=[DataRequired()])

class NewAdminForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=2, max=50)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])


class SpecialistForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    speciality = StringField('Speciality', validators=[DataRequired(), Length(min=2, max=50)])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])

class NewPatientForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    age = IntegerField('Age', validators=[DataRequired()])
    gender = StringField('Gender', validators=[DataRequired()])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    phone_number = IntegerField('Phone Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    zip_code = StringField('Zip Code', validators=[DataRequired()])
    card_uuid = StringField('Card UUID', validators=[DataRequired()])

