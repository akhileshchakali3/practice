import hashlib
from flask import Flask, render_template, request, jsonify, session
import db_service

app = Flask(__name__)

# --- Configurations ---
app.secret_key = 'your_super_secure_session_encryption_key'

def hash_text(text):
    return hashlib.sha256(text.strip().lower().encode()).hexdigest()

@app.route('/')
def index():
    return render_template('index.html')

# --- AUTH API: SIGNUP ---
@app.route('/api/auth/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        question = data.get('question')
        answer = data.get('answer')
        
        if not all([username, password, question, answer]):
            return jsonify({"error": "All fields are mandatory!"}), 400
            
        user = db_service.get_user_by_username(username)
        if user:
            return jsonify({"error": "Username is already taken!"}), 400
            
        pass_hashed = hash_text(password)
        ans_hashed = hash_text(answer)
        
        db_service.create_user(username, pass_hashed, question, ans_hashed)
        return jsonify({"message": "Account registered successfully! Now log in."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- AUTH API: LOGIN ---
@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({"error": "Username and password are required!"}), 400

        hashed_pass = hash_text(password)
        user = db_service.get_user_by_username(username)
        
        if user and user['password_hash'] == hashed_pass:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return jsonify({"message": "Access granted!", "username": user['username']}), 200
            
        return jsonify({"error": "Invalid username or password!"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- AUTH API: FETCH RECOVERY QUESTION ---
@app.route('/api/auth/get-question', methods=['POST'])
def get_question():
    try:
        data = request.json
        username = data.get('username')
        if not username:
            return jsonify({"error": "Username is required!"}), 400

        user = db_service.get_user_by_username(username)
        if user:
            return jsonify({"question": user['recovery_question']}), 200
        return jsonify({"error": "User profile not found!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- AUTH API: RESET PASSWORD VIA RECOVERY ---
@app.route('/api/auth/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.json
        username = data.get('username')
        answer = data.get('answer')
        new_password = data.get('newPassword')
        
        if not all([username, answer, new_password]):
            return jsonify({"error": "All fields are required!"}), 400

        ans_hashed = hash_text(answer)
        new_pass_hashed = hash_text(new_password)
        
        user = db_service.get_user_by_username(username)
        
        if not user or user['recovery_answer_hash'] != ans_hashed:
            return jsonify({"error": "Incorrect recovery security answer!"}), 401
            
        db_service.update_user_password(username, new_pass_hashed)
        return jsonify({"message": "Password updated successfully! Please log in now."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- AUTH API: USER CONTROLLED CHANGE PASSWORD (INSIDE APP) ---
@app.route('/api/auth/change-password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized session context!"}), 401
    try:
        data = request.json
        old_pass = data.get('oldPassword')
        new_pass = data.get('newPassword')
        
        if not old_pass or not new_pass:
            return jsonify({"error": "Old password and new password are required!"}), 400

        old_hashed = hash_text(old_pass)
        new_hashed = hash_text(new_pass)
        
        user = db_service.get_user_by_username(session['user_id'])
        if not user or user['password_hash'] != old_hashed:
            return jsonify({"error": "Current password does not match!"}), 400
            
        db_service.update_user_password(session['user_id'], new_hashed)
        return jsonify({"message": "Password updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- AUTH API: LOGOUT ---
@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully."}), 200

# --- DATA API: READ ALL ---
@app.route('/api/students', methods=['GET'])
def get_students():
    if 'user_id' not in session:
        return jsonify({"error": "Please log in first"}), 401
    try:
        students = db_service.get_all_students()
        return jsonify(students), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- DATA API: CREATE ---
@app.route('/api/students', methods=['POST'])
def add_student():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        data = request.json
        student_data = {
            'fName': data.get('fName'),
            'lName': data.get('lName'),
            'rollNo': data.get('rollNo'),
            'branch': data.get('branch'),
            'batchNo': data.get('batchNo'),
            'domain': data.get('domain'),
            'submissionDate': data.get('submissionDate'),
            'status': data.get('status'),
            'email': data.get('email'),
            'phone': data.get('phone'),
            'guide': data.get('guide')
        }
        db_service.add_student(student_data)
        return jsonify({"message": "Data saved to database successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- DATA API: UPDATE ---
# Note: Endpoint route parameter '<id>' matches Firestore string document ID
@app.route('/api/students/<id>', methods=['PUT'])
def update_student(id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        data = request.json
        student_data = {
            'fName': data.get('fName'),
            'lName': data.get('lName'),
            'rollNo': data.get('rollNo'),
            'branch': data.get('branch'),
            'batchNo': data.get('batchNo'),
            'domain': data.get('domain'),
            'submissionDate': data.get('submissionDate'),
            'status': data.get('status'),
            'email': data.get('email'),
            'phone': data.get('phone'),
            'guide': data.get('guide')
        }
        db_service.update_student(id, student_data)
        return jsonify({"message": "Student record updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- DATA API: DELETE ---
# Note: Endpoint route parameter '<id>' matches Firestore string document ID
@app.route('/api/students/<id>', methods=['DELETE'])
def delete_student(id):
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        db_service.delete_student(id)
        return jsonify({"message": "Record dropped from database completely."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)