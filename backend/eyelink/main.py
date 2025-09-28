from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import crud, schemas
from .database import init_db, get_db

# create tables (safe to call even if they already exist)
init_db()

app = FastAPI(title="EyeLink Cargo API 🚛✈️🚢", version="1.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to EyeLink Cargo API 🚛✈️🚢"}

# ---------- Customers ----------
@app.post("/customers/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    if crud.get_customer_by_email(db, customer.email):
        raise HTTPException(status_code=400, detail="Customer already exists")
    return crud.create_customer(db, customer)

@app.get("/customers/", response_model=List[schemas.Customer])
def list_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_customers(db, skip=skip, limit=limit)

@app.get("/customers/{customer_id}", response_model=schemas.Customer)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    cust = crud.get_customer(db, customer_id)
    if not cust:
        raise HTTPException(status_code=404, detail="Customer not found")
    return cust

# ---------- Shipments ----------
@app.post("/shipments/", response_model=schemas.Shipment)
def create_shipment(shipment: schemas.ShipmentCreate, db: Session = Depends(get_db)):
    # ensure customer exists
    if not crud.get_customer(db, shipment.customer_id):
        raise HTTPException(status_code=400, detail="customer_id does not exist")
    # basic validation: if method is Air require flight_number; if Sea require container_number (you can relax if you like)
    if shipment.method.lower() == "air" and not shipment.flight_number:
        raise HTTPException(status_code=400, detail="flight_number required for Air shipments")
    if shipment.method.lower() == "sea" and not shipment.container_number:
        raise HTTPException(status_code=400, detail="container_number required for Sea shipments")
    return crud.create_shipment(db, shipment)

@app.get("/shipments/", response_model=List[schemas.Shipment])
def list_shipments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_shipments(db, skip=skip, limit=limit)

@app.get("/shipments/{shipment_id}", response_model=schemas.Shipment)
def get_shipment(shipment_id: int, db: Session = Depends(get_db)):
    s = crud.get_shipment(db, shipment_id)
    if not s:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return s

@app.get("/shipments/by-tracking/{tracking_number}", response_model=schemas.Shipment)
def get_shipment_by_tracking(tracking_number: str, db: Session = Depends(get_db)):
    s = crud.get_shipment_by_tracking(db, tracking_number)
    if not s:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return s

@app.put("/shipments/{shipment_id}/status", response_model=schemas.Shipment)
def update_shipment_status(shipment_id: int, status: str, db: Session = Depends(get_db)):
    s = crud.update_shipment_status(db, shipment_id, status)
    if not s:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return s

@app.delete("/shipments/{shipment_id}", response_model=schemas.Shipment)
def delete_shipment(shipment_id: int, db: Session = Depends(get_db)):
    s = crud.delete_shipment(db, shipment_id)
    if not s:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return s

# ---------- Tracking ----------
@app.post("/tracking/", response_model=schemas.Tracking)
def add_tracking(track: schemas.TrackingCreate, db: Session = Depends(get_db)):
    if not crud.get_shipment(db, track.shipment_id):
        raise HTTPException(status_code=400, detail="Shipment does not exist")
    return crud.add_tracking_update(db, track)

@app.get("/tracking/{shipment_id}", response_model=List[schemas.Tracking])
def get_tracking(shipment_id: int, db: Session = Depends(get_db)):
    if not crud.get_shipment(db, shipment_id):
        raise HTTPException(status_code=404, detail="Shipment not found")
    return crud.get_tracking_for_shipment(db, shipment_id)

