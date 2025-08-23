import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    created_orders = relationship("Order", foreign_keys="Order.created_by", back_populates="creator")
    modified_orders = relationship("Order", foreign_keys="Order.modified_by", back_populates="modifier")
    created_sub_orders = relationship("SubOrder", back_populates="creator")

class Order(Base):
    __tablename__ = "orders"
    
    order_id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(255), nullable=False)
    product_name = Column(String(255), nullable=False)
    molecule = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="Open")
    quantity = Column(Integer, nullable=False)
    pack = Column(String(100), nullable=False)
    order_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Audit fields
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    modified_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    created_date = Column(DateTime, default=datetime.utcnow)
    modified_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Ingredients
    carton = Column(String(10), nullable=False, default="N/A")
    label = Column(String(10), nullable=False, default="N/A")
    rm = Column(String(10), nullable=False, default="N/A")
    sterios = Column(String(10), nullable=False, default="N/A")
    bottles = Column(String(10), nullable=False, default="N/A")
    m_cups = Column(String(10), nullable=False, default="N/A")
    caps = Column(String(10), nullable=False, default="N/A")
    shippers = Column(String(10), nullable=False, default="N/A")
    
    # Relationships
    sub_orders = relationship("SubOrder", back_populates="order")
    creator = relationship("User", foreign_keys=[created_by], back_populates="created_orders")
    modifier = relationship("User", foreign_keys=[modified_by], back_populates="modified_orders")

class SubOrder(Base):
    __tablename__ = "sub_orders"
    
    sub_order_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False)
    ingredient_type = Column(String(50), nullable=False)  # carton, label, rm, etc.
    status = Column(String(50), nullable=False, default="Open")
    
    # New comprehensive fields
    sub_order_date = Column(DateTime, nullable=True, default=datetime.utcnow)
    vendor_company = Column(String(255), nullable=True)
    product_name = Column(String(255), nullable=True)
    main_order_date = Column(DateTime, nullable=True)
    designer_name = Column(String(255), nullable=True)
    sizes = Column(String(255), nullable=True)
    approved_by_first_name = Column(String(100), nullable=True)
    approved_by_last_name = Column(String(100), nullable=True)
    approved_date = Column(DateTime, nullable=True)
    remarks = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey("users.user_id"), nullable=True)
    
    # Relationships
    order = relationship("Order", back_populates="sub_orders")
    creator = relationship("User", back_populates="created_sub_orders")