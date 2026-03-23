FROM python:3.14-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./backend /code/backend

CMD ["fastapi", "run", "backend/src/main.py", "--port", "8000", "--host", "0.0.0.0"]