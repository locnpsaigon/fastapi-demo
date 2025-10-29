from sqlalchemy.orm import Session
import models, schemas

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def create_order(db: Session, order: schemas.OrderCreate):
    # create Order
    db_order = models.Order(
        code=order.code,
        description=order.description,
        status=order.status,
        customer_id=order.customer_id
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    # create details if provided
    if order.details:
        for d in order.details:
            detail = models.OrderDetail(
                order_id=db_order.id,
                product_id=d.product_id,
                quantity=d.quantity,
                price=d.price
            )
            db.add(detail)
        db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.id == order_id).first()

def update_order(db: Session, order_id: int, data: dict):
    db_order = get_order(db, order_id)
    if not db_order:
        return None
    for k, v in data.items():
        setattr(db_order, k, v)
    db.commit()
    db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)
    if db_order:
        db.delete(db_order)
        db.commit()
    return db_order
