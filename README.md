# 🏥 Healthcare Risk Prediction System

An AI-powered healthcare risk prediction application that uses machine learning to assess patient risk levels based on medical and demographic data. **Now with multi-user authentication and role-based access control!**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![ML](https://img.shields.io/badge/ML-K--means%20%7C%20PCA-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### **Core ML Features:**
- **AI-Powered Predictions**: Uses K-means clustering with PCA for dimensionality reduction
- **Real-time Risk Assessment**: Instant prediction of patient risk levels (Low, Medium, High)
- **Comprehensive Input**: Analyzes multiple patient factors including demographics, medical conditions, and billing data
- **Visual Feedback**: Color-coded risk indicators with detailed recommendations

### **🆕 Multi-User Authentication System:**
- **Secure Login/Signup**: Beautiful authentication pages with password hashing
- **Role-Based Access Control**: Three user types (Doctor, Nurse, Receptionist)
- **Customized Dashboards**: Each role has a personalized dashboard with appropriate permissions
- **Prediction History**: Track and view predictions with role-based filtering
- **User Management**: Doctors can view and manage all system users
- **Session Management**: Secure session handling with Flask-Session

### **Premium UI/UX:**
- **Modern Design**: Glassmorphism effects with gradient backgrounds
- **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile
- **Smooth Animations**: Floating elements, fade-ins, and transitions
- **Role-Specific Interfaces**: Customized navigation and features for each user type

## 🎯 Risk Categories

| Risk Level | Indicator | Description |
|------------|-----------|-------------|
| **Low Risk** | ✅ Green | Minimal intervention needed, standard care protocols |
| **Medium Risk** | ⚠️ Orange | Regular monitoring recommended, preventive measures |
| **High Risk** | 🚨 Red | Immediate attention required, comprehensive care plan |

## 👥 User Roles & Permissions

### 👨‍⚕️ **Doctor** (Full Access)
- ✅ View ALL patient predictions (system-wide)
- ✅ Access complete analytics and statistics
- ✅ Manage users (view all system users)
- ✅ Make new risk predictions
- ✅ View prediction history from all staff members

### 👩‍⚕️ **Nurse** (Limited Access)
- ✅ Make new patient assessments
- ✅ View ONLY their own predictions
- ✅ Access their personal statistics
- ❌ Cannot view other users' predictions
- ❌ Cannot manage users

### 👨‍💼 **Receptionist** (Basic Access)
- ✅ Register new patients
- ✅ View ONLY their own registrations
- ✅ Access basic statistics
- ❌ Cannot view other users' data
- ❌ Cannot manage users

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Machine Learning**: 
  - scikit-learn (K-means clustering)
  - PCA (Principal Component Analysis)
  - OneHotEncoder for categorical features
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Processing**: Pandas, NumPy
- **Model Persistence**: Joblib

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## 🚀 Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "c:\PROJECTS\ML MODEL 1"
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or manually:
   ```bash
   pip install flask pandas scikit-learn joblib numpy werkzeug flask-session
   ```

## 📊 Dataset

The application uses a healthcare dataset (`healthcare_dataset.csv`) containing:
- Patient demographics (Age, Gender, Blood Type)
- Medical information (Medical Condition, Medication)
- Administrative data (Admission Type, Insurance Provider)
- Financial data (Billing Amount)

## 🎓 Model Training

The system uses pre-trained models:
- `kmeans_model.pkl`: K-means clustering model (3 clusters for risk levels)
- `pca_model.pkl`: PCA model for dimensionality reduction
- `encoder.pkl`: OneHotEncoder for categorical features
- `feature_columns.pkl`: Feature column definitions

To retrain the models, use the provided training scripts:
```bash
python train_encoder.py
python create_features_column.py
```

## 🗄️ Database Seeding (Optional)

To populate the database with sample data for testing/demo purposes:

```bash
python seed_data.py
```

This will create:
- **20 users** (7 doctors, 9 nurses, 4 receptionists)
- **150 predictions** spread over 90 days
- Realistic patient data with varied risk levels
- All with password: `password123`

**Note:** This is optional and only needed for demonstration purposes.

## 🏃‍♂️ Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

3. **Create an account** (first time):
   - Click "Sign up here"
   - Fill in your details (Full Name, Username, Email, Password)
   - Select your role (Doctor, Nurse, or Receptionist)
   - Click "Create Account"

4. **Login** with your credentials:
   - Enter username and password
   - Access your role-specific dashboard

5. **Make predictions**:
   - Click "New Prediction" (or "New Assessment"/"Registration")
   - Enter patient information:
     - Patient Name
     - Age, Gender, Blood Type
     - Medical Condition
     - Admission Type, Medication
     - Insurance Provider
     - Room Number, Billing Amount
   - Click "Predict Risk Level"
   - View the AI-powered risk assessment

6. **View history**:
   - Click "History" or "My Records"
   - See all your predictions (or all system predictions if you're a Doctor)

7. **Manage users** (Doctors only):
   - Click "Manage Users"
   - View all system users and their roles

## 📁 Project Structure

```
ML MODEL 1/
├── app.py                          # Main Flask application with authentication
├── database.py                     # Database management (SQLite)
├── healthcare_dataset.csv          # Training dataset
├── healthcare.db                   # SQLite database (auto-created)
├── kmeans_model.pkl               # Trained K-means model
├── pca_model.pkl                  # Trained PCA model
├── encoder.pkl                    # OneHotEncoder
├── feature_columns.pkl            # Feature definitions
├── train_encoder.py               # Encoder training script
├── create_features_column.py      # Feature creation script
├── requirements.txt               # Python dependencies
├── templates/
│   ├── login.html                 # Login page
│   ├── signup.html                # Registration page
│   ├── dashboard_doctor.html      # Doctor dashboard
│   ├── dashboard_nurse.html       # Nurse dashboard
│   ├── dashboard_receptionist.html # Receptionist dashboard
│   ├── predict.html               # Prediction form
│   ├── history.html               # Prediction history
│   └── users.html                 # User management (doctors only)
├── static/
│   └── css/
│       ├── style.css              # Main application styling
│       ├── auth.css               # Authentication pages styling
│       └── dashboard.css          # Dashboard styling
├── README.md                      # This file
├── AUTHENTICATION_GUIDE.md        # Complete authentication guide
├── AUTHENTICATION_COMPLETE.md     # Implementation summary
├── DOCUMENTATION.md               # Technical documentation
└── PROJECT_COMPLETE.md            # Project completion summary
```

## 🎨 UI Features

- **Modern Design**: Glassmorphism effects with gradient backgrounds
- **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile
- **Smooth Animations**: Floating elements, fade-ins, and transitions
- **Interactive Elements**: Hover effects and loading states
- **Accessibility**: Proper labels, semantic HTML, and keyboard navigation
- **Visual Hierarchy**: Clear information architecture with color-coded results
- **Role-Based UI**: Customized navigation and features for each user type

## 🔒 Privacy & Security

### **Authentication Security:**
- ✅ **Password Hashing**: PBKDF2 algorithm (Werkzeug)
- ✅ **Session Management**: Secure Flask sessions
- ✅ **Role-Based Access Control**: Decorator-enforced permissions
- ✅ **SQL Injection Protection**: Parameterized queries
- ✅ **Input Validation**: Client and server-side validation
- ✅ **Unique Constraints**: Username and email uniqueness enforced

### **Data Privacy:**
- Patient predictions stored securely in SQLite database
- User passwords never stored in plain text
- Session data encrypted
- Role-based data filtering (users only see authorized data)

### **Production Recommendations:**
- Change `app.secret_key` to a strong random value
- Use HTTPS for all connections
- Implement rate limiting for login attempts
- Add email verification (optional)
- Enable two-factor authentication (optional)
- Regular security audits

## 📈 Model Performance

The K-means clustering model with PCA achieves:
- Efficient dimensionality reduction
- Clear cluster separation for risk stratification
- Fast prediction times (<100ms)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Created with ❤️ for healthcare professionals and data scientists

## 🙏 Acknowledgments

- Healthcare dataset for model training
- Flask framework for web application
- scikit-learn for machine learning capabilities

## 📞 Support

For issues, questions, or suggestions, please open an issue in the repository.

---

**Note**: This is a demonstration application for educational purposes. Always consult with qualified healthcare professionals for actual medical decisions.
