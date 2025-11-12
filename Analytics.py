import streamlit as st
import json
from datetime import datetime
import uuid

st.set_page_config(page_title="Unified Event Analytics Engine", layout="wide")

# ------------------------------
# Persistent In-Memory Storage
# ------------------------------
if "apps_db" not in st.session_state:
    st.session_state.apps_db = {"DemoApp": "demo-api-key-001"}  # default demo app

if "events_db" not in st.session_state:
    st.session_state.events_db = []

# ------------------------------
# Helper Functions
# ------------------------------
def generate_api_key():
    return str(uuid.uuid4())

def validate_api_key(api_key):
    return api_key in st.session_state.apps_db.values()

# ------------------------------
# Sidebar - App Management
# ------------------------------
st.sidebar.header("🔐 API Key Management")
app_name = st.sidebar.text_input("Enter App Name")

if st.sidebar.button("Register App"):
    if app_name:
        api_key = generate_api_key()
        st.session_state.apps_db[app_name] = api_key
        st.sidebar.success(f"API Key for '{app_name}': {api_key}")
    else:
        st.sidebar.error("Please enter a valid App Name.")

st.sidebar.write("### Registered Apps")
for k, v in st.session_state.apps_db.items():
    st.sidebar.write(f"**{k}** → `{v}`")

# ------------------------------
# Event Submission
# ------------------------------
st.title("🔑 Unified Event Analytics Engine (Demo)")
st.subheader("Collect and Analyze Event Data")

with st.expander("📌 Example Input"):
    st.json({
        "apiKey": "demo-api-key-001",
        "event": "button_click",
        "url": "https://example.com/home",
        "referrer": "https://google.com",
        "device": "desktop",
        "ipAddress": "192.168.1.1",
        "metadata": {
            "browser": "Chrome",
            "os": "Windows",
            "screenSize": "1366x768"
        }
    })

api_key_input = st.text_input("Enter API Key:", value="demo-api-key-001")
event_name = st.text_input("Event Name:", value="button_click")
url = st.text_input("URL:", value="https://example.com/home")
referrer = st.text_input("Referrer:", value="https://google.com")
device = st.selectbox("Device Type", ["desktop", "mobile", "tablet"])
ip_address = st.text_input("IP Address:", value="192.168.1.1")
browser = st.text_input("Browser:", value="Chrome")
os_name = st.text_input("Operating System:", value="Windows")
screen_size = st.text_input("Screen Size:", value="1366x768")

if st.button("🚀 Submit Event"):
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
        st.session_state.events_db.append(event_data)
        st.success(f"✅ Event '{event_name}' recorded successfully.")
    else:
        st.error("❌ Invalid API Key! Please check or register a new one.")

# ------------------------------
# Analytics Dashboard
# ------------------------------
st.header("📊 Analytics Dashboard")

if st.button("📈 Generate Summary"):
    if st.session_state.events_db:
        total_events = len(st.session_state.events_db)
        unique_events = len(set(e["event"] for e in st.session_state.events_db))
        device_counts = {
            "desktop": sum(1 for e in st.session_state.events_db if e["device"] == "desktop"),
            "mobile": sum(1 for e in st.session_state.events_db if e["device"] == "mobile"),
            "tablet": sum(1 for e in st.session_state.events_db if e["device"] == "tablet"),
        }

        st.write(f"**Total Events:** {total_events}")
        st.write(f"**Unique Event Types:** {unique_events}")
        st.json({"deviceData": device_counts})
    else:
        st.warning("No events to analyze yet!")

# ------------------------------
# View Collected Events
# ------------------------------
st.header("📂 View Collected Events")
if st.session_state.events_db:
    st.dataframe(st.session_state.events_db)
else:
    st.info("No events submitted yet.")
