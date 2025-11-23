from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table, Enum as SQLEnum, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
import enum
from datetime import datetime

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
    timestamp = Column(DateTime, default=func.now())
    
    user = relationship("User", back_populates="activities")