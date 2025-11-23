from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
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
    
    # Связи для системы штрафов и финансов
    fines_created = relationship("Fine", foreign_keys="Fine.created_by_user_id", back_populates="created_by")
    fines_waived = relationship("Fine", foreign_keys="Fine.waived_by_user_id", back_populates="waived_by")
    payments_processed = relationship("Payment", back_populates="processed_by")
    library_settings_updated = relationship("LibrarySettings", back_populates="updated_by_user")