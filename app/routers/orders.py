from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import orders
from database import get_db
import schemas

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/", response_model=list[schemas.Order])
def list_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return orders.get_orders(db, skip, limit)

@router.post("/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    # optional: validate customer exists
    return orders.create_order(db, order)

@router.get("/{order_id}", response_model=schemas.Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = orders.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, payload: schemas.OrderCreate, db: Session = Depends(get_db)):
    updated = orders.update_order(db, order_id, payload.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated

@router.delete("/{order_id}", response_model=schemas.Order)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    deleted = orders.delete_order(db, order_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found")
    return deleted
