from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.db import SessionLocal
from app.schemas.article import ArticleCreate, ArticleUpdate, ArticleOut
from app.crud.article import create_article, get_article, list_articles, update_article, delete_article
import json

router = APIRouter(prefix="/articles", tags=["articles"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def parse_citations_str(article):
    if article.citations:
        try:
            article.citations = json.loads(article.citations)
        except Exception:
            article.citations = None
    return article

@router.get("/", response_model=List[ArticleOut])
def api_list_articles(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    items = list_articles(db, skip=skip, limit=limit)
    return [parse_citations_str(a) for a in items]

@router.get("/{article_id}", response_model=ArticleOut)
def api_get_article(article_id: int, db: Session = Depends(get_db)):
    a = get_article(db, article_id)
    if not a:
        raise HTTPException(status_code=404, detail="Article not found")
    return parse_citations_str(a)

@router.post("/", response_model=ArticleOut)
def api_create_article(payload: ArticleCreate, db: Session = Depends(get_db)):
    a = create_article(db, payload)
    return parse_citations_str(a)

@router.put("/{article_id}", response_model=ArticleOut)
def api_update_article(article_id: int, payload: ArticleUpdate, db: Session = Depends(get_db)):
    a = get_article(db, article_id)
    if not a:
        raise HTTPException(status_code=404, detail="Article not found")
    a = update_article(db, a, payload)
    return parse_citations_str(a)

@router.delete("/{article_id}")
def api_delete_article(article_id: int, db: Session = Depends(get_db)):
    a = get_article(db, article_id)
    if not a:
        raise HTTPException(status_code=404, detail="Article not found")
    delete_article(db, a)
    return {"status": "deleted"}
