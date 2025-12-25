from flask import Flask, render_template, request, jsonify
import mysql.connector
import os
from datetime import datetime

app = Flask(__name__)

# DB Connection
def get_db():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'db'),
        user=os.getenv('DB_USER', 'intel'),
        password=os.getenv('DB_PASSWORD', 'secure123'),
        database=os.getenv('DB_NAME', 'intel_db')
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/gather', methods=['POST'])
def gather_info():
    data = request.json
    target = data.get('target')
    
    # Simulate info gathering (replace with nmap, whois, etc.)
    intel = {
        'target': target,
        'ip': f"{target}.1",  # Simulated
        'ports': ['22/open', '80/open', '443/open'],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'os': 'Linux/Unix'
    }
    
    # Store in DB
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO intel (target, ip, ports, os_info, collected_at) VALUES (%s, %s, %s, %s, %s)",
        (intel['target'], intel['ip'], str(intel['ports']), intel['os'], intel['timestamp'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify(intel)
    # 🚀 AUTO-DEPLOY TEST - Build #${BUILD_NUMBER}
    print("🔥 Security Intel Gathering App - Live from Jenkins CI/CD!")

@app.route('/intel')
def view_intel():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM intel ORDER BY collected_at DESC LIMIT 50")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
