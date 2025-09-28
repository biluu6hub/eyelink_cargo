from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, func
from sqlalchemy.orm import relationship
from .database import Base

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)

    shipments = relationship("Shipment", back_populates="customer", cascade="all, delete-orphan")


class Shipment(Base):
    __tablename__ = "shipments"
    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String, unique=True, index=True, nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    method = Column(String, nullable=False)           # "Air" or "Sea"
    container_number = Column(String, nullable=True)  # for Sea
    flight_number = Column(String, nullable=True)     # for Air
    status = Column(String, default="Pending")        # Pending, In Transit, Delivered
    cbm = Column(Float, nullable=True)                # Cubic meters
    kgs = Column(Float, nullable=True)                # Weight in kilograms
    pieces = Column(Integer, nullable=True)           # 👈 NEW FIELD (number of packages/pieces)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    customer_id = Column(Integer, ForeignKey("customers.id"))
    customer = relationship("Customer", back_populates="shipments")

    tracking_updates = relationship("Tracking", back_populates="shipment", cascade="all, delete-orphan")


class Tracking(Base):
    __tablename__ = "tracking"
    id = Column(Integer, primary_key=True, index=True)
    status_update = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    shipment_id = Column(Integer, ForeignKey("shipments.id"))
    shipment = relationship("Shipment", back_populates="tracking_updates")
