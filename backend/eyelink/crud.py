from sqlalchemy.orm import Session
from . import models, schemas
import uuid
from typing import List, Optional

# Customers
def create_customer(db: Session, customer: schemas.CustomerCreate) -> models.Customer:
    db_customer = models.Customer(**customer.dict())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_customer(db: Session, customer_id: int) -> Optional[models.Customer]:
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()

def get_customer_by_email(db: Session, email: str) -> Optional[models.Customer]:
    return db.query(models.Customer).filter(models.Customer.email == email).first()

def get_customers(db: Session, skip: int = 0, limit: int = 100) -> List[models.Customer]:
    return db.query(models.Customer).offset(skip).limit(limit).all()


# Shipments
def create_shipment(db: Session, shipment: schemas.ShipmentCreate) -> models.Shipment:
    tracking_number = shipment.tracking_number or str(uuid.uuid4()).replace("-", "")[:12].upper()
    payload = shipment.dict()
    payload["tracking_number"] = tracking_number
    db_shipment = models.Shipment(**payload)
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment

def get_shipment(db: Session, shipment_id: int) -> Optional[models.Shipment]:
    return db.query(models.Shipment).filter(models.Shipment.id == shipment_id).first()

def get_shipment_by_tracking(db: Session, tracking_number: str) -> Optional[models.Shipment]:
    return db.query(models.Shipment).filter(models.Shipment.tracking_number == tracking_number).first()

def get_shipments(db: Session, skip: int = 0, limit: int = 100) -> List[models.Shipment]:
    return db.query(models.Shipment).offset(skip).limit(limit).all()

def update_shipment_status(db: Session, shipment_id: int, new_status: str) -> Optional[models.Shipment]:
    db_shipment = get_shipment(db, shipment_id)
    if not db_shipment:
        return None
    db_shipment.status = new_status
    db.commit()
    db.refresh(db_shipment)
    return db_shipment

def delete_shipment(db: Session, shipment_id: int) -> Optional[models.Shipment]:
    db_shipment = get_shipment(db, shipment_id)
    if not db_shipment:
        return None
    db.delete(db_shipment)
    db.commit()
    return db_shipment

# Tracking
def add_tracking_update(db: Session, track: schemas.TrackingCreate) -> models.Tracking:
    db_track = models.Tracking(**track.dict())
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track

def get_tracking_for_shipment(db: Session, shipment_id: int):
    return db.query(models.Tracking).filter(models.Tracking.shipment_id == shipment_id).order_by(models.Tracking.timestamp).all()
