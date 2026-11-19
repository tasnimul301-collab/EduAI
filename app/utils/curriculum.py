"""Curriculum & Pre-seeded Quizzes for Class 6 to Class 12.

Defines:
- Standard secondary and higher secondary curriculum structures (Class 6 - 12)
- Topic suggestions per subject
- Pre-built active recall quizzes covering all subjects from Class 6 to Class 12
- Seeding utility to ensure every student account has access to all quizzes
"""

from app.extensions import db
from app.models.quiz import Quiz, QuizQuestion


CLASS_CURRICULUM = {
    "Class 6": {
        "subjects": [
            "General Science",
            "Mathematics",
            "English",
            "Bangla",
            "ICT",
            "Bangladesh & Global Studies",
        ],
        "topics": {
            "General Science": ["Living World & Plant Cells", "States of Matter", "Structure of Organisms", "Light & Vision"],
            "Mathematics": ["Basic Equations & Fractions", "Prime Numbers & Factors", "Integers & Number Line", "Basic Geometry"],
            "English": ["Parts of Speech & Grammar", "Tenses & Auxiliary Verbs", "Sentence Structure", "Punctuation"],
            "Bangla": ["বাংলা ব্যাকরণ: সন্ধি ও বর্ণ", "বাক্য গঠন", "শব্দার্থ ও বিপরীত শব্দ", "সাধু ও চলিত রীতি"],
            "ICT": ["Fundamentals of Computers", "Input and Output Devices", "Storage Devices & RAM", "Internet Basics"],
            "Bangladesh & Global Studies": ["Heritage & Geography", "Riverine Bangladesh", "Historic Language Movement", "Society & Culture"],
        },
    },
    "Class 7": {
        "subjects": [
            "General Science",
            "Mathematics",
            "English",
            "Bangla",
            "ICT",
            "Bangladesh & Global Studies",
        ],
        "topics": {
            "General Science": ["Heat, Temperature & Energy", "Respiration in Organisms", "Solar System & Planets", "Acids, Bases & Salts"],
            "Mathematics": ["Algebraic Expressions & Unitary Method", "Ratio & Percentage", "Triangles & Geometric Angles", "Linear Equations"],
            "English": ["Tenses & Voice Change", "Prepositions & Articles", "Subject-Verb Agreement", "Vocabulary & Antonyms"],
            "Bangla": ["কারক ও বিভক্তি", "সমাস পরিচিতি", "বাগধারা ও প্রবাদ", "বানান শুদ্ধিকরণ"],
            "ICT": ["Internet, Web Browsers & Cyber Safety", "Computer Viruses & Malware", "Word Processing Basics", "Email Communication"],
            "Bangladesh & Global Studies": ["Environment & Culture", "Sundarbans & Ecosystems", "Climate Change Effects", "Human Rights"],
        },
    },
    "Class 8": {
        "subjects": [
            "General Science",
            "Mathematics",
            "English",
            "Bangla",
            "ICT",
            "Bangladesh & Global Studies",
        ],
        "topics": {
            "General Science": ["Atoms, Light & Sound Waves", "Chemical Reactions & Equations", "Nervous System", "Earth & Universe"],
            "Mathematics": ["Pythagorean Theorem & Factorization", "Compound Interest & Profit", "Circles & Theorems", "Quadrilateral Properties"],
            "English": ["Modals, Conjunctions & Prepositions", "Direct & Indirect Speech", "Transformation of Sentences", "Idioms & Phrases"],
            "Bangla": ["ধ্বনি পরিবর্তন ও ণ-ত্ব ষ-ত্ব বিধান", "প্রত্যয় ও উপসর্গ", "সমাস ও বাক্যান্তর", "বিরামচিহ্ন"],
            "ICT": ["Networking & Spreadsheet Basics", "Network Topologies (Star, Bus)", "Formulae in Spreadsheets", "Cyber Crimes"],
            "Bangladesh & Global Studies": ["Governance & Constitution", "Organs of State", "Social Issues & Remediation", "UN & Global Peace"],
        },
    },
    "Class 9": {
        "subjects": [
            "Physics",
            "Chemistry",
            "Biology",
            "General Mathematics",
            "Higher Mathematics",
            "ICT",
            "English",
            "Bangla",
            "Business Studies",
        ],
        "topics": {
            "Physics": ["Laws of Motion & Gravitation (SSC)", "Force & Acceleration", "Work, Power & Energy", "Pressure in Fluids"],
            "Chemistry": ["Atomic Structure & Periodic Table (SSC)", "Chemical Bonding & Valency", "States of Matter & Gas Laws", "Symbols & Formulas"],
            "Biology": ["Plant & Animal Tissues (SSC)", "Cell Structure & Organelles", "Photosynthesis in Plants", "Digestive System"],
            "General Mathematics": ["Sets & Algebraic Formulae (SSC)", "Linear & Quadratic Equations", "Logarithms & Exponents", "Geometric Theorems"],
            "Higher Mathematics": ["Polynomials & Proofs (SSC)", "Cartesian Coordinate Geometry", "Trigonometric Ratios", "Set Operations & Venn Diagrams"],
            "ICT": ["E-Services & Spreadsheet Data (SSC)", "Digital Content Creation", "Software Installation & Security", "Internet Services"],
            "English": ["Right Form of Verbs", "Completing Sentences", "Tag Questions & Connectors", "Modifiers"],
            "Bangla": ["শব্দ সম্ভার ও বাংলা ব্যাকরণ", "প্রত্যয় ও ধাতু", "বাক্য বিশ্লেষণ", "উক্তি পরিবর্তন"],
            "Business Studies": ["Introduction to Business", "Forms of Business Ownership", "Basic Accounting Principles", "Entrepreneurship"],
        },
    },
    "Class 10": {
        "subjects": [
            "Physics",
            "Chemistry",
            "Biology",
            "General Mathematics",
            "Higher Mathematics",
            "ICT",
            "English",
            "Bangla",
            "Business Studies",
        ],
        "topics": {
            "Physics": ["Electricity, Magnetism & Wave Optics (SSC)", "Ohm's Law & Circuits", "Reflection & Refraction", "Electromagnetism"],
            "Chemistry": ["Chemical Bonds, Acids & Salts (SSC)", "Mole Concept & Calculations", "Acid-Base Reactions & pH", "Electrochemistry Basics"],
            "Biology": ["Cell Division, Mitosis & Genetics (SSC)", "Mendel's Laws of Heredity", "Human Excretory System", "Blood Circulation"],
            "General Mathematics": ["Trigonometry & Mensuration (SSC)", "Statistics & Frequency Distribution", "Circle Theorems & Tangents", "Quadratic Equations"],
            "Higher Mathematics": ["Vectors & Coordinates (SSC)", "Binomial Expansion", "Trigonometric Formulas", "Inequalities"],
            "ICT": ["Database Management & Querying (SSC)", "SQL Queries & Primary Keys", "Multimedia & Presentations", "Information Security"],
            "English": ["Reading Comprehension", "Transformation of Degrees", "Passage Narration", "Formal Writing"],
            "Bangla": ["বাংলা ব্যাকরণ ও নির্মিতি", "সমাস ও ছন্দ", "প্রতিবেদন রচনা", "ভাবসম্প্রসারণ"],
            "Business Studies": ["Financial Statements", "Journal, Ledger & Trial Balance", "Business Finance", "Marketing"],
        },
    },
    "Class 11": {
        "subjects": [
            "Physics",
            "Chemistry",
            "Biology",
            "Higher Mathematics",
            "ICT",
            "English",
            "Bangla",
            "Accounting & Finance",
        ],
        "topics": {
            "Physics": ["Vector Analysis, Kinematics & Dynamics (HSC)", "Newtonian Mechanics & Torque", "Gravitation & Gravity", "Work, Energy & Power"],
            "Chemistry": ["Quantum Numbers & Chemical Periodic Properties (HSC)", "Atomic Structure & Orbitals", "Hybridization & VSEPR", "Gas Laws & Ideal Gases"],
            "Biology": ["Cell Structure, Cell Cycle & Botany (HSC)", "RuBisCO & Calvin Cycle", "Cell Wall & Plasma Membrane", "Meiosis & Crossing Over"],
            "Higher Mathematics": ["Matrices, Determinants & Straight Lines (HSC)", "Matrices Multiplication & Inversion", "Differential Calculus Basics", "Trigonometric Transformations"],
            "ICT": ["Data Communication & Number Systems (HSC)", "Number Base Conversions (Bin/Hex/Oct)", "Logic Gates & Boolean Algebra", "Fiber Optics & Networks"],
            "English": ["Advanced Reading Comprehension & Synonyms (HSC)", "Conditionals & Subjunctive Mood", "Cohesive Devices & Discourse Markers", "Vocabulary"],
            "Bangla": ["বাংলা ১ম পত্র: সাহিত্য ও কবিতা", "শব্দার্থ ও ছন্দ", "বাংলা ব্যাকরণিক শব্দশ্রেণী", "ব্যাকরণিক আলোচনা"],
            "Accounting & Finance": ["Financial Accounting Principles", "Accounting Equation & Journal", "Bank Reconciliation Statement", "Worksheet"],
        },
    },
    "Class 12": {
        "subjects": [
            "Physics",
            "Chemistry",
            "Biology",
            "Higher Mathematics",
            "ICT",
            "English",
            "Bangla",
            "Accounting & Economics",
        ],
        "topics": {
            "Physics": ["Thermodynamics, Wave Optics & Modern Physics (HSC)", "Carnot Engine & Entropy", "Photoelectric Effect & Quantum Physics", "Nuclear Physics & Radioactivity"],
            "Chemistry": ["Organic Hydrocarbons & Electrochemistry (HSC)", "Aldehydes, Ketones & Tollens Reagent", "Markovnikov Rule & Alkenes", "Galvanic Cells & Nernst Equation"],
            "Biology": ["Genetics, Evolution & Zoology (HSC)", "DNA Replication & Double Helix", "Nephron & Renal Filtration", "Heart Anatomy & Blood Pressure"],
            "Higher Mathematics": ["Differential & Integral Calculus (HSC)", "Definite & Indefinite Integration", "Complex Numbers & Argand Diagrams", "Conic Sections (Parabola/Ellipse)"],
            "ICT": ["C Programming Language & Web Design with HTML (HSC)", "C Language Loops & Data Types", "HTML Tags & Hyperlinks", "Relational Database SQL"],
            "English": ["Academic Writing & Critical Analysis", "Formal Proposals & Reports", "Advanced Synthesis & Idioms", "Literary Analysis"],
            "Bangla": ["বাংলা ২য় পত্র: ব্যাকরণ ও অনুচ্ছেদ", "সমাস ও বাক্যশুদ্ধি", "দিনলিপি ও আবেদনপত্র", "প্রবন্ধ রচনা"],
            "Accounting & Economics": ["Financial Statements & Microeconomics (HSC)", "Balance Sheet & Equity Analysis", "Law of Demand & Price Elasticity", "National Income & GDP"],
        },
    },
}


# Pre-built comprehensive quiz catalog for all classes 6-12
PREBUILT_QUIZZES = [
    # ========================== CLASS 6 ==========================
    {
        "class_level": "Class 6",
        "subject": "General Science",
        "title": "[Class 6] General Science: Living World & Plant Cells",
        "topic": "Living World & Cells",
        "difficulty": "easy",
        "questions": [
            {
                "question": "Which cell organelle is known as the powerhouse of the cell?",
                "options": {"A": "Nucleus", "B": "Mitochondria", "C": "Chloroplast", "D": "Ribosome"},
                "correct": "B",
                "explanation": "Mitochondria generate most of the cell's ATP supply, known as the cell's energy powerhouse.",
            },
            {
                "question": "What green pigment in plant leaves absorbs sunlight for photosynthesis?",
                "options": {"A": "Carotene", "B": "Hemoglobin", "C": "Chlorophyll", "D": "Xanthophyll"},
                "correct": "C",
                "explanation": "Chlorophyll is the green pigment in chloroplasts that absorbs light energy for photosynthesis.",
            },
            {
                "question": "Which state of matter has a definite volume but no definite shape?",
                "options": {"A": "Solid", "B": "Liquid", "C": "Gas", "D": "Plasma"},
                "correct": "B",
                "explanation": "Liquids have a fixed volume but conform to the shape of their container.",
            },
        ],
    },
    {
        "class_level": "Class 6",
        "subject": "Mathematics",
        "title": "[Class 6] Mathematics: Basic Equations & Fractions",
        "topic": "Fractions & Linear Equations",
        "difficulty": "easy",
        "questions": [
            {
                "question": "If 3x + 5 = 20, what is the value of x?",
                "options": {"A": "3", "B": "5", "C": "7", "D": "15"},
                "correct": "B",
                "explanation": "3x = 20 - 5 = 15 => x = 15 / 3 = 5.",
            },
            {
                "question": "What is the sum of 1/4 and 2/4?",
                "options": {"A": "3/8", "B": "3/4", "C": "2/4", "D": "1/2"},
                "correct": "B",
                "explanation": "Adding fractions with equal denominators: (1+2)/4 = 3/4.",
            },
            {
                "question": "What is the smallest prime number?",
                "options": {"A": "0", "B": "1", "C": "2", "D": "3"},
                "correct": "C",
                "explanation": "2 is the smallest and only even prime number.",
            },
        ],
    },
    {
        "class_level": "Class 6",
        "subject": "English",
        "title": "[Class 6] English: Parts of Speech & Grammar",
        "topic": "Parts of Speech",
        "difficulty": "easy",
        "questions": [
            {
                "question": "In the sentence 'The quick brown fox jumps quickly', which word is an adverb?",
                "options": {"A": "quick", "B": "brown", "C": "jumps", "D": "quickly"},
                "correct": "D",
                "explanation": "'Quickly' modifies the verb 'jumps' and indicates manner, so it is an adverb.",
            },
            {
                "question": "Which of the following is a collective noun?",
                "options": {"A": "Teacher", "B": "Fleet", "C": "Water", "D": "Happiness"},
                "correct": "B",
                "explanation": "'Fleet' refers to a group of ships, making it a collective noun.",
            },
            {
                "question": "What is the past tense of the irregular verb 'begin'?",
                "options": {"A": "Begun", "B": "Began", "C": "Beginned", "D": "Begined"},
                "correct": "B",
                "explanation": "The simple past form of 'begin' is 'began'; 'begun' is the past participle.",
            },
        ],
    },
    {
        "class_level": "Class 6",
        "subject": "ICT",
        "title": "[Class 6] ICT: Fundamentals of Computers",
        "topic": "Computer Hardware & Software",
        "difficulty": "easy",
        "questions": [
            {
                "question": "Which part of the computer is known as its brain?",
                "options": {"A": "Monitor", "B": "CPU (Central Processing Unit)", "C": "Keyboard", "D": "Hard Drive"},
                "correct": "B",
                "explanation": "The CPU performs all processing, calculations, and instructions.",
            },
            {
                "question": "Which of the following is an input device?",
                "options": {"A": "Printer", "B": "Speaker", "C": "Monitor", "D": "Mouse"},
                "correct": "D",
                "explanation": "A mouse sends pointer data into the computer, making it an input device.",
            },
            {
                "question": "What does 'RAM' stand for in computer systems?",
                "options": {"A": "Read All Memory", "B": "Random Access Memory", "C": "Rapid Application Module", "D": "Real Audio Mode"},
                "correct": "B",
                "explanation": "RAM is volatile, high-speed primary memory used by active applications.",
            },
        ],
    },
    {
        "class_level": "Class 6",
        "subject": "Bangladesh & Global Studies",
        "title": "[Class 6] Bangladesh & Global Studies: Heritage & Geography",
        "topic": "History & Riverine Geography",
        "difficulty": "easy",
        "questions": [
            {
                "question": "What is the longest river running through Bangladesh?",
                "options": {"A": "Padma", "B": "Meghna", "C": "Jamuna", "D": "Surma"},
                "correct": "B",
                "explanation": "The Meghna is the widest and one of the longest major river systems discharging into the Bay of Bengal.",
            },
            {
                "question": "In which year was the historic Language Movement martyrs sacrifice in Dhaka?",
                "options": {"A": "1947", "B": "1952", "C": "1969", "D": "1971"},
                "correct": "B",
                "explanation": "On 21 February 1952, students sacrificed their lives in Dhaka to establish Bangla as a state language.",
            },
            {
                "question": "Which international organization observes 21st February as International Mother Language Day?",
                "options": {"A": "UNICEF", "B": "UNESCO", "C": "WHO", "D": "UNDP"},
                "correct": "B",
                "explanation": "UNESCO declared 21st February as International Mother Language Day in 1999.",
            },
        ],
    },

    # ========================== CLASS 7 ==========================
    {
        "class_level": "Class 7",
        "subject": "General Science",
        "title": "[Class 7] General Science: Heat, Temperature & Energy",
        "topic": "Heat Transfer & Energy",
        "difficulty": "medium",
        "questions": [
            {
                "question": "Which mode of heat transfer does NOT require any physical medium?",
                "options": {"A": "Conduction", "B": "Convection", "C": "Radiation", "D": "Evaporation"},
                "correct": "C",
                "explanation": "Radiation transfers thermal energy via electromagnetic waves through vacuum (e.g. sunlight reaching Earth).",
            },
            {
                "question": "What is the normal human body temperature in degrees Fahrenheit?",
                "options": {"A": "96.4°F", "B": "98.4°F to 98.6°F", "C": "100.2°F", "D": "102.0°F"},
                "correct": "B",
                "explanation": "Standard baseline human body temperature is approximately 98.4°F - 98.6°F (37°C).",
            },
            {
                "question": "In which unit is work and energy measured in the SI system?",
                "options": {"A": "Watt", "B": "Joule", "C": "Newton", "D": "Pascal"},
                "correct": "B",
                "explanation": "The SI unit of work and energy is the Joule (J).",
            },
        ],
    },
    {
        "class_level": "Class 7",
        "subject": "Mathematics",
        "title": "[Class 7] Mathematics: Algebraic Expressions & Unitary Method",
        "topic": "Algebra & Proportions",
        "difficulty": "medium",
        "questions": [
            {
                "question": "What is the expanded form of (a + b)^2?",
                "options": {"A": "a^2 + b^2", "B": "a^2 + 2ab + b^2", "C": "a^2 - 2ab + b^2", "D": "2a + 2b"},
                "correct": "B",
                "explanation": "(a + b)^2 = (a + b)(a + b) = a^2 + ab + ba + b^2 = a^2 + 2ab + b^2.",
            },
            {
                "question": "If 12 pens cost $72, how much do 5 pens cost?",
                "options": {"A": "$25", "B": "$30", "C": "$35", "D": "$40"},
                "correct": "B",
                "explanation": "Cost per pen = 72 / 12 = $6. Cost of 5 pens = 5 * 6 = $30.",
            },
            {
                "question": "What is the sum of the interior angles of any triangle?",
                "options": {"A": "90°", "B": "180°", "C": "270°", "D": "360°"},
                "correct": "B",
                "explanation": "The sum of angles in any Euclidean triangle is always 180 degrees.",
            },
        ],
    },
    {
        "class_level": "Class 7",
        "subject": "English",
        "title": "[Class 7] English: Tenses & Voice Change",
        "topic": "Tenses & Passive Voice",
        "difficulty": "medium",
        "questions": [
            {
                "question": "Change into passive: 'She wrote a letter.'",
                "options": {"A": "A letter is written by her.", "B": "A letter was written by her.", "C": "A letter had been written by her.", "D": "A letter will be written by her."},
                "correct": "B",
                "explanation": "Simple past active changes to 'was/were + past participle' in passive voice.",
            },
            {
                "question": "Choose the correct tense: 'They ____ football since morning.'",
                "options": {"A": "are playing", "B": "have been playing", "C": "played", "D": "had played"},
                "correct": "B",
                "explanation": "An action continuing from a past point to the present uses the present perfect continuous tense.",
            },
            {
                "question": "Which word is an antonym for 'Generous'?",
                "options": {"A": "Kind", "B": "Selfish", "C": "Polite", "D": "Brave"},
                "correct": "B",
                "explanation": "'Selfish' or 'stingy' is the opposite of 'generous'.",
            },
        ],
    },
    {
        "class_level": "Class 7",
        "subject": "ICT",
        "title": "[Class 7] ICT: Internet, Web Browsers & Cyber Safety",
        "topic": "Internet Safety & Networking",
        "difficulty": "medium",
        "questions": [
            {
                "question": "What does 'URL' stand for in web browsing?",
                "options": {"A": "Uniform Resource Locator", "B": "Universal Remote Link", "C": "United Radio Line", "D": "User Routing Language"},
                "correct": "A",
                "explanation": "URL specifies the location and retrieval mechanism of internet resources.",
            },
            {
                "question": "Which protocol secures web data using encryption?",
                "options": {"A": "HTTP", "B": "FTP", "C": "HTTPS", "D": "SMTP"},
                "correct": "C",
                "explanation": "HTTPS (Hypertext Transfer Protocol Secure) encrypts transmission using TLS/SSL.",
            },
            {
                "question": "What is software specifically designed to harm or exploit a computer called?",
                "options": {"A": "Freeware", "B": "Malware", "C": "Firmware", "D": "Shareware"},
                "correct": "B",
                "explanation": "Malware encompasses viruses, trojans, spyware, and ransomware.",
            },
        ],
    },
    {
        "class_level": "Class 7",
        "subject": "Bangladesh & Global Studies",
        "title": "[Class 7] Bangladesh & Global Studies: Environment & Culture",
        "topic": "Ecosystems & Culture",
        "difficulty": "medium",
        "questions": [
            {
                "question": "Which is the largest mangrove forest in the world, located in southwestern Bangladesh?",
                "options": {"A": "Amazon", "B": "Sundarbans", "C": "Taiga", "D": "Black Forest"},
                "correct": "B",
                "explanation": "The Sundarbans is the world's largest contiguous tidal halophytic mangrove ecosystem.",
            },
            {
                "question": "What is the iconic flagship animal of the Sundarbans mangrove forest?",
                "options": {"A": "Asian Elephant", "B": "Royal Bengal Tiger", "C": "Snow Leopard", "D": "One-horned Rhino"},
                "correct": "B",
                "explanation": "The Sundarbans is a primary habitat of the endangered Royal Bengal Tiger.",
            },
            {
                "question": "What causes seasonal variation on planet Earth?",
                "options": {"A": "Moon rotation", "B": "Earth's revolution and tilted axis", "C": "Sunspots", "D": "Ocean tides"},
                "correct": "B",
                "explanation": "Earth's 23.5-degree axial tilt during its annual revolution around the Sun creates seasons.",
            },
        ],
    },

    # ========================== CLASS 8 ==========================
    {
        "class_level": "Class 8",
        "subject": "General Science",
        "title": "[Class 8] General Science: Atoms, Light & Sound Waves",
        "topic": "Atomic Structure & Waves",
        "difficulty": "medium",
        "questions": [
            {
                "question": "What are the subatomic particles located inside the atomic nucleus?",
                "options": {"A": "Protons and electrons", "B": "Protons and neutrons", "C": "Neutrons and electrons", "D": "Electrons only"},
                "correct": "B",
                "explanation": "Protons and neutrons constitute the dense atomic nucleus, while electrons orbit around it.",
            },
            {
                "question": "What is the bending of light rays as they pass from one optical medium to another called?",
                "options": {"A": "Reflection", "B": "Refraction", "C": "Diffraction", "D": "Dispersion"},
                "correct": "B",
                "explanation": "Refraction occurs due to changes in light wave propagation speed between different media.",
            },
            {
                "question": "Sound waves cannot travel through which of the following?",
                "options": {"A": "Water", "B": "Steel", "C": "Air", "D": "Vacuum"},
                "correct": "D",
                "explanation": "Sound is a mechanical longitudinal wave requiring a physical material medium to propagate.",
            },
        ],
    },
    {
        "class_level": "Class 8",
        "subject": "Mathematics",
        "title": "[Class 8] Mathematics: Pythagorean Theorem & Factorization",
        "topic": "Geometry & Polynomials",
        "difficulty": "medium",
        "questions": [
            {
                "question": "In a right-angled triangle, if base = 3 cm and perpendicular = 4 cm, what is the hypotenuse?",
                "options": {"A": "5 cm", "B": "6 cm", "C": "7 cm", "D": "25 cm"},
                "correct": "A",
                "explanation": "Hypotenuse^2 = 3^2 + 4^2 = 9 + 16 = 25 => Hypotenuse = 5 cm.",
            },
            {
                "question": "Factorize: x^2 - 16.",
                "options": {"A": "(x - 4)^2", "B": "(x + 4)(x - 4)", "C": "(x - 2)(x + 8)", "D": "x(x - 16)"},
                "correct": "B",
                "explanation": "Difference of squares formula: a^2 - b^2 = (a + b)(a - b). Here 16 = 4^2.",
            },
            {
                "question": "What is the formula for the circumference of a circle with radius r?",
                "options": {"A": "πr^2", "B": "2πr", "C": "πd^2", "D": "2πr^2"},
                "correct": "B",
                "explanation": "Circumference = 2πr (or πd where d is diameter).",
            },
        ],
    },
    {
        "class_level": "Class 8",
        "subject": "English",
        "title": "[Class 8] English: Modals, Conjunctions & Prepositions",
        "topic": "Grammar & Prepositions",
        "difficulty": "medium",
        "questions": [
            {
                "question": "Choose the correct preposition: 'The student is proficient ____ mathematics.'",
                "options": {"A": "in", "B": "at", "C": "with", "D": "on"},
                "correct": "B",
                "explanation": "The adjective 'proficient' idiomatically takes 'at' when denoting skill mastery.",
            },
            {
                "question": "Which modal verb expresses polite permission?",
                "options": {"A": "Must", "B": "May", "C": "Will", "D": "Shall"},
                "correct": "B",
                "explanation": "'May' is formal and polite for asking permission (e.g., 'May I come in?').",
            },
            {
                "question": "Identify the coordinating conjunction: 'He studied hard, yet he failed.'",
                "options": {"A": "hard", "B": "yet", "C": "studied", "D": "failed"},
                "correct": "B",
                "explanation": "'Yet' connects two independent clauses showing contrast.",
            },
        ],
    },
    {
        "class_level": "Class 8",
        "subject": "ICT",
        "title": "[Class 8] ICT: Networking & Spreadsheet Basics",
        "topic": "Computer Networks & Excel",
        "difficulty": "medium",
        "questions": [
            {
                "question": "Which network topology connects all nodes to a single central hub or switch?",
                "options": {"A": "Ring topology", "B": "Star topology", "C": "Bus topology", "D": "Mesh topology"},
                "correct": "B",
                "explanation": "In a star topology, each computer connects independently to a central networking device.",
            },
            {
                "question": "In Microsoft Excel, what symbol must precede any mathematical formula?",
                "options": {"A": "#", "B": "$", "C": "=", "D": "@"},
                "correct": "C",
                "explanation": "All spreadsheet calculations and formulas in Excel/Calc begin with an equals sign (=).",
            },
            {
                "question": "What does LAN stand for in computer networking?",
                "options": {"A": "Large Area Network", "B": "Local Area Network", "C": "Logical Array Node", "D": "Linked Access Network"},
                "correct": "B",
                "explanation": "Local Area Network (LAN) spans a confined geographic area such as a school or office.",
            },
        ],
    },
    {
        "class_level": "Class 8",
        "subject": "Bangladesh & Global Studies",
        "title": "[Class 8] Bangladesh & Global Studies: Governance & Constitution",
        "topic": "Constitution & Society",
        "difficulty": "medium",
        "questions": [
            {
                "question": "In which year was the Constitution of the People's Republic of Bangladesh adopted?",
                "options": {"A": "1971", "B": "1972", "C": "1973", "D": "1974"},
                "correct": "B",
                "explanation": "The Constitution of Bangladesh was adopted on 4 November 1972 and came into effect on 16 December 1972.",
            },
            {
                "question": "What are the three fundamental organs of state governance?",
                "options": {"A": "Police, Military, Civil Service", "B": "Executive, Legislature, Judiciary", "C": "President, Prime Minister, Speaker", "D": "Municipal, District, Division"},
                "correct": "B",
                "explanation": "Democratic state power is balanced across Executive, Legislative, and Judicial branches.",
            },
            {
                "question": "What is the national parliament of Bangladesh called?",
                "options": {"A": "Senate", "B": "Jatiya Sangsad", "C": "Lok Sabha", "D": "House of Commons"},
                "correct": "B",
                "explanation": "The unicameral national legislature of Bangladesh is the Jatiya Sangsad.",
            },
        ],
    },

    # ========================== CLASS 9 (SSC) ==========================
    {
        "class_level": "Class 9",
        "subject": "Physics",
        "title": "[Class 9] Physics: Laws of Motion & Gravitation (SSC)",
        "topic": "Motion, Force & Gravity",
        "difficulty": "medium",
        "questions": [
            {
                "question": "According to Newton's Second Law of Motion, what is force equal to?",
                "options": {"A": "F = m/a", "B": "F = m * a", "C": "F = m * v", "D": "F = m * a^2"},
                "correct": "B",
                "explanation": "Force equals mass multiplied by acceleration (F = ma).",
            },
            {
                "question": "What is the acceleration due to gravity (g) near the Earth's surface?",
                "options": {"A": "8.9 m/s^2", "B": "9.8 m/s^2", "C": "10.8 m/s^2", "D": "11.2 m/s^2"},
                "correct": "B",
                "explanation": "Standard mean gravitational acceleration near Earth's surface is approximately 9.8 m/s^2.",
            },
            {
                "question": "What is the rate of change of displacement called?",
                "options": {"A": "Speed", "B": "Velocity", "C": "Acceleration", "D": "Momentum"},
                "correct": "B",
                "explanation": "Velocity is the vector quantity defined as rate of change of displacement over time.",
            },
        ],
    },
    {
        "class_level": "Class 9",
        "subject": "Chemistry",
        "title": "[Class 9] Chemistry: Atomic Structure & Periodic Table (SSC)",
        "topic": "Atoms & Periodic Properties",
        "difficulty": "medium",
        "questions": [
            {
                "question": "What is the maximum number of electrons that can occupy the M-shell (n = 3)?",
                "options": {"A": "2", "B": "8", "C": "18", "D": "32"},
                "correct": "C",
                "explanation": "The 2n^2 rule gives 2 * (3^2) = 2 * 9 = 18 electrons for the 3rd principal shell.",
            },
            {
                "question": "Which group in the modern periodic table contains noble (inert) gases?",
                "options": {"A": "Group 1", "B": "Group 7", "C": "Group 17", "D": "Group 18"},
                "correct": "D",
                "explanation": "Group 18 elements have complete valence octets/duplets and are chemically inert.",
            },
            {
                "question": "What type of bond is formed when electrons are transferred between atoms?",
                "options": {"A": "Covalent bond", "B": "Ionic bond", "C": "Metallic bond", "D": "Hydrogen bond"},
                "correct": "B",
                "explanation": "Complete electron transfer from electropositive metal to electronegative non-metal forms ionic bonds.",
            },
        ],
    },
    {
        "class_level": "Class 9",
        "subject": "Biology",
        "title": "[Class 9] Biology: Plant & Animal Tissues (SSC)",
        "topic": "Cell & Tissue Organization",
        "difficulty": "medium",
        "questions": [
            {
                "question": "Which complex plant tissue is responsible for transporting water and dissolved minerals from roots to leaves?",
                "options": {"A": "Phloem", "B": "Xylem", "C": "Collenchyma", "D": "Sclerenchyma"},
                "correct": "B",
                "explanation": "Xylem conducts water and minerals upward; Phloem transports organic nutrients.",
            },
            {
                "question": "Which blood cells are responsible for carrying oxygen throughout the human body?",
                "options": {"A": "White Blood Cells", "B": "Platelets", "C": "Red Blood Cells (Erythrocytes)", "D": "Plasma"},
                "correct": "C",
                "explanation": "RBCs contain hemoglobin, which reversibly binds and transports oxygen molecules.",
            },
            {
                "question": "What type of muscle tissue is found in the walls of the human heart?",
                "options": {"A": "Skeletal muscle", "B": "Smooth muscle", "C": "Cardiac muscle", "D": "Voluntary muscle"},
                "correct": "C",
                "explanation": "Cardiac muscle is involuntary, striated, and specialized for continuous rhythmic contractions.",
            },
        ],
    },
    {
        "class_level": "Class 9",
        "subject": "General Mathematics",
        "title": "[Class 9] General Mathematics: Sets & Algebraic Formulae (SSC)",
        "topic": "Sets & Algebra",
        "difficulty": "medium",
        "questions": [
            {
                "question": "If Set A = {1, 2, 3} and Set B = {3, 4, 5}, what is A ∩ B?",
                "options": {"A": "{1, 2, 4, 5}", "B": "{3}", "C": "{1, 2, 3, 4, 5}", "D": "Empty set"},
                "correct": "B",
                "explanation": "The intersection A ∩ B contains elements present in both sets, which is {3}.",
            },
            {
                "question": "What is the value of (a + b)^2 - (a - b)^2?",
                "options": {"A": "2ab", "B": "4ab", "C": "2(a^2 + b^2)", "D": "a^2 - b^2"},
                "correct": "B",
                "explanation": "(a^2 + 2ab + b^2) - (a^2 - 2ab + b^2) = 4ab.",
            },
            {
                "question": "What is the log base 10 of 1000?",
                "options": {"A": "1", "B": "2", "C": "3", "D": "4"},
                "correct": "C",
                "explanation": "10^3 = 1000, so log10(1000) = 3.",
            },
        ],
    },
    {
        "class_level": "Class 9",
        "subject": "Higher Mathematics",
        "title": "[Class 9] Higher Mathematics: Polynomials & Proofs (SSC)",
        "topic": "Polynomials & Coordinate Geometry",
        "difficulty": "hard",
        "questions": [
            {
                "question": "If polynomial P(x) is divided by (x - a), the remainder is equal to:",
                "options": {"A": "P(0)", "B": "P(a)", "C": "P(-a)", "D": "0"},
                "correct": "B",
                "explanation": "By the Remainder Theorem, dividing P(x) by (x - a) yields remainder R = P(a).",
            },
            {
                "question": "What is the distance between the points (0, 0) and (3, 4) in the Cartesian plane?",
                "options": {"A": "4", "B": "5", "C": "7", "D": "25"},
                "correct": "B",
                "explanation": "d = sqrt((3-0)^2 + (4-0)^2) = sqrt(9 + 16) = sqrt(25) = 5.",
            },
            {
                "question": "What is the value of sin^2(θ) + cos^2(θ) for any angle θ?",
                "options": {"A": "0", "B": "1", "C": "2", "D": "tan^2(θ)"},
                "correct": "B",
                "explanation": "This is the fundamental Pythagorean trigonometric identity: sin^2(θ) + cos^2(θ) = 1.",
            },
        ],
    },
    {
        "class_level": "Class 9",
        "subject": "ICT",
        "title": "[Class 9] ICT: E-Services & Spreadsheet Data (SSC)",
        "topic": "Digital Services & Spreadsheets",
        "difficulty": "medium",
        "questions": [
            {
                "question": "Which government digital service allows citizens to obtain birth certificates online?",
                "options": {"A": "E-Purjee", "B": "E-Registration / Citizen Portal", "C": "E-TIN", "D": "E-Passbook"},
                "correct": "B",
                "explanation": "Citizen service portals enable digital civic registration including birth and death records.",
            },
            {
                "question": "In spreadsheet software, what formula calculates the arithmetic average of cells A1 through A10?",
                "options": {"A": "=MEAN(A1:A10)", "B": "=AVERAGE(A1:A10)", "C": "=SUM(A1:A10)/COUNT", "D": "=AVG(A1:A10)"},
                "correct": "B",
                "explanation": "=AVERAGE(range) calculates the arithmetic mean in Excel and LibreOffice Calc.",
            },
            {
                "question": "What is intellectual property theft via digital duplication without permission termed?",
                "options": {"A": "Phishing", "B": "Software Piracy", "C": "Hacking", "D": "Spamming"},
                "correct": "B",
                "explanation": "Software piracy refers to unauthorized copying, distribution, or reproduction of proprietary software.",
            },
        ],
    },

    # ========================== CLASS 10 (SSC) ==========================
    {
        "class_level": "Class 10",
        "subject": "Physics",
        "title": "[Class 10] Physics: Electricity, Magnetism & Wave Optics (SSC)",
        "topic": "Current Electricity & Light",
        "difficulty": "medium",
        "questions": [
            {
                "question": "According to Ohm's Law, what is the mathematical relationship between Voltage (V), Current (I), and Resistance (R)?",
                "options": {"A": "V = I / R", "B": "V = I * R", "C": "I = V * R", "D": "R = V * I"},
                "correct": "B",
                "explanation": "Ohm's Law states V = IR, meaning current is directly proportional to voltage and inversely to resistance.",
            },
            {
                "question": "What is the electric power consumed by a device calculated as?",
                "options": {"A": "P = V * I", "B": "P = V / I", "C": "P = I / V", "D": "P = V^2 * I"},
                "correct": "A",
                "explanation": "Electrical power P = V * I = I^2 * R = V^2 / R.",
            },
            {
                "question": "What type of lens converges parallel rays of light to a focal point?",
                "options": {"A": "Concave lens", "B": "Convex lens", "C": "Cylindrical lens", "D": "Plano-concave lens"},
                "correct": "B",
                "explanation": "A convex (biconvex) lens is thicker at the center and converges light rays to a real focus.",
            },
        ],
    },
    {
        "class_level": "Class 10",
        "subject": "Chemistry",
        "title": "[Class 10] Chemistry: Chemical Bonds, Acids & Salts (SSC)",
        "topic": "Acids, Bases & Mole Concept",
        "difficulty": "medium",
        "questions": [
            {
                "question": "What is Avogadro's constant, the number of particles in one mole of any substance?",
                "options": {"A": "6.023 * 10^21", "B": "6.023 * 10^23", "C": "3.00 * 10^8", "D": "1.602 * 10^-19"},
                "correct": "B",
                "explanation": "1 mole contains 6.02214 * 10^23 elementary entities (Avogadro's number).",
            },
            {
                "question": "A solution with a pH value of 3 is classified as:",
                "options": {"A": "Strongly basic", "B": "Neutral", "C": "Strongly acidic", "D": "Weakly basic"},
                "correct": "C",
                "explanation": "pH < 7 is acidic; a pH of 3 indicates a high hydronium ion concentration, hence strongly acidic.",
            },
            {
                "question": "What gas is released when hydrochloric acid reacts with calcium carbonate (CaCO3)?",
                "options": {"A": "Oxygen (O2)", "B": "Hydrogen (H2)", "C": "Carbon dioxide (CO2)", "D": "Chlorine (Cl2)"},
                "correct": "C",
                "explanation": "CaCO3 + 2HCl -> CaCl2 + H2O + CO2 (carbon dioxide gas effervesces).",
            },
        ],
    },
    {
        "class_level": "Class 10",
        "subject": "Biology",
        "title": "[Class 10] Biology: Cell Division, Mitosis & Genetics (SSC)",
        "topic": "Mitosis, Meiosis & DNA",
        "difficulty": "medium",
        "questions": [
            {
                "question": "In which stage of mitosis do chromosomes align along the equatorial plate of the cell?",
                "options": {"A": "Prophase", "B": "Metaphase", "C": "Anaphase", "D": "Telophase"},
                "correct": "B",
                "explanation": "During metaphase, chromosomes align symmetrically along the metaphase equatorial plate.",
            },
            {
                "question": "How many chromosomes are present in a normal diploid human somatic cell?",
                "options": {"A": "23", "B": "46", "C": "48", "D": "92"},
                "correct": "B",
                "explanation": "Human somatic cells contain 23 pairs (46 total) of diploid chromosomes.",
            },
            {
                "question": "What type of cell division produces haploid gametes (sperm and egg cells)?",
                "options": {"A": "Binary fission", "B": "Mitosis", "C": "Meiosis", "D": "Amitosis"},
                "correct": "C",
                "explanation": "Meiosis halves the chromosome count from 2n to n, producing genetic diversity in gametes.",
            },
        ],
    },
    {
        "class_level": "Class 10",
        "subject": "General Mathematics",
        "title": "[Class 10] General Mathematics: Trigonometry & Mensuration (SSC)",
        "topic": "Trigonometry & Solid Geometry",
        "difficulty": "medium",
        "questions": [
            {
                "question": "What is the value of tan(45°)?",
                "options": {"A": "0", "B": "1/2", "C": "1", "D": "sqrt(3)"},
                "correct": "C",
                "explanation": "tan(45°) = sin(45°)/cos(45°) = (1/√2)/(1/√2) = 1.",
            },
            {
                "question": "What is the formula for the volume of a sphere of radius r?",
                "options": {"A": "2πr^2", "B": "4πr^2", "C": "(4/3)πr^3", "D": "πr^2h"},
                "correct": "C",
                "explanation": "Volume of a sphere = (4/3)πr^3.",
            },
            {
                "question": "What is the discriminant of the quadratic equation ax^2 + bx + c = 0?",
                "options": {"A": "b^2 - 4ac", "B": "b^2 + 4ac", "C": "-b ± sqrt(d)", "D": "4ac - b^2"},
                "correct": "A",
                "explanation": "The discriminant D = b^2 - 4ac determines the nature of quadratic roots.",
            },
        ],
    },
    {
        "class_level": "Class 10",
        "subject": "Higher Mathematics",
        "title": "[Class 10] Higher Mathematics: Vectors & Coordinates (SSC)",
        "topic": "Vectors & Analytic Geometry",
        "difficulty": "hard",
        "questions": [
            {
                "question": "What is the slope (gradient) of a line passing through (1, 2) and (3, 6)?",
                "options": {"A": "1", "B": "2", "C": "3", "D": "4"},
                "correct": "B",
                "explanation": "m = (y2 - y1) / (x2 - x1) = (6 - 2) / (3 - 1) = 4 / 2 = 2.",
            },
            {
                "question": "If two non-zero vectors A and B are perpendicular, their dot product A · B equals:",
                "options": {"A": "1", "B": "0", "C": "|A||B|", "D": "-1"},
                "correct": "B",
                "explanation": "A · B = |A||B| cos(90°) = |A||B| * 0 = 0.",
            },
            {
                "question": "In binomial expansion of (1 + x)^n, what is the general r-th term?",
                "options": {"A": "nCr * x^r", "B": "nPr * x^r", "C": "n! * x", "D": "x^(n-r)"},
                "correct": "A",
                "explanation": "The general term Tr+1 in binomial expansion is nCr * x^r.",
            },
        ],
    },
    {
        "class_level": "Class 10",
        "subject": "ICT",
        "title": "[Class 10] ICT: Database Management & Querying (SSC)",
        "topic": "Databases & SQL",
        "difficulty": "medium",
        "questions": [
            {
                "question": "In database design, what is a field that uniquely identifies each record in a table?",
                "options": {"A": "Foreign Key", "B": "Secondary Key", "C": "Primary Key", "D": "Index Key"},
                "correct": "C",
                "explanation": "A Primary Key uniquely identifies each row in a relational database table with no null values.",
            },
            {
                "question": "Which SQL keyword is used to retrieve data from a database?",
                "options": {"A": "GET", "B": "FETCH", "C": "SELECT", "D": "RETRIEVE"},
                "correct": "C",
                "explanation": "The SQL SELECT statement retrieves designated rows and columns from database tables.",
            },
            {
                "question": "What is the smallest unit of digital data storage?",
                "options": {"A": "Byte", "B": "Bit", "C": "Nibble", "D": "Word"},
                "correct": "B",
                "explanation": "A bit (binary digit, 0 or 1) is the fundamental unit of digital information.",
            },
        ],
    },

    # ========================== CLASS 11 (HSC) ==========================
    {
        "class_level": "Class 11",
        "subject": "Physics",
        "title": "[Class 11] Physics: Vector Analysis, Kinematics & Dynamics (HSC)",
        "topic": "Vectors & Classical Mechanics",
        "difficulty": "hard",
        "questions": [
            {
                "question": "What is the magnitude of the cross product of two parallel vectors?",
                "options": {"A": "|A||B|", "B": "0", "C": "1", "D": "2|A||B|"},
                "correct": "B",
                "explanation": "|A x B| = |A||B| sin(0°) = 0 for parallel vectors.",
            },
            {
                "question": "In projectile motion launched at an angle θ, what launch angle yields the maximum horizontal range (R_max)?",
                "options": {"A": "30°", "B": "45°", "C": "60°", "D": "90°"},
                "correct": "B",
                "explanation": "Range R = (v^2 sin 2θ)/g. Maximum occurs when sin 2θ = 1 => 2θ = 90° => θ = 45°.",
            },
            {
                "question": "In rotational motion, what is the rotational analogue of mass in linear motion?",
                "options": {"A": "Angular momentum", "B": "Torque", "C": "Moment of Inertia", "D": "Angular acceleration"},
                "correct": "C",
                "explanation": "Moment of inertia (I = Σmr^2) measures rotational inertia against angular acceleration.",
            },
        ],
    },
    {
        "class_level": "Class 11",
        "subject": "Chemistry",
        "title": "[Class 11] Chemistry: Quantum Numbers & Chemical Periodic Properties (HSC)",
        "topic": "Atomic Orbitals & Chemical Bonds",
        "difficulty": "hard",
        "questions": [
            {
                "question": "Which quantum number determines the spatial orientation of an atomic orbital?",
                "options": {"A": "Principal (n)", "B": "Azimuthal (l)", "C": "Magnetic (m_l)", "D": "Spin (m_s)"},
                "correct": "C",
                "explanation": "The magnetic quantum number (m_l) designates orbital orientation in three-dimensional space.",
            },
            {
                "question": "What is the geometry of a methane (CH4) molecule based on VSEPR theory and sp3 hybridization?",
                "options": {"A": "Linear", "B": "Trigonal planar", "C": "Tetrahedral", "D": "Octahedral"},
                "correct": "C",
                "explanation": "CH4 has sp3 hybridization with 4 bonding pairs and 0 lone pairs, forming a symmetric tetrahedron with 109.5° angles.",
            },
            {
                "question": "Which principle states that no two electrons in an atom can have the same four quantum numbers?",
                "options": {"A": "Aufbau Principle", "B": "Pauli Exclusion Principle", "C": "Hund's Rule", "D": "Heisenberg Uncertainty"},
                "correct": "B",
                "explanation": "Pauli's Exclusion Principle dictates each orbital can hold at most 2 electrons with opposite spins.",
            },
        ],
    },
    {
        "class_level": "Class 11",
        "subject": "Biology",
        "title": "[Class 11] Biology: Cell Structure, Cell Cycle & Botany (HSC)",
        "topic": "Cell Biology & Photosynthesis",
        "difficulty": "hard",
        "questions": [
            {
                "question": "Which primary enzyme catalyzes CO2 fixation in the Calvin cycle (C3 pathway)?",
                "options": {"A": "ATP Synthase", "B": "RuBisCO", "C": "DNA Polymerase", "D": "Amylase"},
                "correct": "B",
                "explanation": "RuBisCO (Ribulose-1,5-bisphosphate carboxylase-oxygenase) catalyzes photosynthetic carbon fixation.",
            },
            {
                "question": "What is the primary structural carbohydrate component of plant cell walls?",
                "options": {"A": "Glycogen", "B": "Starch", "C": "Cellulose", "D": "Chitin"},
                "correct": "C",
                "explanation": "Cellulose forms linear chains of β-glucose microfibrils providing rigidity to plant cell walls.",
            },
            {
                "question": "In which sub-stage of Prophase I does crossing over occur between non-sister chromatids?",
                "options": {"A": "Leptotene", "B": "Zygotene", "C": "Pachytene", "D": "Diplotene"},
                "correct": "C",
                "explanation": "Genetic recombination via crossing over and chiasma formation occurs during the Pachytene stage of Meiosis I.",
            },
        ],
    },
    {
        "class_level": "Class 11",
        "subject": "Higher Mathematics",
        "title": "[Class 11] Higher Mathematics: Matrices, Determinants & Straight Lines (HSC)",
        "topic": "Linear Algebra & Calculus",
        "difficulty": "hard",
        "questions": [
            {
                "question": "If determinant |A| = 0, what is matrix A termed?",
                "options": {"A": "Symmetric matrix", "B": "Singular matrix", "C": "Identity matrix", "D": "Orthogonal matrix"},
                "correct": "B",
                "explanation": "A square matrix whose determinant is zero is called a singular matrix and has no inverse.",
            },
            {
                "question": "What is the derivative of f(x) = sin(x) with respect to x?",
                "options": {"A": "-cos(x)", "B": "cos(x)", "C": "tan(x)", "D": "-sin(x)"},
                "correct": "B",
                "explanation": "d/dx[sin(x)] = cos(x).",
            },
            {
                "question": "What is the angle between two lines with slopes m1 and m2 when m1 * m2 = -1?",
                "options": {"A": "0°", "B": "45°", "C": "90°", "D": "180°"},
                "correct": "C",
                "explanation": "When the product of two linear slopes is -1, the lines are perpendicular (orthogonal, 90°).",
            },
        ],
    },
    {
        "class_level": "Class 11",
        "subject": "ICT",
        "title": "[Class 11] ICT: Data Communication & Number Systems (HSC)",
        "topic": "Networking & Binary Logic",
        "difficulty": "medium",
        "questions": [
            {
                "question": "What is the binary representation of decimal number 13?",
                "options": {"A": "1011", "B": "1101", "C": "1110", "D": "1001"},
                "correct": "B",
                "explanation": "13 = 8 + 4 + 0 + 1 = 2^3 + 2^2 + 0 + 2^0 = (1101)2.",
            },
            {
                "question": "Which transmission medium uses total internal reflection of light pulses to transmit high-speed data?",
                "options": {"A": "Coaxial cable", "B": "Twisted pair cable", "C": "Fiber optic cable", "D": "Radio wave"},
                "correct": "C",
                "explanation": "Fiber optic cables transmit modulated light signals via optical core reflection at near speed of light.",
            },
            {
                "question": "What logic gate outputs 1 only when BOTH of its inputs are 1?",
                "options": {"A": "OR Gate", "B": "AND Gate", "C": "NOT Gate", "D": "XOR Gate"},
                "correct": "B",
                "explanation": "An AND gate requires all inputs to be true (1) to generate a true (1) output.",
            },
        ],
    },
    {
        "class_level": "Class 11",
        "subject": "English",
        "title": "[Class 11] English: Advanced Reading Comprehension & Synonyms (HSC)",
        "topic": "Advanced Grammar & Vocabulary",
        "difficulty": "medium",
        "questions": [
            {
                "question": "Choose the word closest in meaning to 'Pragmatic':",
                "options": {"A": "Idealistic", "B": "Practical", "C": "Theoretical", "D": "Careless"},
                "correct": "B",
                "explanation": "'Pragmatic' describes dealing with things sensibly and realistically based on practical considerations.",
            },
            {
                "question": "Identify the conditional type: 'If it rains, we will cancel the match.'",
                "options": {"A": "Zero conditional", "B": "First conditional", "C": "Second conditional", "D": "Third conditional"},
                "correct": "B",
                "explanation": "'If + present simple, will + base verb' is the first conditional denoting a real future condition.",
            },
            {
                "question": "What is the term for a word that sounds the same as another word but has a different meaning and spelling?",
                "options": {"A": "Synonym", "B": "Antonym", "C": "Homophone", "D": "Acronym"},
                "correct": "C",
                "explanation": "Homophones (e.g. 'their', 'there', 'they're') share identical pronunciation with differing spellings/meanings.",
            },
        ],
    },

    # ========================== CLASS 12 (HSC) ==========================
    {
        "class_level": "Class 12",
        "subject": "Physics",
        "title": "[Class 12] Physics: Thermodynamics, Wave Optics & Modern Physics (HSC)",
        "topic": "Thermodynamics & Quantum Physics",
        "difficulty": "hard",
        "questions": [
            {
                "question": "What is the maximum theoretical efficiency limit for any heat engine operating between temperatures T_H and T_C?",
                "options": {"A": "η = 1 - (T_C / T_H)", "B": "η = 1 - (T_H / T_C)", "C": "η = T_C / T_H", "D": "η = 100%"},
                "correct": "A",
                "explanation": "Carnot engine efficiency η = 1 - (T_C / T_H) represents the thermodynamic upper bound.",
            },
            {
                "question": "According to Einstein's photoelectric equation, what is the kinetic energy of an emitted photoelectron?",
                "options": {"A": "KE = hf - Φ (work function)", "B": "KE = hf + Φ", "C": "KE = Φ / hf", "D": "KE = mc^2"},
                "correct": "A",
                "explanation": "Photon energy hf overcomes surface work function Φ with excess energy manifesting as kinetic energy: KE_max = hf - Φ.",
            },
            {
                "question": "What phenomenon demonstrates the wave nature of light in Young's Double Slit Experiment?",
                "options": {"A": "Photoelectric effect", "B": "Interference", "C": "Compton scattering", "D": "Pair production"},
                "correct": "B",
                "explanation": "The alternating bright and dark fringe pattern results from optical wave interference.",
            },
        ],
    },
    {
        "class_level": "Class 12",
        "subject": "Chemistry",
        "title": "[Class 12] Chemistry: Organic Hydrocarbons & Electrochemistry (HSC)",
        "topic": "Organic Chemistry & Electrochemistry",
        "difficulty": "hard",
        "questions": [
            {
                "question": "Which reagent is commonly used to distinguish between aldehydes and ketones via a silver mirror formation?",
                "options": {"A": "Fehling's solution", "B": "Tollens' reagent", "C": "Grignard reagent", "D": "Lucas reagent"},
                "correct": "B",
                "explanation": "Tollens' reagent ([Ag(NH3)2]+) oxidizes aldehydes to form a metallic silver mirror; ketones do not react.",
            },
            {
                "question": "What rule governs electrophilic addition of hydrogen halides to unsymmetrical alkenes?",
                "options": {"A": "Markovnikov's Rule", "B": "Saytzeff's Rule", "C": "Hund's Rule", "D": "Le Chatelier's Principle"},
                "correct": "A",
                "explanation": "Markovnikov's rule dictates that hydrogen adds to the carbon with more hydrogen atoms attached.",
            },
            {
                "question": "In an electrochemical galvanic cell, where does oxidation occur?",
                "options": {"A": "Anode", "B": "Cathode", "C": "Salt bridge", "D": "Electrolyte solution"},
                "correct": "A",
                "explanation": "Oxidation (loss of electrons) occurs at the anode; reduction occurs at the cathode (AN OX, RED CAT).",
            },
        ],
    },
    {
        "class_level": "Class 12",
        "subject": "Biology",
        "title": "[Class 12] Biology: Genetics, Evolution & Zoology (HSC)",
        "topic": "Mendelian Genetics & Human Physiology",
        "difficulty": "hard",
        "questions": [
            {
                "question": "What is the phenotypic ratio in the F2 generation of a classic Mendelian monohybrid cross?",
                "options": {"A": "1:2:1", "B": "3:1", "C": "9:3:3:1", "D": "1:1:1:1"},
                "correct": "B",
                "explanation": "The F2 generation exhibits a 3:1 dominant to recessive phenotypic ratio.",
            },
            {
                "question": "In DNA double helix, which nitrogenous base pairs with Adenine (A) via two hydrogen bonds?",
                "options": {"A": "Guanine", "B": "Cytosine", "C": "Thymine", "D": "Uracil"},
                "correct": "C",
                "explanation": "In DNA, Adenine (A) pairs with Thymine (T) via 2 hydrogen bonds; Guanine (G) pairs with Cytosine (C) via 3 bonds.",
            },
            {
                "question": "What is the functional and structural microscopic filtration unit of the human kidney?",
                "options": {"A": "Neuron", "B": "Nephron", "C": "Alveolus", "D": "Hepatocyte"},
                "correct": "B",
                "explanation": "Each kidney contains approximately 1 million nephrons that filter blood and form urine.",
            },
        ],
    },
    {
        "class_level": "Class 12",
        "subject": "Higher Mathematics",
        "title": "[Class 12] Higher Mathematics: Differential & Integral Calculus (HSC)",
        "topic": "Integration & Complex Numbers",
        "difficulty": "hard",
        "questions": [
            {
                "question": "What is the indefinite integral of e^(2x) with respect to x?",
                "options": {"A": "e^(2x) + C", "B": "(1/2) e^(2x) + C", "C": "2 e^(2x) + C", "D": "e^x + C"},
                "correct": "B",
                "explanation": "∫ e^(kx) dx = (1/k) e^(kx) + C. Here k = 2.",
            },
            {
                "question": "What is the value of i^2 in the complex number system, where i = sqrt(-1)?",
                "options": {"A": "1", "B": "-1", "C": "0", "D": "-i"},
                "correct": "B",
                "explanation": "By definition, imaginary unit i = √-1, hence i^2 = -1.",
            },
            {
                "question": "What is the eccentricity (e) of a parabola in conic sections?",
                "options": {"A": "e = 0", "B": "e = 1", "C": "e < 1", "D": "e > 1"},
                "correct": "B",
                "explanation": "For conic sections: circle has e = 0, ellipse has e < 1, parabola has e = 1, hyperbola has e > 1.",
            },
        ],
    },
    {
        "class_level": "Class 12",
        "subject": "ICT",
        "title": "[Class 12] ICT: C Programming Language & Web Design with HTML (HSC)",
        "topic": "C Programming & HTML",
        "difficulty": "hard",
        "questions": [
            {
                "question": "Which format specifier is used in C programming to read or print an integer with printf/scanf?",
                "options": {"A": "%f", "B": "%d", "C": "%c", "D": "%s"},
                "correct": "B",
                "explanation": "%d (or %i) denotes signed decimal integers in C standard I/O library.",
            },
            {
                "question": "In HTML, which tag is used to create a clickable hyperlink?",
                "options": {"A": "<link>", "B": "<a>", "C": "<href>", "D": "<url>"},
                "correct": "B",
                "explanation": "The anchor tag <a href=\"...\"> creates hyperlinks in HTML documents.",
            },
            {
                "question": "What will be the output of the C expression: 10 % 3?",
                "options": {"A": "3", "B": "1", "C": "3.33", "D": "0"},
                "correct": "B",
                "explanation": "The modulus operator (%) calculates the integer remainder of division: 10 / 3 = 3 with remainder 1.",
            },
        ],
    },
    {
        "class_level": "Class 12",
        "subject": "Accounting & Economics",
        "title": "[Class 12] Accounting & Economics: Financial Statements & Microeconomics (HSC)",
        "topic": "Financial Accounting & Elasticity",
        "difficulty": "medium",
        "questions": [
            {
                "question": "What is the fundamental accounting equation in financial balance sheets?",
                "options": {"A": "Assets = Liabilities - Equity", "B": "Assets = Liabilities + Equity", "C": "Equity = Assets + Liabilities", "D": "Revenue - Expenses = Assets"},
                "correct": "B",
                "explanation": "The double-entry accounting equation states: Assets = Liabilities + Owner's Equity.",
            },
            {
                "question": "When the price elasticity of demand (|Ed|) is greater than 1, demand is described as:",
                "options": {"A": "Inelastic", "B": "Unitary elastic", "C": "Elastic", "D": "Perfectly inelastic"},
                "correct": "C",
                "explanation": "If % change in quantity demanded exceeds % change in price (|Ed| > 1), demand is elastic.",
            },
            {
                "question": "In modern accounting, which financial statement reports a firm's profitability over an operating period?",
                "options": {"A": "Balance Sheet", "B": "Income Statement (Profit & Loss)", "C": "Cash Flow Statement", "D": "Statement of Retained Earnings"},
                "correct": "B",
                "explanation": "The Income Statement presents revenues, expenses, and net profit/loss across a designated fiscal duration.",
            },
        ],
    },
]


def seed_class_quizzes_for_user(user_id: int) -> int:
    """Ensure all Class 6-12 curriculum quizzes exist for the given user ID.

    Returns the count of newly inserted quizzes.
    """
    existing_titles = {
        q.title for q in Quiz.query.filter_by(user_id=user_id).all()
    }

    added_count = 0
    for q_data in PREBUILT_QUIZZES:
        if q_data["title"] in existing_titles:
            continue

        new_quiz = Quiz(
            user_id=user_id,
            subject_id=None,
            title=q_data["title"],
            topic=q_data["topic"],
            class_level=q_data["class_level"],
            difficulty=q_data["difficulty"],
            total_questions=len(q_data["questions"]),
        )
        db.session.add(new_quiz)
        db.session.flush()

        for question_data in q_data["questions"]:
            question = QuizQuestion(
                quiz_id=new_quiz.id,
                question_text=question_data["question"],
                option_a=question_data["options"]["A"],
                option_b=question_data["options"]["B"],
                option_c=question_data["options"]["C"],
                option_d=question_data["options"]["D"],
                correct_option=question_data["correct"],
                explanation=question_data.get("explanation", ""),
            )
            db.session.add(question)

        existing_titles.add(q_data["title"])
        added_count += 1

    if added_count > 0:
        db.session.commit()

    return added_count


# =============================================================================
# Curriculum Subjects for Class 6 to Class 12
# =============================================================================
CURRICULUM_SUBJECTS = [
    # Class 6
    {"class_level": "Class 6", "name": "Class 6: General Science", "code": "SCI-06", "color_hex": "#10B981"},
    {"class_level": "Class 6", "name": "Class 6: Mathematics", "code": "MTH-06", "color_hex": "#3B82F6"},
    {"class_level": "Class 6", "name": "Class 6: English", "code": "ENG-06", "color_hex": "#8B5CF6"},
    {"class_level": "Class 6", "name": "Class 6: Bangla", "code": "BAN-06", "color_hex": "#EC4899"},
    {"class_level": "Class 6", "name": "Class 6: ICT", "code": "ICT-06", "color_hex": "#06B6D4"},
    {"class_level": "Class 6", "name": "Class 6: Bangladesh & Global Studies", "code": "BGS-06", "color_hex": "#F59E0B"},

    # Class 7
    {"class_level": "Class 7", "name": "Class 7: General Science", "code": "SCI-07", "color_hex": "#10B981"},
    {"class_level": "Class 7", "name": "Class 7: Mathematics", "code": "MTH-07", "color_hex": "#3B82F6"},
    {"class_level": "Class 7", "name": "Class 7: English", "code": "ENG-07", "color_hex": "#8B5CF6"},
    {"class_level": "Class 7", "name": "Class 7: Bangla", "code": "BAN-07", "color_hex": "#EC4899"},
    {"class_level": "Class 7", "name": "Class 7: ICT", "code": "ICT-07", "color_hex": "#06B6D4"},
    {"class_level": "Class 7", "name": "Class 7: Bangladesh & Global Studies", "code": "BGS-07", "color_hex": "#F59E0B"},

    # Class 8
    {"class_level": "Class 8", "name": "Class 8: General Science", "code": "SCI-08", "color_hex": "#10B981"},
    {"class_level": "Class 8", "name": "Class 8: Mathematics", "code": "MTH-08", "color_hex": "#3B82F6"},
    {"class_level": "Class 8", "name": "Class 8: English", "code": "ENG-08", "color_hex": "#8B5CF6"},
    {"class_level": "Class 8", "name": "Class 8: Bangla", "code": "BAN-08", "color_hex": "#EC4899"},
    {"class_level": "Class 8", "name": "Class 8: ICT", "code": "ICT-08", "color_hex": "#06B6D4"},
    {"class_level": "Class 8", "name": "Class 8: Bangladesh & Global Studies", "code": "BGS-08", "color_hex": "#F59E0B"},

    # Class 9 (SSC)
    {"class_level": "Class 9", "name": "Class 9: Physics", "code": "PHY-09", "color_hex": "#6366F1"},
    {"class_level": "Class 9", "name": "Class 9: Chemistry", "code": "CHM-09", "color_hex": "#14B8A6"},
    {"class_level": "Class 9", "name": "Class 9: Biology", "code": "BIO-09", "color_hex": "#22C55E"},
    {"class_level": "Class 9", "name": "Class 9: General Mathematics", "code": "GMTH-09", "color_hex": "#2563EB"},
    {"class_level": "Class 9", "name": "Class 9: Higher Mathematics", "code": "HMTH-09", "color_hex": "#7C3AED"},
    {"class_level": "Class 9", "name": "Class 9: ICT", "code": "ICT-09", "color_hex": "#0EA5E9"},
    {"class_level": "Class 9", "name": "Class 9: English", "code": "ENG-09", "color_hex": "#A855F7"},
    {"class_level": "Class 9", "name": "Class 9: Bangla", "code": "BAN-09", "color_hex": "#F43F5E"},
    {"class_level": "Class 9", "name": "Class 9: Business Studies", "code": "BUS-09", "color_hex": "#F97316"},

    # Class 10 (SSC)
    {"class_level": "Class 10", "name": "Class 10: Physics", "code": "PHY-10", "color_hex": "#6366F1"},
    {"class_level": "Class 10", "name": "Class 10: Chemistry", "code": "CHM-10", "color_hex": "#14B8A6"},
    {"class_level": "Class 10", "name": "Class 10: Biology", "code": "BIO-10", "color_hex": "#22C55E"},
    {"class_level": "Class 10", "name": "Class 10: General Mathematics", "code": "GMTH-10", "color_hex": "#2563EB"},
    {"class_level": "Class 10", "name": "Class 10: Higher Mathematics", "code": "HMTH-10", "color_hex": "#7C3AED"},
    {"class_level": "Class 10", "name": "Class 10: ICT", "code": "ICT-10", "color_hex": "#0EA5E9"},
    {"class_level": "Class 10", "name": "Class 10: English", "code": "ENG-10", "color_hex": "#A855F7"},
    {"class_level": "Class 10", "name": "Class 10: Bangla", "code": "BAN-10", "color_hex": "#F43F5E"},
    {"class_level": "Class 10", "name": "Class 10: Business Studies", "code": "BUS-10", "color_hex": "#F97316"},

    # Class 11 (HSC)
    {"class_level": "Class 11", "name": "Class 11: Physics 1st Paper", "code": "PHY-11", "color_hex": "#4F46E5"},
    {"class_level": "Class 11", "name": "Class 11: Chemistry 1st Paper", "code": "CHM-11", "color_hex": "#0D9488"},
    {"class_level": "Class 11", "name": "Class 11: Biology 1st Paper (Botany)", "code": "BIO-11", "color_hex": "#16A34A"},
    {"class_level": "Class 11", "name": "Class 11: Higher Mathematics 1st Paper", "code": "HMTH-11", "color_hex": "#9333EA"},
    {"class_level": "Class 11", "name": "Class 11: ICT", "code": "ICT-11", "color_hex": "#0284C7"},
    {"class_level": "Class 11", "name": "Class 11: English 1st Paper", "code": "ENG-11", "color_hex": "#C026D3"},
    {"class_level": "Class 11", "name": "Class 11: Bangla 1st Paper", "code": "BAN-11", "color_hex": "#E11D48"},
    {"class_level": "Class 11", "name": "Class 11: Accounting & Finance", "code": "ACC-11", "color_hex": "#EA580C"},

    # Class 12 (HSC)
    {"class_level": "Class 12", "name": "Class 12: Physics 2nd Paper", "code": "PHY-12", "color_hex": "#4338CA"},
    {"class_level": "Class 12", "name": "Class 12: Chemistry 2nd Paper", "code": "CHM-12", "color_hex": "#0F766E"},
    {"class_level": "Class 12", "name": "Class 12: Biology 2nd Paper (Zoology)", "code": "BIO-12", "color_hex": "#15803D"},
    {"class_level": "Class 12", "name": "Class 12: Higher Mathematics 2nd Paper", "code": "HMTH-12", "color_hex": "#7E22CE"},
    {"class_level": "Class 12", "name": "Class 12: ICT", "code": "ICT-12", "color_hex": "#0369A1"},
    {"class_level": "Class 12", "name": "Class 12: English 2nd Paper", "code": "ENG-12", "color_hex": "#A21CAF"},
    {"class_level": "Class 12", "name": "Class 12: Bangla 2nd Paper", "code": "BAN-12", "color_hex": "#BE123C"},
    {"class_level": "Class 12", "name": "Class 12: Accounting & Economics", "code": "ECO-12", "color_hex": "#C2410C"},
]


def seed_class_subjects_for_user(user_id: int) -> int:
    """Ensure all Class 6-12 curriculum subjects exist for the given user ID.

    Returns the count of newly inserted subjects.
    """
    from app.models.subject import Subject

    existing_names = {
        s.name for s in Subject.query.filter_by(user_id=user_id).all()
    }

    added_count = 0
    for subj_data in CURRICULUM_SUBJECTS:
        if subj_data["name"] in existing_names:
            continue

        new_subj = Subject(
            user_id=user_id,
            name=subj_data["name"],
            code=subj_data["code"],
            class_level=subj_data["class_level"],
            color_hex=subj_data["color_hex"],
        )
        db.session.add(new_subj)
        existing_names.add(subj_data["name"])
        added_count += 1

    if added_count > 0:
        db.session.commit()

    return added_count
