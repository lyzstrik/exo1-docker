from flask import Flask, request
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="db",
        user="flask",
        password="flaskpass",
        database="appdb"
    )

@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = f"SELECT * FROM users WHERE id = {user_id};"
        cursor.execute(query)
        result = cursor.fetchall()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

print("Web server started...")
app.run(host="0.0.0.0", port=8080)
print("Web server stopped.")
