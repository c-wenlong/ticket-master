import streamlit as st
from entities import User

st.set_page_config(
    layout="centered",
    initial_sidebar_state="expanded",
    page_icon="🎫",
    page_title="Ticket Master",
)
st.title("Welcome to Ticket Master")

curr_user = User(
    id="USER-TESTING",
    name="Chen Wenlong",
    email="chenwenlong@u.nus.edu",
    role="developer",
)

st.markdown("## Current User")
st.session_state.curr_user = curr_user
st.json(curr_user)
