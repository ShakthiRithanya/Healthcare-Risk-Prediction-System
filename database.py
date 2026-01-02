import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Database:
    def __init__(self, db_name='healthcare.db'):
        self.db_name = db_name
        self.init_db()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                full_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Predictions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                patient_name TEXT,
                age INTEGER NOT NULL,
                room_number INTEGER NOT NULL,
                billing_amount REAL NOT NULL,
                gender TEXT,
                blood_type TEXT,
                medical_condition TEXT,
                admission_type TEXT,
                medication TEXT,
                insurance_provider TEXT,
                risk_level TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_user(self, username, email, password, role, full_name):
        """Create a new user"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            password_hash = generate_password_hash(password)
            
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, role, full_name)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, email, password_hash, role, full_name))
            
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return True, "User created successfully"
        except sqlite3.IntegrityError:
            return False, "Username or email already exists"
        except Exception as e:
            return False, str(e)
    
    def verify_user(self, username, password):
        """Verify user credentials"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            return True, dict(user)
        return False, None
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        return dict(user) if user else None
    
    def save_prediction(self, user_id, patient_data, risk_level):
        """Save a prediction to database"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO predictions (
                    user_id, patient_name, age, room_number, billing_amount,
                    gender, blood_type, medical_condition, admission_type,
                    medication, insurance_provider, risk_level
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_id,
                patient_data.get('patient_name', 'Unknown'),
                patient_data['age'],
                patient_data['room_number'],
                patient_data['billing_amount'],
                patient_data.get('gender'),
                patient_data.get('blood_type'),
                patient_data.get('medical_condition'),
                patient_data.get('admission_type'),
                patient_data.get('medication'),
                patient_data.get('insurance_provider'),
                risk_level
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error saving prediction: {e}")
            return False
    
    def get_predictions(self, user_id=None, limit=50):
        """Get predictions, optionally filtered by user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute('''
                SELECT p.*, u.full_name as user_name
                FROM predictions p
                JOIN users u ON p.user_id = u.id
                WHERE p.user_id = ?
                ORDER BY p.created_at DESC
                LIMIT ?
            ''', (user_id, limit))
        else:
            cursor.execute('''
                SELECT p.*, u.full_name as user_name
                FROM predictions p
                JOIN users u ON p.user_id = u.id
                ORDER BY p.created_at DESC
                LIMIT ?
            ''', (limit,))
        
        predictions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return predictions
    
    def get_statistics(self, user_id=None):
        """Get statistics for dashboard"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if user_id:
            # User-specific stats
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_predictions,
                    SUM(CASE WHEN risk_level = 'Low Risk' THEN 1 ELSE 0 END) as low_risk,
                    SUM(CASE WHEN risk_level = 'Medium Risk' THEN 1 ELSE 0 END) as medium_risk,
                    SUM(CASE WHEN risk_level = 'High Risk' THEN 1 ELSE 0 END) as high_risk
                FROM predictions
                WHERE user_id = ?
            ''', (user_id,))
        else:
            # Global stats
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_predictions,
                    SUM(CASE WHEN risk_level = 'Low Risk' THEN 1 ELSE 0 END) as low_risk,
                    SUM(CASE WHEN risk_level = 'Medium Risk' THEN 1 ELSE 0 END) as medium_risk,
                    SUM(CASE WHEN risk_level = 'High Risk' THEN 1 ELSE 0 END) as high_risk
                FROM predictions
            ''')
        
        stats = dict(cursor.fetchone())
        conn.close()
        return stats
    
    def get_all_users(self):
        """Get all users (for admin/doctor view)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, username, email, role, full_name, created_at FROM users')
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return users
