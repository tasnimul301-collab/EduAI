"""Flashcards Blueprint Routes.

Handles active recall flashcard deck creation, AI generation,
interactive 3D card review sessions, and Spaced Repetition mastery tracking.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.extensions import db
from app.models.flashcard import FlashcardDeck, Flashcard
from app.models.subject import Subject
from app.services.ai_service import AIService
from app.utils.auth import login_required, log_activity, get_current_user
from app.utils.curriculum import CLASS_CURRICULUM

flashcards_bp = Blueprint("flashcards", __name__, url_prefix="/flashcards")


def _ensure_demo_decks_for_user(user_id: int):
    """Seed ready-to-use study flashcard decks for the student."""
    if FlashcardDeck.query.filter_by(user_id=user_id).first():
        return

    sample_decks = [
        {
            "title": "[Class 9-10] Physics: Motion, Speed & Force",
            "class_level": "Class 10",
            "subject_name": "Physics",
            "topic": "Laws of Motion & Force",
            "cards": [
                {"front": "What is Newton's First Law of Motion?", "back": "An object at rest stays at rest, and an object in motion stays in motion with constant velocity, unless acted upon by a net external force (Law of Inertia).", "hint": "Inertia"},
                {"front": "What is the formula for Newton's Second Law?", "back": "F = m * a (Force = Mass × Acceleration). SI unit is Newton (N).", "hint": "F = ma"},
                {"front": "State Newton's Third Law of Motion.", "back": "To every action there is always an equal and opposite reaction.", "hint": "Action = Reaction"},
                {"front": "What is the acceleration due to gravity (g) near Earth's surface?", "back": "g ≈ 9.8 m/s² directed vertically downwards.", "hint": "9.8 m/s²"},
                {"front": "What is the difference between Speed and Velocity?", "back": "Speed is a scalar quantity (magnitude only), while Velocity is a vector quantity (magnitude with direction).", "hint": "Scalar vs Vector"},
            ],
        },
        {
            "title": "[Class 9-10] Chemistry: Periodic Table & Chemical Bonds",
            "class_level": "Class 10",
            "subject_name": "Chemistry",
            "topic": "Periodic Table & Bonding",
            "cards": [
                {"front": "What is Avogadro's constant?", "back": "6.022 × 10²³ particles per mole.", "hint": "6.022 × 10²³"},
                {"front": "What is an Ionic Bond?", "back": "A bond formed by the complete transfer of one or more electrons from a metal to a non-metal.", "hint": "Electron transfer"},
                {"front": "What is a Covalent Bond?", "back": "A chemical bond formed by the mutual sharing of valence electron pairs between atoms.", "hint": "Electron sharing"},
                {"front": "What defines the pH scale?", "back": "pH = -log[H+]. pH < 7 is acidic, pH = 7 is neutral, and pH > 7 is basic/alkaline.", "hint": "Acidity / Basicity"},
                {"front": "Which group contains the Noble (Inert) Gases?", "back": "Group 18 (Helium, Neon, Argon, Krypton, Xenon, Radon) with stable full octets.", "hint": "Group 18"},
            ],
        },
        {
            "title": "[Class 11-12] ICT: C Programming & Number Systems",
            "class_level": "Class 12",
            "subject_name": "ICT",
            "topic": "C Programming & Logic",
            "cards": [
                {"front": "What is the binary equivalent of decimal 13?", "back": "1101 in binary (8 + 4 + 0 + 1 = 13).", "hint": "8 + 4 + 1"},
                {"front": "Which format specifier prints an integer in C?", "back": "%d (or %i) for signed decimal integers in printf/scanf.", "hint": "%d"},
                {"front": "What does an AND logic gate output?", "back": "Outputs 1 ONLY when all of its inputs are 1. Otherwise outputs 0.", "hint": "All 1s"},
                {"front": "What is the purpose of the 'break' statement in a loop?", "back": "Immediately terminates the loop or switch-case construct and passes control to the next statement.", "hint": "Loop exit"},
                {"front": "What is an HTML anchor tag?", "back": "<a href=\"url\">Link Text</a> creates clickable hyperlinks in web documents.", "hint": "<a> tag"},
            ],
        },
    ]

    for d_data in sample_decks:
        deck = FlashcardDeck(
            user_id=user_id,
            title=d_data["title"],
            class_level=d_data["class_level"],
            topic=d_data["topic"],
        )
        db.session.add(deck)
        db.session.flush()

        for c in d_data["cards"]:
            card = Flashcard(
                deck_id=deck.id,
                front_question=c["front"],
                back_answer=c["back"],
                hint=c["hint"],
            )
            db.session.add(card)

    db.session.commit()


@flashcards_bp.route("/")
@login_required
def index():
    """List flashcard decks with mastery statistics."""
    user = get_current_user()
    _ensure_demo_decks_for_user(user.id)

    decks = FlashcardDeck.query.filter_by(user_id=user.id).order_by(FlashcardDeck.created_at.desc()).all()
    subjects = Subject.query.filter_by(user_id=user.id).all()

    total_cards = sum(len(d.cards) for d in decks)
    total_mastered = sum(d.mastered_count() for d in decks)
    mastery_rate = round((total_mastered / total_cards * 100)) if total_cards > 0 else 0

    return render_template(
        "flashcards/index.html",
        user=user,
        decks=decks,
        subjects=subjects,
        curriculum=CLASS_CURRICULUM,
        total_cards=total_cards,
        total_mastered=total_mastered,
        mastery_rate=mastery_rate,
        ai_configured=AIService.is_configured(),
    )


@flashcards_bp.route("/deck/<int:deck_id>")
@login_required
def study_deck(deck_id):
    """Interactive 3D flashcard study session."""
    user = get_current_user()
    deck = FlashcardDeck.query.filter_by(id=deck_id, user_id=user.id).first_or_404()
    return render_template("flashcards/study.html", user=user, deck=deck)


@flashcards_bp.route("/generate", methods=["POST"])
@login_required
def generate():
    """Generate new flashcards deck via Gemini AI."""
    user = get_current_user()

    class_level = request.form.get("class_level", "Class 10").strip()
    subject_name = request.form.get("curriculum_subject", "General Science").strip()
    topic = request.form.get("topic", "").strip()
    count_str = request.form.get("count", "6")

    try:
        count = int(count_str)
        count = max(4, min(count, 12))
    except ValueError:
        count = 6

    if not topic:
        flash("Please provide a topic or chapter name for the flashcards.", "warning")
        return redirect(url_for("flashcards.index"))

    result = AIService.generate_flashcards(
        subject_name=subject_name,
        topic=topic,
        count=count,
        class_level=class_level,
    )

    if not result.get("success") or not result.get("cards"):
        flash("Could not generate flashcards at this moment. Please try again.", "danger")
        return redirect(url_for("flashcards.index"))

    deck_title = f"[{class_level}] {subject_name}: {topic}"
    new_deck = FlashcardDeck(
        user_id=user.id,
        title=deck_title,
        class_level=class_level,
        topic=topic,
    )
    db.session.add(new_deck)
    db.session.flush()

    for c in result["cards"]:
        card = Flashcard(
            deck_id=new_deck.id,
            front_question=c["front"],
            back_answer=c["back"],
            hint=c.get("hint", ""),
        )
        db.session.add(card)

    user.total_points += 20  # Award points for creating flashcards
    user.add_badge("Flashcard Creator")
    db.session.commit()

    log_activity(f"Generated flashcard deck '{deck_title}'", "Flashcards", user.id)
    flash(f"Successfully generated '{deck_title}' with {len(result['cards'])} cards!", "success")
    return redirect(url_for("flashcards.study_deck", deck_id=new_deck.id))


@flashcards_bp.route("/card/<int:card_id>/toggle", methods=["POST"])
@login_required
def toggle_card(card_id):
    """Toggle flashcard mastery status via AJAX."""
    user = get_current_user()
    card = Flashcard.query.join(FlashcardDeck).filter(
        Flashcard.id == card_id, FlashcardDeck.user_id == user.id
    ).first_or_404()

    card.is_mastered = not card.is_mastered
    if card.is_mastered:
        user.total_points += 5
        if user.total_points >= 200:
            user.add_badge("Knowledge Master")
    db.session.commit()

    return jsonify({
        "success": True,
        "is_mastered": card.is_mastered,
        "deck_mastered": card.deck.mastered_count(),
        "deck_total": len(card.deck.cards),
        "deck_percentage": card.deck.progress_percentage(),
        "user_points": user.total_points,
    })


@flashcards_bp.route("/deck/<int:deck_id>/delete", methods=["POST"])
@login_required
def delete_deck(deck_id):
    """Delete a flashcard deck."""
    user = get_current_user()
    deck = FlashcardDeck.query.filter_by(id=deck_id, user_id=user.id).first_or_404()
    name = deck.title
    db.session.delete(deck)
    db.session.commit()
    log_activity(f"Deleted flashcard deck '{name}'", "Flashcards", user.id)
    flash(f"Flashcard deck '{name}' has been deleted.", "info")
    return redirect(url_for("flashcards.index"))
