
.PHONY: run_server
run_server:
	@uvicorn main:app --reload --log-level debug --port 8000