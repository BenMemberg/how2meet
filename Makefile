
.PHONY: run_server
run_server:
	@uvicorn how2meet.main:app --reload --log-level info --port ${PORT} --host ${HOST}
