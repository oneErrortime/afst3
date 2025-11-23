from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime

class Borrow(Base):
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime)  # NULL if not returned yet
    is_returned = Column(Boolean, default=False)  # To track return status

    # Relationships
    book = relationship("Book", back_populates="borrows")
    reader = relationship("Reader", back_populates="borrows")
    fines = relationship("Fine", back_populates="borrow")