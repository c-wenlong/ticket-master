import streamlit as st
from components import create_ticket_form
from entities import Ticket

st.set_page_config(page_title="Ticket Management System", page_icon="🎫")

# Simulate a logged-in user
current_user_id = st.session_state.curr_user.id

# Create the ticket form
ticket = create_ticket_form(current_user_id)

# Handle form submission
if ticket:
    st.success("Ticket created successfully!")
    st.write("Ticket Details:")
    st.json(ticket)
