from fastapi import Body
@router.post("/insert_many")
def insert_many_indicators(
    indicators: list[IndicatorCreate] = Body(...),
    db: Session = Depends(get_db),
    admin=Depends(get_current_active_admin),
):
    objs = [
        Indicator(
            source_id=i.source_id,
            type=i.type,
            value=i.value,
            unit=i.unit,
            timestamp=i.timestamp or datetime.utcnow(),
            zone_id=i.zone_id,
            metadata_json=i.metadata_json,
        ) for i in indicators
    ]
    db.add_all(objs)
    db.commit()
    return {"inserted": len(objs)}
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from collections import defaultdict

from app.database import get_db
from app.models.indicator import Indicator
from app.schemas.indicator import IndicatorCreate, IndicatorRead, IndicatorUpdate
from app.core.deps import get_current_active_admin, get_current_active_user

router = APIRouter()


@router.post("/", response_model=IndicatorRead)
def create_indicator(ind_in: IndicatorCreate, db: Session = Depends(get_db), admin=Depends(get_current_active_admin)):
    ind = Indicator(
        source_id=ind_in.source_id,
        type=ind_in.type,
        value=ind_in.value,
        unit=ind_in.unit,
        timestamp=ind_in.timestamp or datetime.utcnow(),
        zone_id=ind_in.zone_id,
        metadata_json=ind_in.metadata_json,
    )
    db.add(ind)
    db.commit()
    db.refresh(ind)
    return ind


@router.get("/", response_model=List[IndicatorRead])
def list_indicators(
    type: Optional[str] = Query(None),
    zone_id: Optional[int] = Query(None),
    from_ts: Optional[str] = Query(None),
    to_ts: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user=Depends(get_current_active_user),
) -> List[Indicator]:
    q = db.query(Indicator)
    if type:
        q = q.filter(Indicator.type == type)
    if zone_id:
        q = q.filter(Indicator.zone_id == zone_id)
    if from_ts:
        try:
            dt = datetime.fromisoformat(from_ts)
            q = q.filter(Indicator.timestamp >= dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="from_ts must be ISO datetime")
    if to_ts:
        try:
            dt = datetime.fromisoformat(to_ts)
            q = q.filter(Indicator.timestamp <= dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="to_ts must be ISO datetime")
    return q.order_by(Indicator.timestamp.desc()).offset(skip).limit(limit).all()


@router.get("/{indicator_id}", response_model=IndicatorRead)
def get_indicator(indicator_id: int, db: Session = Depends(get_db), user=Depends(get_current_active_user)):
    ind = db.query(Indicator).filter(Indicator.id == indicator_id).first()
    if not ind:
        raise HTTPException(status_code=404, detail="Indicator not found")
    return ind


@router.put("/{indicator_id}", response_model=IndicatorRead)
def update_indicator(indicator_id: int, ind_in: IndicatorUpdate, db: Session = Depends(get_db), admin=Depends(get_current_active_admin)):
    ind = db.query(Indicator).filter(Indicator.id == indicator_id).first()
    if not ind:
        raise HTTPException(status_code=404, detail="Indicator not found")
    if ind_in.value is not None:
        ind.value = ind_in.value
    if ind_in.unit is not None:
        ind.unit = ind_in.unit
    if ind_in.timestamp is not None:
        ind.timestamp = ind_in.timestamp
    if ind_in.metadata_json is not None:
        ind.metadata_json = ind_in.metadata_json
    db.add(ind)
    db.commit()
    db.refresh(ind)
    return ind


@router.delete("/{indicator_id}")
def delete_indicator(indicator_id: int, db: Session = Depends(get_db), admin=Depends(get_current_active_admin)):
    ind = db.query(Indicator).filter(Indicator.id == indicator_id).first()
    if not ind:
        raise HTTPException(status_code=404, detail="Indicator not found")
    db.delete(ind)
    db.commit()
    return {"ok": True}


@router.get("/stats/average")
def indicators_average(
    type: Optional[str] = Query(None),
    zone_id: Optional[int] = Query(None),
    from_ts: Optional[str] = Query(None),
    to_ts: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user=Depends(get_current_active_user),
):
    """Return daily averages for the selected indicators (labels=daily dates, series=averages).
    This is a simple implementation that aggregates in Python (works with SQLite)."""
    q = db.query(Indicator)
    if type:
        q = q.filter(Indicator.type == type)
    if zone_id:
        q = q.filter(Indicator.zone_id == zone_id)
    if from_ts:
        try:
            dt = datetime.fromisoformat(from_ts)
            q = q.filter(Indicator.timestamp >= dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="from_ts must be ISO datetime")
    if to_ts:
        try:
            dt = datetime.fromisoformat(to_ts)
            q = q.filter(Indicator.timestamp <= dt)
        except ValueError:
            raise HTTPException(status_code=400, detail="to_ts must be ISO datetime")
    rows = q.all()
    if not rows:
        return {"labels": [], "series": []}
    groups = defaultdict(list)
    for r in rows:
        day = r.timestamp.date().isoformat()
        groups[day].append(r.value)
    labels = sorted(groups.keys())
    series = [sum(groups[d]) / len(groups[d]) for d in labels]
    return {"labels": labels, "series": series}
