import os
import MySQLdb
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

DB_CONFIG = {
    'host': os.environ.get('MYSQL_HOST', 'localhost'),
    'user': os.environ.get('MYSQL_USER', 'default_user'),
    'passwd': os.environ.get('MYSQL_PASSWORD', 'default_password'),
    'db': os.environ.get('MYSQL_DB', 'default_db'),
}

print("✅ DB Config:")
print("Host:", DB_CONFIG['host'])
print("User:", DB_CONFIG['user'])
print("DB:  ", DB_CONFIG['db'])

def get_db():
    return MySQLdb.connect(**DB_CONFIG)

def init_db():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                message TEXT
            );
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Table created or already exists.")
    except Exception as e:
        print("❌ DB init error:", e)

@app.route('/')
def hello():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT message FROM messages')
        messages = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('index.html', messages=messages)
    except Exception as e:
        return f"❌ Error loading messages: {e}"

@app.route('/submit', methods=['POST'])
def submit():
    try:
        new_message = request.form.get('new_message')
        conn = get_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': new_message})
    except Exception as e:
        return f"❌ Error submitting message: {e}"

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
