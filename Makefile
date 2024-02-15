
.PHONY: run_server
run_server:
	@uvicorn how2meet.main:app --reload --log-level debug --port 8000 --host 0.0.0.0
