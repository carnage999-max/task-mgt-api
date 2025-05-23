# Task Management API

A simple yet robust Task Management API built with Django REST Framework and Celery, designed to handle user tasks with features such as scheduling, deadline notifications via email, and timezone-aware deadlines.

---

## Features

* User authentication (JWT-based)
* Create, read, update, and delete tasks
* Searching and filtering of tasks
* Task Rescheduling
* Tasks with deadlines stored in timezone-aware format (UTC)
* Automatic marking of tasks as completed when deadlines are reached
* Reminder and due notification emails sent asynchronously using Celery
* API endpoints follow RESTful conventions
* Proper handling of timezone-naive and timezone-aware datetime inputs

---

## Technology Stack

* Python 3.12.4
* Django & Django REST Framework
* Celery with Redis (or your choice of broker) for asynchronous task processing
* PostgreSQL / MySQL (or any Django-supported DB)
* JWT Authentication (`djangorestframework-simplejwt`)
* Docker (optional, for local development)

---

## Getting Started

### Prerequisites

* Python 3.12+
* Redis (for Celery broker)
* Database (PostgreSQL)
* Docker (optional)

### Installation

1. Clone the repo:

   ```bash
   git clone https://github.com/carnage999-max/task-mgt-api.git
   cd task-mgt-api
   ```

2. Create and activate a virtual environment:

* Using venv:
  
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

   Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

* Using ``` pipenv ```(Recommended):
  
  ```bash
   pipenv install
   pipenv shell
  ```

1. Set up environment variables in `.env` file (e.g., database credentials, email settings, Celery broker URL)

2. Run migrations:

   ```bash
   python manage.py migrate
   ```

3. Start Redis server (or your Celery broker)

4. Run Celery worker:

   ```bash
   celery -A project_name worker --loglevel=info
   ```

5. Run the development server:

   ```bash
   python manage.py runserver
   ```

---

## API Usage

### Authentication

* Obtain JWT tokens via `/api/token/` and `/api/token/refresh/`
* Include the access token in the `Authorization` header as `Bearer <token>` for authenticated endpoints

### Tasks Endpoints

| Endpoint           | Method | Description                |
| ------------------ | ------ | -------------------------- |
| `/api/tasks/`      | GET    | List all tasks of the user |
| `/api/tasks/`      | POST   | Create a new task          |
| `/api/tasks/{id}/` | GET    | Retrieve a specific task   |
| `/api/tasks/{id}/` | PUT    | Update a specific task     |
| `/api/tasks/{id}/` | DELETE | Delete a specific task     |

---

## Key Implementation Details

* **Timezone Handling:** Deadlines sent from clients are expected to include timezone information (ISO 8601 format). The backend converts and stores all deadlines in UTC.
* **Task Scheduling:** Celery schedules tasks to automatically mark tasks as completed when their deadlines are reached and sends notification emails asynchronously.
* **Email Notifications:** Users receive emails when their tasks are due. Email sending is managed by Celery to avoid blocking API responses.

---

## Future Improvements

* Add support for task priorities and labels
* Implement social login (OAuth) for easier authentication
* Add webhook integrations (Telegram, Discord) for notifications
* Expand notifications with SMS or push notifications
* Build frontend client with React or React Native

---

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

## License

MIT License

---

## Contact

Your Name — [your.email@example.com](mailto:your.email@example.com)
GitHub: [https://github.com/yourusername](https://github.com/yourusername)

---

If you want, I can help customize any section or generate a `requirements.txt` snippet as well!
