"""
Testing crud operations for events and invites.
"""
# Import the necessary modules for testing
from how2meet.db import crud, schemas
from how2meet.db.database import get_db


def test_get_event():
    """
    Test the get_event function.

    This uses the local db and event 0. TODO: replace with mocking
    """
    db = next(get_db())
    event_id = "0"

    # Function under test
    result = crud.get_event(db, event_id)

    # Assert the result
    assert result is not None


def test_update_event():
    """
    Test the update event function.

    Test that an event can be updated correctly in the database
    This uses the local db and event 0.

    TODO: replace with mocking, remove the portion that "resets" the db after each test
    """
    db = next(get_db())
    event_id = "0"

    event = crud.get_event(db, event_id)

    # TODO: test all fields
    update_data = schemas.EventUpdate(
        name="Updated Name",
    )

    # Function under test
    result = crud.update_event(db, event, update_data)

    # Assert the result matches new data
    assert result is not None
    assert result.name == update_data.name

    # Assert the result does not match old data
    assert event.name != result.name

    # Reset the db
    crud.update_event(db, event, event)
