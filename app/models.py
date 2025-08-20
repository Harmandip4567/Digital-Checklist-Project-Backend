from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, JSON, Boolean
from app.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)

class ChecklistTemplate(Base):
    __tablename__ = "checklist_templates"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    created_by = Column(Integer,ForeignKey("users.id",ondelete="CASCADE")) 
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="pending")

    items = relationship("ChecklistItem", back_populates="template", cascade="all, delete-orphan")

class ChecklistItem(Base):
    __tablename__ = "checklist_items"
    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("checklist_templates.id", ondelete="CASCADE"))
    order = Column(Integer, default=1)
    label = Column(String, nullable=False) # task
    input_type = Column(String, nullable=False)   # "text","number","checkbox","select","date","file"
    required = Column(Boolean, default=False)
    frequency = Column(String, nullable=True)
    unit = Column(String, nullable=True)
    options = Column(JSON, nullable=True)         # JSON array for select options

    template = relationship("ChecklistTemplate", back_populates="items")