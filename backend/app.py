import os
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL config
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'mysql')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'root')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'testdb')

mysql = MySQL(app)

# Create table
@app.before_first_request
def create_table():
    cur = mysql.connection.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            text VARCHAR(255)
        )
    """)
    mysql.connection.commit()
    cur.close()

# Add message
@app.route('/add', methods=['POST'])
def add_message():
    data = request.json
    msg = data.get('text')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO messages(text) VALUES(%s)", (msg,))
    mysql.connection.commit()
    cur.close()

    return jsonify({"status": "added"})

# Get messages
@app.route('/messages', methods=['GET'])
def get_messages():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM messages")
    data = cur.fetchall()
    cur.close()

    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
