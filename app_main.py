import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import inspect

# -------------------------------------------------
# Streamlit page setup
# -------------------------------------------------
st.set_page_config(page_title="Deployment and Login Test - Stable Version", layout="centered")

st.title("Deployment and Login Test - Stable Version")

# -------------------------------------------------
# Load credentials from config.yaml
# -------------------------------------------------
try:
    with open('config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)
except FileNotFoundError:
    st.error("Missing config.yaml file in current directory.")
    st.stop()

# -------------------------------------------------
# Initialize authenticator
# -------------------------------------------------
try:
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config.get('preauthorized', None)
    )
except Exception as e:
    st.error(f"Error initializing authenticator: {e}")
    st.stop()

# -------------------------------------------------
# Display version info
# -------------------------------------------------
try:
    st.info(f"streamlit-authenticator version: {stauth.__version__}")
except Exception:
    st.info("streamlit-authenticator version: Unknown")

# -------------------------------------------------
# Login section
# -------------------------------------------------
try:
    # Correct for streamlit-authenticator >= 0.4.0
    name, auth_status, username = authenticator.login(location='main')

    if auth_status:
        st.success(f"Welcome {name}")
        st.write("Login successful. You can now view your reports below.")
        authenticator.logout('Logout', 'sidebar')

    elif auth_status is False:
        st.error("Invalid username or password.")

    elif auth_status is None:
        st.warning("Please enter your username and password.")

except Exception as e:
    st.error(f"Unexpected error: {e}")

# -------------------------------------------------
# Footer
# -------------
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("Sita Air | Internal Test Build | Stable Login System")
