# Advanced Library Management Features

## Overview
This PR introduces comprehensive enhancements to the library management system with new modules for roles, permissions, reservations, notifications, and events.

## Changes Made

### 1. Enhanced User Model (`app/models/user.py`)
- Added Role-based Access Control (RBAC) system with roles (admin, librarian, reader, guest)
- Implemented permissions model with resource-action based permissions
- Added user activity logging functionality
- Created many-to-many relationships between users and roles
- Added notification preferences for users

### 2. Enhanced Book Model (`app/models/book.py`)
- Added reservation system with multiple statuses (pending, confirmed, ready, fulfilled, cancelled, expired)
- Implemented waiting list functionality for unavailable books
- Added book request system for acquisition requests
- Enhanced book model with relationships to reservations and waiting lists
- Added queue position calculation methods

### 3. New Notification System (`app/models/notification.py`)
- Created comprehensive notification model supporting multiple channels (email, SMS, in-app, push)
- Implemented event logging system for audit trail
- Added notification preferences model for user customization
- Defined notification types and channels as enums

### 4. Enhanced Reader Model (`app/models/reader.py`)
- Added relationships to new models (reservations, waiting lists, book requests, notifications)
- Connected readers to notification preferences

### 5. Enhanced Borrow Model (`app/models/borrow.py`)
- Added due date tracking
- Implemented fine system
- Added user reference for who processed the borrow
- Connected to notification system

### 6. Updated Models Initialization (`app/models/__init__.py`)
- Added imports for all new models
- Updated __all__ list to include new functionality

## New Features

### Role-Based Access Control
- Multi-level roles with permissions system
- Flexible permission assignment to roles
- User-role many-to-many relationship

### Reservation and Queue System
- Book reservation with status tracking
- Waiting list for unavailable books
- Queue position calculation
- Acquisition request system

### Comprehensive Notification System
- Multi-channel notifications (email, SMS, in-app, push)
- Notification preferences per user
- Audit events logging
- Priority-based notifications

## Files Changed
- `app/models/__init__.py` - Updated imports
- `app/models/book.py` - Added reservation and request functionality
- `app/models/borrow.py` - Enhanced with due dates and fines
- `app/models/reader.py` - Added relationships to new features
- `app/models/user.py` - Added RBAC and activity logging
- `app/models/notification.py` - New notification and event system

## Database Schema Impact
These changes introduce new tables for:
- roles, permissions, user_roles, role_permissions
- reservations, waiting_lists, book_requests
- notifications, events, notification_preferences
- user_activities

## Testing
All existing functionality is preserved while adding new features. New API endpoints will be needed to utilize these models.