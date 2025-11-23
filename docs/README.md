# Library Management System - GitHub Pages Demo

This is a frontend-only demo of the Library Management System that can be deployed on GitHub Pages. It connects to a backend API to provide full functionality for managing books, readers, and borrowing operations.

## Features

- User authentication (register/login/logout)
- Book management (add, search, view books)
- Reader management (add, search, view readers)
- Borrow/return system
- Dashboard with statistics
- Responsive design using Bootstrap 5
- Modern UI with Font Awesome icons

## How to Use

1. Deploy this frontend to GitHub Pages
2. Configure the backend API URL using the API Configuration section
3. Register/login to access the full functionality
4. Use the various sections to manage your library

## API Endpoints Used

The frontend communicates with the backend using these endpoints:
- `/auth/register` - User registration
- `/auth/login` - User login
- `/books/` - Book management
- `/readers/` - Reader management
- `/borrows/borrow` - Borrow a book
- `/borrows/return` - Return a book
- `/borrows/reader/{reader_id}/borrowed` - Get borrowed books for a reader

## Advanced Features

The backend API provides additional functionality that is not currently implemented in the frontend. These features include:

- **Reservations**: Book reservation system with queue management
- **Reviews & Ratings**: User reviews and book ratings
- **Fines & Payments**: Fine management and payment processing
- **Statistics & Analytics**: Dashboard statistics, book statistics, and popularity analytics
- **Notifications**: User notification system

For complete documentation of these advanced features, see [advanced_features.md](advanced_features.md).

## API Documentation

Complete documentation for the system:

- [Documentation Home](documentation.html) - Centralized page with all documentation
- [API Endpoints Reference](api_endpoints.md) - Comprehensive list of all available API endpoints
- [Architecture Documentation](architecture.md) - Detailed architecture overview
- [Advanced Features](advanced_features.md) - Documentation of extended functionality

## Configuration

The API URL can be configured and saved in the browser's localStorage. This allows the frontend to remember your backend URL between sessions.

## Local Development

To test locally, you can run a simple HTTP server:

```bash
cd docs
python -m http.server 8000
```

Then open `http://localhost:8000` in your browser.

## Backend Integration

This frontend is designed to work with a FastAPI backend that implements the Library Management System API. The backend should provide JWT-based authentication and implement all the endpoints referenced in the JavaScript code.

## Technologies Used

- HTML5
- CSS3 (with Bootstrap 5)
- JavaScript (ES6+)
- Font Awesome (icons)
- GitHub Pages (deployment)

## Deployment

To deploy to GitHub Pages:

1. Push this code to a GitHub repository
2. Go to repository Settings → Pages
3. Select source as "GitHub Actions" or "Deploy from a branch"
4. Choose the `main` branch and `/docs` folder
5. Save settings and wait for deployment

The site will be available at `https://<username>.github.io/<repository-name>`.