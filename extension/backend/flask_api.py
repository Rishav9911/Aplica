from flask import Flask, request, jsonify
from pymongo import MongoClient
import base64

app = Flask(__name__)

# MongoDB Connection
MONGO_URI = "mongodb+srv://sachdevarishav449:Parishu449%40@aplica.cozta.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["user-info"] 
collection = db["user-main-details"] 

# Function to fetch student data
def get_student_data(email):
    student = collection.find_one({"email": {"$regex": f"^{email}$", "$options": "i"}}, {"_id": 0})

    if student:
        for key, value in student.items():
            if isinstance(value, bytes):
                student[key] = base64.b64encode(value).decode("utf-8") 

        return student
    else:
        return {"error": "Student not found"}

@app.route('/get_student_data', methods=['GET'])
def api_get_student_data():
    email = request.args.get("email")
    if not email:
        return jsonify({"error": "Email is required"}), 400

    student_data = get_student_data(email)
    return jsonify(student_data)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
