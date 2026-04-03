"""
Database Repository
===================

Encapsulates database operations for StreamIQ using SQLAlchemy ORM.
"""

from sqlalchemy.orm import Session
from src.db.models import CustomerInteraction, SentimentResult

def save_interaction(session: Session, customer_id: str, transcript: str) -> CustomerInteraction:
    """
    Save a new customer interaction.

    Parameters
    ----------
    session : Session
        Active SQLAlchemy session
    customer_id : str
        Unique identifier for the customer
    transcript : str
        Transcribed text of the interaction

    Returns
    -------
    CustomerInteraction
        The persisted interaction object
    """
    interaction = CustomerInteraction(customer_id=customer_id, transcript=transcript)
    session.add(interaction)
    session.commit()
    session.refresh(interaction)
    return interaction


def save_sentiment_result(session: Session, interaction_id: int, sentiment: str, satisfaction_score: float) -> SentimentResult:
    """
    Save sentiment analysis result linked to an interaction.

    Parameters
    ----------
    session : Session
        Active SQLAlchemy session
    interaction_id : int
        ID of the related customer interaction
    sentiment : str
        Sentiment label (positive, negative, neutral)
    satisfaction_score : float
        Numeric satisfaction score

    Returns
    -------
    SentimentResult
        The persisted sentiment result object
    """
    result = SentimentResult(
        interaction_id=interaction_id,
        sentiment=sentiment,
        satisfaction_score=satisfaction_score
    )
    session.add(result)
    session.commit()
    session.refresh(result)
    return result


def get_interaction_with_results(session: Session, interaction_id: int) -> CustomerInteraction:
    """
    Retrieve a customer interaction along with its sentiment results.

    Parameters
    ----------
    session : Session
        Active SQLAlchemy session
    interaction_id : int
        ID of the interaction

    Returns
    -------
    CustomerInteraction
        Interaction object with sentiment results loaded
    """
    return session.query(CustomerInteraction).filter_by(id=interaction_id).first()
