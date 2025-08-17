from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import uvicorn

from . import crud, models, schemas
from config.database import SessionLocal, engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Order Management API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Order Management API"}

@app.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db=db, order=order)

@app.get("/orders/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return orders

@app.get("/orders/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@app.put("/orders/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, order: schemas.OrderUpdate, db: Session = Depends(get_db)):
    db_order = crud.update_order(db, order_id=order_id, order_update=order)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return db_order

@app.delete("/orders/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.delete_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted successfully"}

@app.get("/orders/{order_id}/sub-orders/", response_model=List[schemas.SubOrder])
def read_sub_orders(order_id: int, db: Session = Depends(get_db)):
    return crud.get_sub_orders(db, order_id=order_id)

@app.get("/sub-orders/", response_model=List[schemas.SubOrder])
def read_all_sub_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_all_sub_orders(db, skip=skip, limit=limit)

@app.put("/sub-orders/{sub_order_id}/status")
def update_sub_order_status(sub_order_id: int, status: schemas.StatusEnum, db: Session = Depends(get_db)):
    db_sub_order = crud.update_sub_order_status(db, sub_order_id=sub_order_id, status=status)
    if db_sub_order is None:
        raise HTTPException(status_code=404, detail="Sub-order not found")
    return {"message": "Sub-order status updated successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)