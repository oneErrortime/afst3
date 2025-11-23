from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=True)

    # Связи для ролевой системы
    roles = relationship("app.models.role.Role", secondary="user_roles", back_populates="users")
    activities = relationship("app.models.role.UserActivity", back_populates="user")