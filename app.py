from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# Database setup
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Create users table if it doesn't exist
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check against the database for user validation
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.close()
        
        if user:
            session['username'] = username  # Store username in session
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid username or password.")  # Handle invalid credentials
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Logic to save user to database
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            flash("Registration successful! You can now log in.")
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash("Username already exists. Please choose a different username.")
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/iot_alerts')
def iot_alerts():
    # Logic to display IoT alerts would go here
    return render_template('iot_alerts.html')

@app.route('/report_incident', methods=['GET', 'POST'])
def report_incident():
    if request.method == 'POST':
        # Logic to handle incident report submission
        return redirect(url_for('dashboard'))
    return render_template('report_incident.html')

@app.route('/eco_tourism')
def eco_tourism():
    # Logic to display eco-tourism options would go here
    return render_template('eco_tourism.html')

@app.route('/community')
def community():
    # Logic to display community challenges would go here
    return render_template('community.html')

@app.route('/incident_management')
def incident_management():
    # Logic to manage incidents would go here
    return render_template('incident_management.html')

@app.route('/profile')
def profile():
    # Logic to display user profile would go here
    return render_template('profile.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True)
