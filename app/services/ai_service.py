"""AI Service Module.

Provides integration with Google Gemini Generative AI API for:
1. Academic Study Assistant (conversational question answering, step-by-step reasoning)
2. Automated Multiple-Choice Question (MCQ) Quiz Generation

Features direct HTTPS REST calls with automatic model failover
(gemini-3.5-flash-lite -> gemini-3.5-flash -> gemini-3.8-flash) and an offline
curated university question bank for seamless 100% uptime.
"""

import json
import os
import re
import random
import requests
from flask import current_app
from app.extensions import db


# =============================================================================
# Curated Offline Academic Question Bank (Zero External Dependency Fallback)
# =============================================================================
OFFLINE_QUESTION_BANK = {
    "algorithms": [
        {
            "question": "What is the tight asymptotic upper bound (Big-O) of Merge Sort in the worst case?",
            "options": {"A": "O(n)", "B": "O(n log n)", "C": "O(n^2)", "D": "O(log n)"},
            "correct": "B",
            "explanation": "Merge Sort recursively divides the input in half (log n levels) and performs linear merging at each level, ensuring O(n log n) across best, average, and worst cases.",
        },
        {
            "question": "Which algorithm is capable of computing single-source shortest paths on directed graphs with negative edge weights?",
            "options": {"A": "Dijkstra's Algorithm", "B": "Prim's Algorithm", "C": "Bellman-Ford Algorithm", "D": "Kruskal's Algorithm"},
            "correct": "C",
            "explanation": "Bellman-Ford operates in O(V*E) time and correctly relaxes all edges V-1 times, detecting and handling negative weight edges.",
        },
        {
            "question": "What is the worst-case time complexity of QuickSort when a deterministic first-element pivot is used on an already sorted array?",
            "options": {"A": "O(n)", "B": "O(n log n)", "C": "O(n^2)", "D": "O(2^n)"},
            "correct": "C",
            "explanation": "When the array is already sorted, picking the first element creates unbalanced partitions of sizes 0 and n-1, leading to a recurrence of T(n) = T(n-1) + O(n) = O(n^2).",
        },
        {
            "question": "Which dynamic programming problem finds the longest subsequence present in two given sequences in identical relative order?",
            "options": {"A": "Longest Common Subsequence (LCS)", "B": "Shortest Common Supersequence", "C": "Matrix Chain Multiplication", "D": "Huffman Coding"},
            "correct": "A",
            "explanation": "LCS uses a 2D table of dimension (m+1)x(n+1) to determine the length and composition of the longest shared subsequence in O(m*n) time.",
        },
        {
            "question": "What algorithmic paradigm does the Fractional Knapsack problem solve optimally?",
            "options": {"A": "Dynamic Programming", "B": "Greedy Approach", "C": "Divide and Conquer", "D": "Backtracking"},
            "correct": "B",
            "explanation": "Fractional Knapsack exhibits the greedy-choice property by sorting items by value-to-weight ratio. 0/1 Knapsack requires Dynamic Programming.",
        },
    ],
    "database": [
        {
            "question": "Which Normal Form (NF) eliminates transitive functional dependencies on non-prime attributes?",
            "options": {"A": "First Normal Form (1NF)", "B": "Second Normal Form (2NF)", "C": "Third Normal Form (3NF)", "D": "Boyce-Codd Normal Form (BCNF)"},
            "correct": "C",
            "explanation": "3NF requires relations to be in 2NF and mandates that no non-prime attribute is transitively dependent on any candidate key.",
        },
        {
            "question": "What does the 'A' represent in the relational database ACID properties?",
            "options": {"A": "Availability", "B": "Atomicity", "C": "Authentication", "D": "Asynchrony"},
            "correct": "B",
            "explanation": "Atomicity guarantees that all transaction operations execute completely or the entire transaction is rolled back with zero side effects.",
        },
        {
            "question": "Which database index structure maintains balance such that all leaf nodes reside at equal depth with sequential pointers?",
            "options": {"A": "Hash Index", "B": "B+ Tree Index", "C": "Bitmap Index", "D": "Inverted Index"},
            "correct": "B",
            "explanation": "B+ trees store data record pointers exclusively at the leaf level and chain leaves horizontally, optimizing range scans and equality lookups.",
        },
        {
            "question": "Which SQL clause is executed after GROUP BY to filter aggregate calculations?",
            "options": {"A": "WHERE", "B": "ORDER BY", "C": "HAVING", "D": "LIMIT"},
            "correct": "C",
            "explanation": "HAVING filters groups created by GROUP BY based on aggregate expressions, whereas WHERE filters individual rows before grouping occurs.",
        },
        {
            "question": "In relational algebra, which fundamental operator extracts specified vertical columns from a relation?",
            "options": {"A": "Selection (σ)", "B": "Projection (π)", "C": "Cartesian Product (×)", "D": "Union (∪)"},
            "correct": "B",
            "explanation": "Projection (represented by π) extracts designated columns while eliminating duplicate output tuples.",
        },
    ],
    "operating_systems": [
        {
            "question": "Which of the following is NOT one of the four necessary Coffman conditions for system deadlock?",
            "options": {"A": "Mutual Exclusion", "B": "Hold and Wait", "C": "Preemption Permitted", "D": "Circular Wait"},
            "correct": "C",
            "explanation": "No preemption is the necessary condition. If resources can be preempted involuntarily, deadlock cannot occur.",
        },
        {
            "question": "What phenomenon occurs in virtual memory when the operating system spends more time swapping pages than executing user code?",
            "options": {"A": "Fragmentation", "B": "Thrashing", "C": "Belady's Anomaly", "D": "Starvation"},
            "correct": "B",
            "explanation": "Thrashing happens when the total working sets of active processes exceed physical RAM, causing endless disk I/O page faults.",
        },
        {
            "question": "Which CPU scheduling algorithm is mathematically proven to minimize average waiting time for a static batch of processes?",
            "options": {"A": "First-Come First-Served (FCFS)", "B": "Shortest Job First (SJF)", "C": "Round Robin (RR)", "D": "Priority Scheduling"},
            "correct": "B",
            "explanation": "Shortest Job First (SJF) minimizes average waiting time by scheduling shorter burst durations ahead of longer tasks.",
        },
        {
            "question": "What hardware component translates virtual memory addresses into physical RAM addresses?",
            "options": {"A": "Arithmetic Logic Unit (ALU)", "B": "Memory Management Unit (MMU)", "C": "Direct Memory Access (DMA)", "D": "Instruction Register"},
            "correct": "B",
            "explanation": "The MMU translates virtual addresses to physical memory addresses utilizing hardware page tables and the Translation Lookaside Buffer (TLB).",
        },
    ],
    "data_structures": [
        {
            "question": "In an AVL self-balancing binary search tree, what is the maximum permissible balance factor magnitude for every node?",
            "options": {"A": "0", "B": "1", "C": "2", "D": "No limit"},
            "correct": "B",
            "explanation": "An AVL tree requires that the height difference between the left and right subtrees of any node is at most 1 (i.e. -1, 0, or +1).",
        },
        {
            "question": "Which data structure is fundamentally utilized to implement Breadth-First Search (BFS) graph traversal?",
            "options": {"A": "Stack", "B": "Queue", "C": "Max-Heap", "D": "Disjoint Set"},
            "correct": "B",
            "explanation": "BFS explores vertices in order of frontier distance using a FIFO Queue. Depth-First Search (DFS) utilizes a LIFO Stack.",
        },
        {
            "question": "What is the average-case time complexity of searching a key in a well-distributed Hash Table using chaining?",
            "options": {"A": "O(1)", "B": "O(log n)", "C": "O(n)", "D": "O(n log n)"},
            "correct": "A",
            "explanation": "Under simple uniform hashing with a bounded load factor, searching a Hash Table runs in O(1) expected constant time.",
        },
    ],
    "networks": [
        {
            "question": "At which layer of the OSI model do routers and the Internet Protocol (IP) operate?",
            "options": {"A": "Data Link Layer (Layer 2)", "B": "Network Layer (Layer 3)", "C": "Transport Layer (Layer 4)", "D": "Session Layer (Layer 5)"},
            "correct": "B",
            "explanation": "The Network Layer is responsible for packet forwarding, routing across logical networks, and IP addressing.",
        },
        {
            "question": "What key protocol mechanism distinguishes TCP from UDP at the Transport layer?",
            "options": {"A": "Port numbering", "B": "Three-way handshake & guaranteed delivery", "C": "Checksum validation", "D": "Packet framing"},
            "correct": "B",
            "explanation": "TCP establishes a stateful connection via a 3-way handshake (SYN, SYN-ACK, ACK) and provides reliable, ordered data stream delivery.",
        },
    ],
    "software_engineering": [
        {
            "question": "Which SOLID design principle states that software entities should be open for extension but closed for modification?",
            "options": {"A": "Single Responsibility Principle", "B": "Open/Closed Principle", "C": "Liskov Substitution Principle", "D": "Interface Segregation Principle"},
            "correct": "B",
            "explanation": "The Open/Closed Principle encourages using interfaces and abstract classes so new functionality can be added without modifying existing code.",
        },
        {
            "question": "Which Creational Design Pattern ensures that a class has only one instance while providing a global access point to it?",
            "options": {"A": "Factory Method", "B": "Singleton Pattern", "C": "Adapter Pattern", "D": "Observer Pattern"},
            "correct": "B",
            "explanation": "The Singleton pattern restricts class instantiation to a single object via a private constructor and a static getter.",
        },
    ],
}


class AIService:
    """Encapsulates all Google Gemini AI operations with REST transport and offline fallback."""

    # Active 2026 production models in order of priority
    ACTIVE_MODELS = [
        "gemini-3.5-flash-lite",
        "gemini-3.5-flash",
        "gemini-3.8-flash",
    ]

    @classmethod
    def get_api_key(cls) -> str:
        """Retrieve API key from Flask configuration or environment."""
        return current_app.config.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY", "").strip()

    @classmethod
    def is_configured(cls) -> bool:
        """Check whether a valid Gemini API key is provided."""
        key = cls.get_api_key()
        return bool(key and key not in ["your_gemini_api_key_here", "your_actual_gemini_key_here"])

    @classmethod
    def _call_gemini_rest(cls, prompt: str, timeout: int = 15) -> tuple[bool, str, str | None]:
        """Call Gemini REST API directly with model failover."""
        api_key = cls.get_api_key()
        if not api_key:
            return False, "", "API_KEY_MISSING"

        last_error = None
        for model in cls.ACTIVE_MODELS:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            try:
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}]
                }
                resp = requests.post(url, json=payload, timeout=timeout)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates and "content" in candidates[0] and "parts" in candidates[0]["content"]:
                        text = candidates[0]["content"]["parts"][0].get("text", "").strip()
                        if text:
                            return True, text, None
                else:
                    err_data = resp.json().get("error", {})
                    last_error = err_data.get("message", f"HTTP {resp.status_code}")
                    continue
            except Exception as e:
                last_error = str(e)
                continue

        return False, "", last_error or "Unable to reach Gemini API service."

    @classmethod
    def _get_offline_quiz_questions(cls, topic: str, count: int = 5, class_level: str = "General") -> list[dict]:
        """Retrieve curated questions matching the requested topic and class level."""
        from app.utils.curriculum import PREBUILT_QUIZZES
        pool = []
        topic_lower = topic.lower()

        # Check prebuilt curriculum quizzes matching class_level or topic
        for q in PREBUILT_QUIZZES:
            if class_level and class_level != "General" and class_level.lower() in q.get("class_level", "").lower():
                pool.extend(q["questions"])
            elif any(k in q.get("topic", "").lower() or k in q.get("subject", "").lower() for k in topic_lower.split() if len(k) > 2):
                pool.extend(q["questions"])

        if not pool:
            selected_category = None
            if any(k in topic_lower for k in ["algo", "sort", "dijkstra", "bellman", "greedy", "dynamic", "dp"]):
                selected_category = "algorithms"
            elif any(k in topic_lower for k in ["data", "sql", "acid", "normal", "index", "b+", "relational"]):
                selected_category = "database"
            elif any(k in topic_lower for k in ["os", "operat", "deadlock", "thread", "process", "schedul", "memory"]):
                selected_category = "operating_systems"
            elif any(k in topic_lower for k in ["tree", "avl", "bst", "heap", "stack", "queue", "hash"]):
                selected_category = "data_structures"
            elif any(k in topic_lower for k in ["net", "tcp", "udp", "ip", "osi", "router"]):
                selected_category = "networks"
            elif any(k in topic_lower for k in ["pattern", "solid", "oop", "design", "soft"]):
                selected_category = "software_engineering"

            if selected_category and selected_category in OFFLINE_QUESTION_BANK:
                pool = OFFLINE_QUESTION_BANK[selected_category]
            else:
                pool = [q for questions in OFFLINE_QUESTION_BANK.values() for q in questions]

        count = max(3, min(count, len(pool)))
        return random.sample(pool, min(count, len(pool)))

    @classmethod
    def ask_study_assistant(
        cls, prompt: str, conversation_history: list[dict] | None = None
    ) -> dict:
        """Send an academic question to Gemini with automatic REST failover and offline answers."""
        if cls.is_configured():
            system_instruction = (
                "You are EduSmart AI, an ultra-crisp, direct, and helpful academic tutor.\n\n"
                "STRICT RULES ON ANSWER LENGTH & CONCISENESS (যতটুকু প্রয়োজন ঠিক ততটুকু):\n"
                "1. For direct/factual questions (e.g. 'what is the capital of China?'): Output ONLY the direct answer in 1 sentence. Example: 'The capital of China is Beijing.' Never add unsolicited historical background, facts, or bullet points.\n"
                "2. For definitions (e.g. 'what is a variable?'): Provide a clean 2-3 sentence definition with 1 brief example. No long essays.\n"
                "3. For step-by-step math/science problems: Show only the essential calculation steps clearly.\n"
                "4. Absolutely NO robotic greetings (Do NOT say 'Hello! I am EduSmart AI...'). Start immediately with the answer.\n"
                "5. NEVER output boilerplate decorative sections like '### Core Definition' or '📌 Key Facts' unless the user specifically asked for them.\n"
                "6. Language: Match the student's language (English, Bangla/বাংলা, Banglish)."
            )
            full_prompt = f"{system_instruction}\n\nStudent Query: {prompt}"
            success, response_text, error = cls._call_gemini_rest(full_prompt)

            if success:
                return {"success": True, "response": response_text, "error": None}

        # Offline fallback for common academic queries
        prompt_lower = prompt.lower()
        if "dijkstra" in prompt_lower:
            return {
                "success": True,
                "response": (
                    "### 🔍 Dijkstra's Algorithm Overview\n\n"
                    "**Purpose:** Finds the shortest path from a single source vertex to all other vertices in a weighted graph with **non-negative** edge weights.\n\n"
                    "#### Step-by-Step Execution:\n"
                    "1. **Initialize:** Set distance to source = 0 and all other vertices = ∞. Insert all vertices into a Min-Priority Queue.\n"
                    "2. **Extract Min:** Extract vertex `u` with the smallest tentative distance.\n"
                    "3. **Relax Edges:** For each neighbor `v` of `u`:\n"
                    "   - If `dist[u] + weight(u, v) < dist[v]`, update `dist[v] = dist[u] + weight(u, v)`.\n"
                    "4. **Repeat:** Continue until the Priority Queue is empty.\n\n"
                    "**Complexity:** With a Fibonacci Heap: `O(V log V + E)`. With a Binary Min-Heap: `O((V + E) log V)`."
                ),
                "error": None,
            }
        elif "acid" in prompt_lower:
            return {
                "success": True,
                "response": (
                    "### 🏛️ ACID Properties in Relational Databases\n\n"
                    "ACID guarantees that database transactions are processed reliably:\n\n"
                    "* **A - Atomicity ('All or Nothing'):** Every operation in a transaction must complete successfully or the entire transaction rolls back.\n"
                    "* **C - Consistency:** The database moves from one valid state to another, satisfying all schema constraints and foreign keys.\n"
                    "* **I - Isolation:** Concurrent transactions execute without mutual interference.\n"
                    "* **D - Durability:** Committed updates persist permanently on non-volatile storage, surviving crashes."
                ),
                "error": None,
            }
        elif "tcp" in prompt_lower or "udp" in prompt_lower:
            return {
                "success": True,
                "response": (
                    "### 🌐 TCP vs UDP Comparison\n\n"
                    "| Feature | TCP (Transmission Control Protocol) | UDP (User Datagram Protocol) |\n"
                    "|---|---|---|\n"
                    "| **Connection** | Connection-oriented (3-way handshake) | Connectionless |\n"
                    "| **Reliability** | Guaranteed delivery (retransmissions) | Best-effort (packets can be dropped) |\n"
                    "| **Ordering** | In-order delivery via sequence numbers | No ordering guarantees |\n"
                    "| **Speed / Overhead** | Higher latency, 20-60 byte header | Minimal latency, 8 byte header |\n"
                    "| **Use Cases** | Web (HTTP/HTTPS), Email (SMTP), File Transfer | Gaming, VoIP, DNS, Video streaming |"
                ),
                "error": None,
            }
        elif any(w in prompt_lower for w in ["exam", "revision", "study", "strateg"]):
            return {
                "success": True,
                "response": (
                    "### 🎓 4 Proven Evidence-Based University Study Strategies\n\n"
                    "1. **Active Recall Testing:** Instead of passively re-reading notes, generate practice quizzes to force memory retrieval.\n"
                    "2. **Spaced Repetition (The Leitner System):** Review challenging concepts after 1 day, 3 days, 1 week, and 2 weeks.\n"
                    "3. **The Feynman Technique:** Explain the concept in plain, simple terms. If you encounter a gap, revisit your notes to master it.\n"
                    "4. **Interleaved Practice:** Mix problem types rather than blocking all problems of the same type."
                ),
                "error": None,
            }

        return {
            "success": False,
            "response": (
                "⚠️ The AI Study Assistant is currently in **Offline Academic Mode**.\n\n"
                "To ask open-ended questions in any language or subject, please set your free Google Gemini API key in your `.env` file:\n"
                "```ini\nGEMINI_API_KEY=AIzaSy...\n```\n"
                "👉 Get your key at: [Google AI Studio](https://aistudio.google.com/app/apikey)\n\n"
                "*Tip: Click one of the Quick Prompts above for instant answers!*"
            ),
            "error": "API_KEY_UNAVAILABLE",
        }

    @classmethod
    def generate_quiz_questions(
        cls, subject_name: str, topic: str, difficulty: str, count: int = 5, class_level: str = "General"
    ) -> dict:
        """Generate multiple-choice questions with live Gemini API and offline fallback."""
        if cls.is_configured():
            prompt = f"""
You are an expert educator creating an academic multiple-choice quiz.
Target Academic Level: {class_level}
Subject: {subject_name}
Topic / Chapter: {topic}
Difficulty: {difficulty} (easy, medium, or hard)
Number of questions: {count}

Requirements:
- Ensure all questions and options strictly match the curriculum standards for {class_level} students (NCTB / secondary / higher-secondary standards).
- Questions must be clear, educational, and unambiguous.
- Each question must have 4 distinct choices labeled A, B, C, D with exactly one unambiguously correct answer.
- Provide a brief, helpful explanation for each question.

Generate exactly {count} multiple-choice questions in strict JSON format.
Return ONLY a valid JSON array of objects. Do not include markdown code fences (like ```json), commentary, or extra text.

Format:
[
  {{
    "question": "What is the primary function of ...?",
    "options": {{
      "A": "Option text 1",
      "B": "Option text 2",
      "C": "Option text 3",
      "D": "Option text 4"
    }},
    "correct": "A",
    "explanation": "Explanation for why A is correct."
  }}
]
"""
            success, raw_text, error = cls._call_gemini_rest(prompt, timeout=20)
            if success:
                # Clean code fences
                cleaned = re.sub(r"^```(?:json)?\s*", "", raw_text, flags=re.MULTILINE)
                cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.MULTILINE).strip()

                parsed = None
                try:
                    parsed = json.loads(cleaned)
                except json.JSONDecodeError:
                    match = re.search(r"\[\s*\{.*\}\s*\]", raw_text, re.DOTALL)
                    if match:
                        try:
                            parsed = json.loads(match.group(0))
                        except json.JSONDecodeError:
                            parsed = None

                if isinstance(parsed, list) and len(parsed) > 0:
                    validated_questions = []
                    for item in parsed:
                        if (
                            "question" in item
                            and "options" in item
                            and "correct" in item
                            and item["correct"] in ["A", "B", "C", "D"]
                        ):
                            validated_questions.append({
                                "question": item["question"],
                                "options": {
                                    "A": str(item["options"].get("A", "")),
                                    "B": str(item["options"].get("B", "")),
                                    "C": str(item["options"].get("C", "")),
                                    "D": str(item["options"].get("D", "")),
                                },
                                "correct": item["correct"],
                                "explanation": item.get("explanation", ""),
                            })

                    if validated_questions:
                        return {
                            "success": True,
                            "questions": validated_questions,
                            "is_fallback": False,
                            "error": None,
                        }

        # Seamless offline academic question bank fallback
        return {
            "success": True,
            "questions": cls._get_offline_quiz_questions(topic, count=count, class_level=class_level),
            "is_fallback": True,
            "error": None,
        }
