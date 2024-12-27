import pytest
from datetime import datetime
from pydantic import ValidationError
from schemas import (
    Ticket,
    TicketType,
    TicketPriority,
    TicketStatus,
)  # Assuming previous schema is in ticket_schema.py


def test_minimal_valid_ticket():
    """Test creation of ticket with only required fields."""
    ticket = Ticket(
        title="Fix login page error",
        description="Login page crashes with special characters",
    )
    assert ticket.title == "Fix login page error"
    assert ticket.description == "Login page crashes with special characters"
    assert ticket.type == TicketType.TASK  # default value
    assert ticket.priority == TicketPriority.MEDIUM  # default value
    assert ticket.status == TicketStatus.NEW  # default value
    assert isinstance(ticket.created, datetime)
    assert isinstance(ticket.id, str)
    assert ticket.id.startswith("TICKET-")
    assert len(ticket.components) == 0  # empty list by default
    assert len(ticket.labels) == 0  # empty list by default


def test_full_valid_ticket():
    """Test creation of ticket with all fields specified."""
    ticket = Ticket(
        title="Implement OAuth2 Authentication",
        description="Add OAuth2 authentication support",
        type=TicketType.FEATURE,
        priority=TicketPriority.HIGH,
        status=TicketStatus.IN_PROGRESS,
        components=["Authentication", "Frontend"],
        labels=["security", "user-experience"],
    )
    assert ticket.type == TicketType.FEATURE
    assert ticket.priority == TicketPriority.HIGH
    assert ticket.status == TicketStatus.IN_PROGRESS
    assert ticket.components == ["Authentication", "Frontend"]
    assert ticket.labels == ["security", "user-experience"]


def test_title_validation():
    """Test title field validation rules."""
    # Test title too short (single word)
    with pytest.raises(ValidationError) as exc_info:
        Ticket(title="Login", description="Test description")
    assert "Title must contain at least two words" in str(exc_info.value)

    # Test title too long (>100 chars)
    long_title = "This is a very long title that exceeds the maximum length " * 3
    with pytest.raises(ValidationError) as exc_info:
        Ticket(title=long_title, description="Test description")
    assert "ensure this value has at most 100 characters" in str(exc_info.value)

    # Test empty title
    with pytest.raises(ValidationError):
        Ticket(title="", description="Test description")

    # Test title with leading/trailing spaces (should be stripped)
    ticket = Ticket(title="  Fix login page error  ", description="Test description")
    assert ticket.title == "Fix login page error"


def test_description_validation():
    """Test description field validation."""
    # Test empty description
    with pytest.raises(ValidationError):
        Ticket(title="Fix login error", description="")


def test_enum_validation():
    """Test enum field validation."""
    # Test invalid ticket type
    with pytest.raises(ValidationError):
        Ticket(title="Test ticket", description="Test description", type="INVALID_TYPE")

    # Test invalid priority
    with pytest.raises(ValidationError):
        Ticket(
            title="Test ticket",
            description="Test description",
            priority="INVALID_PRIORITY",
        )

    # Test invalid status
    with pytest.raises(ValidationError):
        Ticket(
            title="Test ticket", description="Test description", status="INVALID_STATUS"
        )


def test_list_field_validation():
    """Test list field validation and deduplication."""
    ticket = Ticket(
        title="Test ticket",
        description="Test description",
        components=["Auth", "Auth", "Frontend"],  # Duplicate component
        labels=["bug", "bug", "critical"],  # Duplicate label
    )
    assert ticket.components == ["Auth", "Frontend"]  # Duplicates removed
    assert ticket.labels == ["bug", "critical"]  # Duplicates removed


def test_json_serialization():
    """Test JSON serialization and deserialization."""
    ticket_data = {
        "title": "Test JSON handling",
        "description": "Testing JSON serialization",
        "type": "BUG",
        "priority": "HIGH",
        "components": ["Backend"],
        "labels": ["test"],
    }

    # Test deserialization
    ticket = Ticket.model_validate(ticket_data)
    assert ticket.title == ticket_data["title"]
    assert ticket.type == TicketType.BUG

    # Test serialization
    json_data = ticket.model_dump_json()
    assert isinstance(json_data, str)

    # Test roundtrip
    reconstructed_ticket = Ticket.model_validate_json(json_data)
    assert reconstructed_ticket.title == ticket.title
    assert reconstructed_ticket.type == ticket.type


def test_optional_fields():
    """Test handling of optional fields."""
    # Test with None values
    ticket = Ticket(
        title="Test optional fields",
        description="Testing optional fields",
        components=None,
        labels=None,
    )
    assert ticket.components == []  # Should default to empty list
    assert ticket.labels == []  # Should default to empty list


def test_default_values():
    """Test default value generation."""
    ticket1 = Ticket(title="Test defaults 1", description="Testing default values")
    ticket2 = Ticket(title="Test defaults 2", description="Testing default values")

    # IDs should be unique
    assert ticket1.id != ticket2.id

    # Created timestamps should be close to now
    now = datetime.utcnow()
    assert abs((ticket1.created - now).total_seconds()) < 1
    assert abs((ticket2.created - now).total_seconds()) < 1


@pytest.mark.parametrize(
    "invalid_data,expected_error",
    [
        ({"title": "Test ticket"}, "Field required"),  # Missing description
        ({"description": "Test description"}, "Field required"),  # Missing title
        (
            {
                "title": "Test",
                "description": "Test",
                "priority": "SUPER_HIGH",
            },  # Invalid priority
            "Input should be 'LOW', 'MEDIUM' or 'HIGH'",
        ),
    ],
)
def test_invalid_tickets(invalid_data, expected_error):
    """Test various invalid ticket scenarios."""
    with pytest.raises(ValidationError) as exc_info:
        Ticket.model_validate(invalid_data)
    assert expected_error in str(exc_info.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
