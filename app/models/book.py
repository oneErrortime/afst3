from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime, timedelta
import enum


class ReservationStatus(str, enum.Enum):
    """Статусы бронирования"""
    PENDING = "pending"  # Ожидает подтверждения
    CONFIRMED = "confirmed"  # Подтверждено
    READY = "ready"  # Готово к выдаче
    FULFILLED = "fulfilled"  # Выполнено
    CANCELLED = "cancelled"  # Отменено
    EXPIRED = "expired"  # Истекло


class Reservation(Base):
    """Модель бронирования книг"""
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    
    # Временные метки
    created_at = Column(DateTime, default=datetime.utcnow)
    reserved_until = Column(DateTime)  # Срок действия бронирования
    pickup_deadline = Column(DateTime)  # Крайний срок получения
    fulfilled_at = Column(DateTime)  # Когда выполнено
    
    # Статус
    status = Column(SQLEnum(ReservationStatus), default=ReservationStatus.PENDING)
    
    # Приоритет (для очереди)
    priority = Column(Integer, default=0)  # Чем выше, тем важнее
    queue_position = Column(Integer)  # Позиция в очереди
    
    # Уведомления
    notification_sent = Column(Boolean, default=False)
    email_sent = Column(Boolean, default=False)
    
    # Связи
    book = relationship("Book", back_populates="reservations")
    reader = relationship("Reader", back_populates="reservations")
    
    def is_expired(self):
        """Проверка, истекло ли бронирование"""
        from datetime import datetime
        if self.reserved_until and datetime.utcnow() > self.reserved_until:
            return True
        return False
    
    def calculate_queue_position(self, db):
        """Вычисление позиции в очереди"""
        active_reservations = db.query(Reservation).filter(
            Reservation.book_id == self.book_id,
            Reservation.status.in_([ReservationStatus.PENDING, ReservationStatus.CONFIRMED]),
            Reservation.created_at < self.created_at
        ).order_by(Reservation.priority.desc(), Reservation.created_at).all()
        
        return len(active_reservations) + 1


class WaitingList(Base):
    """Лист ожидания для недоступных книг"""
    __tablename__ = "waiting_lists"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    
    joined_at = Column(DateTime, default=datetime.utcnow)
    position = Column(Integer)
    notified = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    
    # Связи
    book = relationship("Book", back_populates="waiting_list")
    reader = relationship("Reader", back_populates="waiting_list")


class BookRequest(Base):
    """Запросы на приобретение книг"""
    __tablename__ = "book_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    isbn = Column(String)
    reason = Column(String)  # Причина запроса
    
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")  # pending, approved, rejected, fulfilled
    votes = Column(Integer, default=1)  # Поддержка от других читателей
    
    # Связи
    reader = relationship("Reader", back_populates="book_requests")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    year = Column(Integer)  # Publication year, optional
    isbn = Column(String, unique=True)  # Unique ISBN, optional
    copies = Column(Integer, default=1)  # Number of copies available
    description = Column(String)  # Added for the second migration
    
    # Relationship with borrows
    borrows = relationship("Borrow", back_populates="book")
    
    # Новые связи для бронирования
    reservations = relationship("Reservation", back_populates="book")
    waiting_list = relationship("WaitingList", back_populates="book")