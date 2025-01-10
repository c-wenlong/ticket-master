import streamlit as st
from components import create_ticket_form

st.set_page_config(page_title="Ticket Management System", page_icon="🎫")

if "show_form" not in st.session_state:
    st.session_state.show_form = False

# Simulate a logged-in user
current_user_id = st.session_state.curr_user.id

# Create the ticket form
create_ticket_form(current_user_id)
