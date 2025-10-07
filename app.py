# FILE: app.py
import streamlit as st
import yaml
from yaml.loader import SafeLoader

try:
    import streamlit_authenticator as stauth
except ModuleNotFoundError:
    st.error("streamlit-authenticator not installed. Check requirements.txt.")
    st.stop()

st.set_page_config(page_title="Login Test", page_icon="✅", layout="centered")
st.title("Deployment and Login Test - Clean Build")

st.info(f"streamlit-authenticator version: {getattr(stauth, '__version__', 'Unknown')}")

try:
    with open('config.yaml', 'r') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    try:
        name, authentication_status, username = authenticator.login('Login', location='sidebar')
    except TypeError:
        name, authentication_status, username = authenticator.login('Login')

    if authentication_status:
        st.success(f"Welcome, {name}!")
        authenticator.logout('Logout', location='sidebar')
    elif authentication_status is False:
        st.error("Incorrect username or password.")
    elif authentication_status is None:
        st.warning("Please enter your credentials.")

except FileNotFoundError:
    st.error("Missing config.yaml file in repository.")
except Exception as e:
    st.error(f"Unexpected error: {e}")
