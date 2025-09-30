# Task Management Application with Task Completion Report

We are enhancing the Task Management Application by allowing users to submit a short report and their worked hours when they complete a task. This will help track what was done on each task and how much time it took.

- When users mark a task as completed, they must also submit a Completion Report and Worked Hours.
- These reports will be visible to Admins and SuperAdmins for review and monitoring.
- This feature makes task tracking more transparent and improves accountability.

Develop API endpoints and an Admin Panel utilizing Python and Django to enhance task management functionality.

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
   - Update `taskmanagement/settings.py` with a secure `SECRET_KEY`.
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

- **Admin Panel**:
  - Log in at `http://127.0.0.1:8000/` with SuperAdmin or Admin credentials.
  - SuperAdmins can manage users, admins, and tasks; Admins can manage tasks and view reports for their users.

## Notes
- Use SQLite as the database.
- The `requirements.txt` file must be included with the necessary packages.
- Read the task carefully. If you have any doubts, feel free to ask at any time.