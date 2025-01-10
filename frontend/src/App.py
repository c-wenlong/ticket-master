import streamlit as st
from entities import User

st.set_page_config(
    layout="centered",
    initial_sidebar_state="expanded",
    page_icon="🎫",
    page_title="Ticket Master",
)

curr_user = User(
    id="USER-TESTING",
    name="Chen Wenlong",
    email="chenwenlong@u.nus.edu",
    role="developer",
)


def initialise_states():
    if "tickets" not in st.session_state:
        st.session_state.tickets = []
    if "show_form" not in st.session_state:
        st.session_state.show_form = False
    if "curr_user" not in st.session_state:
        st.session_state.curr_user = curr_user


st.title("Welcome to Ticket Master")
initialise_states()
st.markdown("## Current User")
st.json(curr_user)
