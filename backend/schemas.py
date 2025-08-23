from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum

class StatusEnum(str, Enum):
    OPEN = "Open"
    IN_PROCESS = "In-Process"
    CLOSED = "Closed"

class IngredientEnum(str, Enum):
    Y = "Y"
    N = "N"
    NA = "N/A"

class OrderBase(BaseModel):
    company_name: str
    product_name: str
    molecule: str
    status: StatusEnum = StatusEnum.OPEN
    quantity: int
    pack: str
    order_date: Optional[datetime] = None
    carton: IngredientEnum = IngredientEnum.NA
    label: IngredientEnum = IngredientEnum.NA
    rm: IngredientEnum = IngredientEnum.NA
    sterios: IngredientEnum = IngredientEnum.NA
    bottles: IngredientEnum = IngredientEnum.NA
    m_cups: IngredientEnum = IngredientEnum.NA
    caps: IngredientEnum = IngredientEnum.NA
    shippers: IngredientEnum = IngredientEnum.NA

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    company_name: Optional[str] = None
    product_name: Optional[str] = None
    molecule: Optional[str] = None
    status: Optional[StatusEnum] = None
    quantity: Optional[int] = None
    pack: Optional[str] = None
    order_date: Optional[datetime] = None
    carton: Optional[IngredientEnum] = None
    label: Optional[IngredientEnum] = None
    rm: Optional[IngredientEnum] = None
    sterios: Optional[IngredientEnum] = None
    bottles: Optional[IngredientEnum] = None
    m_cups: Optional[IngredientEnum] = None
    caps: Optional[IngredientEnum] = None
    shippers: Optional[IngredientEnum] = None

class SubOrderBase(BaseModel):
    ingredient_type: str
    status: StatusEnum = StatusEnum.OPEN
    sub_order_date: Optional[datetime] = None
    vendor_company: Optional[str] = None
    product_name: Optional[str] = None
    main_order_date: Optional[datetime] = None
    designer_name: Optional[str] = None
    sizes: Optional[str] = None
    approved_by_first_name: Optional[str] = None
    approved_by_last_name: Optional[str] = None
    approved_date: Optional[datetime] = None
    remarks: Optional[str] = None

class SubOrderCreate(SubOrderBase):
    order_id: int

class SubOrderUpdate(BaseModel):
    status: Optional[StatusEnum] = None
    sub_order_date: Optional[datetime] = None
    vendor_company: Optional[str] = None
    product_name: Optional[str] = None
    main_order_date: Optional[datetime] = None
    designer_name: Optional[str] = None
    sizes: Optional[str] = None
    approved_by_first_name: Optional[str] = None
    approved_by_last_name: Optional[str] = None
    approved_date: Optional[datetime] = None
    remarks: Optional[str] = None

class SubOrder(SubOrderBase):
    sub_order_id: int
    order_id: int
    
    class Config:
        from_attributes = True

class Order(OrderBase):
    order_id: int
    sub_orders: List[SubOrder] = []
    
    class Config:
        from_attributes = True

# User schemas for authentication
class UserBase(BaseModel):
    username: str
    email: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    user_id: int
    is_active: bool = True
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None