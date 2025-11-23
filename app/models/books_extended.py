from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Table, Text
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime

# Many-to-many таблица для книг и категорий
book_categories = Table(
    'book_categories',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('categories.id'), primary_key=True)
)

# Many-to-many таблица для книг и авторов (если авторов несколько)
book_authors = Table(
    'book_authors',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('author_id', Integer, ForeignKey('authors.id'), primary_key=True)
)

# Many-to-many таблица для книг и тегов
book_tags = Table(
    'book_tags',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class Category(Base):
    """Категории книг"""
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey('categories.id'))  # Для иерархии
    
    # Связи
    books = relationship("Book", secondary=book_categories, back_populates="categories")
    parent = relationship("Category", remote_side=[id], backref="subcategories")

class Author(Base):
    """Отдельная таблица авторов"""
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    biography = Column(Text)
    birth_year = Column(Integer)
    country = Column(String)
    website = Column(String)
    
    # Связи
    books = relationship("Book", secondary=book_authors, back_populates="authors")

class Tag(Base):
    """Теги для книг"""
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    usage_count = Column(Integer, default=0)
    
    # Связи
    books = relationship("Book", secondary=book_tags, back_populates="tags")

class BookReview(Base):
    """Отзывы на книги"""
    __tablename__ = "book_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    
    rating = Column(Float, nullable=False)  # 1-5 звезд
    title = Column(String)
    review_text = Column(Text)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
    
    # Модерация
    is_approved = Column(Boolean, default=False)
    is_flagged = Column(Boolean, default=False)
    
    # Полезность отзыва
    helpful_count = Column(Integer, default=0)
    not_helpful_count = Column(Integer, default=0)
    
    # Связи
    book = relationship("Book", back_populates="reviews")
    reader = relationship("Reader", back_populates="reviews")

class BookStatistics(Base):
    """Статистика по книгам"""
    __tablename__ = "book_statistics"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), unique=True, nullable=False)
    
    # Статистика выдач
    total_borrows = Column(Integer, default=0)
    current_borrows = Column(Integer, default=0)
    total_reservations = Column(Integer, default=0)
    
    # Популярность
    popularity_score = Column(Float, default=0.0)
    average_rating = Column(Float)
    total_reviews = Column(Integer, default=0)
    
    # Временные метрики
    last_borrowed = Column(DateTime)
    last_returned = Column(DateTime)
    average_borrow_duration = Column(Integer)  # В днях
    
    # Доступность
    availability_rate = Column(Float, default=100.0)  # Процент времени, когда книга доступна
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    book = relationship("Book", back_populates="statistics", uselist=False)

class BookSeries(Base):
    """Серии книг"""
    __tablename__ = "book_series"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    total_books = Column(Integer)
    
    # Связи
    books = relationship("Book", back_populates="series")

class BookEdition(Base):
    """Разные издания одной книги"""
    __tablename__ = "book_editions"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    
    edition_name = Column(String)  # "First Edition", "Revised", etc.
    publisher = Column(String)
    publication_date = Column(DateTime)
    language = Column(String)
    pages = Column(Integer)
    format = Column(String)  # hardcover, paperback, ebook, audiobook
    
    isbn = Column(String, unique=True)
    copies = Column(Integer, default=1)
    
    # Связи
    book = relationship("Book", back_populates="editions")

# Расширение существующей модели Book
"""
Добавить в существующую модель Book:

categories = relationship("Category", secondary=book_categories, back_populates="books")
authors = relationship("Author", secondary=book_authors, back_populates="books")
tags = relationship("Tag", secondary=book_tags, back_populates="books")
reviews = relationship("BookReview", back_populates="book")
statistics = relationship("BookStatistics", back_populates="book", uselist=False)
series_id = Column(Integer, ForeignKey("book_series.id"))
series = relationship("BookSeries", back_populates="books")
editions = relationship("BookEdition", back_populates="book")
reservations = relationship("Reservation", back_populates="book")

# Дополнительные поля
publisher = Column(String)
language = Column(String, default="English")
pages = Column(Integer)
format = Column(String)  # hardcover, paperback, ebook
cover_image_url = Column(String)
featured = Column(Boolean, default=False)
new_arrival = Column(Boolean, default=False)
"""