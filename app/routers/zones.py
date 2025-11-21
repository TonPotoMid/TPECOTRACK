from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.zone import Zone
from app.schemas.zone import ZoneCreate, ZoneRead, ZoneUpdate
from app.core.deps import get_current_active_admin, get_current_active_user

router = APIRouter()


@router.post("/", response_model=ZoneRead)
def create_zone(zone_in: ZoneCreate, db: Session = Depends(get_db), admin=Depends(get_current_active_admin)):
    z = Zone(name=zone_in.name, postal_code=zone_in.postal_code, geom=zone_in.geom)
    db.add(z)
    db.commit()
    db.refresh(z)
    return z


@router.get("/", response_model=List[ZoneRead])
def list_zones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    return db.query(Zone).offset(skip).limit(limit).all()


@router.get("/{zone_id}", response_model=ZoneRead)
def get_zone(zone_id: int, db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    z = db.query(Zone).filter(Zone.id == zone_id).first()
    if not z:
        raise HTTPException(status_code=404, detail="Zone not found")
    return z


@router.put("/{zone_id}", response_model=ZoneRead)
def update_zone(zone_id: int, zone_in: ZoneUpdate, db: Session = Depends(get_db), admin=Depends(get_current_active_admin)):
    z = db.query(Zone).filter(Zone.id == zone_id).first()
    if not z:
        raise HTTPException(status_code=404, detail="Zone not found")
    if zone_in.name:
        z.name = zone_in.name
    if zone_in.postal_code is not None:
        z.postal_code = zone_in.postal_code
    if zone_in.geom is not None:
        z.geom = zone_in.geom
    db.add(z)
    db.commit()
    db.refresh(z)
    return z


@router.delete("/{zone_id}")
def delete_zone(zone_id: int, db: Session = Depends(get_db), admin=Depends(get_current_active_admin)):
    z = db.query(Zone).filter(Zone.id == zone_id).first()
    if not z:
        raise HTTPException(status_code=404, detail="Zone not found")
    db.delete(z)
    db.commit()
    return {"ok": True}
