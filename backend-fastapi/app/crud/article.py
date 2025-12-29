from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.article import Article
from app.schemas.article import ArticleCreate, ArticleUpdate
import json

def _citations_to_str(citations):
    return json.dumps([c.dict() for c in citations]) if citations else None

def create_article(db: Session, payload: ArticleCreate) -> Article:
    obj = Article(
        title=payload.title,
        url=payload.url,
        content_html=payload.content_html,
        content_text=payload.content_text,
        is_updated_version=payload.is_updated_version,
        origin_id=payload.origin_id,
        citations=_citations_to_str(payload.citations),
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_article(db: Session, article_id: int) -> Optional[Article]:
    return db.query(Article).filter(Article.id == article_id).first()

def list_articles(db: Session, skip: int = 0, limit: int = 50) -> List[Article]:
    return db.query(Article).order_by(Article.created_at.asc()).offset(skip).limit(limit).all()

def update_article(db: Session, article: Article, payload: ArticleUpdate) -> Article:
    for field, value in payload.dict(exclude_unset=True).items():
        if field == "citations" and value is not None:
            setattr(article, field, _citations_to_str(value))
        else:
            setattr(article, field, value)
    db.commit()
    db.refresh(article)
    return article

def delete_article(db: Session, article: Article):
    db.delete(article)
    db.commit()
