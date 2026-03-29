import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

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
@app.route("/openapi.json")
def openapi_spec():
    """
    สร้างแผนผัง API แบบง่ายๆ เพื่อให้ Schemathesis อ่านไปใช้ทำ Fuzzing ได้
    """
    return jsonify({
        "openapi": "3.0.0",
        "info": {"title": "Master Project API", "version": "1.0.0"},
        "paths": {
            "/users": {
                "get": {
                    "responses": {"200": {"description": "List users"}}
                },
                "post": {
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "email": {"type": "string"}
                                    },
                                    "required": ["name", "email"]
                                }
                            }
                        }
                    },
                    "responses": {"201": {"description": "User created"}}
                }
            }
        }
    })


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data or 'username' not in data or 'email' not in data:
        return jsonify({'error': 'Missing required fields: username, email'}), 400
    
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
    db_password = "mySuperSecretPassword123"
    app.run(host='0.0.0.0', port=5000)  # nosec B104