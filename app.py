from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask import render_template, request, redirect, url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:brayookk7@localhost/livestock'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# User and Cattle Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    breed = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)

class Calf(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    dam_name = db.Column(db.String(255))  # Dam is the mother cow's name
    sire_name = db.Column(db.String(255))  # Sire is the father bull's name

# Routes
@app.route('/')
def dashboard():
    cattle = animal.query.all()
    return render_template('dashboard.html', cattle=cattle)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register_cattle', methods=['GET', 'POST'])
def register_cattle():
    if request.method == 'POST':
        name = request.form['name']
        breed = request.form['breed']
        age = request.form['age']
        weight = request.form['weight']
        new_cattle = animal(name=name, breed=breed, age=age, weight=weight)
        db.session.add(new_cattle)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('register_cattle.html')

@app.route('/help', methods=['GET', 'POST'])
def help():
    if request.method == 'POST':
        issue = request.form['issue']
        email = request.form['email']
        # TODO: Handle the help request (e.g., save to the database, send an email, etc.)
        return redirect(url_for('help'))
    return render_template('help.html')

@app.route('/submit_help_request', methods=['POST'])
def submit_help_request():
    issue = request.form['issue']
    email = request.form['email']
    # Handle the help request (e.g., save to the database, send an email, etc.)
    return redirect(url_for('help'))

@app.route('/logout')
def logout():
    # Add any logout logic here (e.g., clearing sessions)
    return redirect(url_for('login'))

@app.route('/cows')
def cows():
    cows = [
        {"name": "Cow 1", "breed": "Breed A", "age": 5, "weight": 600},
        {"name": "Cow 2", "breed": "Breed B", "age": 3, "weight": 500}
    ]
    breeds = [("Breed A", 10), ("Breed B", 5)]
    return render_template('cows.html', cows=cows, breeds=breeds, total_cows=len(cows))

@app.route('/total_cows')
def total_cows():
    # Replace with actual logic
    total_cows = 15
    return render_template('total_cows.html', total_cows=total_cows)

@app.route('/cow_types')
def cow_types():
    # Replace with actual logic
    cow_types = [("Breed A", 10), ("Breed B", 5)]
    return render_template('cow_types.html', cow_types=cow_types)

@app.route('/search_cows', methods=['POST'])
def search_cows():
    search_term = request.form.get('search_term')
    # Replace with actual search logic
    cows = [
        {"name": "Cow 1", "breed": "Breed A", "age": 5, "weight": 600},
        {"name": "Cow 2", "breed": "Breed B", "age": 3, "weight": 500}
    ]
    result = [cow for cow in cows if search_term.lower() in cow['name'].lower()]
    return render_template('cows.html', cows=result, breeds=[], total_cows=len(result))


@app.route('/calvings')
def calvings():
    # Retrieve calvings data from the database
    calvings = []  # Replace with actual data retrieval
    return render_template('calvings.html', calvings=calvings)

@app.route('/weaners')
def weaners():
    # Retrieve weaners data from the database
    weaners = []  # Replace with actual data retrieval
    return render_template('weaners.html', weaners=weaners)

@app.route('/milk_records')
def milk_records():
    # Retrieve milk records data from the database
    milk_records = []  # Replace with actual data retrieval
    return render_template('milk_records.html', milk_records=milk_records)

@app.route('/reports')
def reports():
    # Retrieve reports data from the database
    reports = []  # Replace with actual data retrieval
    return render_template('reports.html', reports=reports)

@app.route('/inventory')
def inventory():
    # Retrieve inventory data from the database
    inventory = []  # Replace with actual data retrieval
    return render_template('inventory.html', inventory=inventory)

@app.route('/register_calf', methods=['POST'])
def register_calf():
    # Extract form data
    calf_name = request.form['calf_name']
    calf_birth_date = request.form['calf_birth_date']
    calf_breed = request.form['calf_breed']
    calf_weight = request.form['calf_weight']
    # Save to the database
    # TODO: Add your database code here to save the new calf
    return redirect(url_for('calvings'))

@app.route('/add_health_record', methods=['POST'])
def add_health_record():
    # Extract form data
    calf_id = request.form['calf_id']
    health_record = request.form['health_record']
    # Save to the database
    # TODO: Add your database code here to save the health record
    return redirect(url_for('calvings'))

@app.route('/view_schedules', methods=['GET'])
def view_schedules():
    # Extract form data
    calf_id_schedule = request.args['calf_id_schedule']
    # Fetch from the database
    # TODO: Add your database code here to fetch the schedule
    # For now, let's return a simple page
    schedules = [
        {'task': 'Feeding', 'time': '08:00 AM'},
        {'task': 'Health Check', 'time': '12:00 PM'}
    ]
    return render_template('schedules.html', schedules=schedules, calf_id=calf_id_schedule)

@app.route('/calving', methods=['GET', 'POST'])
def calving():
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birth_date']
        weight = request.form['weight']
        dam_name = request.form['dam_name']
        sire_name = request.form['sire_name']

        # Convert birth_date to a datetime object
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d')

        # Create a new calf instance
        new_calf = Calf(name=name, birth_date=birth_date, weight=weight, dam_name=dam_name, sire_name=sire_name)

        # Add the calf to the database
        db.session.add(new_calf)
        db.session.commit()

        return redirect(url_for('calving'))

    calves = Calf.query.all()
    return render_template('calving.html', calves=calves)



if __name__ == '__main__':
    app.run(debug=True)
