import streamlit as st
import json
import time

from components import KanbanBoard
from utils import SAMPLE_TICKETS, SAMPLE_USERS
from entities import User
from components import create_ticket_form
from services import text_to_ticket
from entities import Ticket


st.set_page_config(
    page_title="Sprint Kanban Board",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🎯",
)


def initialise_states():
    if "show_manual_form" not in st.session_state:
        st.session_state.show_manual_form = False
    if "show_ai_form" not in st.session_state:
        st.session_state.show_ai_form = False
    if "curr_user" not in st.session_state:
        st.session_state.curr_user = None


def add_ticket():
    manual, ai_assisted = st.columns([1, 1])

    with manual:
        if not st.session_state.show_manual_form:
            if st.button("+ Add Ticket", use_container_width=True):
                st.session_state.show_manual_form = True
                st.session_state.show_ai_form = False  # Close other form if open
                st.rerun()
        else:
            if st.button("❌ Cancel Manual Ticket", use_container_width=True):
                st.session_state.show_manual_form = False
                st.rerun()
            create_ticket_form(st.session_state.curr_user)

    # TODO: this should be a submit form too
    # TODO: integration - after receiving payload (similar tickets) from frontend, decide whether to force insert tickets
    with ai_assisted:
        if not st.session_state.show_ai_form:
            if st.button("+ AI Assisted Ticket", use_container_width=True):
                st.session_state.show_ai_form = True
                st.session_state.show_manual_form = False  # Close other form if open
                st.rerun()
        else:
            if st.button("❌ Cancel AI Ticket", use_container_width=True):
                st.session_state.show_ai_form = False
                st.rerun()
            ticket_prompt = st.text_area("What would your ticket be?")
            if ticket_prompt:
                try:
                    ticket_str = text_to_ticket(ticket_prompt)
                    st.markdown(f"```json\n{ticket_str}\n```")
                    ticket = json.loads(ticket_str)
                    ticket_entity = Ticket(
                        title=ticket["title"],
                        description=ticket["description"],
                        assignee_id=ticket.get("assignee_id", None),
                        status=ticket["status"],
                        type=ticket["type"],
                        priority=ticket["priority"],
                        labels=ticket["labels"],
                        embeddings=ticket.get("embeddings", None),
                    )
                    st.session_state.tickets.append(ticket_entity)
                    st.success("Ticket created successfully!")
                    st.session_state.show_ai_form = False  # Auto-close after success
                    time.sleep(0.5)  # Small delay to show the success message
                    st.rerun()
                # except KeyError:
                #   st.error("Failed to create ticket. Please try again.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")


initialise_states()

if st.session_state.curr_user:
    board = KanbanBoard(SAMPLE_TICKETS)
    board.render()
    add_ticket()
else:
    st.error("Please authenticate first!")
