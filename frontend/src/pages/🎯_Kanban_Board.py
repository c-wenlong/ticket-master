import streamlit as st
import json
import time
from typing import List

from components import KanbanBoard
from utils import SAMPLE_TICKETS, SAMPLE_USERS
from entities import User
from components import create_ticket_form
from services import text_to_ticket
from entities import Ticket
from services.ticket import list_tickets, generate_ticket, create_tickets, create_ticket


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
            # st.success("Ticket created successfully!")
            # time.sleep(0.5)
            # st.rerun()

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
                    gen_tickets = generate_ticket(ticket_prompt, st.session_state.curr_user, st.session_state.curr_user).model_dump()
                    # st.error(gen_tickets)
                    sub_tickets = gen_tickets["sub_tickets"]
                    if len(sub_tickets) == 0:
                        if len(gen_tickets["master_ticket"]['similar_tickets']) == 0:
                            extracted_master_ticket = []
                            extracted_master_ticket.append(gen_tickets["master_ticket"]['ticket'])
                            created_ticket = create_tickets(extracted_master_ticket)
                            st.session_state.tickets.append(created_ticket)
                            st.success("Ticket created successfully!")
                        else:
                            st.error("Ticket not created. Duplicate detected.")
                    else:
                        extracted_sub_tickets = []
                        for sub_ticket in sub_tickets:
                            if len(sub_ticket['similar_tickets']) == 0:
                                extracted_sub_tickets.append(sub_ticket['ticket'])
                        # TODO: handle dupes based on similarity
                        if len(extracted_sub_tickets) > 0:
                            created_tickets = create_tickets(extracted_sub_tickets)
                            for ticket_entity in created_tickets:
                                st.session_state.tickets.append(ticket_entity)
                            st.success("Ticket(s) created successfully!")
                        else:
                            st.error("Tickets not created. Duplicates detected.")


                    st.session_state.show_ai_form = False  # Auto-close after success
                    time.sleep(2)  # Small delay to show the success message
                    st.rerun()
                # except KeyError:
                #   st.error("Failed to create ticket. Please try again.")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")


initialise_states()

if st.session_state.curr_user:
    board = KanbanBoard(list_tickets())
    board.render()
    add_ticket()
else:
    st.error("Please authenticate first!")
