import streamlit as st
import pandas as pd
from datetime import datetime, timezone
from typing import List, Union, Dict
from entities import Ticket, Type, Status, Priority


def format_datetime(dt):
    """Format datetime for display"""
    if not dt:
        return ""

    if isinstance(dt, str):
        try:
            # Try to parse ISO format string
            dt = datetime.fromisoformat(dt.replace("Z", "+00:00"))
        except ValueError:
            # If parsing fails, return the original string
            return dt

    if isinstance(dt, datetime):
        return dt.strftime("%Y-%m-%d %H:%M UTC")

    return str(dt)


def get_value(obj: Union[Dict, Ticket], key: str, default=None):
    """Safely get value from either dict or Pydantic object"""
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def ticket_table(tickets: List[Union[Dict, Ticket]]):
    """
    Display and edit tickets in a table format

    Args:
        tickets (list): List of Ticket objects or dictionaries
    """
    if not tickets:
        st.warning("No tickets found")
        return

    # Convert tickets to dataframe for display
    df = pd.DataFrame(
        [
            {
                "ID": get_value(t, "id"),
                "Title": get_value(t, "title"),
                "Type": (
                    get_value(t, "type")
                    if isinstance(t, dict)
                    else get_value(t, "type").value
                ),
                "Status": (
                    get_value(t, "status")
                    if isinstance(t, dict)
                    else get_value(t, "status").value
                ),
                "Priority": (
                    get_value(t, "priority")
                    if isinstance(t, dict)
                    else get_value(t, "priority").value
                ),
                "Assignee": get_value(t, "assignee_id") or "Unassigned",
                "Reporter": get_value(t, "reporter_id"),
                "Created": format_datetime(get_value(t, "created_at")),
                "Updated": format_datetime(get_value(t, "updated_at")),
                "Labels": ", ".join(get_value(t, "labels", [])),
            }
            for t in tickets
        ]
    )

    # Create tabs for view and edit modes
    tab1, tab2 = st.tabs(["View Tickets", "Edit Ticket"])

    with tab1:
        st.dataframe(
            df,
            hide_index=True,
            column_config={
                "ID": st.column_config.TextColumn("ID", width="small"),
                "Title": st.column_config.TextColumn("Title", width="medium"),
                "Type": st.column_config.SelectboxColumn(
                    "Type",
                    options=[t.value for t in Type],
                    width="small",
                ),
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    options=[s.value for s in Status],
                    width="small",
                ),
                "Priority": st.column_config.SelectboxColumn(
                    "Priority",
                    options=[p.value for p in Priority],
                    width="small",
                ),
            },
        )

    with tab2:
        # Ticket selection for editing
        selected_ticket_id = st.selectbox(
            "Select Ticket to Edit",
            options=[get_value(t, "id") for t in tickets],
            format_func=lambda x: f"{x} - {next((get_value(t, 'title') for t in tickets if get_value(t, 'id') == x), '')}",
        )

        if selected_ticket_id:
            ticket = next(
                (t for t in tickets if get_value(t, "id") == selected_ticket_id), None
            )
            if ticket:
                with st.form(key=f"edit_ticket_{selected_ticket_id}"):
                    st.text_input("ID", get_value(ticket, "id"), disabled=True)

                    # Editable fields
                    new_title = st.text_input("Title", get_value(ticket, "title"))
                    new_description = st.text_area(
                        "Description", get_value(ticket, "description")
                    )

                    current_type = get_value(ticket, "type")
                    if isinstance(current_type, Type):
                        current_type = current_type.value
                    new_type = st.selectbox(
                        "Type",
                        options=[t.value for t in Type],
                        index=[t.value for t in Type].index(current_type),
                    )

                    current_status = get_value(ticket, "status")
                    if isinstance(current_status, Status):
                        current_status = current_status.value
                    new_status = st.selectbox(
                        "Status",
                        options=[s.value for s in Status],
                        index=[s.value for s in Status].index(current_status),
                    )

                    current_priority = get_value(ticket, "priority")
                    if isinstance(current_priority, Priority):
                        current_priority = current_priority.value
                    new_priority = st.selectbox(
                        "Priority",
                        options=[p.value for p in Priority],
                        index=[p.value for p in Priority].index(current_priority),
                    )

                    new_assignee = st.text_input(
                        "Assignee ID", get_value(ticket, "assignee_id") or ""
                    )
                    new_labels = st.text_input(
                        "Labels (comma-separated)",
                        ", ".join(get_value(ticket, "labels", [])),
                    )

                    # Read-only fields
                    st.text_input(
                        "Reporter", get_value(ticket, "reporter_id"), disabled=True
                    )
                    st.text_input(
                        "Created At",
                        format_datetime(get_value(ticket, "created_at")),
                        disabled=True,
                    )
                    st.text_input(
                        "Updated At",
                        format_datetime(get_value(ticket, "updated_at")),
                        disabled=True,
                    )

                    if st.form_submit_button("Update Ticket"):
                        # Create updated ticket
                        updated_data = {
                            "id": get_value(ticket, "id"),
                            "title": new_title,
                            "description": new_description,
                            "type": Type(new_type),
                            "status": Status(new_status),
                            "priority": Priority(new_priority),
                            "assignee_id": (
                                new_assignee if new_assignee != "Unassigned" else None
                            ),
                            "reporter_id": get_value(ticket, "reporter_id"),
                            "created_at": get_value(ticket, "created_at"),
                            "updated_at": datetime.now(timezone.utc),
                            "labels": [
                                label.strip()
                                for label in new_labels.split(",")
                                if label.strip()
                            ],
                            "embedding": get_value(ticket, "embedding"),
                            "parent_ticket_id": get_value(ticket, "parent_ticket_id"),
                        }

                        if isinstance(ticket, dict):
                            updated_ticket = updated_data
                        else:
                            updated_ticket = Ticket(**updated_data)

                        # Save to session state
                        if "tickets" in st.session_state:
                            ticket_index = next(
                                (
                                    i
                                    for i, t in enumerate(st.session_state.tickets)
                                    if get_value(t, "id") == selected_ticket_id
                                ),
                                None,
                            )
                            if ticket_index is not None:
                                st.session_state.tickets[ticket_index] = updated_ticket

                        st.success(f"Ticket {selected_ticket_id} updated successfully!")
                        st.rerun()
