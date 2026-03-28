import os
import subprocess

def run_command(command, stage_name):
    # (โค้ดฟังก์ชัน run_command เหมือนเดิม ไม่ต้องแก้)
    print(f"\n{'='*60}")
    print(f"🚀 เริ่มด่าน: {stage_name}")
    print(f"{'='*60}")
    
    result = subprocess.run(command, shell=True)
    
    if result.returncode != 0:
        print(f"\n❌ [FAIL] ด่าน {stage_name} ไม่ผ่าน! Pipeline ถูกบังคับหยุดทำงาน ❌")
        exit(1)
        
    print(f"\n✅ [PASS] ด่าน {stage_name} ผ่านฉลุย!")

if __name__ == "__main__":
    print("🛠️  Starting Local CI Pipeline (Cross-Platform)...")
    
    # ---------------------------------------------------------
    # ด่าน 1: Code Quality & Security Scan (Ruff)
    # ---------------------------------------------------------
    # เปลี่ยนจาก bandit มาใช้ ruff แทน ทำงานไวปานสายฟ้าแลบ
    run_command("ruff check app.py", "Stage 1: Code Quality & Security Scan (Ruff)")
    
    # ---------------------------------------------------------
    # ด่าน 2: Integration Testing
    # ---------------------------------------------------------
    run_command("python -m pytest -v tests/", "Stage 2: Integration Tests (Testcontainers)")
    
    print("\n🎉 Pipeline Completed Successfully! โค้ดชุดนี้ปลอดภัย พร้อม Commit แล้ว! 🎉\n")