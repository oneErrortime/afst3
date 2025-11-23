# API Endpoints Reference

This document provides a comprehensive reference of all available API endpoints in the Library Management System backend.

## Authentication Endpoints

### Register
- **Endpoint**: `POST /auth/register`
- **Description**: Register a new user
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword"
  }
  ```
- **Response**: `200 OK`

### Login
- **Endpoint**: `POST /auth/login`
- **Description**: Authenticate user and return JWT token
- **Request Body**:
  ```
  username=user@example.com&password=securepassword
  ```
- **Response**:
  ```json
  {
    "access_token": "jwt_token_here",
    "token_type": "bearer"
  }
  ```

## Books Endpoints

### Get All Books
- **Endpoint**: `GET /books/`
- **Description**: Retrieve all books
- **Query Parameters**:
  - `skip` (int, optional): Number of records to skip (default: 0)
  - `limit` (int, optional): Maximum number of records to return (default: 100)
- **Response**: Array of Book objects

### Get Book by ID
- **Endpoint**: `GET /books/{book_id}`
- **Description**: Retrieve a specific book
- **Response**: Book object

### Create Book
- **Endpoint**: `POST /books/`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "title": "Book Title",
    "author": "Author Name",
    "year": 2023,
    "isbn": "1234567890",
    "copies": 5,
    "description": "Book description"
  }
  ```
- **Response**: Created Book object

### Update Book
- **Endpoint**: `PUT /books/{book_id}`
- **Authentication**: Required
- **Request Body** (all fields optional):
  ```json
  {
    "title": "Updated Title",
    "author": "Updated Author",
    "year": 2024,
    "isbn": "0987654321",
    "copies": 3,
    "description": "Updated description"
  }
  ```
- **Response**: Updated Book object

### Delete Book
- **Endpoint**: `DELETE /books/{book_id}`
- **Authentication**: Required
- **Response**: Success message

## Readers Endpoints

### Get All Readers
- **Endpoint**: `GET /readers/`
- **Authentication**: Required
- **Query Parameters**:
  - `skip` (int, optional): Number of records to skip (default: 0)
  - `limit` (int, optional): Maximum number of records to return (default: 100)
- **Response**: Array of Reader objects

### Get Reader by ID
- **Endpoint**: `GET /readers/{reader_id}`
- **Description**: Retrieve a specific reader
- **Response**: Reader object

### Create Reader
- **Endpoint**: `POST /readers/`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "name": "Reader Name",
    "email": "reader@example.com"
  }
  ```
- **Response**: Created Reader object

### Update Reader
- **Endpoint**: `PUT /readers/{reader_id}`
- **Authentication**: Required
- **Request Body** (all fields optional):
  ```json
  {
    "name": "Updated Name",
    "email": "updated@example.com"
  }
  ```
- **Response**: Updated Reader object

### Delete Reader
- **Endpoint**: `DELETE /readers/{reader_id}`
- **Authentication**: Required
- **Response**: Success message

## Borrow/Return Endpoints

### Borrow Book
- **Endpoint**: `POST /borrows/borrow`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "book_id": 1,
    "reader_id": 2
  }
  ```
- **Response**:
  ```json
  {
    "message": "Book borrowed successfully",
    "borrow_id": 1
  }
  ```

### Return Book
- **Endpoint**: `POST /borrows/return`
- **Authentication**: Required
- **Request Body**:
  ```json
  {
    "book_id": 1,
    "reader_id": 2
  }
  ```
- **Response**:
  ```json
  {
    "message": "Book returned successfully"
  }
  ```

### Get Reader's Borrowed Books
- **Endpoint**: `GET /borrows/reader/{reader_id}/borrowed`
- **Description**: Get all books currently borrowed by a specific reader
- **Response**: Array of Borrow objects

### Get All Borrows
- **Endpoint**: `GET /borrows/`
- **Authentication**: Required
- **Description**: Get all borrow records
- **Response**: Array of Borrow objects

## Advanced Feature Endpoints

### Reservations

#### Create Reservation
- **Endpoint**: `POST /reservations/`
- **Authentication**: Required
- **Query Parameters**:
  - `book_id` (int): ID of the book to reserve
  - `reader_id` (int): ID of the reader
  - `priority` (int, optional): Priority level (default: 0)
- **Response**:
  ```json
  {
    "message": "Reservation created successfully",
    "reservation_id": 1,
    "queue_position": 2
  }
  ```

#### Get Reader's Reservations
- **Endpoint**: `GET /reservations/reader/{reader_id}`
- **Query Parameters**:
  - `status` (string, optional): Filter by status
- **Response**: Array of Reservation objects

#### Cancel Reservation
- **Endpoint**: `PUT /reservations/{reservation_id}/cancel`
- **Authentication**: Required
- **Response**: Success message

### Reviews & Ratings

#### Create Review
- **Endpoint**: `POST /books/{book_id}/reviews`
- **Authentication**: Required
- **Query Parameters**:
  - `reader_id` (int): ID of the reader
  - `rating` (float): Rating (1-5)
  - `title` (string, optional): Review title
  - `review_text` (string, optional): Review content
- **Response**: Review object

#### Get Book Reviews
- **Endpoint**: `GET /books/{book_id}/reviews`
- **Query Parameters**:
  - `skip` (int, optional): Number of records to skip (default: 0)
  - `limit` (int, optional): Maximum number of records to return (default: 20)
- **Response**: Array of Review objects

### Fines & Payments

#### Get Reader's Fines
- **Endpoint**: `GET /readers/{reader_id}/fines`
- **Query Parameters**:
  - `status` (string, optional): Filter by status
- **Response**: Array of Fine objects

#### Pay Fine
- **Endpoint**: `POST /fines/{fine_id}/pay`
- **Authentication**: Required
- **Query Parameters**:
  - `amount` (float): Payment amount
  - `method` (string): Payment method
- **Response**:
  ```json
  {
    "message": "Payment processed successfully",
    "remaining_amount": 0.0
  }
  ```

### Statistics & Analytics

#### Dashboard Statistics
- **Endpoint**: `GET /statistics/dashboard`
- **Authentication**: Required
- **Response**:
  ```json
  {
    "total_books": 100,
    "total_readers": 50,
    "active_borrows": 25,
    "overdue_borrows": 5,
    "pending_fines": 10
  }
  ```

#### Book Statistics
- **Endpoint**: `GET /books/{book_id}/statistics`
- **Response**: Book statistics object

#### Popular Books
- **Endpoint**: `GET /analytics/popular-books`
- **Query Parameters**:
  - `limit` (int, optional): Number of books to return (1-50, default: 10)
- **Response**: Array of Book objects

### Notifications

#### Get User Notifications
- **Endpoint**: `GET /notifications/my`
- **Authentication**: Required
- **Query Parameters**:
  - `unread_only` (bool, optional): Return only unread notifications (default: false)
  - `skip` (int, optional): Number of records to skip (default: 0)
  - `limit` (int, optional): Maximum number of records to return (default: 20)
- **Response**: Array of Notification objects

#### Mark Notification as Read
- **Endpoint**: `PUT /notifications/{notification_id}/read`
- **Authentication**: Required
- **Response**: Success message