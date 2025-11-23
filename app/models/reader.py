from sqlalchemy import Column, Integer, String
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