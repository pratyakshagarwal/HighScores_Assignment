from pymongo import MongoClient
from datetime import datetime, timezone

client = MongoClient("mongodb://localhost:27017/")
db = client["adaptive_test"]

questions_col = db["questions"]
sessions_col = db["user_sessions"]

questions_col.drop()
sessions_col.drop()
print("Database cleared.")

questions = [
    # ── ALGEBRA ──────────────────────────────────────────────
    {
        "question_id": "ALG001", "topic": "Algebra", "difficulty": 0.2, "discrimination": 0.4,
        "tags": ["linear equations", "basic algebra"],
        "question_text": "Solve for x: 3x + 9 = 0",
        "options": {"A": "3", "B": "-3", "C": "0", "D": "-9"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "ALG002", "topic": "Algebra", "difficulty": 0.4, "discrimination": 0.7,
        "tags": ["quadratic equations", "factoring"],
        "question_text": "Which values of x satisfy x² - 5x + 6 = 0?",
        "options": {"A": "1,6", "B": "2,3", "C": "-2,-3", "D": "-1,6"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "ALG003", "topic": "Algebra", "difficulty": 0.6, "discrimination": 0.8,
        "tags": ["functions", "substitution"],
        "question_text": "If f(x) = 2x² - 3x + 1, what is f(3)?",
        "options": {"A": "10", "B": "12", "C": "16", "D": "9"},
        "correct_answer": "A", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "ALG004", "topic": "Algebra", "difficulty": 0.75, "discrimination": 0.9,
        "tags": ["absolute value", "equations"],
        "question_text": "Solve: |2x - 4| = 10",
        "options": {"A": "x=7 or x=-3", "B": "x=3 or x=-7", "C": "x=7 only", "D": "x=5 or x=-1"},
        "correct_answer": "A", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "ALG005", "topic": "Algebra", "difficulty": 0.85, "discrimination": 0.95,
        "tags": ["quadratic equations", "discriminant", "real roots"],
        "question_text": "For what values of k does kx² - 4x + k = 0 have real roots?",
        "options": {"A": "k ≤ 2", "B": "-2 ≤ k ≤ 2", "C": "k ≥ 2", "D": "k ≤ -2 or k ≥ 2"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "ALG006", "topic": "Algebra", "difficulty": 0.3, "discrimination": 0.55,
        "tags": ["linear equations", "slope"],
        "question_text": "What is the slope of the line y = 4x - 7?",
        "options": {"A": "-7", "B": "4", "C": "7", "D": "-4"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "ALG007", "topic": "Algebra", "difficulty": 0.5, "discrimination": 0.75,
        "tags": ["simultaneous equations", "substitution"],
        "question_text": "If 2x + y = 10 and x - y = 2, what is x?",
        "options": {"A": "3", "B": "4", "C": "5", "D": "6"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "ALG008", "topic": "Algebra", "difficulty": 0.65, "discrimination": 0.85,
        "tags": ["inequalities", "number line"],
        "question_text": "Which value of x satisfies 3x - 5 > 10?",
        "options": {"A": "4", "B": "5", "C": "6", "D": "3"},
        "correct_answer": "C", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "ALG009", "topic": "Algebra", "difficulty": 0.9, "discrimination": 0.95,
        "tags": ["polynomials", "remainder theorem"],
        "question_text": "What is the remainder when x³ - 4x² + 5x - 2 is divided by (x - 1)?",
        "options": {"A": "1", "B": "0", "C": "-1", "D": "2"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },

    # ── GEOMETRY ─────────────────────────────────────────────
    {
        "question_id": "GEO001", "topic": "Geometry", "difficulty": 0.2, "discrimination": 0.4,
        "tags": ["area", "triangles"],
        "question_text": "What is the area of a triangle with base 8 and height 5?",
        "options": {"A": "40", "B": "20", "C": "13", "D": "80"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "GEO002", "topic": "Geometry", "difficulty": 0.4, "discrimination": 0.65,
        "tags": ["circles", "circumference"],
        "question_text": "What is the circumference of a circle with radius 7? (π = 3.14)",
        "options": {"A": "43.96", "B": "21.98", "C": "49", "D": "153.86"},
        "correct_answer": "A", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "GEO003", "topic": "Geometry", "difficulty": 0.55, "discrimination": 0.75,
        "tags": ["pythagorean theorem", "right triangles"],
        "question_text": "In a right triangle, the two legs are 6 and 8. What is the hypotenuse?",
        "options": {"A": "12", "B": "10", "C": "14", "D": "9"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "GEO004", "topic": "Geometry", "difficulty": 0.7, "discrimination": 0.85,
        "tags": ["volume", "cylinder"],
        "question_text": "What is the volume of a cylinder with radius 3 and height 10? (π = 3.14)",
        "options": {"A": "282.6", "B": "94.2", "C": "188.4", "D": "300"},
        "correct_answer": "A", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "GEO005", "topic": "Geometry", "difficulty": 0.8, "discrimination": 0.9,
        "tags": ["parallel lines", "transversal", "angles"],
        "question_text": "Two parallel lines are cut by a transversal. One co-interior angle is 65°. What is the other?",
        "options": {"A": "65°", "B": "115°", "C": "125°", "D": "90°"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "GEO006", "topic": "Geometry", "difficulty": 0.3, "discrimination": 0.5,
        "tags": ["perimeter", "rectangle"],
        "question_text": "What is the perimeter of a rectangle with length 9 and width 4?",
        "options": {"A": "36", "B": "26", "C": "13", "D": "40"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "GEO007", "topic": "Geometry", "difficulty": 0.45, "discrimination": 0.7,
        "tags": ["circles", "area"],
        "question_text": "What is the area of a circle with diameter 10? (π = 3.14)",
        "options": {"A": "31.4", "B": "78.5", "C": "314", "D": "62.8"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "GEO008", "topic": "Geometry", "difficulty": 0.65, "discrimination": 0.8,
        "tags": ["angles", "polygons", "interior angles"],
        "question_text": "What is the sum of interior angles of a hexagon?",
        "options": {"A": "540°", "B": "720°", "C": "900°", "D": "360°"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "GEO009", "topic": "Geometry", "difficulty": 0.85, "discrimination": 0.92,
        "tags": ["coordinate geometry", "distance formula"],
        "question_text": "What is the distance between points (1, 2) and (4, 6)?",
        "options": {"A": "3", "B": "5", "C": "7", "D": "4"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },

    # ── VOCABULARY ───────────────────────────────────────────
    {
        "question_id": "VOC001", "topic": "Vocabulary", "difficulty": 0.2, "discrimination": 0.4,
        "tags": ["GRE vocab", "adjectives"],
        "question_text": "What does 'benevolent' mean?",
        "options": {"A": "Hostile", "B": "Kind and generous", "C": "Confused", "D": "Cautious"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "VOC002", "topic": "Vocabulary", "difficulty": 0.35, "discrimination": 0.6,
        "tags": ["GRE vocab", "synonyms"],
        "question_text": "Choose the word closest in meaning to 'eloquent'.",
        "options": {"A": "Silent", "B": "Articulate", "C": "Rude", "D": "Nervous"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "VOC003", "topic": "Vocabulary", "difficulty": 0.55, "discrimination": 0.75,
        "tags": ["GRE vocab", "adjectives"],
        "question_text": "What does 'ephemeral' mean?",
        "options": {"A": "Permanent", "B": "Short-lived", "C": "Enormous", "D": "Secretive"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "VOC004", "topic": "Vocabulary", "difficulty": 0.7, "discrimination": 0.85,
        "tags": ["GRE vocab", "nouns"],
        "question_text": "The word 'sycophant' refers to someone who is:",
        "options": {"A": "Excessively flattering to gain favor", "B": "Extremely intelligent", "C": "Deeply religious", "D": "Chronically ill"},
        "correct_answer": "A", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "VOC005", "topic": "Vocabulary", "difficulty": 0.4, "discrimination": 0.65,
        "tags": ["GRE vocab", "antonyms"],
        "question_text": "What is the antonym of 'laconic'?",
        "options": {"A": "Brief", "B": "Verbose", "C": "Quiet", "D": "Angry"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "VOC006", "topic": "Vocabulary", "difficulty": 0.6, "discrimination": 0.8,
        "tags": ["GRE vocab", "adjectives"],
        "question_text": "What does 'perfidious' mean?",
        "options": {"A": "Loyal", "B": "Treacherous", "C": "Courageous", "D": "Generous"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "VOC007", "topic": "Vocabulary", "difficulty": 0.8, "discrimination": 0.9,
        "tags": ["GRE vocab", "rare words"],
        "question_text": "What does 'obsequious' mean?",
        "options": {"A": "Defiant", "B": "Servilely compliant", "C": "Loudly assertive", "D": "Deeply thoughtful"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "VOC008", "topic": "Vocabulary", "difficulty": 0.25, "discrimination": 0.45,
        "tags": ["GRE vocab", "basic"],
        "question_text": "What does 'candid' mean?",
        "options": {"A": "Hidden", "B": "Frank and honest", "C": "Colorful", "D": "Slow"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },

    # ── ARITHMETIC ───────────────────────────────────────────
    {
        "question_id": "ARI001", "topic": "Arithmetic", "difficulty": 0.3, "discrimination": 0.5,
        "tags": ["percentages", "basic arithmetic"],
        "question_text": "What is 35% of 200?",
        "options": {"A": "35", "B": "70", "C": "65", "D": "57"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "ARI002", "topic": "Arithmetic", "difficulty": 0.45, "discrimination": 0.7,
        "tags": ["LCM", "number theory"],
        "question_text": "What is the LCM of 12 and 18?",
        "options": {"A": "6", "B": "36", "C": "24", "D": "72"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "ARI003", "topic": "Arithmetic", "difficulty": 0.6, "discrimination": 0.8,
        "tags": ["profit and loss", "percentages"],
        "question_text": "A shopkeeper buys an item for ₹400 and sells it for ₹500. What is the profit percentage?",
        "options": {"A": "20%", "B": "25%", "C": "15%", "D": "10%"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "ARI004", "topic": "Arithmetic", "difficulty": 0.75, "discrimination": 0.88,
        "tags": ["simple interest", "rate"],
        "question_text": "If a sum doubles in 8 years at simple interest, what is the annual rate?",
        "options": {"A": "10%", "B": "12.5%", "C": "15%", "D": "8%"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "ARI005", "topic": "Arithmetic", "difficulty": 0.2, "discrimination": 0.4,
        "tags": ["basic arithmetic", "division"],
        "question_text": "What is the HCF of 24 and 36?",
        "options": {"A": "6", "B": "12", "C": "18", "D": "9"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "ARI006", "topic": "Arithmetic", "difficulty": 0.5, "discrimination": 0.72,
        "tags": ["ratio", "proportion"],
        "question_text": "A:B = 3:4 and B:C = 2:5. What is A:C?",
        "options": {"A": "3:10", "B": "6:20", "C": "3:5", "D": "6:10"},
        "correct_answer": "A", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "ARI007", "topic": "Arithmetic", "difficulty": 0.65, "discrimination": 0.82,
        "tags": ["compound interest", "exponential growth"],
        "question_text": "What is the compound interest on ₹1000 at 10% per annum for 2 years?",
        "options": {"A": "₹200", "B": "₹210", "C": "₹220", "D": "₹190"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "ARI008", "topic": "Arithmetic", "difficulty": 0.85, "discrimination": 0.93,
        "tags": ["speed distance time", "relative speed"],
        "question_text": "Two trains 150m and 100m long travel at 60 km/h and 40 km/h towards each other. How long to cross?",
        "options": {"A": "9 sec", "B": "10 sec", "C": "12 sec", "D": "8 sec"},
        "correct_answer": "A", "created_at": datetime.now(timezone.utc)
    },

    # ── DATA ANALYSIS ─────────────────────────────────────────
    {
        "question_id": "DAT001", "topic": "Data Analysis", "difficulty": 0.25, "discrimination": 0.45,
        "tags": ["mean", "descriptive statistics"],
        "question_text": "What is the mean of 4, 8, 6, 10, 12?",
        "options": {"A": "6", "B": "8", "C": "10", "D": "7"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "DAT002", "topic": "Data Analysis", "difficulty": 0.4, "discrimination": 0.65,
        "tags": ["median", "descriptive statistics"],
        "question_text": "What is the median of: 3, 7, 2, 9, 5?",
        "options": {"A": "7", "B": "5", "C": "3", "D": "9"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "DAT003", "topic": "Data Analysis", "difficulty": 0.55, "discrimination": 0.75,
        "tags": ["pie chart", "proportions"],
        "question_text": "A pie chart shows 25% for category A. In a dataset of 200, how many items are in category A?",
        "options": {"A": "25", "B": "50", "C": "75", "D": "40"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "DAT004", "topic": "Data Analysis", "difficulty": 0.7, "discrimination": 0.85,
        "tags": ["standard deviation", "variance"],
        "question_text": "The standard deviation of a dataset is 0. What does this imply?",
        "options": {"A": "All values are zero", "B": "All values are identical", "C": "The mean is zero", "D": "The dataset is empty"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "DAT005", "topic": "Data Analysis", "difficulty": 0.8, "discrimination": 0.92,
        "tags": ["skewness", "distribution"],
        "question_text": "In a positively skewed distribution, which measure is typically largest?",
        "options": {"A": "Mean", "B": "Median", "C": "Mode", "D": "Range"},
        "correct_answer": "A", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "DAT006", "topic": "Data Analysis", "difficulty": 0.35, "discrimination": 0.58,
        "tags": ["mode", "descriptive statistics"],
        "question_text": "What is the mode of: 2, 4, 4, 5, 7, 7, 7, 9?",
        "options": {"A": "4", "B": "7", "C": "5", "D": "9"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "DAT007", "topic": "Data Analysis", "difficulty": 0.6, "discrimination": 0.78,
        "tags": ["probability", "basic"],
        "question_text": "A bag has 3 red and 7 blue balls. What is the probability of picking a red ball?",
        "options": {"A": "0.7", "B": "0.3", "C": "0.5", "D": "0.4"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "DAT008", "topic": "Data Analysis", "difficulty": 0.75, "discrimination": 0.88,
        "tags": ["correlation", "regression"],
        "question_text": "A correlation coefficient of -0.95 indicates:",
        "options": {"A": "Weak positive relationship", "B": "Strong negative relationship", "C": "No relationship", "D": "Moderate positive relationship"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "DAT009", "topic": "Data Analysis", "difficulty": 0.9, "discrimination": 0.95,
        "tags": ["probability", "conditional"],
        "question_text": "P(A) = 0.4, P(B) = 0.5, P(A∩B) = 0.2. What is P(A|B)?",
        "options": {"A": "0.5", "B": "0.4", "C": "0.8", "D": "0.2"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },

    # ── LOGICAL REASONING ────────────────────────────────────
    {
        "question_id": "LOG001", "topic": "Logical Reasoning", "difficulty": 0.35, "discrimination": 0.6,
        "tags": ["syllogisms", "deductive reasoning"],
        "question_text": "All cats are animals. Some animals are wild. Which conclusion is valid?",
        "options": {"A": "All cats are wild", "B": "Some cats may be wild", "C": "No cats are wild", "D": "All animals are cats"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "LOG002", "topic": "Logical Reasoning", "difficulty": 0.65, "discrimination": 0.85,
        "tags": ["propositional logic", "transitivity"],
        "question_text": "If P → Q and Q → R, which must be true?",
        "options": {"A": "R → P", "B": "P → R", "C": "Q → P", "D": "R → Q"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "LOG003", "topic": "Logical Reasoning", "difficulty": 0.25, "discrimination": 0.45,
        "tags": ["patterns", "sequences"],
        "question_text": "What comes next in the sequence: 2, 4, 8, 16, __?",
        "options": {"A": "24", "B": "32", "C": "28", "D": "20"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "LOG004", "topic": "Logical Reasoning", "difficulty": 0.5, "discrimination": 0.72,
        "tags": ["deductive reasoning", "statements"],
        "question_text": "No politicians are honest. Ram is honest. Therefore:",
        "options": {"A": "Ram is a politician", "B": "Ram is not a politician", "C": "Some politicians are honest", "D": "Ram may be a politician"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "LOG005", "topic": "Logical Reasoning", "difficulty": 0.75, "discrimination": 0.88,
        "tags": ["critical reasoning", "assumptions"],
        "question_text": "All A are B. Some B are C. Which is definitely true?",
        "options": {"A": "All A are C", "B": "Some A are C", "C": "No A are C", "D": "None of the above"},
        "correct_answer": "D", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "LOG006", "topic": "Logical Reasoning", "difficulty": 0.4, "discrimination": 0.65,
        "tags": ["analogies", "word relationships"],
        "question_text": "Doctor : Hospital :: Teacher : ?",
        "options": {"A": "Book", "B": "School", "C": "Student", "D": "Lesson"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
    {
        "question_id": "LOG007", "topic": "Logical Reasoning", "difficulty": 0.85, "discrimination": 0.93,
        "tags": ["propositional logic", "negation", "contrapositive"],
        "question_text": "The contrapositive of 'If it rains, the ground is wet' is:",
        "options": {"A": "If it doesn't rain, the ground is not wet", "B": "If the ground is not wet, it didn't rain", "C": "If the ground is wet, it rained", "D": "It rains if and only if the ground is wet"},
        "correct_answer": "B", "created_at": datetime.now(timezone.utc)
    },
]

result = questions_col.insert_many(questions)
print(f"Inserted {len(result.inserted_ids)} questions.")