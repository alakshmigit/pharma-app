from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, func
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime

class Order(Base):
    __tablename__ = "orders"
    
    order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    company_name = Column(String(255), nullable=False, index=True)
    product_name = Column(String(255), nullable=False, index=True)
    molecule = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="Open", index=True)
    quantity = Column(Integer, nullable=False)
    pack = Column(String(100), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Ingredients
    carton = Column(String(10), nullable=False, default="N/A")
    label = Column(String(10), nullable=False, default="N/A")
    rm = Column(String(10), nullable=False, default="N/A")
    sterios = Column(String(10), nullable=False, default="N/A")
    bottles = Column(String(10), nullable=False, default="N/A")
    m_cups = Column(String(10), nullable=False, default="N/A")
    caps = Column(String(10), nullable=False, default="N/A")
    shippers = Column(String(10), nullable=False, default="N/A")
    
    # Relationship
    sub_orders = relationship("SubOrder", back_populates="order", cascade="all, delete-orphan")

class SubOrder(Base):
    __tablename__ = "sub_orders"
    
    sub_order_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id", ondelete="CASCADE"), nullable=False, index=True)
    ingredient_type = Column(String(50), nullable=False, index=True)  # carton, label, rm, etc.
    status = Column(String(50), nullable=False, default="Open", index=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Comprehensive fields
    sub_order_date = Column(DateTime(timezone=True), nullable=True, default=func.now())
    vendor_company = Column(String(255), nullable=True)
    product_name = Column(String(255), nullable=True)
    main_order_date = Column(DateTime(timezone=True), nullable=True)
    designer_name = Column(String(255), nullable=True)
    sizes = Column(String(255), nullable=True)
    approved_by_first_name = Column(String(100), nullable=True)
    approved_by_last_name = Column(String(100), nullable=True)
    approved_date = Column(DateTime(timezone=True), nullable=True)
    remarks = Column(Text, nullable=True)
    
    # Relationship
    order = relationship("Order", back_populates="sub_orders")