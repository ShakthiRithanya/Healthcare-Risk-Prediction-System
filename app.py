from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import joblib
from functools import wraps
from database import Database

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'  # Change this in production!

# Initialize database
db = Database()

# Load ML models
pca_model = joblib.load("pca_model.pkl")
kmeans_model = joblib.load("kmeans_model.pkl")

# Role-based access decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please login to access this page', 'warning')
                return redirect(url_for('login'))
            if session.get('role') not in roles:
                flash('You do not have permission to access this page', 'danger')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        success, user = db.verify_user(username, password)
        if success:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            session['full_name'] = user['full_name']
            flash(f'Welcome back, {user["full_name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        role = request.form['role']
        full_name = request.form['full_name']
        
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('signup.html')
        
        success, message = db.create_user(username, email, password, role, full_name)
        if success:
            flash('Account created successfully! Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash(message, 'danger')
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    role = session.get('role')
    user_id = session.get('user_id')
    
    # Get statistics
    if role == 'Doctor':
        stats = db.get_statistics()  # Doctors see all stats
        recent_predictions = db.get_predictions(limit=10)
    else:
        stats = db.get_statistics(user_id)  # Others see only their stats
        recent_predictions = db.get_predictions(user_id, limit=10)
    
    return render_template(f'dashboard_{role.lower()}.html', 
                         stats=stats, 
                         recent_predictions=recent_predictions)

@app.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    result = None
    
    if request.method == 'POST':
        # Collect patient data
        patient_data = {
            'patient_name': request.form.get('patient_name', 'Unknown'),
            'age': float(request.form['age']),
            'room_number': float(request.form['room_number']),
            'billing_amount': float(request.form['billing_amount']),
            'gender': request.form.get('gender'),
            'blood_type': request.form.get('blood_type'),
            'medical_condition': request.form.get('medical_condition'),
            'admission_type': request.form.get('admission_type'),
            'medication': request.form.get('medication'),
            'insurance_provider': request.form.get('insurance_provider')
        }
        
        # Prepare data for ML model (only numerical features)
        input_data = pd.DataFrame([{
            "Age": patient_data['age'],
            "Billing Amount": patient_data['billing_amount'],
            "Room Number": patient_data['room_number']
        }])
        
        # PCA transformation
        pca_features = pca_model.transform(input_data)
        
        # KMeans prediction
        cluster = kmeans_model.predict(pca_features)[0]
        
        # Map cluster to risk label
        risk_map = {0: "Low Risk", 1: "Medium Risk", 2: "High Risk"}
        result = risk_map.get(cluster, "Unknown")
        
        # Save prediction to database
        db.save_prediction(session['user_id'], patient_data, result)
        
        flash(f'Prediction completed: {result}', 'success')
    
    return render_template('predict.html', result=result)

@app.route('/history')
@login_required
def history():
    user_id = session.get('user_id')
    role = session.get('role')
    
    # Doctors can see all predictions, others see only their own
    if role == 'Doctor':
        predictions = db.get_predictions(limit=100)
    else:
        predictions = db.get_predictions(user_id, limit=100)
    
    return render_template('history.html', predictions=predictions)

@app.route('/users')
@role_required('Doctor')
def users():
    all_users = db.get_all_users()
    return render_template('users.html', users=all_users)

if __name__ == "__main__":
    app.run(debug=True)
