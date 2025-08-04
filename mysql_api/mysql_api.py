from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="college"
    )

# ------------------ GET all students ------------------
@app.route('/students', methods=['GET'])
def get_all_students():
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM STUDENTSINFO")
    students = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(students)

# ------------------ GET student by SNO ------------------
@app.route('/students/<int:sno>', methods=['GET'])
def get_student(sno):
    db = connect_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM STUDENTSINFO WHERE SNO = %s", (sno,))
    student = cursor.fetchone()
    cursor.close()
    db.close()
    if student:
        return jsonify(student)
    else:
        return jsonify({"error": "Student not found"}), 404

# ------------------ POST add a new student ------------------
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    db = connect_db()
    cursor = db.cursor()
    try:
        cursor.execute("""
            INSERT INTO STUDENTSINFO (SNO, FIRST_NAME, LAST_NAME, AGE, DEPT, CGPA)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (data['SNO'], data['FIRST_NAME'], data['LAST_NAME'], data['AGE'], data['DEPT'], data['CGPA']))
        db.commit()
        return jsonify({"message": "Student added successfully"}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cursor.close()
        db.close()

# ------------------ PUT update a student ------------------
@app.route('/students/<int:sno>', methods=['PUT'])
def update_student(sno):
    data = request.get_json()
    db = connect_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM STUDENTSINFO WHERE SNO = %s", (sno,))
    student = cur.fetchone()

    if not student:
        cur.close(); db.close()
        return jsonify({"error": "Student not found"}), 404

    # Merge existing and new data
    for key in ['FIRST_NAME', 'LAST_NAME', 'AGE', 'DEPT', 'CGPA']:
        data[key] = data.get(key, student[key])

    try:
        cur.execute("""
            UPDATE STUDENTSINFO SET FIRST_NAME=%s, LAST_NAME=%s, AGE=%s, DEPT=%s, CGPA=%s WHERE SNO=%s
        """, (data['FIRST_NAME'], data['LAST_NAME'], data['AGE'], data['DEPT'], data['CGPA'], sno))
        db.commit()
        return jsonify({"message": "Student updated successfully"})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 400
    finally:
        cur.close(); db.close()

# ------------------ DELETE a student ------------------
@app.route('/students/<int:sno>', methods=['DELETE'])
def delete_student(sno):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM STUDENTSINFO WHERE SNO = %s", (sno,))
    if cursor.fetchone() is None:
        return jsonify({"error": "Student not found"}), 404
    try:
        cursor.execute("DELETE FROM STUDENTSINFO WHERE SNO = %s", (sno,))
        db.commit()
        return jsonify({"message": f"Student with SNO {sno} deleted successfully"})
    finally:
        cursor.close()
        db.close()

# ------------------ Run ------------------
if __name__ == '__main__':
    app.run(debug=True)
