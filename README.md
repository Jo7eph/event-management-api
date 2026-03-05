# Event Management API

## Project Overview
The Event Management API is a backend service built using **Django** and **Django REST Framework**.  
It allows users to browse events publicly while authenticated users can create, manage, and register for events.

Authentication is implemented using **JWT (JSON Web Tokens)** and the API supports filtering, searching, and event registration.

---

# Key Features

### Public Access
- View all events
- View event details
- Filter upcoming events

### Authentication
- User registration
- JWT login authentication

### Event Management
- Create events (authenticated users)
- Update events (organizer only)
- Delete events (organizer only)

### Event Registration
- Register for events
- Unregister from events

---

# Tech Stack

- Python
- Django
- Django REST Framework
- SimpleJWT
- SQLite

---

# Installation

Clone the repository

```bash
git clone https://github.com/Jo7eph/Alx_DjangoLearnLab.git
cd Alx_DjangoLearnLab/event_api

## API Endpoints

### Authentication

POST /api/auth/register/
Register a new user

POST /api/auth/token/
Login and obtain JWT tokens

---

### Events

GET /api/events/
List all events

POST /api/events/
Create a new event (requires authentication)

GET /api/events/{id}/
Retrieve event details

PUT /api/events/{id}/
Update event (organizer only)

DELETE /api/events/{id}/
Delete event (organizer only)

---

### Event Registration

POST /api/events/{id}/register/
Register for an event

POST /api/events/{id}/unregister/
Cancel event registration