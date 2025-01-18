import streamlit as st
from utils import SAMPLE_TICKETS, SAMPLE_USERS

st.markdown("## Sample Users")
st.json(SAMPLE_USERS)

st.markdown("## Sample Tickets")
st.json(SAMPLE_TICKETS)
