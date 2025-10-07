# FILE: app.py
import streamlit as st
import yaml
from yaml.loader import SafeLoader

try:
    import streamlit_authenticator as stauth
except ModuleNotFoundError:
    st.error("streamlit-authenticator not installed. Check requirements.txt.")
    st.stop()

st.set_page_config(page_title="Flight Report Login", page_icon="✈️", layout="centered")
st.title("Deployment and Login Test - Compatible Version")

# Check authenticator version
auth_version = getattr(stauth, "__version__", "Unknown")
st.info(f"streamlit-authenticator version: {auth_version}")

try:
    # Load YAML config
    with open("config.yaml", "r") as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Initialize authenticator
    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"]
    )

    # Try positional arguments first (old versions)
    try:
        name, auth_status, username = authenticator.login("Login", "main")
    except TypeError:
        # Fallback: single argument for older versions
        name, auth_status, username = authenticator.login("Login")

    # Authentication result handling
    if auth_status:
        st.success(f"Welcome, {name}!")
        try:
            authenticator.logout("Logout", "sidebar")
        except TypeError:
            authenticator.logout("Logout")
    elif auth_status is False:
        st.error("Incorrect username or password.")
    elif auth_status is None:
        st.warning("Please enter your credentials.")

except FileNotFoundError:
    st.error("Missing config.yaml file.")
except Exception as e:
    st.error(f"Unexpected error: {e}")
