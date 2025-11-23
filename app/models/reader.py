from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Reader(Base):
    __tablename__ = "readers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    # Relationship with borrows
    borrows = relationship("Borrow", back_populates="reader")
    
    # Relationships for reservation system
    reservations = relationship("Reservation", back_populates="reader")
    book_requests = relationship("BookRequest", back_populates="reader")
    
    # Relationships for fine system
    fines = relationship("Fine", back_populates="reader")
    payments = relationship("Payment", back_populates="reader")
    membership = relationship("Membership", back_populates="reader", uselist=False)
    balance = relationship("ReaderBalance", back_populates="reader", uselist=False)