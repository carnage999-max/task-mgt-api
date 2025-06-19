# Task Management API

A simple yet robust Task Management API built with Django REST Framework and Celery, designed to handle user tasks with features such as scheduling, deadline notifications via email and Telegram, and timezone-aware deadlines.

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
    - [Telegram Notifications](#telegram-notifications) <!-- NEW -->
    - [Sample Requests & Responses](#sample-requests--responses)
      - [Create Task](#create-task)
      - [Retrieve Task](#retrieve-task)
      - [Delete Task](#delete-task)
      - [Task Rescheduling](#task-rescheduling)
      - [Update Telegram Chat ID](#update-telegram-chat-id)
  - [Future Improvements](#future-improvements) <!-- MODIFIED -->
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
- Telegram notifications for task deadlines (opt-in) <!-- NEW -->
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

3. Set up environment variables in `.env` file (e.g., database credentials, email settings, Celery broker URL, Telegram bot token) <!-- MODIFIED -->

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

- Obtain JWT tokens (login) via:

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

| Endpoint                          | Method | Description                        |
|-----------------------------------|--------|------------------------------------|
| `/api/v1/task/tasks/`             | GET    | List all user tasks                |
| `/api/v1/task/tasks/`             | POST   | Create a new task                  |
| `/api/v1/task/tasks/{id}/`        | GET    | Retrieve a specific task           |
| `/api/v1/task/tasks/{id}/`        | PUT    | Update a specific task             |
| `/api/v1/task/tasks/{id}/`        | DELETE | Delete a specific task             |
| `/api/v1/task/tasks/{id}/mark_complete/` | PATCH | Mark a specific task as "completed" |

---

### Telegram Notifications <!-- NEW -->

Users can opt to receive Telegram notifications for task deadlines. To enable this feature, follow these steps:

1. **Obtain Your Telegram Chat ID**:
   - Open Telegram and message `@userinfobot`. Send `/start` to receive your chat ID (e.g., `0027981002`).

2. **Initiate a Session with the Telegram Bot**:
   - Message the API’s Telegram bot at `@BinaryTaskReminder_bot` (replace with the actual bot username provided by the API response).
   - Send `/start` to allow the bot to send you notifications. This is a Telegram requirement.

3. **Update Your Profile**:
   - Send a POST request to the `/api/v1/users/update-telegram-chat-id/` endpoint with your chat ID and notification preference.
   - See the [Update Telegram Chat ID](#update-telegram-chat-id) section for details.

4. **Receive Notifications**:
   - When a task’s deadline is reached, you’ll receive a Telegram message (e.g., “Reminder: Task 'Finish report' deadline reached on 2025-06-01 15:00!”) if notifications are enabled.

**Note**: Ensure you send `/start` to `@BinaryTaskReminder_bot` before enabling notifications, or the bot will return a “chat not found” error.

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
  "name": "Finish report",
  "description": "Weekly summary report",
  "deadline": "2025-06-01T15:00:00+01:00",
  "priority": "high"
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

Response (204 No Content)

---

#### Task Rescheduling

Task can be rescheduled by sending a `PUT` request to the API and updating the deadline. Tasks with `status` of `completed` cannot be updated.

```http
PUT /api/v1/task/tasks/1/
Authorization: Bearer <access_token>
```

Request Body:

```json
{
  "deadline": "2026-06-01T15:00:00+01:00"
}
```

Response (200 OK):

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

---

#### Update Telegram Chat ID <!-- NEW -->

```http
POST /api/v1/users/update-telegram-chat-id/
Authorization: Bearer <access_token>
Content-Type: application/json
```

Request Body:

```json
{
  "chat_id": "1234567890",
}
```

Response (200 OK):

```json
{
  "message": "Telegram chat ID and notification preference updated",
}
```

**Notes**:
- `telegram_chat_id`: Your Telegram chat ID (required if `receive_telegram_notifications` is `true`).
- `receive_telegram_notifications`: Set to `true` to enable Telegram notifications (default: `false`).
- After sending this request, message `@YourBotName` in Telegram and send `/start` to allow notifications.
- If `receive_telegram_notifications` is set to `false`, no Telegram notifications will be sent, even if a `telegram_chat_id` is provided.

---

## Key Implementation Details <!-- MODIFIED -->

- **Timezone Handling**: Deadlines sent from clients are expected to include timezone information (ISO 8601 format). The backend converts and stores all deadlines in UTC.
- **Task Scheduling**: Celery schedules tasks to automatically mark tasks as completed when their deadlines are reached and sends notification emails and Telegram messages asynchronously.
- **Email Notifications**: Users receive emails when their tasks are due. Email sending is managed by Celery to avoid blocking API responses.
- **Telegram Notifications**: Users who opt in receive Telegram messages when task deadlines are reached. Notifications are sent via the Telegram Bot API using a bot (`@BinaryTaskReminder_bot`). Users must send `/start` to the bot to enable messaging.

---

## Future Improvements <!-- MODIFIED -->

- Add support for Subtasks
- Implement social login (OAuth) for easier authentication
- Add webhook integrations (Discord, Slack) for notifications
- Expand notifications with push notifications
- Automate Telegram bot session initiation via deep links

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