# Real Estate Django Web App

This is a real estate listings website built with Django, designed to be responsive and functional. It utilizes Python, Django, Bootstrap 4, Vanilla JS, and JQuery.

## Features

- Responsive web design
- Integration with PostgreSQL
- Full CRUD functionality for real estate listings
- User authentication and authorization
- Admin panel for managing listings, realtors, and user enquiries

## Prerequisites

- Python 3.6 or higher
- pip
- PostgreSQL

## Setup and Installation

1. **Clone the repository**

   ```sh
   git clone https://github.com/osokuka/realestateapp.git
   ```

2. **Navigate to the project directory**

   ```sh
   cd Real-Estate-Django-Web-App
   ```

3. **Install required Python packages**

      ```sh
      sudo apt-get install wget ca-certificates
      
      wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
      
      # Now add the repository to your system.
      
      sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
      ```

4. **Setup PostgreSQL**

   - Install PostgreSQL and create a database named `real_estate`.
   - Create a user and grant all privileges on the database.

5. **Apply migrations**

   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Run the development server**

   ```sh
   python manage.py runserver
   ```

## Docker and Nginx Configuration

Refer to the provided `docker-compose.yml` and `nginx/nginx.conf` files for setting up the application using Docker and Nginx.

## Deployment

For detailed deployment instructions on a live server, refer to the Docker and Nginx configuration files included in the repository.

## Owner

- **Name:** Real Estate Pro Solutions
- **Email:** realestate@prosolutions-ks.com
- **GitHub Repository:** [Real Estate App](https://github.com/osokuka/realestateapp.git)

## Acknowledgments

Special thanks to all contributors and developers who have worked on this project.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

