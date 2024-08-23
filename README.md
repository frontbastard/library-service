# Library Management System

## Description

This project aims to modernize and streamline the operations of a city library by implementing an online management system for book borrowings. The current system, which relies on manual processes and paper-based tracking.

---

## Features

Our Library Management System offers a comprehensive set of features designed to modernize library operations:

### Book Management
- Full CRUD functionality for book records
- Detailed book information including title, author, cover type, and daily fee
- Real-time inventory tracking

### User Management
- User registration and authentication system
- JWT token-based security
- User profile management

### Borrowing System
- Create and manage book borrowings
- Automatic inventory adjustment upon borrowing and return
- Tracking of borrow dates, expected and actual return dates

### Payment Integration
- Seamless integration with Stripe for secure payments
- Support for both regular payments and fines
- Real-time payment status tracking

### Notification System
- Automated notifications via Telegram for:
  - New borrowings
  - Overdue returns
  - Successful payments
- Utilizes Django Q or Celery for efficient background processing

### Advanced Search and Filtering
- Ability to search and filter books based on various criteria
- User-specific borrowing history and active loans

---

## Installing / Getting started

To get the Task Manager up and running, follow these steps:

1. **Install Docker**:
https://www.docker.com/

2. **Clone the Repository**:
    ```bash
    git clone https://github.com/frontbastard/library-service
    cd library-service/
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**:
    Rename the `.env.example` file to `.env` in the root directory and add the necessary environment variables.

5. **Run the Project**:
    ```bash
    docker-compose up --build
    ```
---

## Getting access
- Create user via http://localhost:8001/api/v1/user/register/
- Get access token via http://localhost:8001/api/v1/user/token
- Superuser has been already created with the credentials described in the `.env` file
- Borrowings API http://localhost:8001/api/v1/borrowings/
- Books API http://localhost:8001/api/v1/books/

---

## Swagger
After launching the project, swagger will be available at http://localhost:8001/api/v1/doc/swagger/

---

## Testing
Just use the command:
```bash
 coverage run --source='.' manage.py test
```

---

## Contributing

We welcome contributions to the Task Manager project. To contribute, please fork the repository and create a feature branch. Pull requests are warmly welcome.

---

## Links

- **Repository:** [GitHub Repository](https://github.com/frontbastard/library-service/)
- **Issue Tracker:** [GitHub Issues](https://github.com/frontbastard/library-service/issues/)

---

**Licensing**

The code in this project is licensed under the MIT License.
