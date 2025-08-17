from pydantic import BaseModel
from typing import List, Optional
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
    quantity: int
    pack: str
    status: StatusEnum = StatusEnum.OPEN

class SubOrderCreate(SubOrderBase):
    order_id: int

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