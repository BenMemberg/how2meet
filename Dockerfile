FROM python:3.10-slim

# RUN mkdir /how2meet
WORKDIR /app
COPY . .

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --only main

# Maybe run migrations here? Do we want them to be automatic or manual?
# RUN alembic upgrade head
# ^ Might have to be in an entrypoint script? (That's how a tutorial did it at least)

CMD ["uvicorn", "how2meet.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
