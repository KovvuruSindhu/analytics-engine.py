import streamlit as st
import json
import time
from datetime import datetime
import uuid

st.set_page_config(page_title="Unified Event Analytics Engine", layout="wide")

# ------------------------------
# In-Memory Database Simulation
# ------------------------------
apps_db = {}
events_db = []

# ------------------------------
# Helper Functions
# ------------------------------
def generate_api_key():
    return str(uuid.uuid4())

def validate_api_key(api_key):
    return api_key in apps_db.values()

# ------------------------------
# UI - API Key Management
# ------------------------------
st.title("🔑 Unified Event Analytics Engine (Demo)")
st.subheader("Manage API Keys & Collect Event Data")

st.sidebar.header("🔐 API Key Management")
app_name = st.sidebar.text_input("Enter App Name")
if st.sidebar.button("Register App"):
    if app_name:
        api_key = generate_api_key()
        apps_db[app_name] = api_key
        st.sidebar.success(f"API Key for '{app_name}': {api_key}")
    else:
        st.sidebar.error("Please enter a valid App Name.")

st.sidebar.write("### Registered Apps")
if apps_db:
    for k, v in apps_db.items():
        st.sidebar.write(f"**{k}** → `{v}`")
else:
    st.sidebar.info("No registered apps yet.")

# ------------------------------
# Event Collection Section
# ------------------------------
st.header("📥 Collect Analytics Events")

api_key_input = st.text_input("Enter API Key:")
event_name = st.text_input("Event Name:")
url = st.text_input("URL:")
referrer = st.text_input("Referrer:")
device = st.selectbox("Device Type", ["mobile", "desktop", "tablet"])
ip_address = st.text_input("IP Address (Optional):")
browser = st.text_input("Browser:")
os_name = st.text_input("Operating System:")
screen_size = st.text_input("Screen Size:")

if st.button("Submit Event"):
    if validate_api_key(api_key_input):
        event_data = {
            "event": event_name,
            "url": url,
            "referrer": referrer,
            "device": device,
            "ipAddress": ip_address,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": {
                "browser": browser,
                "os": os_name,
                "screenSize": screen_size
            },
            "apiKey": api_key_input
        }
        events_db.append(event_data)
        st.success(f"Event '{event_name}' recorded successfully.")
    else:
        st.error("Invalid API Key!")

# ------------------------------
# Analytics Section
# ------------------------------
st.header("📊 Analytics Dashboard")

if st.button("Generate Summary"):
    if events_db:
        total_events = len(events_db)
        unique_events = len(set([e["event"] for e in events_db]))
        mobile = sum(1 for e in events_db if e["device"] == "mobile")
        desktop = sum(1 for e in events_db if e["device"] == "desktop")
        tablet = sum(1 for e in events_db if e["device"] == "tablet")

        st.write(f"**Total Events:** {total_events}")
        st.write(f"**Unique Event Types:** {unique_events}")
        st.json({
            "deviceData": {
                "mobile": mobile,
                "desktop": desktop,
                "tablet": tablet
            }
        })
    else:
        st.warning("No events available.")

# ------------------------------
# Data Viewer
# ------------------------------
st.header("📂 View Collected Events")
st.dataframe(events_db)
