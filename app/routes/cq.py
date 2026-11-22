"""Creative Questions (CQ / সৃজনশীল প্রশ্ন) Blueprint Routes.

Handles generation of Board-style Creative Questions (ক, খ, গ, ঘ),
interactive study view with revealable model answers, and Class 6-12 filtering.
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.extensions import db
from app.models.creative_question import CreativeQuestion
from app.services.ai_service import AIService
from app.utils.auth import login_required, log_activity, get_current_user
from app.utils.curriculum import CLASS_CURRICULUM

cq_bp = Blueprint("cq", __name__, url_prefix="/cq")


def _ensure_demo_cq_for_user(user_id: int):
    """Seed sample Board-style Creative Questions for immediate practice."""
    if CreativeQuestion.query.filter_by(user_id=user_id).first():
        return

    sample_cqs = [
        {
            "class_level": "Class 5",
            "subject_name": "Primary Science",
            "chapter_topic": "আমাদের পরিবেশ ও বাস্তুসংস্থান (Environment & Ecosystem)",
            "stimulus": "একটি বিদ্যালয়ের বাগানে সবুজ ঘাস, বিভিন্ন ফুলের গাছ, প্রজাপতি, ব্যাঙ এবং কিছু ঘাসফড়িং বাস করে। শিক্ষার্থীরা লক্ষ্য করল তীব্র খরায় ঘাস মরে যাওয়ায় ঘাসফড়িংয়ের সংখ্যা অনেক কমে গেল এবং পরে ব্যাঙের সংখ্যাও হ্রাস পেল।",
            "question_a": "ক. খাদ্যশৃঙ্খল (Food Chain) কী? (১)",
            "answer_a": "উদ্ভিদ উৎস থেকে বিভিন্ন প্রাণীর মধ্যে একে অপরকে খাওয়ার মাধ্যমে শক্তি স্থানান্তরের ধারাবাহিক প্রক্রিয়াই হলো খাদ্যশৃঙ্খল।",
            "question_b": "খ. সবুজ উদ্ভিদকে উৎপাদক বলা হয় কেন? (২)",
            "answer_b": "সবুজ উদ্ভিদ সূর্যালোক এবং ক্লোরোফিলের সাহায্যে পরিবেশের পানি ও কার্বন ডাই-অক্সাইড ব্যবহার করে সালোকসংশ্লেষণ প্রক্রিয়ায় নিজের খাদ্য নিজেই তৈরি করতে পারে। অন্য কোনো প্রাণী খাদ্য তৈরি করতে পারে না, তাই উদ্ভিদকে উৎপাদক বলা হয়।",
            "question_c": "গ. উদ্দীপকের পরিবেশে একটি সম্পূর্ণ খাদ্যশৃঙ্খল তৈরি করে প্রবাহচিত্রের মাধ্যমে ব্যাখ্যা করো। (৩)",
            "answer_c": "উদ্দীপকের তথ্য অনুযায়ী খাদ্যশৃঙ্খলটি হলো:\nসবুজ ঘাস (উৎপাদক) ➔ ঘাসফড়িং (প্রথম স্তরের খাদক) ➔ ব্যাঙ (দ্বিতীয় স্তরের খাদক)।\n\nএখানে সবুজ ঘাস সূর্যালোক থেকে শক্তি সঞ্চয় করে। ঘাসফড়িং ঘাস খেয়ে বেঁচে থাকে এবং পরবর্তীতে ব্যাঙ ঘাসফড়িংকে খাদ্য হিসেবে গ্রহণ করে শক্তি লাভ করে।",
            "question_d": "ঘ. 'খাদ্যশৃঙ্খলের একটি উপাদানের সংকট পুরো বাস্তুসংস্থানের ভারসাম্যে প্রভাব ফেলে' — উদ্দীপকের আলোকে বিশ্লেষণ করো। (৪)",
            "answer_d": "উদ্দীপকে দেখা যায়, খরার কারণে উৎপাদক (ঘাস) বিনষ্ট হওয়ায় প্রথম স্তরের খাদক ঘাসফড়িং খাদ্যাভাবে মারা যায়। ফলে ঘাসফড়িংয়ের ওপর নির্ভরশীল দ্বিতীয় স্তরের খাদক ব্যাঙও অনাহারে সংকটগ্রস্ত হয়ে পড়ে।\nসুতরাং, খাদ্যশৃঙ্খলের কোনো একটি স্তরে বিপর্যয় ঘটলে পরবর্তী প্রতিটি স্তরের খাদকেরা সরাসরি ক্ষতিগ্রস্ত হয় এবং সার্বিক পরিবেশের বাস্তুসংস্থানিক ভারসাম্য নষ্ট হয়।",
        },
        {
            "class_level": "Class 10",
            "subject_name": "Physics",
            "chapter_topic": "গতি ও বল (Motion & Force)",
            "stimulus": "১২০০ কেজি ভরের একটি প্রাইভেট কার ২০ মি./সে. বেগে একটি সোজা রাস্তায় চলছিল। হঠাৎ চালক সামনে ৫০ মিটার দূরে একজন পথচারীকে দেখতে পেয়ে সঙ্গে সঙ্গে ব্রেক চাপলেন এবং গাড়িটি ঠিক পথচারীর সামনে এসে ৫ সেকেন্ডে থেমে গেল।",
            "question_a": "ক. ত্বরণ কাকে বলে? (১)",
            "answer_a": "সময়ের সাথে বস্তুর অসম বেগের পরিবর্তনের হারকে ত্বরণ বলে। এর এসআই একক m/s²।",
            "question_b": "খ. চলন্ত বাস হঠাৎ ব্রেক করলে যাত্রীরা সামনের দিকে ঝুঁকে পড়েন কেন? (২)",
            "answer_b": "গতির জড়তার কারণে এমনটি ঘটে। বাস যখন গতিশীল থাকে, তখন বাসের সাথে যাত্রীর পুরো শরীরও একই গতিশীল অবস্থায় থাকে। কিন্তু চালক যখন হঠাৎ ব্রেক করেন, তখন শরীরের নিচের অংশ বাসের সাথে স্থির হয়ে গেলেও শরীরের উপরের অংশ গতির জড়তার কারণে তার আগের গতির অবস্থা বজায় রাখতে চায়। ফলে যাত্রীরা সামনের দিকে ঝুঁকে পড়েন।",
            "question_c": "গ. গাড়িটির ওপর প্রযুক্ত মন্দন বলের মান নির্ণয় করো। (৩)",
            "answer_c": "দেওয়া আছে:\nআদিবেগ, u = ২০ মি./সে.\nশেষবেগ, v = ০ মি./সে. (যেহেতু থেমে গেল)\nসময়, t = ৫ সে.\nগাড়ির ভর, m = ১২০০ কেজি\n\nআমরা জানি, ত্বরণ a = (v - u) / t = (০ - ২০) / ৫ = -৪ মি./সে.²\nঅতএব, মন্দন = ৪ মি./সে.²\nপ্রযুক্ত বল F = m * a = ১২০০ কেজি × (-৪ মি./সে.²) = -৪৮০০ নিউটন।\nঅতএব, প্রযুক্ত মন্দন বলের মান ৪৮০০ নিউটন (N)।",
            "question_d": "ঘ. উদ্দীপকের ঘটনায় গাড়িটি থামার প্রক্রিয়ায় শক্তির সংরক্ষণশীলতা নীতি যথাযথভাবে রক্ষিত হয়েছিল কি? গাণিতিক যুক্তিসহ বিশ্লেষণ করো। (৪)",
            "answer_d": "হ্যাঁ, শক্তির সংরক্ষণশীলতা নীতি যথাযথভাবে রক্ষিত হয়েছিল।\n\nগাণিতিক বিশ্লেষণ:\nগাড়ির প্রারম্ভিক গতিশক্তি E_k = 0.5 × m × u² = 0.5 × ১২০০ × (২০)² = ২৪০,০০০ জুল (J)।\nগাড়িটি থামার সময়ে ব্রেকজনিত ঘর্ষণ বলের বিরুদ্ধে অতিক্রান্ত দূরত্ব s = ৫০ মিটার।\nঘর্ষণ বল দ্বারা কৃতকাজ W = F × s = ৪৮০০ N × ৫০ m = ২৪০,০০০ জুল (J)।\n\nদেখা যাচ্ছে, গাড়ির সম্পূর্ণ গতিশক্তি (২৪০,০০০ জুল) ঘর্ষণ বল দ্বারা কাজ সম্পাদনের মাধ্যমে তাপ ও শব্দ শক্তিতে রূপান্তরিত হয়েছে। শক্তি ধ্বংস বা নতুন করে সৃষ্টি হয়নি, কেবল এক রূপ থেকে অন্য রূপে পরিবর্তিত হয়েছে। সুতরাং শক্তির সংরক্ষণশীলতা নীতি সম্পূর্ণরূপে রক্ষিত হয়েছে।",
        },
        {
            "class_level": "Class 10",
            "subject_name": "Chemistry",
            "chapter_topic": "পর্যায় সারণি ও রাসায়নিক বন্ধন (Periodic Table & Bonding)",
            "stimulus": "পর্যায় সারণির তিনটি মৌল X, Y ও Z যাদের পারমাণবিক সংখ্যা যথাক্রমে ১১, ১২ ও ১৭। মৌলগুলো পরস্পর যুক্ত হয়ে বিভিন্ন প্রকার যৌগ গঠন করে।",
            "question_a": "ক. অষ্টক নিয়ম (Octet Rule) কী? (১)",
            "answer_a": "পরমাণুসমূহ রাসায়নিক বন্ধন গঠনের মাধ্যমে তাদের সর্ববহিস্থ শক্তিস্তরে নিষ্ক্রিয় গ্যাসের মতো আটটি ইলেকট্রন বিন্যাস অর্জনের যে প্রবণতা দেখায়, তাকে অষ্টক নিয়ম বলে।",
            "question_b": "খ. পর্যায় সারণিতে নোবেল গ্যাসগুলোকে নিষ্ক্রিয় গ্যাস বলা হয় কেন? (২)",
            "answer_b": "পর্যায় সারণির ১৮ নং গ্রুপের মৌলগুলোর (যেমন- He, Ne, Ar ইত্যাদি) সর্ববহিস্থ শক্তিস্তর ইলেকট্রন দ্বারা সম্পূর্ণ পূর্ণ (হিলিয়ামের ক্ষেত্রে ২টি এবং বাকিদের ক্ষেত্রে ৮টি) থাকে। এই স্থিতিশীল ইলেকট্রন বিন্যাসের কারণে তারা সহজে ইলেকট্রন গ্রহণ, বর্জন বা শেয়ার করে না এবং সাধারণ অবস্থায় রাসায়নিক বিক্রিয়ায় অংশ নেয় না। তাই এদের নিষ্ক্রিয় গ্যাস বলা হয়।",
            "question_c": "গ. X ও Z মৌলদ্বয় দ্বারা গঠিত যৌগের বন্ধন প্রকৃতি ও গঠন চিত্র ব্যাখ্যা করো। (৩)",
            "answer_c": "পারমাণবিক সংখ্যা ১১ বিশিষ্ট মৌল X হলো সোডিয়াম (Na: 2, 8, 1) এবং ১৭ বিশিষ্ট মৌল Z হলো ক্লোরিন (Cl: 2, 8, 7)।\nসোডিয়াম তার সর্ববহিস্থ কক্ষপথের ১টি ইলেকট্রন ক্লোরিনকে দান করে ধনাত্মক সোডিয়াম আয়নে (Na+) পরিণত হয়। ক্লোরিন সেই ইলেকট্রন গ্রহণ করে ঋণাত্মক ক্লোরাইড আয়নে (Cl-) পরিণত হয়।\nবিপরীতধর্মী Na+ ও Cl- আয়নসমূহ তীব্র স্থির তড়িৎ আকর্ষণ বল দ্বারা যুক্ত হয়ে আয়নিক বন্ধনযুক্ত NaCl যৌগ গঠন করে।",
            "question_d": "ঘ. গলনাঙ্ক ও স্ফুটনাঙ্কের দিক থেকে YZ₂ যৌগের সাথে সাধারণ সমযোজী যৌগের ধর্মের তুলনামূলক বিশ্লেষণ করো। (৪)",
            "answer_d": "Y হলো ম্যাগনেসিয়াম (Mg, পারমাণবিক সংখ্যা ১২) এবং Z হলো ক্লোরিন (Cl, ১৭)। এরা যুক্ত হয়ে গঠিত যৌগটি হলো ম্যাগনেসিয়াম ক্লোরাইড (MgCl₂), যা একটি তীব্র আয়নিক যৌগ।\nআয়নিক যৌগে ক্যাটায়ন ও অ্যানায়নগুলো ত্রিমাত্রিক কেলাস জালিকা আকারে তীব্র স্থির-বৈদ্যুতিক আকর্ষণ বল দ্বারা আবদ্ধ থাকে। এই বন্ধন ভাঙতে প্রচুর তাপশক্তির প্রয়োজন হয়, তাই MgCl₂ এর গলনাঙ্ক (৭১৪° সে.) ও স্ফুটনাঙ্ক (১৪১২° সে.) অনেক বেশি।\nবিপরীতে, সাধারণ সমযোজী যৌগে দুর্বল ভ্যান ডার ওয়ালস বল থাকায় সামান্য তাপেই অণুগুলো পৃথক হয়ে যায়, ফলে তাদের গলনাঙ্ক ও স্ফুটনাঙ্ক অনেক কম হয়।",
        },
    ]

    for cq_data in sample_cqs:
        cq = CreativeQuestion(
            user_id=user_id,
            class_level=cq_data["class_level"],
            subject_name=cq_data["subject_name"],
            chapter_topic=cq_data["chapter_topic"],
            stimulus=cq_data["stimulus"],
            question_a=cq_data["question_a"],
            answer_a=cq_data["answer_a"],
            question_b=cq_data["question_b"],
            answer_b=cq_data["answer_b"],
            question_c=cq_data["question_c"],
            answer_c=cq_data["answer_c"],
            question_d=cq_data["question_d"],
            answer_d=cq_data["answer_d"],
        )
        db.session.add(cq)

    db.session.commit()


@cq_bp.route("/")
@login_required
def index():
    """List Creative Questions with Class 5-12 filtering."""
    user = get_current_user()
    _ensure_demo_cq_for_user(user.id)

    # All students and admins can see and practice the full collection of CQs
    cqs = CreativeQuestion.query.order_by(CreativeQuestion.created_at.desc()).all()
    return render_template(
        "cq/index.html",
        user=user,
        cqs=cqs,
        curriculum=CLASS_CURRICULUM,
        ai_configured=AIService.is_configured(),
    )


@cq_bp.route("/view/<int:cq_id>")
@login_required
def view_cq(cq_id):
    """View full stimulus and interactive revealable model answers."""
    user = get_current_user()
    cq = CreativeQuestion.query.filter_by(id=cq_id).first_or_404()
    return render_template("cq/view.html", user=user, cq=cq)


@cq_bp.route("/generate", methods=["POST"])
@login_required
def generate():
    """Trigger AI generation of a new Board-style Creative Question (Admin only)."""
    user = get_current_user()

    if user.role != "admin":
        flash("Only administrators have permission to generate or add new Creative Questions.", "danger")
        return redirect(url_for("cq.index"))

    class_level = request.form.get("class_level", "Class 10").strip()
    subject_name = request.form.get("curriculum_subject", "Physics").strip()
    topic = request.form.get("topic", "").strip()

    if not topic:
        flash("Please specify a topic or chapter for the Creative Question.", "warning")
        return redirect(url_for("cq.index"))

    result = AIService.generate_creative_question(
        subject_name=subject_name,
        topic=topic,
        class_level=class_level,
    )

    if not result.get("success") or not result.get("cq"):
        flash("Could not generate Creative Question. Please try again.", "danger")
        return redirect(url_for("cq.index"))

    cq_data = result["cq"]
    new_cq = CreativeQuestion(
        user_id=user.id,
        class_level=class_level,
        subject_name=subject_name,
        chapter_topic=topic,
        stimulus=cq_data.get("stimulus", ""),
        question_a=cq_data.get("question_a", "ক. জ্ঞানমূলক প্রশ্ন"),
        answer_a=cq_data.get("answer_a", "উত্তর"),
        question_b=cq_data.get("question_b", "খ. অনুধাবনমূলক প্রশ্ন"),
        answer_b=cq_data.get("answer_b", "উত্তর"),
        question_c=cq_data.get("question_c", "গ. প্রয়োগমূলক প্রশ্ন"),
        answer_c=cq_data.get("answer_c", "উত্তর"),
        question_d=cq_data.get("question_d", "ঘ. উচ্চতর দক্ষতামূলক প্রশ্ন"),
        answer_d=cq_data.get("answer_d", "উত্তর"),
    )
    db.session.add(new_cq)
    user.total_points += 25
    user.add_badge("Board Exam Challenger")
    db.session.commit()

    log_activity(f"Generated CQ on '{topic}' ({class_level})", "Creative Question", user.id)
    flash(f"Successfully generated Board Creative Question on '{topic}'!", "success")
    return redirect(url_for("cq.view_cq", cq_id=new_cq.id))


@cq_bp.route("/create-manual", methods=["POST"])
@login_required
def create_manual():
    """Manually add a Board-style Creative Question (Admin only)."""
    user = get_current_user()
    if user.role != "admin":
        flash("Only administrators have permission to add Creative Questions.", "danger")
        return redirect(url_for("cq.index"))

    class_level = request.form.get("class_level", "Class 10").strip()
    subject_name = request.form.get("subject_name", "General Science").strip()
    topic = request.form.get("chapter_topic", "").strip() or "General Chapter"
    stimulus = request.form.get("stimulus", "").strip()

    q_a = request.form.get("question_a", "").strip()
    ans_a = request.form.get("answer_a", "").strip()
    q_b = request.form.get("question_b", "").strip()
    ans_b = request.form.get("answer_b", "").strip()
    q_c = request.form.get("question_c", "").strip()
    ans_c = request.form.get("answer_c", "").strip()
    q_d = request.form.get("question_d", "").strip()
    ans_d = request.form.get("answer_d", "").strip()

    if not stimulus or not q_a:
        flash("Stimulus and Question (ক) are required.", "warning")
        return redirect(url_for("cq.index"))

    new_cq = CreativeQuestion(
        user_id=user.id,
        class_level=class_level,
        subject_name=subject_name,
        chapter_topic=topic,
        stimulus=stimulus,
        question_a=q_a,
        answer_a=ans_a or "উত্তর যোগ করা হয়নি",
        question_b=q_b or "খ. অনুধাবনমূলক প্রশ্ন",
        answer_b=ans_b or "উত্তর যোগ করা হয়নি",
        question_c=q_c or "গ. প্রয়োগমূলক প্রশ্ন",
        answer_c=ans_c or "উত্তর যোগ করা হয়নি",
        question_d=q_d or "ঘ. উচ্চতর দক্ষতামূলক প্রশ্ন",
        answer_d=ans_d or "উত্তর যোগ করা হয়নি",
    )
    db.session.add(new_cq)
    db.session.commit()
    log_activity(f"Manually created CQ on '{topic}' ({class_level})", "Creative Question", user.id)
    flash(f"Creative Question for {class_level} ({subject_name}) created successfully!", "success")
    return redirect(url_for("cq.view_cq", cq_id=new_cq.id))


@cq_bp.route("/delete/<int:cq_id>", methods=["POST"])
@login_required
def delete_cq(cq_id):
    """Delete a Creative Question (Admin only)."""
    user = get_current_user()

    if user.role != "admin":
        flash("Only administrators have permission to delete Creative Questions.", "danger")
        return redirect(url_for("cq.index"))

    cq = CreativeQuestion.query.filter_by(id=cq_id).first_or_404()
    db.session.delete(cq)
    db.session.commit()
    flash("Creative question deleted.", "info")
    return redirect(url_for("cq.index"))
