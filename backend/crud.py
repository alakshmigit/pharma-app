from sqlalchemy.orm import Session
from backend import models, schemas
from typing import List, Optional

def get_order(db: Session, order_id: int):
    return db.query(models.Order).filter(models.Order.order_id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Order).offset(skip).limit(limit).all()

def create_order(db: Session, order: schemas.OrderCreate):
    db_order = models.Order(**order.dict())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    # Create sub-orders for ingredients marked as 'Y'
    ingredients = {
        'carton': order.carton,
        'label': order.label,
        'rm': order.rm,
        'sterios': order.sterios,
        'bottles': order.bottles,
        'm_cups': order.m_cups,
        'caps': order.caps,
        'shippers': order.shippers
    }
    
    for ingredient_name, ingredient_value in ingredients.items():
        if ingredient_value == "Y":
            sub_order = models.SubOrder(
                order_id=db_order.order_id,
                ingredient_type=ingredient_name,
                status="Open",
                main_order_date=db_order.order_date
            )
            db.add(sub_order)
    
    db.commit()
    db.refresh(db_order)
    return db_order

def update_order(db: Session, order_id: int, order_update: schemas.OrderUpdate):
    db_order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if db_order:
        update_data = order_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_order, field, value)
        
        # Handle ingredient changes - remove old sub-orders and create new ones if needed
        if any(field in update_data for field in ['carton', 'label', 'rm', 'sterios', 'bottles', 'm_cups', 'caps', 'shippers']):
            # Remove existing sub-orders
            db.query(models.SubOrder).filter(models.SubOrder.order_id == order_id).delete()
            
            # Create new sub-orders based on updated ingredients
            ingredients = {
                'carton': getattr(db_order, 'carton'),
                'label': getattr(db_order, 'label'),
                'rm': getattr(db_order, 'rm'),
                'sterios': getattr(db_order, 'sterios'),
                'bottles': getattr(db_order, 'bottles'),
                'm_cups': getattr(db_order, 'm_cups'),
                'caps': getattr(db_order, 'caps'),
                'shippers': getattr(db_order, 'shippers')
            }
            
            for ingredient_name, ingredient_value in ingredients.items():
                if ingredient_value == "Y":
                    sub_order = models.SubOrder(
                        order_id=db_order.order_id,
                        ingredient_type=ingredient_name,
                        status="Open",
                        main_order_date=db_order.order_date
                    )
                    db.add(sub_order)
        
        db.commit()
        db.refresh(db_order)
    return db_order

def delete_order(db: Session, order_id: int):
    db_order = db.query(models.Order).filter(models.Order.order_id == order_id).first()
    if db_order:
        # Delete associated sub-orders first
        db.query(models.SubOrder).filter(models.SubOrder.order_id == order_id).delete()
        db.delete(db_order)
        db.commit()
    return db_order

def get_sub_orders(db: Session, order_id: int):
    return db.query(models.SubOrder).filter(models.SubOrder.order_id == order_id).all()

def get_all_sub_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SubOrder).offset(skip).limit(limit).all()

def update_sub_order_status(db: Session, sub_order_id: int, status: schemas.StatusEnum):
    db_sub_order = db.query(models.SubOrder).filter(models.SubOrder.sub_order_id == sub_order_id).first()
    if db_sub_order:
        db_sub_order.status = status
        db.commit()
        db.refresh(db_sub_order)
    return db_sub_order

def get_sub_order(db: Session, sub_order_id: int):
    return db.query(models.SubOrder).filter(models.SubOrder.sub_order_id == sub_order_id).first()

def update_sub_order(db: Session, sub_order_id: int, sub_order_update: schemas.SubOrderUpdate):
    db_sub_order = db.query(models.SubOrder).filter(models.SubOrder.sub_order_id == sub_order_id).first()
    if db_sub_order:
        update_data = sub_order_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_sub_order, field, value)
        db.commit()
        db.refresh(db_sub_order)
    return db_sub_order