from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Tracking
class TrackingBase(BaseModel):
    status_update: str

class TrackingCreate(TrackingBase):
    shipment_id: int

class Tracking(TrackingBase):
    id: int
    timestamp: datetime
    shipment_id: int

    class Config:
        orm_mode = True

# Shipment
class ShipmentBase(BaseModel):
    origin: str
    destination: str
    method: str                      # "Air" or "Sea"
    container_number: Optional[str] = None
    flight_number: Optional[str] = None
    customer_id: int
    cbm: Optional[float] = None       # Cubic meters
    kgs: Optional[float] = None       # Weight in kilograms
    pieces: Optional[int] = None      # 👈 NEW FIELD (Number of packages/pieces)

class ShipmentCreate(ShipmentBase):
    tracking_number: Optional[str] = None

class Shipment(ShipmentBase):
    id: int
    tracking_number: str
    status: str
    created_at: datetime
    tracking_updates: List[Tracking] = []

    class Config:
        orm_mode = True

# Customer
class CustomerBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    shipments: List[Shipment] = []

    class Config:
        orm_mode = True
