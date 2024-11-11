FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBUG=0

WORKDIR /usr/src/insurance-reportr-project/reportr

COPY reportr .
RUN pip install --no-cache-dir -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

# Generate any migrations required
RUN python manage.py makemigrations

# Run any  required migrations
RUN python manage.py migrate

# Generate default admin user (admin|admin)
RUN python manage.py generatedefaultsuperuser

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "reportr.wsgi:application"]
