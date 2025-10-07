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
st.title("Deployment and Login Test - Stable Version")

# Display authenticator version if available
auth_version = getattr(stauth, "__version__", "Unknown")
st.info(f"streamlit-authenticator version: {auth_version}")

try:
    # Load configuration
    with open("config.yaml", "r") as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Initialize authenticator
    authenticator = stauth.Authenticate(
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"]
    )

    # Use only valid location parameters
    try:
        name, auth_status, username = authenticator.login("Login", "main")
    except Exception as e:
        st.error(f"Login error: {e}")
        st.stop()

    # Authentication status control
    if auth_status:
        st.success(f"Welcome, {name}!")
        try:
            authenticator.logout("Logout", "sidebar")
        except Exception:
            authenticator.logout("Logout")
    elif auth_status is False:
        st.error("Incorrect username or password.")
    elif auth_status is None:
        st.warning("Please enter your credentials.")

except FileNotFoundError:
    st.error("Missing config.yaml file in the repository.")
except Exception as e:
    st.error(f"Unexpected error: {e}")
