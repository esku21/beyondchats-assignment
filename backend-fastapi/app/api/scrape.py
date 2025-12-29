from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.services.scrape_beyondchats import get_last_page_url, scrape_list_page, scrape_article_content
from app.schemas.article import ArticleCreate
from app.crud.article import create_article

router = APIRouter(prefix="/scrape", tags=["scrape"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/beyondchats/oldest")
def scrape_oldest(db: Session = Depends(get_db)):
    last_page = get_last_page_url()
    items = scrape_list_page(last_page)
    # Pick the oldest 5 — assuming last page lists oldest in ascending order
    selected = items[:5] if len(items) >= 5 else items
    created_ids = []
    for it in selected:
        content = scrape_article_content(it["url"])
        payload = ArticleCreate(
            title=it["title"],
            url=it["url"],
            content_html=content["content_html"],
            content_text=content["content_text"],
            is_updated_version=False,
            origin_id=None,
            citations=None
        )
        obj = create_article(db, payload)
        created_ids.append(obj.id)
    return {"inserted_ids": created_ids, "count": len(created_ids)}
