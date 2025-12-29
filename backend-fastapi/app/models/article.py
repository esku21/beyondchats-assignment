from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.core.db import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(512), index=True)
    url = Column(String(1024), nullable=True)
    content_html = Column(Text, nullable=True)
    content_text = Column(Text, nullable=True)
    is_updated_version = Column(Boolean, default=False)
    origin_id = Column(Integer, ForeignKey("articles.id"), nullable=True)
    citations = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    origin = relationship("Article", remote_side=[id])
