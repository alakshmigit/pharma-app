import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
import uvicorn

import crud, models, schemas
from auth import authenticate_user, create_access_token, get_current_active_user, get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES
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

# Authentication endpoints
@app.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login", response_model=schemas.Token)
def login_user(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@app.get("/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_active_user)):
    return current_user

@app.post("/orders/", response_model=schemas.Order)
def create_order(
    order: schemas.OrderCreate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_order = crud.create_order(db=db, order=order, user_id=current_user.user_id)
    return schemas.Order.model_validate(db_order)

@app.get("/orders/", response_model=List[schemas.Order])
def read_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = crud.get_orders(db, skip=skip, limit=limit)
    return [schemas.Order.model_validate(order) for order in orders]

@app.get("/orders/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = crud.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return schemas.Order.model_validate(db_order)

@app.put("/orders/{order_id}", response_model=schemas.Order)
def update_order(
    order_id: int, 
    order: schemas.OrderUpdate, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_order = crud.update_order(db, order_id=order_id, order_update=order, user_id=current_user.user_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return schemas.Order.model_validate(db_order)

@app.delete("/orders/{order_id}")
def delete_order(
    order_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
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

@app.put("/sub-orders/{sub_order_id}", response_model=schemas.SubOrder)
def update_sub_order(sub_order_id: int, sub_order: schemas.SubOrderUpdate, db: Session = Depends(get_db)):
    db_sub_order = crud.update_sub_order(db, sub_order_id=sub_order_id, sub_order_update=sub_order)
    if db_sub_order is None:
        raise HTTPException(status_code=404, detail="Sub-order not found")
    return db_sub_order

@app.get("/sub-orders/{sub_order_id}", response_model=schemas.SubOrder)
def read_sub_order(sub_order_id: int, db: Session = Depends(get_db)):
    db_sub_order = crud.get_sub_order(db, sub_order_id=sub_order_id)
    if db_sub_order is None:
        raise HTTPException(status_code=404, detail="Sub-order not found")
    return db_sub_order

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)