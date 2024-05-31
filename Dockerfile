# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
#RUN apt-get update && apt-get install -y \
    #libpq-dev \
    #gcc \
    #&& apt-get clean

# Install Python dependencies
#COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install asgiref
RUN pip install bleach==6.1.0
RUN pip install certifi==2024.2.2
RUN pip install charset-normalizer==3.3.2
RUN pip install colorama==0.4.6
RUN pip install django-widget-tweaks==1.5.0
RUN pip install gunicorn
RUN pip install idna
RUN pip install paytmchecksum
RUN pip install pillow
RUN pip install pypng
RUN pip install python-dateutil
RUN pip install pytz
RUN pip install qrcode
RUN pip install setuptools
RUN pip install six
RUN pip install sqlparse
RUN pip install typing_extensions
RUN pip install tzdata
RUN pip install urllib3
RUN pip install webencodings
RUN pip install whitenoise
RUN pip install Django
RUN pip install psycopg2-binary
RUN pip install requests
#RUN pip install pandas
RUN pip install numpy
RUN pip install pandas
# Add the rest of the code
COPY . /app/
# Add the rest of the code
# Create static and media directories if they don't exist
RUN mkdir -p /etc/letsencrypt/live/tetregu.com/

RUN mkdir -p /app/static
RUN mkdir -p /app/media

# Update the STATIC_ROOT directory path
RUN mkdir -p /app/realestate/static

# Copy static files to the expected location
COPY ./realestate/static /app/realestate/static
COPY certificates/archive/tetregu.com/fullchain1.pem /etc/letsencrypt/live/tetregu.com/fullchain.pem
COPY certificates/archive/tetregu.com/privkey1.pem /etc/letsencrypt/live/tetregu.com/privkey.pem
# Run collectstatic to gather all static files
RUN python manage.py collectstatic --noinput

# Make port 8200 available to the world outside this container
EXPOSE 8200

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8200", "realestate.wsgi:application"]