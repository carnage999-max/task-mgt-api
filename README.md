# Task Management API

A simple yet robust Task Management API built with Django REST Framework and Celery, designed to handle user tasks with features such as scheduling, deadline notifications via email, and timezone-aware deadlines.

---

## Table of Contents

- [Task Management API](#task-management-api)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Technology Stack](#technology-stack)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [API Usage](#api-usage)
    - [Authentication](#authentication)
    - [Tasks Endpoints](#tasks-endpoints)
    - [Sample Requests \& Responses](#sample-requests--responses)
      - [Create Task](#create-task)
      - [Retrieve Task](#retrieve-task)
      - [Delete Task](#delete-task)
      - [Task Rescheduling](#task-rescheduling)
  - [Key Implementation Details](#key-implementation-details)
  - [Future Improvements](#future-improvements)
  - [Contributing](#contributing)
  - [License](#license)
  - [Contact](#contact)

---

## Features

- User authentication (JWT-based)
- Create, read, update, and delete tasks
- Searching and filtering of tasks
- Task Rescheduling
- Tasks with deadlines stored in timezone-aware format (UTC)
- Automatic marking of tasks as completed when deadlines are reached
- Reminder and due notification emails sent asynchronously using Celery
- API endpoints follow RESTful conventions
- Proper handling of timezone-naive and timezone-aware datetime inputs

---

## Technology Stack

- Python 3.12.4
- Django & Django REST Framework
- Celery with Redis (or your choice of broker) for asynchronous task processing
- PostgreSQL / MySQL (or any Django-supported DB)
- JWT Authentication (`djangorestframework-simplejwt`)

---

## Getting Started

### Prerequisites

- Python 3.12+
- Redis (for Celery broker)
- Database (PostgreSQL)
- Docker (optional)

### Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/carnage999-max/task-mgt-api.git
   cd task-mgt-api
   ```

2. Create and activate a virtual environment:

- Using venv:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

   Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

- Using pipenv (Recommended):

  ```bash
   pipenv install
   pipenv shell
  ```

3. Set up environment variables in `.env` file (e.g., database credentials, email settings, Celery broker URL)

4. Run migrations:

   ```bash
   python manage.py migrate
   ```

5. Start Redis server (or your Celery broker)

6. Run Celery worker:

   ```bash
   celery -A project_name worker --loglevel=info
   ```

7. Run the development server:

   ```bash
   python manage.py runserver
   ```

---

## API Usage

### Authentication

- Obtain JWT tokens(login) via:

   ```http
   POST /api/v1/users/login/
   ```

   Request:

   ```json
   {
     "email": "johndoe@email.com",
     "password": "secretpassword"
   }
   ```

   Response (200 OK):

   ```json
   {
     "access": "<access_token>",
     "refresh": "<refresh_token>"
   }
   ```

- Refresh token:

   ```http
   POST /api/token/refresh/
   ```

- Include the access token in the `Authorization` header:

   ```
   Authorization: Bearer <token>
   ```

---

### Tasks Endpoints

| Endpoint                 | Method | Description                |
|--------------------------|--------|----------------------------|
| `/api/v1/task/tasks/`    | GET    | List all user tasks        |
| `/api/v1/task/tasks/`    | POST   | Create a new task          |
| `/api/v1/task/tasks/{id}/` | GET  | Retrieve a specific task   |
| `/api/v1/task/tasks/{id}/` | PUT  | Update a specific task     |
| `/api/v1/task/tasks/{id}/` | DELETE| Delete a specific task     |
| `/api/v1/task/tasks/{id}/mark_complete/` | PATCH| Mark a specific task as "completed"     |

---

### Sample Requests & Responses

#### Create Task

```http
POST /api/v1/task/tasks/
Authorization: Bearer <access_token>
Content-Type: application/json
```

Request Body:

```json
{
  "name": "Finish report", // Required 
  "description": "Weekly summary report",
  "deadline": "2025-06-01T15:00:00+01:00",
  "priority": "high" // possible values are high, low, medium, urgent
}
```

Response (201 Created):

```json
{
  "id": 1,
  "user": 1,
  "name": "Finish Report",
  "description": "Weekly summary report",
  "deadline": "2025-06-01T15:00:00+01:00",
  "status": "in_progress",
  "priority": "high",
  "created_at": "datetime",
  "updated_at": "datetime",
  "user_email": "useremail@gmail.com"
}
```

---

#### Retrieve Task

```http
GET /api/v1/task/tasks/1/
Authorization: Bearer <access_token>
```

Response (200 OK):

```json
{
  "id": 1,
  "user": 1,
  "name": "Finish Report",
  "description": "Weekly summary report",
  "deadline": "2025-06-01T15:00:00+01:00",
  "status": "in_progress",
  "priority": "high",
  "created_at": "datetime",
  "updated_at": "datetime",
  "user_email": "useremail@gmail.com"
}
```

---

#### Delete Task

```http
DELETE /api/v1/task/tasks/1/
Authorization: Bearer <access_token>
```

Response (200 Ok)

---

#### Task Rescheduling

Task can be rescheduled by sending a `PUT` request to the API and updating the deadline.
Task with `status` of `completed` cannot be updated

```http
   PUT api/v1/task/tasks/1/
   Authorization: Bearer <access_token>
```

Request Body:

```json
   {
      "deadline": "2026-06-01T15:00:00+01:00"
   }
```

Response (200)

```json
   {
   "id": 1,
   "user": 1,
   "name": "Do laundry",
   "description": "Weekly summary report",
   "deadline": "2026-06-01T15:00:00+01:00",
   "status": "in_progress",
   "priority": "high",
   "created_at": "datetime",
   "updated_at": "datetime",
   "user_email": "useremail@gmail.com"
}
```

## Key Implementation Details

- **Timezone Handling:** Deadlines sent from clients are expected to include timezone information (ISO 8601 format). The backend converts and stores all deadlines in UTC.
- **Task Scheduling:** Celery schedules tasks to automatically mark tasks as completed when their deadlines are reached and sends notification emails asynchronously.
- **Email Notifications:** Users receive emails when their tasks are due. Email sending is managed by Celery to avoid blocking API responses.

---

## Future Improvements

- Add support for Subtasks
- Implement social login (OAuth) for easier authentication
- Add webhook integrations (Telegram, Discord) for notifications
- Expand notifications with push notifications

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## License

MIT License

---

## Contact

Ezekiel Okebule — [jamesezekiel039@gmail.com](mailto:jamesezekiel039@gmail.com)

GitHub: [https://github.com/carnage999-max](https://github.com/carnage999-max)

---
