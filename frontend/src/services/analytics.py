from typing import Dict, Union
from datetime import datetime, timezone
from collections import defaultdict

def group_events_by_tix(tickets): 
    # Group events by ticket_id
    events_by_ticket = {}
    for event in tickets["events"]:
        if event["ticket_id"] not in events_by_ticket:
            events_by_ticket[event["ticket_id"]] = []
        events_by_ticket[event["ticket_id"]].append(event)
    
    for ticket_id, events in events_by_ticket.items(): 
        events = list(events)
        events.sort(key=lambda e: e["timestamp"])
        events_by_ticket[ticket_id] = events
        
    return events_by_ticket

def get_analytics_page_header(tickets):
    events_by_ticket = group_events_by_tix(tickets)
    days_remaining_in_sprint = ((tickets["end_time"] - int(datetime.now().timestamp() * 1000))/1000)/86400
    num_in_progress_tix = 0
    for ticket_id, events in events_by_ticket.items(): 
        tix_in_progress = False
        for event in events:
            if event["description"] == "update status - in_progress":
                tix_in_progress = True
            elif event["description"] == "complete ticket":
                tix_in_progress = False
        if tix_in_progress: num_in_progress_tix += 1
            
    return int(days_remaining_in_sprint), num_in_progress_tix
    
# tickets = get_sample_analytics()[0]
# print(tickets)
# events_by_ticket = group_events_by_tix(tickets)

def generate_lead_time(events_by_ticket):
    cycle_times: Dict[str, Union[int, None]] = {}

    # Calculate cycle time for each ticket
    for ticket_id, events in events_by_ticket.items():
        # Find the earliest "create ticket" event
        created_event = min(
            (e for e in events if e["description"] == "create ticket"),
            key=lambda e: e["timestamp"],
            default=None
        )

        # Find the latest "complete ticket" event
        completed_event = max(
            (e for e in events if e["description"] == "complete ticket"),
            key=lambda e: e["timestamp"],
            default=None
        )
        
        if not completed_event: 
            current_time = int(datetime.now().timestamp() * 1000)

            completed_event = {
                "ticket_id": ticket_id,
                "timestamp": current_time,
                "description": "complete ticket",
                "status": "done",
                "priority": created_event["priority"]
            }
        
        # created_event = next((e for e in events if e.description == "ticket created"), None)
        # completed_event = next((e for e in events if e.description == "ticket completed"), None)

        if created_event and completed_event:
            cycle_time = completed_event["timestamp"] - created_event["timestamp"] # in milliseconds
            cycle_time = cycle_time/1000/86400 # Convert to days
            cycle_times[ticket_id] = round(cycle_time, 2) 
        else:
            cycle_times[ticket_id] = None  # Cannot calculate cycle time

    return cycle_times 

def generate_tix_status_breakdown(events_by_ticket): 
    latest_statuses = {"Open": 0, "In Progress": 0, "Done": 0}
    
    # Process each ticket's events to determine the latest status
    for ticket_id, events in events_by_ticket.items():
        # Sort events by timestamp
        events.sort(key=lambda e: e["timestamp"])

        current_status = "open"  # Default status if no updates are present

        for event in events:
            if event["description"].startswith("update status -"):
                # Extract status from "update status - {STATUS}"
                current_status = event["description"].split("update status - ")[1]
            elif event["description"] == "complete ticket":
                current_status = "done"

        if current_status == "open": latest_statuses["Open"] += 1
        elif current_status == "in_progress": latest_statuses["In Progress"] += 1
        else: latest_statuses["Done"] += 1
    
    return latest_statuses

def generate_tix_status_per_unit_time(tickets): 
    events = tickets["events"]
    start_time = tickets["start_time"]
    print(start_time)
    end_time = tickets["end_time"]

    # Step 1: Sort all events by timestamp
    events_sorted = sorted(events, key=lambda x: x['timestamp'])

    # Step 2: Initialize tracking dictionaries
    ticket_statuses = defaultdict(str)  # Track status of each ticket

    # Step 3: Initialize data lists
    time_points = []
    tickets_open = []
    tickets_in_progress = []
    tickets_done = []

    # Step 4: Generate daily time points
    current_time = start_time
    while current_time <= end_time:
        time_points.append(current_time)
        current_time += 24 * 60 * 60 * 1000  # Add one day in milliseconds

    # Step 5: Iterate through daily time points and update ticket statuses
    event_index = 0
    for time_point in time_points:
        # Process events up to the current time point
        while event_index < len(events_sorted) and events_sorted[event_index]["timestamp"] <= time_point:
            event = events_sorted[event_index]
            ticket_id = event["ticket_id"]
            if event["description"] == "create ticket":
                ticket_statuses[ticket_id] = "open"
            elif event["description"] == "update status - in_progress":
                ticket_statuses[ticket_id] = "in_progress"
            elif event["description"] == "complete ticket":
                ticket_statuses[ticket_id] = "done"
            event_index += 1

        # Count tickets that are not yet completed
        tickets_open.append(sum(1 for status in ticket_statuses.values() if status == "open"))
        tickets_in_progress.append(sum(1 for status in ticket_statuses.values() if status == "in_progress"))
        tickets_done.append(sum(1 for status in ticket_statuses.values() if status == "done"))

    # Convert time_points from timestamps to readable dates
    # time_points_readable = [datetime.utcfromtimestamp(tp / 1000).strftime('%Y-%m-%d') for tp in time_points]
    return tickets_open, tickets_in_progress, tickets_done

def generate_sprint_burndown(tickets): 
    tickets_open, tickets_in_progress, _ = generate_tix_status_per_unit_time(tickets)
    tickets_remaining = [tickets_open[i] + tickets_in_progress[i] for i in range(len(tickets_open))]

    return tickets["start_time"], tickets["end_time"], tickets_remaining