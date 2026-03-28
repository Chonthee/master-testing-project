# --- ตัวแปรและ Config ---
-include .env

RUN_SAST ?= true
RUN_TESTS ?= true

# --- คำสั่งหลัก ---
run-pipeline: run-sast run-tests
	@echo "🎉 Pipeline Completed Successfully! โค้ดชุดนี้พร้อม Commit แล้ว!"

# --- ด่านที่ 1: Security Scan ---
run-sast:
ifeq ($(RUN_SAST),true)
	@echo "🛡️ Stage 1: Running SAST (Bandit)..."
	bandit -r app.py
else
	@echo "⏩ Stage 1: Skipping SAST..."
endif

# --- ด่านที่ 2: Integration Testing ---
run-tests:
ifeq ($(RUN_TESTS),true)
	@echo "🧪 Stage 2: Running Integration Tests (Testcontainers)..."
	python -m pytest -v tests/
else
	@echo "⏩ Stage 2: Skipping Integration Tests..."
endif