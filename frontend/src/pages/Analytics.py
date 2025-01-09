import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

class ScrumDashboard:
    def __init__(self):
        st.set_page_config(page_title="Scrum Dashboard", layout="wide")
        
        # Initialize session state
        if 'selected_sprint' not in st.session_state:
            st.session_state.selected_sprint = "Sprint 1"

    def sprint_overview(self, sprint_data: dict):
        """Display sprint overview metrics."""
        st.header("Sprint Overview")
        
        # Create three columns for key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Story Points Completed",
                value=sprint_data['completed_points'],
                delta=f"{sprint_data['completed_percentage']}%"
            )
        
        with col2:
            st.metric(
                label="Days Remaining",
                value=sprint_data['days_remaining']
            )
        
        with col3:
            st.metric(
                label="Tickets In Progress",
                value=sprint_data['in_progress_count']
            )
        
        with col4:
            st.metric(
                label="Blockers",
                value=sprint_data['blocker_count'],
                delta_color="inverse"
            )

    def create_burndown_chart(self, burndown_data: pd.DataFrame):
        """Create and display burndown chart."""
        st.subheader("Sprint Burndown")
        
        fig = go.Figure()
        
        # Ideal burndown line
        fig.add_trace(go.Scatter(
            x=burndown_data['date'],
            y=burndown_data['ideal_points'],
            name='Ideal Burndown',
            line=dict(color='gray', dash='dash')
        ))
        
        # Actual burndown line
        fig.add_trace(go.Scatter(
            x=burndown_data['date'],
            y=burndown_data['actual_points'],
            name='Actual Burndown',
            line=dict(color='blue')
        ))
        
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Story Points Remaining",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def team_velocity_chart(self, velocity_data: pd.DataFrame):
        """Display team velocity over sprints."""
        st.subheader("Team Velocity")
        
        fig = px.bar(
            velocity_data,
            x='sprint',
            y=['completed_points', 'committed_points'],
            barmode='group',
            height=400
        )
        
        fig.update_layout(
            xaxis_title="Sprint",
            yaxis_title="Story Points",
            legend_title="Points Type"
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

    def display_team_workload(self, team_workload: pd.DataFrame):
        """Show team member workload distribution."""
        st.subheader("Team Workload")
        
        fig = px.bar(
            team_workload,
            x='team_member',
            y='story_points',
            color='status',
            height=400
        )
        
        fig.update_layout(
            xaxis_title="Team Member",
            yaxis_title="Story Points"
        )
        
        st.plotly_chart(fig, use_container_width=True)

def main():
    dashboard = ScrumDashboard()
    
    # Sidebar for filters and controls
    with st.sidebar:
        st.title("Sprint Controls")
        selected_sprint = st.selectbox(
            "Select Sprint",
            ["Sprint 1", "Sprint 2", "Sprint 3"]
        )
        
        st.divider()
        
        # Sprint dates
        sprint_start = st.date_input("Sprint Start", datetime.now() - timedelta(days=7))
        sprint_end = st.date_input("Sprint End", datetime.now() + timedelta(days=7))
    
    # Sample data - replace with your actual data
    sprint_data = {
        'completed_points': 34,
        'completed_percentage': 75,
        'days_remaining': 5,
        'in_progress_count': 8,
        'blocker_count': 2
    }
    
    # Create burndown data
    date_range = pd.date_range(sprint_start, sprint_end)
    num_days = len(date_range)
    
    # Calculate ideal burndown (linear decrease)
    start_points = 100
    daily_decrease = start_points / (num_days - 1)
    ideal_points = [start_points - (daily_decrease * i) for i in range(num_days)]
    
    # Sample actual points (ensure same length as dates)
    actual_points = [
        start_points * (1 - i/num_days) + np.random.randint(-5, 5) 
        for i in range(num_days)
    ]
    
    burndown_data = pd.DataFrame({
        'date': date_range,
        'ideal_points': ideal_points,
        'actual_points': actual_points
    })
    
    # Create velocity data
    velocity_data = pd.DataFrame({
        'sprint': ['Sprint 1', 'Sprint 2', 'Sprint 3'],
        'completed_points': [45, 50, 34],
        'committed_points': [50, 55, 45]
    })
    
    # Create ticket status data
    tickets_df = pd.DataFrame({
        'status': ['To Do', 'In Progress', 'Review', 'Done'],
        'count': [10, 8, 5, 15]
    })
    
    # Create team workload data
    team_workload = pd.DataFrame({
        'team_member': ['Alice', 'Bob', 'Charlie', 'David'],
        'story_points': [13, 8, 21, 13],
        'status': ['In Progress', 'To Do', 'In Progress', 'Review']
    })
    
    # Display dashboard components
    dashboard.sprint_overview(sprint_data)
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        dashboard.create_burndown_chart(burndown_data)
        dashboard.ticket_status_breakdown(tickets_df)
    
    with col2:
        dashboard.team_velocity_chart(velocity_data)
        dashboard.display_team_workload(team_workload)

if __name__ == "__main__":
    main()