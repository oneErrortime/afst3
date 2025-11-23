from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime


class Reader(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    # Relationship with borrows
    borrows = relationship("Borrow", back_populates="reader")
    
    # Новые связи для расширенного функционала
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="reader")
    reservations = relationship("Reservation", back_populates="reader")
    waiting_list = relationship("WaitingList", back_populates="reader")
    book_requests = relationship("BookRequest", back_populates="reader")
    notifications = relationship("Notification", back_populates="reader")
    notification_preferences = relationship("NotificationPreference", back_populates="reader", uselist=False)