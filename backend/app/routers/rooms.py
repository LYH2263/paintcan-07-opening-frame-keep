from fastapi import APIRouter, HTTPException
from app.schemas.estimate import OpeningTrimRequest
from app.services.paint_service import PaintService
router = APIRouter()
@router.get("/rooms")
def list_rooms():
    with PaintService() as s: return {"items": s.list_rooms()}
@router.get("/rooms/{room_id}")
def room_detail(room_id: int):
    with PaintService() as s:
        d = s.room_detail(room_id)
        if not d: raise HTTPException(404)
        return d
@router.patch("/openings/{opening_id}/trim")
def set_opening_trim(opening_id: int, body: OpeningTrimRequest):
    with PaintService() as s:
        try:
            o = s.set_opening_trim(opening_id, body.trim)
        except ValueError as e:
            raise HTTPException(422, str(e))
        if not o: raise HTTPException(404)
        return {"opening": o}
