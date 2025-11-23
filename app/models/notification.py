from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime
import enum


class NotificationType(str, enum.Enum):
    """Типы уведомлений"""
    BOOK_AVAILABLE = "book_available"
    BOOK_DUE = "book_due"
    BOOK_OVERDUE = "book_overdue"
    RESERVATION_READY = "reservation_ready"
    RESERVATION_EXPIRED = "reservation_expired"
    NEW_BOOK_ADDED = "new_book_added"
    ACCOUNT_UPDATE = "account_update"
    FINE_APPLIED = "fine_applied"
    SYSTEM_MESSAGE = "system_message"


class NotificationChannel(str, enum.Enum):
    """Каналы уведомлений"""
    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"
    PUSH = "push"


class Notification(Base):
    """Модель уведомлений"""
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    reader_id = Column(Integer, ForeignKey("readers.id"))
    
    type = Column(SQLEnum(NotificationType), nullable=False)
    channel = Column(SQLEnum(NotificationChannel), default=NotificationChannel.IN_APP)
    
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    
    # Метаданные
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime)
    read_at = Column(DateTime)
    
    is_read = Column(Boolean, default=False)
    is_sent = Column(Boolean, default=False)
    
    # Связанные сущности
    related_book_id = Column(Integer, ForeignKey("books.id"))
    related_borrow_id = Column(Integer, ForeignKey("borrows.id"))
    related_reservation_id = Column(Integer, ForeignKey("reservations.id"))
    
    # Приоритет
    priority = Column(Integer, default=0)  # 0 - low, 1 - medium, 2 - high, 3 - urgent
    
    # Связи
    user = relationship("User", back_populates="notifications")
    reader = relationship("Reader", back_populates="notifications")
    related_book = relationship("Book")
    related_borrow = relationship("Borrow")
    related_reservation = relationship("Reservation")


class Event(Base):
    """Системные события для аудита"""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False)  # book_borrowed, book_returned, etc.
    
    # Кто совершил действие
    user_id = Column(Integer, ForeignKey("users.id"))
    reader_id = Column(Integer, ForeignKey("readers.id"))
    
    # Что было сделано
    action = Column(String, nullable=False)
    entity_type = Column(String)  # book, reader, borrow
    entity_id = Column(Integer)
    
    # Детали
    details = Column(Text)  # JSON с дополнительной информацией
    
    # Технические данные
    ip_address = Column(String)
    user_agent = Column(String)
    
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Связи
    user = relationship("User")
    reader = relationship("Reader")


class NotificationPreference(Base):
    """Настройки уведомлений для пользователей"""
    __tablename__ = "notification_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    reader_id = Column(Integer, ForeignKey("readers.id"), unique=True)
    
    # Включены ли уведомления по типам
    email_enabled = Column(Boolean, default=True)
    sms_enabled = Column(Boolean, default=False)
    in_app_enabled = Column(Boolean, default=True)
    push_enabled = Column(Boolean, default=True)
    
    # Конкретные типы уведомлений
    book_due_reminder = Column(Boolean, default=True)
    book_available = Column(Boolean, default=True)
    reservation_updates = Column(Boolean, default=True)
    new_books = Column(Boolean, default=False)
    account_updates = Column(Boolean, default=True)
    
    # Частота дайджестов
    digest_frequency = Column(String, default="daily")  # immediate, daily, weekly
    
    user = relationship("User", back_populates="notification_preferences")
    reader = relationship("Reader", back_populates="notification_preferences")