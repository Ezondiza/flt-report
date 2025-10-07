# FILE: app.py
import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import inspect
st.write("Authenticate.login signature:", inspect.signature(stauth.Authenticate.login))


st.set_page_config(page_title="Login Test", page_icon="✅", layout="centered")
st.title("Deployment and Login Test - Stable Version")

# Display version info
try:
    version = getattr(stauth, "__version__", "Unknown")
    st.info(f"streamlit-authenticator version: {version}")
except Exception:
    st.info("streamlit-authenticator version: Unknown")

try:
    # Load config.yaml
    with open('config.yaml', 'r') as file:
        config = yaml.load(file, Loader=SafeLoader)

    # Initialize authenticator (for 0.4.2+)
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    # For 0.4.2 use new login structure
    try:
        name, authentication_status, username = authenticator.login('Login', location='main')
    except TypeError:
        # fallback for older call signature
        name, authentication_status, username = authenticator.login('Login')

    # Auth logic
    if authentication_status:
        st.success(f"Welcome, {name}!")
        authenticator.logout('Logout', location='sidebar')
    elif authentication_status is False:
        st.error("Username or password is incorrect.")
    elif authentication_status is None:
        st.warning("Please enter your username and password.")

except FileNotFoundError:
    st.error("The file 'config.yaml' was not found in your repository.")
except Exception as e:
    st.error(f"Unexpected error: {e}")
