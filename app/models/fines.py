from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime, timedelta
import enum

class FineReason(str, enum.Enum):
    """Причины штрафов"""
    OVERDUE = "overdue"
    LOST_BOOK = "lost_book"
    DAMAGED_BOOK = "damaged_book"
    LATE_RETURN = "late_return"
    RESERVATION_NO_SHOW = "reservation_no_show"
    OTHER = "other"

class PaymentStatus(str, enum.Enum):
    """Статусы платежей"""
    PENDING = "pending"
    PAID = "paid"
    PARTIALLY_PAID = "partially_paid"
    WAIVED = "waived"
    CANCELLED = "cancelled"

class PaymentMethod(str, enum.Enum):
    """Методы оплаты"""
    CASH = "cash"
    CARD = "card"
    ONLINE = "online"
    BANK_TRANSFER = "bank_transfer"

class Fine(Base):
    """Модель штрафов"""
    __tablename__ = "fines"
    
    id = Column(Integer, primary_key=True, index=True)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    borrow_id = Column(Integer, ForeignKey("borrows.id"))
    
    reason = Column(SQLEnum(FineReason), nullable=False)
    amount = Column(Float, nullable=False)
    amount_paid = Column(Float, default=0.0)
    
    description = Column(Text)
    
    # Даты
    created_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime)
    paid_at = Column(DateTime)
    waived_at = Column(DateTime)
    
    status = Column(SQLEnum(PaymentStatus), default=PaymentStatus.PENDING)
    
    # Кто создал/отменил штраф
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    waived_by_user_id = Column(Integer, ForeignKey("users.id"))
    
    # Связи
    reader = relationship("Reader", back_populates="fines")
    borrow = relationship("Borrow", back_populates="fines")
    payments = relationship("Payment", back_populates="fine")
    
    @property
    def remaining_amount(self):
        """Остаток к оплате"""
        return self.amount - self.amount_paid
    
    @property
    def is_overdue(self):
        """Просрочен ли штраф"""
        if self.due_date and datetime.utcnow() > self.due_date:
            return True
        return False

class Payment(Base):
    """История платежей"""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    fine_id = Column(Integer, ForeignKey("fines.id"), nullable=False)
    reader_id = Column(Integer, ForeignKey("readers.id"), nullable=False)
    
    amount = Column(Float, nullable=False)
    method = Column(SQLEnum(PaymentMethod), nullable=False)
    
    # Детали транзакции
    transaction_id = Column(String, unique=True)
    reference_number = Column(String)
    
    paid_at = Column(DateTime, default=datetime.utcnow)
    processed_by_user_id = Column(Integer, ForeignKey("users.id"))
    
    notes = Column(Text)
    
    # Связи
    fine = relationship("Fine", back_populates="payments")
    reader = relationship("Reader", back_populates="payments")
    processed_by = relationship("User", foreign_keys=[processed_by_user_id])

class Membership(Base):
    """Членство/абонементы библиотеки"""
    __tablename__ = "memberships"
    
    id = Column(Integer, primary_key=True, index=True)
    reader_id = Column(Integer, ForeignKey("readers.id"), unique=True, nullable=False)
    
    # Тип членства
    membership_type = Column(String, default="basic")  # basic, premium, student, etc.
    
    # Даты
    start_date = Column(DateTime, default=datetime.utcnow)
    expiry_date = Column(DateTime)
    
    is_active = Column(Boolean, default=True)
    auto_renew = Column(Boolean, default=False)
    
    # Лимиты
    max_books = Column(Integer, default=3)
    max_borrow_days = Column(Integer, default=14)
    
    # Финансы
    membership_fee = Column(Float, default=0.0)
    last_payment_date = Column(DateTime)
    
    # Связи
    reader = relationship("Reader", back_populates="membership", uselist=False)
    
    @property
    def is_expired(self):
        """Истек ли абонемент"""
        if self.expiry_date and datetime.utcnow() > self.expiry_date:
            return True
        return False
    
    @property
    def days_until_expiry(self):
        """Дней до истечения"""
        if self.expiry_date:
            delta = self.expiry_date - datetime.utcnow()
            return delta.days
        return None

class LibrarySettings(Base):
    """Настройки библиотеки (тарифы, правила)"""
    __tablename__ = "library_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False)
    value = Column(String, nullable=False)
    description = Column(Text)
    category = Column(String)  # fines, limits, fees, etc.
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by_user_id = Column(Integer, ForeignKey("users.id"))

# Примеры настроек:
# - overdue_fine_per_day: 0.50
# - max_books_per_reader: 3
# - max_borrow_days: 14
# - lost_book_fine_multiplier: 2.0
# - reservation_fee: 1.00
# - membership_annual_fee: 25.00

class ReaderBalance(Base):
    """Баланс читателя"""
    __tablename__ = "reader_balances"
    
    id = Column(Integer, primary_key=True, index=True)
    reader_id = Column(Integer, ForeignKey("readers.id"), unique=True, nullable=False)
    
    balance = Column(Float, default=0.0)  # Отрицательный = должен, положительный = предоплата
    
    total_fines = Column(Float, default=0.0)
    total_paid = Column(Float, default=0.0)
    
    last_transaction_date = Column(DateTime)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Связи
    reader = relationship("Reader", back_populates="balance", uselist=False)
    
    @property
    def outstanding_amount(self):
        """Сумма задолженности"""
        return abs(min(self.balance, 0))
    
    @property
    def has_outstanding_fines(self):
        """Есть ли непогашенные штрафы"""
        return self.balance < 0