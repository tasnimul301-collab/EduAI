"""Flashcard Models Module.

Defines schemas for active recall study decks and individual question/answer cards.
Supports Spaced Repetition mastery marking.
"""

from datetime import datetime
from app.extensions import db


class FlashcardDeck(db.Model):
    """Deck containing flashcards for a specific subject or topic."""

    __tablename__ = "flashcard_decks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subjects.id"), nullable=True, index=True)

    title = db.Column(db.String(150), nullable=False)
    class_level = db.Column(db.String(50), nullable=True, default="General")
    topic = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    cards = db.relationship("Flashcard", backref="deck", lazy=True, cascade="all, delete-orphan")

    def mastered_count(self) -> int:
        """Count how many cards in this deck have been marked mastered."""
        return sum(1 for c in self.cards if c.is_mastered)

    def progress_percentage(self) -> int:
        """Percentage of mastered flashcards."""
        total = len(self.cards)
        return round((self.mastered_count() / total * 100)) if total > 0 else 0

    def __repr__(self) -> str:
        return f"<FlashcardDeck id={self.id} title='{self.title}'>"


class Flashcard(db.Model):
    """Individual flashcard with front concept/question and back answer/explanation."""

    __tablename__ = "flashcards"

    id = db.Column(db.Integer, primary_key=True)
    deck_id = db.Column(db.Integer, db.ForeignKey("flashcard_decks.id"), nullable=False, index=True)

    front_question = db.Column(db.Text, nullable=False)
    back_answer = db.Column(db.Text, nullable=False)
    hint = db.Column(db.String(255), nullable=True)
    is_mastered = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self) -> str:
        return f"<Flashcard id={self.id} deck_id={self.deck_id} mastered={self.is_mastered}>"
