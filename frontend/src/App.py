import streamlit as st
import time

from utils import SAMPLE_TICKETS, SAMPLE_USERS, get_user, auth_user
from services.ticket import list_tickets

st.set_page_config(
    layout="centered",
    initial_sidebar_state="expanded",
    page_icon="🎫",
    page_title="Ticket Master",
)


curr_user = SAMPLE_USERS[0]


def initialise_states():
    if "tickets" not in st.session_state:
        st.session_state.tickets = list_tickets()
    if "users" not in st.session_state:
        st.session_state.users = SAMPLE_USERS
    if "curr_user" not in st.session_state:
        st.session_state.curr_user = None


initialise_states()
username = st.session_state.curr_user
if st.session_state.curr_user:
    user = get_user(SAMPLE_USERS, st.session_state.curr_user)
    st.title("Welcome to Ticket Master")
    st.subheader(f"You are logged in as {user.name} with {user.email}")
else:
    st.title("Please log in")


if st.session_state.curr_user == None:
    # LETS LOG IN
    name = st.text_input("What is your name?")
    email = st.text_input("What is your email?")
    submitted = st.button("Let's Go!")

    if submitted:
        user = auth_user(SAMPLE_USERS, name, email)
        if user:
            st.success(f"You have logged in as {user.name} with {user.email}.")
            time.sleep(2)
            st.session_state.curr_user = user.name
            st.rerun()
        else:
            st.error("Not the right credentials...")
