from sqlalchemy.orm import Session
import models, schemas

def get_order_details(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.OrderDetail).offset(skip).limit(limit).all()

def create_order_detail(db: Session, order_id: int, detail: schemas.OrderDetailCreate):
    db_detail = models.OrderDetail(
        order_id=order_id,
        product_id=detail.product_id,
        quantity=detail.quantity,
        price=detail.price
    )
    db.add(db_detail)
    db.commit()
    db.refresh(db_detail)
    return db_detail

def get_order_detail(db: Session, detail_id: int):
    return db.query(models.OrderDetail).filter(models.OrderDetail.id == detail_id).first()

def delete_order_detail(db: Session, detail_id: int):
    detail = get_order_detail(db, detail_id)
    if detail:
        db.delete(detail)
        db.commit()
    return detail
