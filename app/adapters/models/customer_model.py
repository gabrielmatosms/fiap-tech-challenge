from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import func
from sqlalchemy.orm import relationship

from app.adapters.models.session import Base


class CustomerModel(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    cpf = Column(String, index=True)
    email = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), default=func.now())

    orders = relationship("OrderModel", back_populates="customer")
