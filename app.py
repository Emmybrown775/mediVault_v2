import os
from datetime import datetime
from html import escape

from flask import Flask, render_template, redirect, url_for, request, jsonify, flash
from sqlalchemy import func, asc
from wtforms.validators import ValidationError

from models import LoginForm, RegisterForm, Hospital, Staff, SpecialistForm, Specialist, Patient, hospital_patient, \
    NewPatientForm, NewAdminForm, File
from models import db
from flask_login import LoginManager, login_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import cloudinary.uploader

app = Flask(__name__)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)
socket=SocketIO(app)
CORS(app, supports_credentials=True)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["WTF_CSRF_SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["WTF_CSRF_ENABLED"] = False

db.init_app(app)


with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(staff_id):
    return Staff.query.get(staff_id)

@app.route("/")
def origin():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("login"))
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        form.process(request.form)
        if form.validate_on_submit():
            staff = Staff.query.filter_by(email=form.email.data).first()
            if staff:
                if bcrypt.check_password_hash(staff.password, form.password.data):
                    login_user(staff)
                    return redirect(url_for("dashboard"))
        print(form.errors)
    return render_template("login.html", form=form)

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            hospital = Hospital.query.filter_by(reader_uuid=form.reader_uuid.data).first()
            if hospital:
                if not hospital.uuid_used:
                    staff = Staff(
                        email=form.email.data,
                        name=form.name.data,
                        password=bcrypt.generate_password_hash(form.password.data).decode("utf-8"),
                        role="ADMIN",
                        hospital_id = hospital.id,
                        is_admin = True,
                    )

                    hospital.uuid_used = True
                    db.session.add(staff)
                    db.session.commit()

                    login_user(staff)

                    return redirect(url_for("dashboard"))

        print(form.errors)
    return render_template("signup.html", form=form)

@app.route('/home')
@login_required
def dashboard():
    specialists_count = len(current_user.hospital.specialist)
    return render_template("dashboard.html", specialists_count=specialists_count)

@app.route('/patients')
@login_required
def patients():
    filter_by = request.args.get('filter', None)  # Capture the filter parameter
    if filter_by == "age":
        new_patients = current_user.hospital.patients.order_by(Patient.age)
    elif filter_by == "id":
        new_patients = current_user.hospital.patients.order_by(Patient.id)
    elif filter_by == "name":
        new_patients = current_user.hospital.patients.order_by(Patient.name)
    elif filter_by == "date_registered":
        new_patients_query = db.session.query(hospital_patient).filter(
            hospital_patient.c.hospital_id == current_user.hospital.id
        ).order_by(asc(hospital_patient.c.enrollment_date)).all()
        new_patients = [Patient.query.filter_by(id=new_patients.patient_id).first() for new_patients in new_patients_query]
        print(new_patients)
    else:
        new_patients = current_user.hospital.patients.all()
    return render_template("patients.html", patients=new_patients)

@app.route("/patient/<string:patient_id>", methods=["GET", "POST"])
@login_required
def patient(patient_id):
    selected_patient_hospital = db.session.query(hospital_patient).filter_by(hospital_id=current_user.hospital_id, patient_id=patient_id).first()


    if selected_patient_hospital:
        selected_patient = Patient.query.filter_by(id=selected_patient_hospital.patient_id).first()
        if request.method == "POST":
            if request.form.get("form") == "file":
                if "file" not in request.files:
                    flash("No file selected")
                    return redirect(request.url)
                file = request.files["file"]
                if file.filename == "":
                    flash("No file selected")
                    return redirect(request.url)

                upload_result = cloudinary.uploader.upload(file, folder=f"{selected_patient_hospital.patient_id}")

                new_file = File(
                    name=file.filename,
                    url=upload_result["url"],
                    size=round(upload_result["bytes"] / 1024, 2),
                    patient_id=patient_id
                )

                db.session.add(new_file)
                db.session.commit()
                return redirect(request.url)

            if request.form.get("form") == "data":
                form = NewPatientForm(formdata=request.form)
                if form.validate_on_submit():
                    print(request.files)
                    if "profile_pic" in request.files:
                        file = request.files["profile_pic"]
                        if file.filename != "":
                            upload_result = cloudinary.uploader.upload(file,
                                                                       folder=f"{selected_patient_hospital.patient_id}")
                            selected_patient.name = form.name.data
                            selected_patient.age = form.age.data
                            selected_patient.gender = form.gender.data
                            selected_patient.date_of_birth = form.dob.data
                            selected_patient.phone_number = form.phone_number.data
                            selected_patient.address = form.address.data
                            selected_patient.city = form.city.data
                            selected_patient.zip_code = form.zip_code.data
                            selected_patient.profile_url = upload_result["url"]

                            db.session.commit()
                            return redirect(url_for("patient", patient_id=selected_patient.id))

                        selected_patient.name = form.name.data
                        selected_patient.age = form.age.data
                        selected_patient.gender = form.gender.data
                        selected_patient.date_of_birth = form.dob.data
                        selected_patient.phone_number = form.phone_number.data
                        selected_patient.address = form.address.data
                        selected_patient.city = form.city.data
                        selected_patient.zip_code = form.zip_code.data

                        db.session.commit()
                        return redirect(url_for("patient", patient_id=selected_patient.id))

                    selected_patient.name = form.name.data
                    selected_patient.age = form.age.data
                    selected_patient.gender = form.gender.data
                    selected_patient.date_of_birth = form.dob.data
                    selected_patient.phone_number = form.phone_number.data
                    selected_patient.address = form.address.data
                    selected_patient.city = form.city.data
                    selected_patient.zip_code = form.zip_code.data

                    db.session.commit()
                    return redirect(url_for("patient", patient_id=selected_patient.id))

                print(form.errors)


        return render_template("details.html", patient=selected_patient)
    return redirect(url_for("dashboard"))

@app.route("/specialist", methods=['GET', 'POST'])
@login_required
def specialist():
    if request.method == "POST":
        specialists = current_user.hospital.specialist
        form=SpecialistForm(request.form)
        if form.validate_on_submit():
            new_specialist = Specialist(
                name=form.name.data,
                email=form.email.data,
                speciality=form.speciality.data,
                phone_number=form.phone_number.data,
                hospital_id=current_user.hospital_id,
                gender=form.gender.data,
            )
            db.session.add(new_specialist)
            db.session.commit()

            return redirect(url_for("specialist"))
        return render_template("specialists.html", errors=form.errors, specialists=specialists)

    else:
        filter_by = request.args.get('filter', None)  # Capture the filter parameter
        if filter_by == "name":
            specialists = Specialist.query.filter_by(hospital_id=current_user.hospital_id).order_by(Specialist.name).all()
        elif filter_by == "speciality":
            specialists = Specialist.query.filter_by(hospital_id=current_user.hospital_id).order_by(Specialist.speciality).all()
        else:
            specialists = current_user.hospital.specialist
    return render_template("specialists.html", specialists=specialists)

@app.route("/settings", methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == "POST":
        if request.form.get("form_name") == "profile":
            name = request.form.get("name")
            email = request.form.get("email")

            if name:
                current_user.name = name
            if email:
                current_user.email = email
            db.session.commit()
            return redirect(url_for("settings"))
        if request.form.get("form_name") == "password":
            old_password = request.form.get("old_password")

            if bcrypt.check_password_hash(current_user.password, old_password):
                new_password = request.form.get("new_password")
                conf_new_password = request.form.get("conf_new_password")

                if new_password == conf_new_password:
                    current_user.password = bcrypt.generate_password_hash(new_password).decode("utf-8")
                    db.session.commit()
                    return redirect(url_for("settings"))



    return render_template("settings.html")

@app.route("/new_admin", methods=["GET", "POST"])
@login_required
def new_admin():
    if request.method == "POST":
        form = NewAdminForm(request.form)
        if form.validate_on_submit():
            new_staff = Staff(
                name=form.name.data,
                email=form.email.data,
                password=bcrypt.generate_password_hash(form.password.data).decode("utf-8"),
                role="ADMIN",
                hospital_id=current_user.hospital_id,
                is_admin = True
            )

            db.session.add(new_staff)
            db.session.commit()

            return redirect(url_for("dashboard"))
        print(form.errors)
        return render_template("new_admin.html", form=form)
    return render_template("new_admin.html")

@app.route("/new_patient", methods=["GET", "POST"])
@login_required
def new_patient():
    if request.method == "POST":
        form = NewPatientForm(request.form)
        if form.validate_on_submit():
            new_new_patient = Patient(
                id=form.card_uuid.data,
                name=form.name.data,
                email=form.email.data,
                age=form.age.data,
                gender=form.gender.data,
                date_of_birth=form.dob.data,
                phone_number=form.phone_number.data,
                address=form.address.data,
                city=form.city.data,
                zip_code=form.zip_code.data,
                registered_date=datetime.now(),
            )
            db.session.add(new_new_patient)
            db.session.commit()
            return redirect(url_for("patient", patient_id=new_new_patient.id))
        else:
            print(form.errors)
    uuid = request.args.get("uuid")
    return render_template("new_patient.html", uuid=uuid)




@socket.on("message")
def handle_message(message):
    print(message)
    uuid = escape(message["uid"]).strip()
    hospital_id = message["hospital_id"]

    scanned_patient = Patient.query.filter_by(id=uuid).first()
    current_hospital = Hospital.query.filter_by(id=hospital_id).first()

    if not current_hospital:
        print("print no hospital")
        return

    if scanned_patient:
        if db.session.query(hospital_patient).filter_by(hospital_id=current_hospital.id, patient_id=uuid).first():
            # Emit a message to the client to redirect to the "patient" page
            emit("redirect", {"url": url_for("patient", patient_id=uuid)}, broadcast=True)
        else:
            print("hello")
            current_hospital.patients.append(scanned_patient)
            db.session.commit()
            # Emit a message to the client to redirect to the "patient" page
            emit("redirect", {"url": url_for("patient", patient_id=uuid)}, broadcast=True)
    else:
        # Emit a message to the client to redirect to the "new_patient" page
        emit("redirect", {"url": url_for("new_patient", uuid=uuid)}, broadcast=True)

@app.route("/chart_data")
@login_required
def chart_data():

    results = db.session.query(
        func.date(hospital_patient.c.enrollment_date).label("day"),
        func.count(hospital_patient.c.patient_id).label("count"),
    ).filter(
        hospital_patient.c.hospital_id == current_user.hospital_id,
    ).group_by(
        func.date(hospital_patient.c.enrollment_date)
    ).order_by(
        func.date(hospital_patient.c.enrollment_date)
    ).all()

    data = {
        "labels": [str(row.day) for row in results],
        "data": [row.count for row in results],
    }
    return jsonify(data)

if __name__ == '__main__':
    socket.run(app)
