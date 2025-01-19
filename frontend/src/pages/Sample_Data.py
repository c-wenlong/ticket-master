import streamlit as st
from utils import SAMPLE_TICKETS, SAMPLE_USERS
from services.ticket import list_tickets

st.markdown("## Sample Users")
st.json(SAMPLE_USERS)

st.markdown("## Sample Tickets")
st.json(list_tickets())
