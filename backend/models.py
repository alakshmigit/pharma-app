from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from config.database import Base
from datetime import datetime

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
    sub_orders = relationship("SubOrder", back_populates="order")

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
    
    # Relationship
    order = relationship("Order", back_populates="sub_orders")