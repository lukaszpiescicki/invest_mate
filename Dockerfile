FROM python:3.12
ENV PYTHONUNBUFFERED=1 \
 POETRY_VIRTUALENVS_CREATE=0

WORKDIR /app

COPY pyproject.toml .
COPY poetry.lock .

RUN pip3 install poetry
RUN poetry install --no-root --with dev

COPY . .

RUN sed -i 's/\r$//g' start_flower.sh

RUN chmod +x start_flower.sh

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
