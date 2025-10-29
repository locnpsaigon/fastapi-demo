from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import order_details
from database import get_db
import schemas

router = APIRouter(prefix="/order-details", tags=["order-details"])

@router.get("/", response_model=list[schemas.OrderDetail])
def list_details(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return order_details.get_order_details(db, skip, limit)

@router.post("/{order_id}", response_model=schemas.OrderDetail)
def create_detail(order_id: int, payload: schemas.OrderDetailCreate, db: Session = Depends(get_db)):
    # optional: validate order/product exist
    return order_details.create_order_detail(db, order_id, payload)

@router.get("/{detail_id}", response_model=schemas.OrderDetail)
def get_detail(detail_id: int, db: Session = Depends(get_db)):
    detail = order_details.get_order_detail(db, detail_id)
    if not detail:
        raise HTTPException(status_code=404, detail="Order detail not found")
    return detail

@router.delete("/{detail_id}", response_model=schemas.OrderDetail)
def delete_detail(detail_id: int, db: Session = Depends(get_db)):
    deleted = order_details.delete_order_detail(db, detail_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order detail not found")
    return deleted
