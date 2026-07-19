import time
import uuid
import firebase_config

# In-memory fallback database variables
MOCK_USERS = {}
MOCK_STUDENTS = []

# ==================== USER AUTH SERVICE ====================

def get_user_by_username(username):
    """
    Fetches a user document by username.
    Supports Firestore database and mock fallback.
    """
    if firebase_config.db:
        try:
            doc = firebase_config.db.collection('users').document(username).get()
            if doc.exists:
                data = doc.to_dict()
                return {
                    "id": username,
                    "username": username,
                    "password_hash": data.get("password_hash"),
                    "recovery_question": data.get("recovery_question"),
                    "recovery_answer_hash": data.get("recovery_answer_hash")
                }
        except Exception as e:
            print(f"Error fetching user from Firestore: {e}")
        return None
    else:
        # Mock database mode
        if username in MOCK_USERS:
            user = MOCK_USERS[username]
            return {
                "id": username,
                "username": username,
                "password_hash": user.get("password_hash"),
                "recovery_question": user.get("recovery_question"),
                "recovery_answer_hash": user.get("recovery_answer_hash")
            }
        return None

def create_user(username, password_hash, question, answer_hash):
    """
    Creates a new user. Supports Firestore and mock fallback.
    """
    if firebase_config.db:
        firebase_config.db.collection('users').document(username).set({
            "password_hash": password_hash,
            "recovery_question": question,
            "recovery_answer_hash": answer_hash,
            "created_at": time.time()
        })
    else:
        # Mock mode
        MOCK_USERS[username] = {
            "password_hash": password_hash,
            "recovery_question": question,
            "recovery_answer_hash": answer_hash,
            "created_at": time.time()
        }

def update_user_password(username, new_password_hash):
    """
    Updates user password. Supports Firestore and mock fallback.
    """
    if firebase_config.db:
        firebase_config.db.collection('users').document(username).update({
            "password_hash": new_password_hash
        })
    else:
        # Mock mode
        if username in MOCK_USERS:
            MOCK_USERS[username]["password_hash"] = new_password_hash

# ==================== STUDENT CRUD SERVICE ====================

def get_all_students():
    """
    Fetches all student records. Supports Firestore and mock fallback.
    """
    if firebase_config.db:
        try:
            docs = firebase_config.db.collection('students').stream()
            students = []
            for doc in docs:
                data = doc.to_dict()
                students.append({
                    "id": doc.id,
                    "fName": data.get("fName", ""),
                    "lName": data.get("lName", ""),
                    "rollNo": data.get("rollNo", ""),
                    "branch": data.get("branch", ""),
                    "batchNo": data.get("batchNo", ""),
                    "domain": data.get("domain", ""),
                    "submissionDate": data.get("submissionDate", ""),
                    "status": data.get("status", ""),
                    "email": data.get("email", ""),
                    "phone": data.get("phone", ""),
                    "guide": data.get("guide", ""),
                    "created_at": data.get("created_at", 0)
                })
            students.sort(key=lambda x: x.get("created_at", 0), reverse=True)
            return students
        except Exception as e:
            print(f"Error fetching students from Firestore: {e}")
            return []
    else:
        # Mock database mode
        students = []
        for s in MOCK_STUDENTS:
            students.append(s.copy())
        students.sort(key=lambda x: x.get("created_at", 0), reverse=True)
        return students

def add_student(student_data):
    """
    Adds a new student. Supports Firestore and mock fallback.
    """
    student_data["created_at"] = time.time()
    if firebase_config.db:
        doc_ref = firebase_config.db.collection('students').document()
        doc_ref.set(student_data)
        return doc_ref.id
    else:
        # Mock mode
        student_id = str(uuid.uuid4())
        student_data["id"] = student_id
        MOCK_STUDENTS.append(student_data)
        return student_id

def update_student(student_id, student_data):
    """
    Updates student. Supports Firestore and mock fallback.
    """
    if firebase_config.db:
        doc_ref = firebase_config.db.collection('students').document(student_id)
        doc_ref.set(student_data, merge=True)
    else:
        # Mock mode
        for idx, s in enumerate(MOCK_STUDENTS):
            if s["id"] == student_id:
                student_data["created_at"] = s.get("created_at", time.time())
                student_data["id"] = student_id
                MOCK_STUDENTS[idx] = student_data
                break

def delete_student(student_id):
    """
    Deletes student. Supports Firestore and mock fallback.
    """
    if firebase_config.db:
        firebase_config.db.collection('students').document(student_id).delete()
    else:
        # Mock mode
        global MOCK_STUDENTS
        MOCK_STUDENTS = [s for s in MOCK_STUDENTS if s["id"] != student_id]
