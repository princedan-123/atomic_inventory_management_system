# **User App**


## 📁 App Structure

The `users` app is structured to manage user accounts and their authentication. The key files and their responsibilities are:

-   **`models.py`**: Defines the custom `User` model, extending Django's `AbstractUser` to include additional fields such as `middle_name`, `phone_number`, `email`, `role`, and `profile_image`.
    
-   **`serializers.py`**: Serializes the `User` model for API communication, with custom methods to handle password hashing during user creation and updates.
    
-   **`views.py`**: Contains the API view logic for user authentication (login, logout) and standard user CRUD operations.
    
-   **`urls.py`**: Maps the user-related API endpoints to their corresponding views.
    
-   **`permissions.py`**: Defines custom permission classes (`IsStockManager`, `AdminUser`, `IsAgent`) to control access to different API views based on the user's role.
    

## 👥 Data Models

The app's primary model is the custom `User` model.

### The `User` Model

The `User` model is a single point of truth for all users in the system. It includes fields for:

-   **`email`**: Used as the `USERNAME_FIELD` for authentication.
    
-   **`role`**: A field with choices for `admin`, `stock manager`, and `agent`, which determines the user's permissions across the entire system.
    
-   **`phone_number`**: A unique field for contact information.
    
-   **`profile_image`**: An optional image field for the user's profile picture.
    

## ⚙️ API Endpoints

All endpoints are located under the root URL of your project.

### 1. User Login

HTTP Method

Path

Authentication

Description

**POST**

`/login/`

None

Authenticates a user using `email` and `password`, returning a token on success.

**Example Request**

```
{
    "email": "user@example.com",
    "password": "yourpassword"
}

```

### 2. User Logout

HTTP Method

Path

Authentication

Description

**GET**

`/logout/`

Required

Deletes the user's current authentication token, logging them out of the system.

### 3. User CRUD Operations

HTTP Method

Path

Permissions

Description

**GET**

`/user/`

Admin

Lists all users in the system, with pagination.

**POST**

`/user/`

Admin

Creates a new user account, hashing the provided password.

**GET**

`/user/{id}/`

Admin

Retrieves details for a specific user by their ID.

**PUT/PATCH**

`/user/{id}/`

Admin

Updates an existing user's details, including the ability to change the password.

**DELETE**

`/user/{id}/`

Admin

Deletes a user account from the system.

## 🚀 Getting Started

1.  **Run Migrations:** Ensure the database schema is updated to include the custom `User` model.
    
2.  **Create an Admin User:** Use `python manage.py createsuperuser` to create your first `admin` user.
    
3.  **Test the Endpoints:** Use an API client like Postman or Insomnia to test the login and user CRUD functionalities.
    
4.  **Assign Roles:** Log in as the `admin` user to create other users with different roles (`stock manager`, `agent`) to test the permission-based access control.
    

For detailed API documentation, including request/response examples and data models, refer to the main project's API Documentation.