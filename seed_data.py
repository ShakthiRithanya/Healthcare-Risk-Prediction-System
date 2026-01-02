"""
Seed Data Script for Healthcare Risk Prediction System
Populates the database with sample users and predictions to simulate an active system
"""

from database import Database
import random
from datetime import datetime, timedelta

# Initialize database
db = Database()

# Sample data
FIRST_NAMES = [
    "John", "Sarah", "Michael", "Emily", "David", "Jessica", "James", "Jennifer",
    "Robert", "Lisa", "William", "Mary", "Richard", "Patricia", "Thomas", "Linda",
    "Charles", "Barbara", "Daniel", "Elizabeth", "Matthew", "Susan", "Anthony", "Karen",
    "Mark", "Nancy", "Donald", "Betty", "Steven", "Helen", "Paul", "Sandra"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Wilson", "Anderson", "Thomas",
    "Taylor", "Moore", "Jackson", "Martin", "Lee", "Thompson", "White", "Harris",
    "Clark", "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright"
]

PATIENT_NAMES = [
    "Alice Cooper", "Bob Wilson", "Carol Martinez", "David Lee", "Emma Thompson",
    "Frank Harris", "Grace Chen", "Henry Davis", "Iris Rodriguez", "Jack Anderson",
    "Kate Brown", "Leo Garcia", "Maria Gonzalez", "Nathan White", "Olivia Taylor",
    "Peter Moore", "Quinn Jackson", "Rachel Martin", "Sam Thomas", "Tina Lewis",
    "Uma Patel", "Victor Kim", "Wendy Clark", "Xavier Hall", "Yara Allen",
    "Zoe Walker", "Adam Young", "Bella King", "Chris Wright", "Diana Hill",
    "Ethan Scott", "Fiona Green", "George Adams", "Hannah Baker", "Ian Nelson",
    "Julia Carter", "Kevin Mitchell", "Laura Perez", "Mason Roberts", "Nina Turner",
    "Oscar Phillips", "Paula Campbell", "Quincy Parker", "Rose Evans", "Sean Edwards"
]

MEDICAL_CONDITIONS = ["Diabetes", "Hypertension", "Asthma", "Arthritis", "Cancer", "Obesity"]
BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
GENDERS = ["Male", "Female"]
ADMISSION_TYPES = ["Emergency", "Elective", "Urgent"]
MEDICATIONS = ["Aspirin", "Ibuprofen", "Penicillin", "Paracetamol", "Lipitor"]
INSURANCE_PROVIDERS = ["Blue Cross", "Aetna", "Cigna", "UnitedHealthcare", "Medicare"]

def create_users():
    """Create sample doctors, nurses, and receptionists"""
    users_created = []
    
    print("Creating users...")
    
    # Create 5 Doctors
    for i in range(5):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        username = f"dr{last_name.lower()}{i+1}"
        email = f"{username}@hospital.com"
        full_name = f"Dr. {first_name} {last_name}"
        
        success, message = db.create_user(username, email, "password123", "Doctor", full_name)
        if success:
            print(f"  ✓ Created Doctor: {full_name} ({username})")
            users_created.append({"username": username, "role": "Doctor", "full_name": full_name})
        else:
            print(f"  ✗ Failed to create {username}: {message}")
    
    # Create 8 Nurses
    for i in range(8):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        username = f"nurse{last_name.lower()}{i+1}"
        email = f"{username}@hospital.com"
        full_name = f"{first_name} {last_name}"
        
        success, message = db.create_user(username, email, "password123", "Nurse", full_name)
        if success:
            print(f"  ✓ Created Nurse: {full_name} ({username})")
            users_created.append({"username": username, "role": "Nurse", "full_name": full_name})
        else:
            print(f"  ✗ Failed to create {username}: {message}")
    
    # Create 4 Receptionists
    for i in range(4):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        username = f"reception{i+1}"
        email = f"{username}@hospital.com"
        full_name = f"{first_name} {last_name}"
        
        success, message = db.create_user(username, email, "password123", "Receptionist", full_name)
        if success:
            print(f"  ✓ Created Receptionist: {full_name} ({username})")
            users_created.append({"username": username, "role": "Receptionist", "full_name": full_name})
        else:
            print(f"  ✗ Failed to create {username}: {message}")
    
    return users_created

def create_predictions(users):
    """Create sample predictions for the past 3 months"""
    print("\nCreating predictions...")
    
    # Get all users from database
    all_users = db.get_all_users()
    
    # Create 150 predictions over the past 90 days
    predictions_created = 0
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    for i in range(150):
        # Random user
        user = random.choice(all_users)
        user_id = user['id']
        
        # Random patient
        patient_name = random.choice(PATIENT_NAMES)
        
        # Random date in the past 90 days
        random_days = random.randint(0, 90)
        prediction_date = end_date - timedelta(days=random_days)
        
        # Generate realistic patient data
        age = random.randint(18, 85)
        room_number = random.randint(100, 500)
        
        # Billing amount correlates somewhat with risk
        base_billing = random.uniform(5000, 50000)
        billing_amount = round(base_billing, 2)
        
        gender = random.choice(GENDERS)
        blood_type = random.choice(BLOOD_TYPES)
        medical_condition = random.choice(MEDICAL_CONDITIONS)
        admission_type = random.choice(ADMISSION_TYPES)
        medication = random.choice(MEDICATIONS)
        insurance_provider = random.choice(INSURANCE_PROVIDERS)
        
        # Determine risk level based on factors
        risk_score = 0
        
        # Age factor
        if age > 70:
            risk_score += 2
        elif age > 50:
            risk_score += 1
        
        # Billing factor
        if billing_amount > 30000:
            risk_score += 2
        elif billing_amount > 15000:
            risk_score += 1
        
        # Medical condition factor
        if medical_condition in ["Cancer", "Diabetes"]:
            risk_score += 2
        elif medical_condition in ["Hypertension", "Obesity"]:
            risk_score += 1
        
        # Admission type factor
        if admission_type == "Emergency":
            risk_score += 2
        elif admission_type == "Urgent":
            risk_score += 1
        
        # Determine risk level
        if risk_score >= 5:
            risk_level = "High Risk"
        elif risk_score >= 3:
            risk_level = "Medium Risk"
        else:
            risk_level = "Low Risk"
        
        # Create patient data dictionary
        patient_data = {
            'patient_name': patient_name,
            'age': age,
            'room_number': room_number,
            'billing_amount': billing_amount,
            'gender': gender,
            'blood_type': blood_type,
            'medical_condition': medical_condition,
            'admission_type': admission_type,
            'medication': medication,
            'insurance_provider': insurance_provider
        }
        
        # Save prediction
        success = db.save_prediction(user_id, patient_data, risk_level)
        
        if success:
            predictions_created += 1
            if predictions_created % 25 == 0:
                print(f"  ✓ Created {predictions_created} predictions...")
        else:
            print(f"  ✗ Failed to create prediction for {patient_name}")
    
    print(f"\n✓ Total predictions created: {predictions_created}")
    return predictions_created

def update_prediction_timestamps():
    """Update prediction timestamps to spread them over 90 days"""
    print("\nUpdating prediction timestamps...")
    
    import sqlite3
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Get all predictions
    cursor.execute('SELECT id FROM predictions ORDER BY id')
    prediction_ids = [row[0] for row in cursor.fetchall()]
    
    end_date = datetime.now()
    
    for idx, pred_id in enumerate(prediction_ids):
        # Spread predictions over 90 days, with more recent activity
        # Use exponential distribution to have more recent predictions
        days_ago = int(random.expovariate(1/30))  # Average 30 days ago
        if days_ago > 90:
            days_ago = 90
        
        # Add some randomness to hours and minutes
        hours = random.randint(8, 18)  # Business hours
        minutes = random.randint(0, 59)
        
        prediction_date = end_date - timedelta(days=days_ago, hours=hours, minutes=minutes)
        timestamp = prediction_date.strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('UPDATE predictions SET created_at = ? WHERE id = ?', (timestamp, pred_id))
    
    conn.commit()
    conn.close()
    print("  ✓ Timestamps updated")

def print_statistics():
    """Print database statistics"""
    print("\n" + "="*60)
    print("DATABASE STATISTICS")
    print("="*60)
    
    # Get all users
    all_users = db.get_all_users()
    doctors = [u for u in all_users if u['role'] == 'Doctor']
    nurses = [u for u in all_users if u['role'] == 'Nurse']
    receptionists = [u for u in all_users if u['role'] == 'Receptionist']
    
    print(f"\n👥 USERS:")
    print(f"  Total Users: {len(all_users)}")
    print(f"  👨‍⚕️ Doctors: {len(doctors)}")
    print(f"  👩‍⚕️ Nurses: {len(nurses)}")
    print(f"  👨‍💼 Receptionists: {len(receptionists)}")
    
    # Get statistics
    stats = db.get_statistics()
    
    print(f"\n📊 PREDICTIONS:")
    print(f"  Total Predictions: {stats['total_predictions']}")
    print(f"  ✅ Low Risk: {stats['low_risk']} ({stats['low_risk']/max(stats['total_predictions'],1)*100:.1f}%)")
    print(f"  ⚠️ Medium Risk: {stats['medium_risk']} ({stats['medium_risk']/max(stats['total_predictions'],1)*100:.1f}%)")
    print(f"  🚨 High Risk: {stats['high_risk']} ({stats['high_risk']/max(stats['total_predictions'],1)*100:.1f}%)")
    
    print("\n" + "="*60)
    print("SAMPLE LOGIN CREDENTIALS")
    print("="*60)
    print("\nAll passwords: password123\n")
    
    if doctors:
        print("👨‍⚕️ DOCTORS:")
        for doc in doctors[:3]:
            print(f"  Username: {doc['username']} | Name: {doc['full_name']}")
    
    if nurses:
        print("\n👩‍⚕️ NURSES:")
        for nurse in nurses[:3]:
            print(f"  Username: {nurse['username']} | Name: {nurse['full_name']}")
    
    if receptionists:
        print("\n👨‍💼 RECEPTIONISTS:")
        for rec in receptionists[:2]:
            print(f"  Username: {rec['username']} | Name: {rec['full_name']}")
    
    print("\n" + "="*60)

def main():
    """Main function to seed the database"""
    print("\n" + "="*60)
    print("HEALTHCARE SYSTEM - DATABASE SEEDING")
    print("="*60 + "\n")
    
    # Create users
    users = create_users()
    
    # Create predictions
    predictions_count = create_predictions(users)
    
    # Update timestamps to spread over time
    update_prediction_timestamps()
    
    # Print statistics
    print_statistics()
    
    print("\n✅ Database seeding completed successfully!")
    print("🚀 You can now login with any of the above credentials\n")

if __name__ == "__main__":
    main()
