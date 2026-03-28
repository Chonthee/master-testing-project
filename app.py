import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 💡 ทริคสำคัญ: เราใช้ Environment Variable รับค่า URL ของ Database 
# เพื่อเปิดทางให้ Testcontainers สามารถเอา URL ของ Database ชั่วคราวมาเสียบแทนได้ตอนรันเทสต์!
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///:memory:')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- สร้างตารางจำลองใน Database ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# สร้างตารางเมื่อเริ่มรันแอป
with app.app_context():
    db.create_all()

# --- API Endpoints ---

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # ดักจับ Error เบื้องต้น
    if not data or 'username' not in data or 'email' not in data:
        return jsonify({'error': 'Missing required fields: username, email'}), 400
    
    # เพิ่มลง Database
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'id': new_user.id, 'username': new_user.username}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [{'id': u.id, 'username': u.username, 'email': u.email} for u in users]
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)