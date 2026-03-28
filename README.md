# 🚀 Master Software Testing Project (Flask API + CI/CD)

[![CI Pipeline](https://img.shields.io/github/actions/workflow/status/Chonthee/master-testing-project/ci.yml?branch=master&label=CI%20Pipeline&style=for-the-badge)](https://github.com/Chonthee/master-testing-project/actions)

โปรเจกต์นี้เป็นส่วนหนึ่งของรายวิชาการทดสอบซอฟต์แวร์ (Software Testing) โดยเน้นการสร้างระบบ **Automated Testing Pipeline** ระดับ Enterprise ที่มีความทนทานสูงและทำงานอัตโนมัติบนระบบ Cloud (GitHub Actions) 

## 🌟 Key Features & Testing Strategy

ระบบนี้ใช้การทดสอบแบบผสมผสาน (Hybrid Testing) เพื่อให้ครอบคลุมทุกมิติของคุณภาพซอฟต์แวร์:

- **Backend Framework:** Flask API พร้อมระบบจัดการข้อมูลผู้ใช้ (PostgreSQL ผ่าน SQLAlchemy)
- **Stage 1 - Code Quality:** ใช้ [Ruff](https://github.com/astral-sh/ruff) ตรวจสอบความสะอาดของโค้ดและมาตรฐาน (Linting)
- **Stage 2 - Integration Testing:** ใช้ [Testcontainers](https://testcontainers.com/) ร่วมกับ Pytest เพื่อ Spin-up ฐานข้อมูล PostgreSQL ของจริงใน Docker ระหว่างการทดสอบ (แก้ปัญหา Environment Mismatch)
- **Stage 3 - API Fuzzing (Robustness):** ใช้ [Schemathesis](https://schemathesis.readthedocs.io/) สุ่มยิงข้อมูลขยะ (Randomized Data) หลายสิบรูปแบบเข้าใส่ API เพื่อหาช่องโหว่ที่ทำให้ Server พัง (No 500 Internal Server Error)
- **Stage 4 - Security Scanning (SAST):** ใช้ [Bandit](https://bandit.readthedocs.io/) สแกน Source Code เพื่อหาช่องโหว่ด้านความปลอดภัยเบื้องต้น (เช่น Hardcoded secrets หรือ SQL Injection)

## 🏗️ Project Structure

```text
.
├── .github/workflows/ci.yml  # การตั้งค่า CI/CD Pipeline บน GitHub Actions
├── tests/                    # โฟลเดอร์เก็บไฟล์ทดสอบ (Integration & Fuzzing)
├── app.py                    # Source Code หลักของ Flask API
├── run_pipeline.py           # สคริปต์ควบคุม Pipeline สำหรับรันในเครื่อง (Local CI)
├── requirements.txt          # รายการ Library ที่จำเป็น
└── .gitignore                # ไฟล์ยกเว้น Artifacts ออกจากระบบ Git
```
## 🚀 How to Run (Local)
เพื่อให้มั่นใจว่าโค้ดทำงานได้สมบูรณ์ก่อนนำขึ้น Cloud แนะนำให้รัน Pipeline ในเครื่องตามขั้นตอนต่อไปนี้:

### 1. Setup Environment
```bash
python -m venv venv
venv\Scripts\activate      # สำหรับ Windows
# source venv/bin/activate # สำหรับ Mac/Linux

pip install -r requirements.txt
```
### 2. Run Local CI Pipeline
```bash
python run_pipeline.py
```
## Automated CI/CD (GitHub Actions)
โปรเจกต์นี้ตั้งค่า Continuous Integration ไว้เรียบร้อยแล้ว ทุกครั้งที่มีการ push หรือ pull_request เข้ามาที่กิ่ง master ระบบ GitHub Actions จะสร้าง Server (Ubuntu) โหลด Docker และรันการทดสอบทั้ง 4 Stages โดยอัตโนมัติ