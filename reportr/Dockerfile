FROM python:3.11-slim

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Generate any migrations required
RUN python manage.py makemigrations

# Run any  required migrations
RUN python manage.py migrate

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "reportr.wsgi:application"]