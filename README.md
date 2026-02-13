# Event Management API

Backend API built with Django and Django REST Framework.

## Features
- JWT authentication
- Event CRUD (create, list, update, delete)
- Only the organizer can edit/delete their events
- Upcoming events endpoint
- Search & filtering (title, location, date range)
- Pagination

## Setup
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

