# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean

# Install Python dependencies
#COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install asgiref==3.2.10
RUN pip install certifi==2024.2.2
RUN pip install charset-normalizer==3.3.2
RUN pip install Django==3.1.1
RUN pip install gunicorn==20.0.4
RUN pip install idna==3.7
RUN pip install numpy==1.24.4
RUN pip install pandas==2.2.2
RUN pip install paytmchecksum==1.7.0
RUN pip install pillow==10.3.0
RUN pip install psycopg2==2.9.9
RUN pip install python-dateutil==2.9.0.post0
RUN pip install pytz==2020.1
RUN pip install requests==2.31.0
RUN pip install six==1.16.0
RUN pip install sqlparse==0.3.1
RUN pip install tzdata==2024.1
RUN pip install urllib3==2.2.1
RUN pip install whitenoise==5.2.0

# Add the rest of the code
COPY . /app/
# Add the rest of the code
# Create static and media directories if they don't exist
RUN mkdir -p /app/static
RUN mkdir -p /app/media

# Update the STATIC_ROOT directory path
RUN mkdir -p /app/realestate/static

# Copy static files to the expected location
COPY ./realestate/static /app/realestate/static

# Run collectstatic to gather all static files
RUN python manage.py collectstatic --noinput

# Make port 8200 available to the world outside this container
EXPOSE 8200

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8200", "realestate.wsgi:application"]