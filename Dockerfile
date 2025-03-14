FROM python:3.13.2-slim-bookworm

WORKDIR /app

RUN pip install --no-cache-dir pipenv

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

COPY . .

EXPOSE 5000

#CMD ["python", "app.py"]

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]