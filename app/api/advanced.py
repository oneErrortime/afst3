from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from .. import models, schemas
from ..database import get_db
from ..auth.jwt_handler import get_current_active_user

router = APIRouter()

# ============= RESERVATIONS =============

@router.post("/reservations/", status_code=status.HTTP_201_CREATED)
def create_reservation(
    book_id: int,
    reader_id: int,
    priority: int = 0,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Создать бронирование книги"""
    # Проверка существования книги и читателя
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    reader = db.query(models.Reader).filter(models.Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    
    # Проверка активных бронирований
    active_reservations = db.query(models.Reservation).filter(
        models.Reservation.reader_id == reader_id,
        models.Reservation.status.in_(['pending', 'confirmed', 'ready'])
    ).count()
    
    if active_reservations >= 5:
        raise HTTPException(
            status_code=400,
            detail="Reader cannot have more than 5 active reservations"
        )
    
    # Создание бронирования
    reservation = models.Reservation(
        book_id=book_id,
        reader_id=reader_id,
        priority=priority,
        reserved_until=datetime.utcnow() + timedelta(days=7),
        status='pending'
    )
    
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    
    # Вычисление позиции в очереди
    queue_position = reservation.calculate_queue_position(db)
    reservation.queue_position = queue_position
    db.commit()
    
    return {
        "message": "Reservation created successfully",
        "reservation_id": reservation.id,
        "queue_position": queue_position
    }

@router.get("/reservations/reader/{reader_id}")
def get_reader_reservations(
    reader_id: int,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Получить бронирования читателя"""
    query = db.query(models.Reservation).filter(
        models.Reservation.reader_id == reader_id
    )
    
    if status:
        query = query.filter(models.Reservation.status == status)
    
    reservations = query.order_by(models.Reservation.created_at.desc()).all()
    return reservations

@router.put("/reservations/{reservation_id}/cancel")
def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Отменить бронирование"""
    reservation = db.query(models.Reservation).filter(
        models.Reservation.id == reservation_id
    ).first()
    
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    if reservation.status in ['fulfilled', 'cancelled', 'expired']:
        raise HTTPException(
            status_code=400,
            detail="Cannot cancel reservation with this status"
        )
    
    reservation.status = 'cancelled'
    db.commit()
    
    return {"message": "Reservation cancelled successfully"}

# ============= REVIEWS & RATINGS =============

@router.post("/books/{book_id}/reviews")
def create_review(
    book_id: int,
    reader_id: int,
    rating: float,
    title: Optional[str] = None,
    review_text: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Создать отзыв на книгу"""
    # Валидация рейтинга
    if not 1 <= rating <= 5:
        raise HTTPException(
            status_code=400,
            detail="Rating must be between 1 and 5"
        )
    
    # Проверка, что читатель брал эту книгу
    has_borrowed = db.query(models.Borrow).filter(
        models.Borrow.book_id == book_id,
        models.Borrow.reader_id == reader_id,
        models.Borrow.is_returned == True
    ).first()
    
    if not has_borrowed:
        raise HTTPException(
            status_code=400,
            detail="You can only review books you have borrowed"
        )
    
    # Проверка на существующий отзыв
    existing_review = db.query(models.BookReview).filter(
        models.BookReview.book_id == book_id,
        models.BookReview.reader_id == reader_id
    ).first()
    
    if existing_review:
        raise HTTPException(
            status_code=400,
            detail="You have already reviewed this book"
        )
    
    # Создание отзыва
    review = models.BookReview(
        book_id=book_id,
        reader_id=reader_id,
        rating=rating,
        title=title,
        review_text=review_text
    )
    
    db.add(review)
    db.commit()
    db.refresh(review)
    
    # Обновление статистики книги
    update_book_statistics(book_id, db)
    
    return review

@router.get("/books/{book_id}/reviews")
def get_book_reviews(
    book_id: int,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Получить отзывы на книгу"""
    reviews = db.query(models.BookReview).filter(
        models.BookReview.book_id == book_id,
        models.BookReview.is_approved == True
    ).order_by(models.BookReview.created_at.desc()).offset(skip).limit(limit).all()
    
    return reviews

# ============= FINES & PAYMENTS =============

@router.get("/readers/{reader_id}/fines")
def get_reader_fines(
    reader_id: int,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Получить штрафы читателя"""
    query = db.query(models.Fine).filter(models.Fine.reader_id == reader_id)
    
    if status:
        query = query.filter(models.Fine.status == status)
    
    fines = query.order_by(models.Fine.created_at.desc()).all()
    return fines

@router.post("/fines/{fine_id}/pay")
def pay_fine(
    fine_id: int,
    amount: float,
    method: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Оплатить штраф"""
    fine = db.query(models.Fine).filter(models.Fine.id == fine_id).first()
    
    if not fine:
        raise HTTPException(status_code=404, detail="Fine not found")
    
    if fine.status == 'paid':
        raise HTTPException(status_code=400, detail="Fine already paid")
    
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Payment amount must be positive")
    
    # Создание платежа
    payment = models.Payment(
        fine_id=fine_id,
        reader_id=fine.reader_id,
        amount=amount,
        method=method,
        processed_by_user_id=current_user.id
    )
    
    db.add(payment)
    
    # Обновление штрафа
    fine.amount_paid += amount
    
    if fine.amount_paid >= fine.amount:
        fine.status = 'paid'
        fine.paid_at = datetime.utcnow()
    elif fine.amount_paid > 0:
        fine.status = 'partially_paid'
    
    db.commit()
    
    return {
        "message": "Payment processed successfully",
        "remaining_amount": fine.remaining_amount
    }

# ============= STATISTICS & ANALYTICS =============

@router.get("/statistics/dashboard")
def get_dashboard_statistics(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Получить общую статистику для дашборда"""
    total_books = db.query(models.Book).count()
    total_readers = db.query(models.Reader).count()
    active_borrows = db.query(models.Borrow).filter(
        models.Borrow.is_returned == False
    ).count()
    overdue_borrows = db.query(models.Borrow).filter(
        models.Borrow.is_returned == False,
        models.Borrow.borrow_date < datetime.utcnow() - timedelta(days=14)
    ).count()
    
    total_fines = db.query(models.Fine).filter(
        models.Fine.status.in_(['pending', 'partially_paid'])
    ).count()
    
    return {
        "total_books": total_books,
        "total_readers": total_readers,
        "active_borrows": active_borrows,
        "overdue_borrows": overdue_borrows,
        "pending_fines": total_fines
    }

@router.get("/books/{book_id}/statistics")
def get_book_statistics(book_id: int, db: Session = Depends(get_db)):
    """Получить подробную статистику по книге"""
    stats = db.query(models.BookStatistics).filter(
        models.BookStatistics.book_id == book_id
    ).first()
    
    if not stats:
        # Создать статистику если не существует
        stats = models.BookStatistics(book_id=book_id)
        db.add(stats)
        db.commit()
        db.refresh(stats)
    
    return stats

@router.get("/analytics/popular-books")
def get_popular_books(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Получить самые популярные книги"""
    popular_books = db.query(models.Book).join(
        models.BookStatistics
    ).order_by(
        models.BookStatistics.popularity_score.desc()
    ).limit(limit).all()
    
    return popular_books

# ============= NOTIFICATIONS =============

@router.get("/notifications/my")
def get_my_notifications(
    unread_only: bool = False,
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Получить уведомления текущего пользователя"""
    query = db.query(models.Notification).filter(
        models.Notification.user_id == current_user.id
    )
    
    if unread_only:
        query = query.filter(models.Notification.is_read == False)
    
    notifications = query.order_by(
        models.Notification.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return notifications

@router.put("/notifications/{notification_id}/read")
def mark_notification_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Отметить уведомление как прочитанное"""
    notification = db.query(models.Notification).filter(
        models.Notification.id == notification_id,
        models.Notification.user_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_read = True
    notification.read_at = datetime.utcnow()
    db.commit()
    
    return {"message": "Notification marked as read"}

# ============= HELPER FUNCTIONS =============

def update_book_statistics(book_id: int, db: Session):
    """Обновить статистику книги"""
    stats = db.query(models.BookStatistics).filter(
        models.BookStatistics.book_id == book_id
    ).first()
    
    if not stats:
        stats = models.BookStatistics(book_id=book_id)
        db.add(stats)
    
    # Подсчет отзывов
    reviews = db.query(models.BookReview).filter(
        models.BookReview.book_id == book_id,
        models.BookReview.is_approved == True
    ).all()
    
    if reviews:
        stats.average_rating = sum(r.rating for r in reviews) / len(reviews)
        stats.total_reviews = len(reviews)
    
    # Подсчет выдач
    total_borrows = db.query(models.Borrow).filter(
        models.Borrow.book_id == book_id
    ).count()
    stats.total_borrows = total_borrows
    
    # Вычисление популярности (можно использовать более сложную формулу)
    stats.popularity_score = (stats.total_borrows * 0.5 + 
                             (stats.average_rating or 0) * 20)
    
    db.commit()