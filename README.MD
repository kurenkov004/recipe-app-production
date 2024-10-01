# Recipe App (Web Application Version)

This project is part of careerFoundry's Python for Web Developers Specialization course.
The main goal is to use the Django framework to develop a web application with multiple users and an admin panel.

This app specifically is a Recipe web app which can create, read, and modify recipes, as well as search for recipes by ingredients. It also includes an admin panel on the backend for data handling and visualization.

## Technical Requirements
- Python 3.6+ and Django 3
- PostgreSQL for production and SQLite for development database connectivity
- Code documentation and automated tests hosted on GitHub

##  Key Features
- allows for user authentication, login, logout
- users can search for recipes by ingredients
- each recipe is automatically rated by difficulty level
- more recipe details displayed per user request
- app receives user input and handles errors effectively
- user-added recipes sorted in a SQLite3 database
- Django Admin dashboard included
- shows statistics and visualizations based on trends and data analysis

## Set up and installation

### 1. Clone the repository:
```
git clone [repository URL] cd recipe-app
```

### 2. Install dependencies:
```
pip install -r requirements.txt
```

### 3. Set up database:
Adjust ```Databases``` configuration in ```settings.py``` as per your development and production environments.

### 4. Run migrations
```
py manage.py migrate
```

### 5. Create Superuser for admin access:
```
py manage.py createsuperuser
```

### 6. Run development server:
```
py manage.py runserver
```

- Development server can be acessed at ```http://127.0.0.1:8000``` in your browser.