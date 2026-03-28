import pytest
from testcontainers.postgres import PostgresContainer

# Import ตัวแอปและ Database จากไฟล์ app.py ของเรา
from app import app, db, User

# ---------------------------------------------------------
# ส่วนที่ 1: ตั้งค่า Fixtures (หัวใจของการทำ Ephemeral Environment)
# ---------------------------------------------------------

@pytest.fixture(scope="session")
def postgres_container():
    """
    ด่านนี้คือความว้าว! เราสั่ง Testcontainers ให้โหลด Docker Image ของ PostgreSQL 
    มาสตาร์ทเป็น Database ชั่วคราว พอเทสต์เสร็จ มันจะปิดและทำลายตัวเองทิ้ง (with statement)
    """
    with PostgresContainer("postgres:15-alpine") as postgres:
        # ส่ง Database URL ของจริงที่เพิ่งสร้างเสร็จกลับไปให้ Flask ใช้งาน
        yield postgres.get_connection_url()

@pytest.fixture
def client(postgres_container):
    """
    เตรียม Flask Test Client และแอบสลับ Database ไปใช้ตัวที่ Testcontainers สร้างมา
    """
    # Override ค่า URL ให้ชี้ไปที่ DB ชั่วคราว
    app.config['SQLALCHEMY_DATABASE_URI'] = postgres_container
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            # สร้างตารางข้อมูลใหม่ทั้งหมดใน DB ชั่วคราว
            db.create_all()
            
            yield client # โยน Client ไปให้ฟังก์ชัน Test ใช้งาน
            
            # ล้างตารางทิ้งให้สะอาดหมดจดเมื่อเทสต์จบ (เตรียมพร้อมสำหรับเทสต์เคสถัดไป)
            db.session.remove()
            db.drop_all()

# ---------------------------------------------------------
# ส่วนที่ 2: เขียน Test Case (จำลองพฤติกรรม User จริง)
# ---------------------------------------------------------

def test_create_user(client):
    """ทดสอบการสร้าง User ใหม่ลง Database"""
    response = client.post('/users', json={
        'username': 'master_student',
        'email': 'student@ku.th'
    })
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['username'] == 'master_student'
    assert 'id' in data

def test_get_users_empty(client):
    """ทดสอบกรณีที่ Database เพิ่งสร้างใหม่และยังไม่มีข้อมูล"""
    response = client.get('/users')
    assert response.status_code == 200
    assert response.get_json() == []

def test_get_users_with_data(client):
    """ทดสอบดึงข้อมูล หลังจากแอบใส่ User จำลองเข้าไปแล้ว"""
    # จำลองยิง API สร้าง User
    client.post('/users', json={'username': 'user1', 'email': 'user1@test.com'})
    client.post('/users', json={'username': 'user2', 'email': 'user2@test.com'})
    
    # ยิง API เพื่อดึงข้อมูลทั้งหมด
    response = client.get('/users')
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['username'] == 'user1'