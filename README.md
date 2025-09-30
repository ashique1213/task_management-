# Task Management Application with Task Completion Report

## 1. API Endpoints (Create endpoints only, no need to integrate)
### User Authentication
- **JWT Authentication**: Implement JSON Web Token (JWT) authentication for the User API to ensure secure access.
  - Users can authenticate via username and password, receiving a JWT token for further requests.

### Tasks APIs
- **GET /tasks**: Fetch all tasks assigned to the logged-in user.
  - Only returns tasks for the logged user who is sending the request.
- **PUT /tasks/{id}**: Allows users to update the status of a task (mark it as Completed).
  - When setting a task status to Completed, users are required to submit a Completion Report and the number of Worked Hours.
- **GET /tasks/{id}/report**: Admins and SuperAdmins can view the Completion Report and Worked Hours for a specific task.
  - This is only available for tasks that are marked as Completed.

## 2. Admin Panel (Web Application for Admin and SuperAdmin – Create your own admin panel using HTML templates)
### SuperAdmin Features
- Can view and manage all users (create, delete, assign roles).
- Can view and manage all admins (create, delete, assign roles).
- Can assign users to admins.
- Can view and manage all tasks across users.
- Can view task reports submitted by users.

### Admin Features
- Can assign tasks to their users.
- Can view and manage tasks assigned to their users.
- Can view the completion reports submitted by users (including worked hours).
- Cannot manage user roles but can manage tasks within their scope.

## 3. Task Workflow
### Roles and Permissions
- **SuperAdmin**:
  - Can manage admin (create, delete, assign roles, and promote/demote admin).
  - Can manage users (create, delete, update).
  - Can access the full Admin panel with all privileges.
- **Admin**:
  - Can create, assign, view, and manage tasks.
  - Can view task completion reports for tasks assigned to users.
  - Has limited access to the Admin panel: Can manage tasks but not users.
- **User**:
  - Can view their assigned tasks, update their task status, and submit a completion report (including worked hours).
  - Can only interact with their own tasks through the User API.


## Setup Instructions
1. **Clone the Repository**:
   - Clone the project directory structure as provided in the implementation.

2. **Install Dependencies**:
   - Ensure you have Python installed.
   - Create a virtual environment: `python -m venv venv`.
   - Activate the virtual environment:
     - Windows: `venv\Scripts\activate`
     - Mac/Linux: `source venv/bin/activate`
   - Install required packages: `pip install -r requirements.txt`.

3. **Configure the Project**:
   - Update `taskmanagement/settings.py`:
    
     SECRET_KEY = config("SECRET_KEY")
     DEBUG = config("DEBUG", default=False, cast=bool)
     ALLOWED_HOSTS = config("ALLOWED_HOSTS")

   - Ensure the database is set to SQLite (default in `settings.py`).

4. **Apply Migrations**:
   - Run `python manage.py makemigrations` to create migration files.
   - Run `python manage.py migrate` to apply migrations to the database.

5. **Create a SuperAdmin User**:
   - Run `python manage.py createsuperuser` and follow the prompts to set a username, email, and password.
   - Manually set the role to 'superadmin' via Django shell:
     - `python manage.py shell`
     - `from authentication.models import User; user = User.objects.get(username='your_username'); user.role = 'superadmin'; user.save()`

6. **Run the Server**:
   - Start the development server: `python manage.py runserver`.
   - Access the application at `http://127.0.0.1:8000/`.

## Usage
- **User API Testing**:
  - Use Postman to test API endpoints with JWT authentication (see separate instructions for Postman setup).
  - Obtain a token via `POST /api/token/` with username and password.
  - Use the token to access `GET /tasks`, `PUT /tasks/{id}`, and attempt `GET /tasks/{id}/report` (restricted).

#### 1. User Authentication (Obtain JWT Token)
- **Endpoint**: `http://127.0.0.1:8000/api/token/`
- **Method**: `POST`
- **Body** (raw JSON):
  ```json
  {
      "username": "testuser",
      "password": "password123"
  }
  ```
- **Expected Response**:
  ```json
  {
      "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...your_refresh_token",
      "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...your_access_token"
  }
  ```
  - Copy the `access` token for use in subsequent requests.

#### 2. Test GET /tasks (Fetch All Tasks Assigned to the Logged-in User)
- **Endpoint**: `http://127.0.0.1:8000/api/tasks/`
- **Method**: `GET`
- **Headers**: 
  - Key: `Authorization`
  - Value: `Bearer your_access_token` (replace with the token from step 1)

  ```json
  [
      {
          "id": 1,
          "title": "Complete Report",
          "description": "Finish the task report",
          "assigned_to": 1,
          "due_date": "2025-10-15",
          "status": "Pending",
          "completion_report": null,
          "worked_hours": null
      },
      {
          "id": 2,
          "title": "Update Documentation",
          "description": "Update project docs",
          "assigned_to": 1,
          "due_date": "2025-10-10",
          "status": "In Progress",
          "completion_report": null,
          "worked_hours": null
      }
  ]
  ```

#### 3. Test PUT /tasks/{id} (Update Task Status, Including Marking as Completed)
- **Endpoint**: `http://127.0.0.1:8000/api/tasks/1/` 
- (replace `1` with the task ID, e.g., 1 for "Complete Report")
- **Method**: `PUT`
- **Headers**: 
  - Key: `Authorization`
  - Value: `Bearer your_access_token`
- **Body** (raw JSON):
  - To update status to "In Progress":
    ```json
    {
        "status": "In Progress"
    }
    ```
  - To mark as "Completed" (requires `completion_report` and `worked_hours`):
    ```json
    {
        "status": "Completed",
        "completion_report": "Task completed successfully, no major challenges faced.",
        "worked_hours": 4.5
    }
    ```
- **Expected Response** (after marking as Completed):
  ```json
  {
      "id": 1,
      "title": "Complete Report",
      "description": "Finish the task report",
      "assigned_to": 1,
      "due_date": "2025-10-15",
      "status": "Completed",
      "completion_report": "Task completed successfully, no major challenges faced.",
      "worked_hours": 4.5
  }
  ```
  - If `completion_report` or `worked_hours` is missing when setting to "Completed", you’ll get a `400 Bad Request` error.

#### 4. Test GET /tasks/{id}/report (Restricted Endpoint)
- **Endpoint**: `http://127.0.0.1:8000/api/tasks/1/report/` (replace `1` with the task ID)
- **Method**: `GET`
- **Headers**: 
  - Key: `Authorization`
  - Value: `Bearer your_access_token`
- **Expected Response**: 
  - A `403 Forbidden` error, as this endpoint is restricted to Admins and SuperAdmins. Example:
    ```json
    {
        "error": "Not authorized"
    }
    ```

- **Admin Panel**:
  - Log in at `http://127.0.0.1:8000/` with SuperAdmin or Admin credentials.
  - SuperAdmins can manage users, admins, and tasks; Admins can manage tasks and view reports for their users.

## Notes
- Use SQLite as the database.
- The `requirements.txt` file must be included with the necessary packages.
- Read the task carefully. If you have any doubts, feel free to ask at any time.