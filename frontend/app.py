import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"  # FastAPI backend URL

st.set_page_config(page_title="EyeLink Cargo", layout="wide")
st.title("EyeLink Cargo Web App")

# --------------------- Helper Functions ---------------------
def fetch_customers():
    try:
        r = requests.get(f"{API_BASE}/customers/")
        return r.json() if r.status_code == 200 else []
    except Exception as e:
        st.error(f"Cannot fetch customers: {e}")
        return []

def create_customer(data):
    try:
        return requests.post(f"{API_BASE}/customers/", json=data)
    except Exception as e:
        st.error(f"Error creating customer: {e}")
        return None

def create_shipment(data):
    try:
        return requests.post(f"{API_BASE}/shipments/", json=data)
    except Exception as e:
        st.error(f"Error creating shipment: {e}")
        return None

def list_shipments():
    try:
        r = requests.get(f"{API_BASE}/shipments/")
        return r.json() if r.status_code == 200 else []
    except Exception as e:
        st.error(f"Cannot fetch shipments: {e}")
        return []


# --------------------- Layout ---------------------
col1, col2 = st.columns([1, 1])

# ----- Add Customer -----
with col1:
    st.header("➕ Add Customer")
    c_name = st.text_input("Name")
    c_email = st.text_input("Email")
    c_phone = st.text_input("Phone")
    if st.button("Save Customer"):
        if not c_name or not c_email:
            st.warning("Name and Email are required.")
        else:
            r = create_customer({"name": c_name, "email": c_email, "phone": c_phone})
            if r and r.status_code in (200, 201):
                st.success("Customer saved!")
            else:
                st.error(f"Failed to create customer ({r.status_code if r else 'No response'})")

    st.markdown("---")
    st.subheader("Existing Customers")
    for cust in fetch_customers():
        st.write(f"ID {cust['id']} • {cust['name']} • {cust['email']} • {cust.get('phone','')}")

# ----- Create Shipment -----
with col2:
    st.header("📦 Create Shipment")
    customers = fetch_customers()
    if customers:
        cust_map = {f"{c['id']} - {c['name']}": c['id'] for c in customers}
        cust_choice = st.selectbox("Select Customer", list(cust_map.keys()))
        customer_id = cust_map[cust_choice]
    else:
        st.info("Add a customer first.")
        customer_id = None

    tracking_number = st.text_input("Tracking Number")
    origin = st.text_input("Origin")
    destination = st.text_input("Destination")
    method = st.selectbox("Method", ["Air", "Sea"])
    container_number = st.text_input("Container Number (for Sea)")
    flight_number = st.text_input("Flight Number (for Air)")
    cbm = st.number_input("CBM (cubic meters)", min_value=0.0, step=0.01)
    kgs = st.number_input("KGS (weight)", min_value=0.0, step=0.1)
    pieces = st.number_input("Pieces (number of packages)", min_value=0, step=1)

    if st.button("Save Shipment"):
        if not customer_id or not origin or not destination or not method:
            st.error("Customer, Origin, Destination, and Method are required.")
        else:
            payload = {
                "customer_id": customer_id,
                "tracking_number": tracking_number or None,
                "origin": origin,
                "destination": destination,
                "method": method,
                "container_number": container_number or None,
                "flight_number": flight_number or None,
                "cbm": float(cbm) if cbm else None,
                "kgs": float(kgs) if kgs else None,
                "pieces": int(pieces) if pieces else None
            }
            r = create_shipment(payload)
            if r and r.status_code in (200, 201):
                st.success("Shipment saved!")
            else:
                st.error(f"Failed to create shipment ({r.status_code if r else 'No response'})")

st.markdown("---")
st.header("📋 All Shipments")
for s in list_shipments():
    st.write(
        f"ID {s['id']} | {s.get('tracking_number','-')} | "
        f"{s['origin']} → {s['destination']} | "
        f"Method: {s['method']} | CBM: {s.get('cbm')} | "
        f"KGS: {s.get('kgs')} | Pieces: {s.get('pieces')} | Status: {s['status']}"
    )
