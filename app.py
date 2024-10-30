import os
import sqlite3
from flask import Flask, request, render_template, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
from datetime import datetime

# Configuration
app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB file size limit
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Initialize database
def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS userssss (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reportssss (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                image_path TEXT,
                timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()

init_db()

# Allowed file checker for uploads
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Routes for each HTML template
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/iot_alerts')
def iot_alerts():
    if 'user_id' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))
    return render_template('iot_alerts.html')

@app.route('/eco_tourism')
def eco_tourism():
    if 'user_id' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))
    return render_template('eco_tourism.html')

@app.route('/community')
def community():
    if 'user_id' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))
    return render_template('community.html')

@app.route('/incident_management')
def incident_management():
    if 'user_id' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))
    return render_template('incident_management.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash("Please log in to view your profile.")
        return redirect(url_for('login'))
    user_id = session['user_id']
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM userssss WHERE id = ?", (user_id,))
        user_data = cursor.fetchone()
    if user_data:
        return render_template('profile.html', username=user_data[0])
    else:
        flash("User not found.")
        return redirect(url_for('dashboard'))

# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Ensure username and password are provided
        if not username or not password:
            flash("Username and password are required.")
            return redirect(url_for('register'))
        
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO userssss (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                flash("Registration successful! Please log in.")
                return redirect(url_for('login'))
            except sqlite3.IntegrityError:
                flash("Username already exists. Please choose another.")
    return render_template('register.html')

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Ensure username and password are provided
        if not username or not password:
            flash("Username and password are required.")
            return redirect(url_for('login'))
        
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM userssss WHERE username = ? AND password = ?", (username, password))
            user = cursor.fetchone()
            if user:
                session['user_id'] = user[0]
                flash("Login successful!")
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid username or password.")
    return render_template('login.html')

# User Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.")
    return redirect(url_for('login'))

# Report an Incident
@app.route('/report_incident', methods=['GET', 'POST'])
def report_incident():
    if 'user_id' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        description = request.form['incident_description']
        photo = request.files.get('photo')
        photo_path = None

        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(photo_path)

        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO reportssss (description, image_path, timestamp) VALUES (?, ?, ?)",
                           (description, photo_path, timestamp))
            conn.commit()
        flash("Incident reported successfully.")
        return redirect(url_for('dashboard'))
    return render_template('report_incident.html')

# View Submitted Reports
@app.route('/reports')
def view_reports():
    if 'user_id' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))
    
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reportssss")
        reports = cursor.fetchall()
    return render_template('database_collection.html', reports=reports)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
