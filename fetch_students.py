import mysql.connector

print("🎉 Script started")
print("🔄 Trying to connect to MySQL using TCP/IP...")

try:
    # Connect to MySQL (XAMPP defaults)
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",           # Leave empty for XAMPP
        database="college"     # Your DB name in phpMyAdmin
    )

    if connection.is_connected():
        db_info = connection.get_server_info()
        print(f"✅ Connected to MySQL Server version {db_info}")

        cursor = connection.cursor()

        # Check which DB is selected
        cursor.execute("SELECT DATABASE();")
        current_db = cursor.fetchone()
        print(f"📌 Using database: {current_db[0]}")

        # Query data from studentsinfo table
        print("📄 Fetching data from 'studentsinfo' table:")
        sql = "SELECT SNO, FIRST_NAME, SECOND_NAME, DEPT, CGPA, AGE FROM studentsinfo"
        cursor.execute(sql)

        # Display column headers
        column_names = [desc[0] for desc in cursor.description]
        print("🧾 Columns:", column_names)

        # Fetch and display rows
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("⚠️ No data found in 'studentsinfo' table.")

except mysql.connector.Error as err:
    print(f"❌ MySQL Error: {err}")

finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("🔒 MySQL connection closed.")
print("🎉 Script completed successfully.")