# Расширенные функции библиотечной системы

## Содержание
- [Бронирования книг](#бронирования-книг)
- [Отзывы и оценки](#отзывы-и-оценки)
- [Штрафы и оплаты](#штрафы-и-оплаты)
- [Статистика и аналитика](#статистика-и-аналитика)
- [Уведомления](#уведомления)

## Бронирования книг

### Создание бронирования
- **Эндпоинт**: `POST /api/reservations/`
- **Аутентификация**: Требуется
- **Параметры**:
  - `book_id` (int): ID книги для бронирования
  - `reader_id` (int): ID читателя
  - `priority` (int, optional): Приоритет бронирования (по умолчанию 0)
- **Ответ**: 
  ```json
  {
    "message": "Reservation created successfully",
    "reservation_id": 1,
    "queue_position": 2
  }
  ```
- **Ошибки**:
  - `404`: Книга или читатель не найден
  - `400`: Превышено максимальное количество бронирований (5)

### Получение бронирований читателя
- **Эндпоинт**: `GET /api/reservations/reader/{reader_id}`
- **Аутентификация**: Требуется
- **Параметры**:
  - `status` (string, optional): Фильтр по статусу (pending, confirmed, ready, fulfilled, cancelled, expired)
- **Ответ**:
  ```json
  [
    {
      "id": 1,
      "book_id": 5,
      "reader_id": 3,
      "status": "pending",
      "created_at": "2023-01-01T10:00:00Z",
      "reserved_until": "2023-01-08T10:00:00Z",
      "queue_position": 2
    }
  ]
  ```

### Отмена бронирования
- **Эндпоинт**: `PUT /api/reservations/{reservation_id}/cancel`
- **Аутентификация**: Требуется
- **Ответ**:
  ```json
  {
    "message": "Reservation cancelled successfully"
  }
  ```

## Отзывы и оценки

### Создание отзыва
- **Эндпоинт**: `POST /api/books/{book_id}/reviews`
- **Аутентификация**: Требуется
- **Параметры**:
  - `reader_id` (int): ID читателя
  - `rating` (float): Оценка (1-5)
  - `title` (string, optional): Заголовок отзыва
  - `review_text` (string, optional): Текст отзыва
- **Ответ**:
  ```json
  {
    "id": 1,
    "book_id": 5,
    "reader_id": 3,
    "rating": 4.5,
    "title": "Отличная книга",
    "review_text": "Очень понравилось читать",
    "created_at": "2023-01-01T10:00:00Z"
  }
  ```
- **Ограничения**:
  - Читатель может оставлять отзыв только на книги, которые он брал и вернул
  - Один отзыв на читателя и книгу

### Получение отзывов книги
- **Эндпоинт**: `GET /api/books/{book_id}/reviews`
- **Параметры**:
  - `skip` (int, optional): Пропустить N записей (по умолчанию 0)
  - `limit` (int, optional): Максимальное количество записей (по умолчанию 20)
- **Ответ**:
  ```json
  [
    {
      "id": 1,
      "book_id": 5,
      "reader_id": 3,
      "rating": 4.5,
      "title": "Отличная книга",
      "review_text": "Очень понравилось читать",
      "created_at": "2023-01-01T10:00:00Z"
    }
  ]
  ```

## Штрафы и оплаты

### Получение штрафов читателя
- **Эндпоинт**: `GET /api/readers/{reader_id}/fines`
- **Параметры**:
  - `status` (string, optional): Фильтр по статусу (pending, partially_paid, paid)
- **Ответ**:
  ```json
  [
    {
      "id": 1,
      "reader_id": 3,
      "amount": 50.0,
      "reason": "Просроченная книга",
      "status": "pending",
      "created_at": "2023-01-01T10:00:00Z",
      "amount_paid": 0.0
    }
  ]
  ```

### Оплата штрафа
- **Эндпоинт**: `POST /api/fines/{fine_id}/pay`
- **Аутентификация**: Требуется
- **Параметры**:
  - `amount` (float): Сумма оплаты
  - `method` (string): Метод оплаты
- **Ответ**:
  ```json
  {
    "message": "Payment processed successfully",
    "remaining_amount": 0.0
  }
  ```

## Статистика и аналитика

### Дашборд статистики
- **Эндпоинт**: `GET /api/statistics/dashboard`
- **Аутентификация**: Требуется
- **Ответ**:
  ```json
  {
    "total_books": 100,
    "total_readers": 50,
    "active_borrows": 25,
    "overdue_borrows": 5,
    "pending_fines": 10
  }
  ```

### Статистика книги
- **Эндпоинт**: `GET /api/books/{book_id}/statistics`
- **Ответ**:
  ```json
  {
    "book_id": 5,
    "average_rating": 4.2,
    "total_reviews": 15,
    "total_borrows": 23,
    "popularity_score": 86.0
  }
  ```

### Популярные книги
- **Эндпоинт**: `GET /api/analytics/popular-books`
- **Параметры**:
  - `limit` (int, optional): Количество книг (1-50, по умолчанию 10)
- **Ответ**:
  ```json
  [
    {
      "id": 5,
      "title": "Война и мир",
      "author": "Толстой",
      "year": 1869,
      "copies": 3,
      "isbn": "1234567890",
      "description": "Классический роман"
    }
  ]
  ```

## Уведомления

### Получение уведомлений
- **Эндпоинт**: `GET /api/notifications/my`
- **Аутентификация**: Требуется
- **Параметры**:
  - `unread_only` (bool, optional): Только непрочитанные (по умолчанию false)
  - `skip` (int, optional): Пропустить N записей (по умолчанию 0)
  - `limit` (int, optional): Максимальное количество записей (по умолчанию 20)
- **Ответ**:
  ```json
  [
    {
      "id": 1,
      "user_id": 3,
      "title": "Напоминание о возврате",
      "message": "Книга должна быть возвращена завтра",
      "type": "reminder",
      "is_read": false,
      "created_at": "2023-01-01T10:00:00Z"
    }
  ]
  ```

### Пометка уведомления как прочитанного
- **Эндпоинт**: `PUT /api/notifications/{notification_id}/read`
- **Аутентификация**: Требуется
- **Ответ**:
  ```json
  {
    "message": "Notification marked as read"
  }
  ```