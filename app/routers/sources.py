from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.source import Source
from app.schemas.source import SourceCreate, SourceRead, SourceUpdate
from app.core.deps import get_current_active_admin, get_current_active_user

router = APIRouter()


@router.post("/", response_model=SourceRead)
def create_source(source_in: SourceCreate, db: Session = Depends(get_db), admin=Depends(get_current_active_admin)):
    s = Source(name=source_in.name, url=source_in.url, description=source_in.description)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@router.get("/", response_model=List[SourceRead])
def list_sources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    return db.query(Source).offset(skip).limit(limit).all()


@router.get("/{source_id}", response_model=SourceRead)
def get_source(source_id: int, db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    s = db.query(Source).filter(Source.id == source_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Source not found")
    return s


@router.put("/{source_id}", response_model=SourceRead)
def update_source(source_id: int, source_in: SourceUpdate, db: Session = Depends(get_db), admin=Depends(get_current_active_admin)):
    s = db.query(Source).filter(Source.id == source_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Source not found")
    if source_in.name:
        s.name = source_in.name
    if source_in.url is not None:
        s.url = source_in.url
    if source_in.description is not None:
        s.description = source_in.description
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@router.delete("/{source_id}")
def delete_source(source_id: int, db: Session = Depends(get_db), admin=Depends(get_current_active_admin)):
    s = db.query(Source).filter(Source.id == source_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Source not found")
    db.delete(s)
    db.commit()
    return {"ok": True}
