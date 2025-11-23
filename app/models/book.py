from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime

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
    
    # Relationships for reservation system
    reservations = relationship("Reservation", back_populates="book")
    waiting_lists = relationship("WaitingList", back_populates="book")