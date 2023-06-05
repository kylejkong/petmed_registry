import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify, url_for,send_from_directory
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from helpers import login_required, apology
import requests
from datetime import datetime, timedelta
import traceback

# Configure application
app = Flask(__name__)




# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set the upload folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'test')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# # Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///petmed.db")






@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()
    message = request.args.get('message')
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Please provide a username", redirect_url="login")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Please provide a password", redirect_url="login")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username or invalid password", redirect_url="login")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached routevia GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html", message = message)


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()


    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # clearing user session
    session.clear()


    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):

            return redirect(url_for('register', message='Please provide a username'))

        # Ensure password was submitted
        elif not request.form.get("password"):

            return redirect(url_for('register', message='Please provide a password'))

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return redirect(url_for('register', message='Please provide a password confirmation'))


        # Ensure passwords must match
        elif request.form.get("password") != request.form.get("confirmation"):
            return redirect(url_for('register', message='Please provide a matching password'))

        #check database for username
        row = db.execute("Select * FROM users WHERE username = ?", request.form.get("username"))

        # If the length of the row list is greater than 0, it means the username already exists
        if len(row) > 0:

            return redirect(url_for('register', message='Username taken'))


        #insert and save new user into database
        userName = request.form.get("username")
        passWord = generate_password_hash(request.form.get("password"))
        db.execute("Insert INTO users (username, hash) VALUES(?,?)",
                   userName, passWord)

        #find the newly added user in the database
        rows = db.execute("Select * FROM users WHERE username = ?",
                                 userName)

        # Get the ID of the newly added user and associate it with the current session
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]


        return redirect("/")

    ##via get method
    else:
        return render_template('register.html', message=request.args.get('message'))



@app.route('/')
@login_required
def index():
    # Retrieve the user's role from the database

    return render_template('index.html')




@app.route("/userprofile/<int:id>")
@login_required
def userprofile(id):
    # Get the user ID from the session and convert it to an integer

    print(f"ID: {id}")
    user_id = int(session["user_id"])

    # Query the database for the user's profile information using the id parameter
    result = db.execute("SELECT name, phone, email, address, user_id FROM userprofile WHERE user_id = :user_id",
                        user_id=id)

    # Store the result in a list of dictionaries
    user_profile = [dict(row) for row in result]

    if len(user_profile) == 0:
        db.execute("INSERT INTO userprofile (user_id) VALUES (:user_id)", user_id=id)
        user_profile = [{'user_id': id}] # Add user_id to user_profile list if it was just inserted

    # Extract the user's profile information from the first dictionary in the list
    user = user_profile[0]

    # Add the user ID to the user dictionary
    user['user_id']= id

    # Pass the user's profile information to the template
    return render_template("userprofile.html", user=user, user_id=user_id)





@app.route("/editprofile/", methods=["GET", "POST"])
def editprofile():
    # Get the user from the database
        # If the user submits the form to update the birthday
    if request.method == "POST":
        user_id = request.form.get("user_id")
        name = request.form.get("name")
        phone = request.form.get("phone")
        email = request.form.get("email")
        address = request.form.get("address")

        # Update the database
        if user_id:
            db.execute("UPDATE userprofile SET name = :name, phone = :phone, email = :email, address = :address WHERE user_id = :user_id", name=name, phone=phone, email=email, address=address, user_id=user_id)


        return redirect(url_for('userprofile', id=user_id))
    # If the user requests the edit page
    else:
        user_id = request.args.get("user_id")
        if user_id:
            # Get the existing  data
            rows = db.execute("SELECT * FROM userprofile WHERE user_id = :user_id", user_id=user_id)
            for row in rows:
                row_dict = dict(row)
                # Render the edit page with the existing data
                return render_template("editprofile.html", user=row_dict)

    # If the user did not provide an ID or the ID was not found in the database
    return redirect("/")

@app.route('/pets')
@login_required
def pets():
    # incomplete
    # if current_user.role != 'admin' and current_user.role != 'superuser':
    #     flash('You do not have permission to view this page.')
    #     return redirect(url_for('index'))
    # pets = Pet.query.all()
    return render_template('pets.html', pets=pets)


@app.route('/registerpet', methods=["GET", "POST"])
@login_required
def registerpet():
    user_id = session["user_id"]

    petspecies = [
        "Dog",
        "Cat",
        "Bird",
        "Rodents",
        "Rabbits",
        "Other"
    ]

    petgender = [
        "Male",
        "Female",
        "Unknown/Other"
    ]

    if request.method == "POST":

        petName = request.form.get('petName')
        petAge = request.form.get('petAge')
        petGender = request.form.get('petGender')
        petSpecies = request.form.get('petSpecies')
        petMedicalHistory = request.form.get('petMedicalHistory')
        petMicrochip = request.form.get('petMicrochip')
        user_id = request.form.get('user_id', None)


        if petMicrochip:
            existing_pet = db.execute("SELECT * FROM pets WHERE microchip_number=:microchip_number", microchip_number=petMicrochip)

            if existing_pet:
                return apology("Pet with this microchip number already exists", redirect_url="registerpet")


        petPhoto = request.files.get('petPhoto')
        # limit file size to 1MB (1048576 bytes)
    

        if petPhoto:
            if len(petPhoto.read()) > 1048576:
                return apology("Picture cannot exceed 1MB.", redirect_url="registerpet")
            # Use petName as the filename for the uploaded photo
            filename = secure_filename(petName) + os.path.splitext(petPhoto.filename)[1]
            petPhotoPath = os.path.join(UPLOAD_FOLDER, filename)
            petPhoto.save(petPhotoPath)
            print(f"File saved to: {os.path.abspath(petPhotoPath)}")
            petPhotoPath = os.path.abspath(petPhotoPath)
        else:
            filename = None
            petPhotoPath = None

        if user_id:
            db.execute("INSERT INTO pets (name, age, gender, species, medical_history, photo, microchip_number, user_id ) VALUES (:name, :age, :gender, :species, :medical_history, :photo, :microchip_number, :user_id)",
                name=petName, age=petAge, gender=petGender, species=petSpecies,
                medical_history=petMedicalHistory, photo=filename, microchip_number=petMicrochip, user_id = user_id)

            return redirect("/med_records")

    return render_template('registerpet.html', petspecies=petspecies, petgender=petgender, user_id = user_id )

@app.route('/med_records')
@login_required
def med_records():
    user_id = session["user_id"]
    pets = db.execute("SELECT id, name, age, gender, species, medical_history, photo, microchip_number FROM pets WHERE user_id = :user_id",
                        user_id=user_id)
    return render_template('med_records.html', pets=pets)



@app.route('/contact', methods=['POST','GET'])
def contact():
    if request.method == "POST":
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        message = request.form['message']
        subject = "New Message"

        # Create the contacts table if it doesn't exist
        db.execute("CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, name TEXT NOT NULL, phone TEXT, email TEXT NOT NULL, message TEXT NOT NULL)")

        # Save the contact to the database
        db.execute("INSERT INTO contacts (name, phone, email, message) VALUES (:name, :phone, :email, :message)",
            name=name, phone=phone, email=email, message=message)
        if 'user_id' in session:
            return apology("Thank you for your message, we will be in touch shortly", redirect_url="index")

        else:
            # return apology("Thank for your message, we will be in touch shortly", redirect_url="login")
            return redirect(url_for('login', message='Thank you for your message, we will be in touch shortly'))

    else:
        # Render the contact page template
        return render_template("contact.html")

@app.route('/appointment', methods=['POST','GET'])
@login_required
def appointment():
    db.execute("CREATE TABLE IF NOT EXISTS appointments (id INTEGER PRIMARY KEY, pet_id TEXT NOT NULL, date TEXT NOT NULL, time TIME NOT NULL, user_id INTEGER NOT NULL REFERENCES users(id), UNIQUE(pet, date, time, user_id))")

    # Generate a list of time slots every hour from 9am to 5pm
    available_slots = []
    start_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    end_time = datetime.now().replace(hour=17, minute=0, second=0, microsecond=0)
    current_time = start_time
    while current_time <= end_time:
        available_slots.append(current_time.strftime("%I:%M %p"))
        current_time += timedelta(hours=1)

    pets = db.execute("SELECT * FROM pets where user_id = :user_id ", user_id=session["user_id"])
    if request.method == "POST":
        user_id = request.form['user_id']
        pet = request.form['pet']
        date = request.form['date']
        time = request.form['time']


        # Convert the selected date to a datetime object
        selected_date = datetime.strptime(date, '%Y-%m-%d')

        if selected_date.date() < datetime.now().date():
            return "Invalid date"

        # Check if the selected date is a weekend
        if selected_date.weekday() >= 5:
            return "Selected date is a weekend"

        # Check if the selected date and timeare available
        existing_appointments = db.execute("SELECT time FROM appointments WHERE date = :date", date=date)

        existing_times = [appointment['time'] for appointment in existing_appointments]

        available_slots = [slot for slot in available_slots if slot not in existing_times]


        # Convert the selected date and time to a datetime object
        selected_datetime = datetime.strptime(date + ' ' + time, '%Y-%m-%d %I:%M %p')

        # Check if the selected date and time are in the future
        if selected_datetime < datetime.now():
            return "Invalid date and time"

        # Check if the selected date and time fall within business hours
        start_time = datetime.strptime(date + ' 09:00', '%Y-%m-%d %H:%M')
        end_time = datetime.strptime(date + ' 17:00', '%Y-%m-%d %H:%M')
        if selected_datetime < start_time or selected_datetime > end_time:
            return "Selected time is outside business hours"

        # Check if the selected time is available
        if time not in available_slots:
            # return "Selected time is not available"
            return apology(f"Sorry only these time slots are available: {available_slots} on {date}", redirect_url="appointment")

        # Add the appointment to the database
        db.execute("INSERT INTO appointments (pet_id, date, time, user_id) VALUES (:pet, :date, :time, :user_id)", pet=pet, date=date, time=time, user_id=user_id)


        pet_rows = db.execute("SELECT name FROM pets WHERE id = :id", id=pet)
        if not pet_rows:
            raise ValueError("Invalid pet ID")
        petName = None
        for pet_row in pet_rows:
            petName = pet_row['name']
            break

        return apology(f"Appointment made for {petName} on {date} at {time}. See you!", redirect_url="index")




    else:
        return render_template('appointment.html', pets=pets, available_slots=available_slots, user_id=session["user_id"])

@app.route('/test/<path:filename>')
def test(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/lostnfound', methods=['POST','GET'])
@login_required
def lostnfound():
    return render_template('lostnfound.html')


@app.route('/allusers', methods=['POST','GET'])
@login_required
def allusers():
    user_id = session["user_id"]
    rows = db.execute("SELECT role FROM users WHERE id = :id", id = user_id)
    for row in rows:
        userType = row['role']

        print(userType)
    if userType == "admin":
        allusers = db.execute("SELECT * FROM userprofile")
        return render_template('allusers.html', allusers=allusers)

    else:
        return apology(f"Admins only", redirect_url="index")



@app.route('/allpets', methods=['POST','GET'])
@login_required
def allpets():
    user_id = session["user_id"]
    rows = db.execute("SELECT role FROM users WHERE id = :id", id = user_id)
    for row in rows:
        userType = row['role']

        print(userType)
    if userType == "admin":
        allpets = db.execute("SELECT * FROM pets")
        return render_template('allpets.html', allpets=allpets)

    else:
        return apology(f"Admins only", redirect_url="index")


    ###to be added in future is allow admin to edit a pet's Medical History




