from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table, Enum as SQLEnum
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime
import enum


# Many-to-many таблица для связи пользователей и ролей
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)


class RoleEnum(str, enum.Enum):
    """Перечисление ролей в системе"""
    ADMIN = "admin"
    LIBRARIAN = "librarian"
    READER = "reader"
    GUEST = "guest"


class Permission(Base):
    """Модель прав доступа"""
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    resource = Column(String, nullable=False)  # books, readers, borrows, etc.
    action = Column(String, nullable=False)  # create, read, update, delete
    
    # Связь с ролями
    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")


# Many-to-many таблица для связи ролей и прав
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)


class Role(Base):
    """Модель ролей"""
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(SQLEnum(RoleEnum), unique=True, nullable=False)
    description = Column(String)
    is_active = Column(Boolean, default=True)
    
    # Связи
    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")


class UserActivity(Base):
    """Логирование действий пользователей"""
    __tablename__ = "user_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    action = Column(String, nullable=False)
    resource_type = Column(String)  # book, reader, borrow
    resource_id = Column(Integer)
    details = Column(String)
    ip_address = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="activities")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    role = Column(String, default="reader")  # admin, librarian, reader

    # Связи
    borrows = relationship("Borrow", back_populates="user")
    reader = relationship("Reader", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    # Новые связи для ролей и уведомлений
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    activities = relationship("UserActivity", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
    notification_preferences = relationship("NotificationPreference", back_populates="user", uselist=False)