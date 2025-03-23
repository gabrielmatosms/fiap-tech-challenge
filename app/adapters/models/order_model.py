from sqlalchemy import DECIMAL
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import relationship

from app.adapters.models.session import Base
from app.domain.entities.order import OrderStatus
from app.domain.entities.payment import PaymentStatus


class OrderModel(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    status = Column(String, default=OrderStatus.PLACED.value)
    payment_status = Column(String, default=PaymentStatus.PENDING.value)
    total = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())

    customer = relationship("CustomerModel", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())

    order = relationship("OrderModel", back_populates="items")
    product = relationship("ProductModel", back_populates="order_items")
