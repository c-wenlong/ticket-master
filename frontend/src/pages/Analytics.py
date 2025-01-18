import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta, timezone
from services import get_analytics_page_header, generate_lead_time, \
generate_tix_status_breakdown, group_events_by_tix, generate_sprint_burndown, \
generate_tix_status_per_unit_time
from utils import get_sample_analytics

class ScrumDashboard:
    def __init__(self):
        st.set_page_config(page_title="Scrum Dashboard", layout="wide")
        
        # Initialize session state
        # if 'selected_sprint' not in st.session_state:
        #     st.session_state.selected_sprint = "Sprint 1"

    def sprint_overview(self, sprint_data: dict):
        """Display sprint overview metrics."""
        st.header("Sprint Overview")
        
        # Create three columns for key metrics
        col1, col2 = st.columns(2)
        
        with col1:
            # st.metric(
            #     label="Story Points Completed",
            #     value=sprint_data['completed_points'],
            #     delta=f"{sprint_data['completed_percentage']}%"
            # )
            st.metric(
                label="Days Remaining",
                value=sprint_data['days_remaining']
            )
        
        with col2:
            st.metric(
                label="Tickets In Progress",
                value=sprint_data['in_progress_count']
            )
        
        # with col3:
        #     st.metric(
        #         label="Tickets In Progress",
        #         value=sprint_data['in_progress_count']
        #     )
        
        # with col4:
        #     st.metric(
        #         label="Blockers",
        #         value=sprint_data['blocker_count'],
        #         delta_color="inverse"
        #     )

    def create_burndown_chart(self, burndown_data: pd.DataFrame):
        """Create and display burndown chart."""
        st.subheader("Sprint Burndown")
        
        fig = go.Figure()
        
        # Ideal burndown line
        # fig.add_trace(go.Scatter(
        #     x=burndown_data['date'],
        #     y=burndown_data['ideal_points'],
        #     name='Ideal Burndown',
        #     line=dict(color='gray', dash='dash')
        # ))
        
        # Actual burndown line
        fig.add_trace(go.Scatter(
            x=burndown_data['date'],
            y=burndown_data['actual_points'],
            name='Actual Burndown',
            line=dict(color='blue')
        ))
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Number of tickets Remaining",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def cumulative_flow_diagram(self, cfd_data: pd.DataFrame):
        """Display cumulative flow diagram."""
        st.subheader("Cumulative Flow Diagram")
        
        # fig = px.bar(
        #     cfd_data,
        #     x='sprint',
        #     y=['completed_points', 'committed_points'],
        #     barmode='group',
        #     height=400
        # )
        fig = px.area(
            cfd_data,
            x='date',
            y=['tickets_open', 'tickets_in_progress', 'tickets_done'], 
            color_discrete_map={
                'tickets_open': 'blue',
                'tickets_in_progress': 'orange',
                'tickets_done': 'green'
            }
        )
        
        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Tickets cumulative count",
            legend_title="Status"
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def ticket_status_breakdown(self, tickets_df: pd.DataFrame):
        """Display ticket status distribution."""
        st.subheader("Ticket Status Breakdown")
        
        # Create pie chart
        fig = px.pie(
            tickets_df, 
            names='status', 
            values='count',
            hole=0.4
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    def display_lead_time(self, lead_time_df: pd.DataFrame):
        """Show lead time for tickets."""
        st.subheader("Lead Time")
        
        fig = px.line(
            lead_time_df,
            x='ticket_id',
            y='lead_time',
            height=400
        )
        
        fig.update_layout(
            xaxis_title="Ticket Id",
            yaxis_title="Lead Time"
        )
        
        st.plotly_chart(fig, use_container_width=True)

def main():
    tickets = get_sample_analytics()[0]
    events_by_ticket = group_events_by_tix(tickets)
    dashboard = ScrumDashboard()
    
    # Sidebar for filters and controls
    # with st.sidebar:
    #     st.title("Sprint Controls")
    #     selected_sprint = st.selectbox(
    #         "Select Sprint",
    #         ["Sprint 1", "Sprint 2", "Sprint 3"]
    #     )
        
    #     st.divider()
        
    #     # Sprint dates
    #     sprint_start = st.date_input("Sprint Start", datetime.now() - timedelta(days=7))
    #     sprint_end = st.date_input("Sprint End", datetime.now() + timedelta(days=7))
    
    # Sample data - replace with your actual data
    sprint_data = {
        'days_remaining': get_analytics_page_header(tickets)[0],
        'in_progress_count': get_analytics_page_header(tickets)[1]
    }
    
    # Create burndown data
    start_time, end_time, burndown_data = generate_sprint_burndown(tickets)
    start_time_convert = datetime.fromtimestamp(start_time / 1000, timezone.utc)
    end_time_convert = datetime.fromtimestamp(end_time / 1000, timezone.utc)
    # st.write(start_time_convert, end_time_convert)
    # st.write(burndown_data)
    date_range = pd.date_range(start_time_convert, end_time_convert)
    # num_days = len(date_range)
    
    # Calculate ideal burndown (linear decrease)
    # start_points = 100
    # daily_decrease = start_points / (num_days - 1)
    # ideal_points = [start_points - (daily_decrease * i) for i in range(num_days)]
    
    # Sample actual points (ensure same length as dates)
    # actual_points = [
    #     start_points * (1 - i/num_days) + np.random.randint(-5, 5) 
    #     for i in range(num_days)
    # ]
    
    burndown_data = pd.DataFrame({
        'date': date_range,
        # 'ideal_points': ideal_points,
        'actual_points': burndown_data
    })
    
    tickets_open, tickets_in_progress, tickets_done = generate_tix_status_per_unit_time(tickets)
    cfd_data = pd.DataFrame({
        'date': date_range,
        'tickets_open': tickets_open,
        'tickets_in_progress': tickets_in_progress,
        'tickets_done': tickets_done
    })
    
    # Create velocity data
    # velocity_data = pd.DataFrame({
    #     'sprint': ['Sprint 1', 'Sprint 2', 'Sprint 3'],
    #     'completed_points': [45, 50, 34],
    #     'committed_points': [50, 55, 45]
    # })
    
    ticket_status = generate_tix_status_breakdown(events_by_ticket)
    # st.write(ticket_status)
    # Create ticket status data
    tickets_df = pd.DataFrame({
        'status': ticket_status.keys(),
        'count': ticket_status.values()
    })
    
    lead_time = generate_lead_time(events_by_ticket)
    # st.write(lead_time)
    # Create team workload data
    lead_time_df = pd.DataFrame({
        'ticket_id': lead_time.keys(),
        'lead_time': lead_time.values()
    })
    # team_workload = pd.DataFrame({
    #     'team_member': ['Alice', 'Bob', 'Charlie', 'David'],
    #     'story_points': [13, 8, 21, 13],
    #     'status': ['In Progress', 'To Do', 'In Progress', 'Review']
    # })
    
    # Display dashboard components
    dashboard.sprint_overview(sprint_data)
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        dashboard.create_burndown_chart(burndown_data)
        dashboard.ticket_status_breakdown(tickets_df)
    
    with col2:
        dashboard.cumulative_flow_diagram(cfd_data)
        dashboard.display_lead_time(lead_time_df)

if __name__ == "__main__":
    main()