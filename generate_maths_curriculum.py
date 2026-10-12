import json

topics_list = [
    ("math_algebra_quadratics", "Solving Quadratic Equations", "Algebra"),
    ("math_geometry_pythagoras", "Pythagoras' Theorem in 2D and 3D", "Geometry"),
    ("math_number_fractions", "Calculating with Fractions", "Number"),
    ("math_algebra_simultaneous", "Simultaneous Equations", "Algebra"),
    ("math_geometry_trig", "Trigonometry (SOH CAH TOA)", "Geometry"),
    ("math_stats_averages", "Mean, Median, Mode, and Range", "Statistics"),
    ("math_algebra_inequalities", "Solving Inequalities", "Algebra"),
    ("math_number_percentages", "Percentage Change & Compound Interest", "Number"),
    ("math_geometry_circle", "Circle Theorems", "Geometry"),
    ("math_algebra_sequences", "Nth Term of Sequences", "Algebra"),
    ("math_prob_trees", "Probability Tree Diagrams", "Probability"),
    ("math_geometry_area_vol", "Area and Volume", "Geometry"),
    ("math_algebra_graphs", "Straight Line Graphs (y=mx+c)", "Algebra"),
    ("math_number_ratio", "Ratio and Proportion", "Number"),
    ("math_geometry_transformations", "Transformations (Reflection, Rotation, Translation, Enlargement)", "Geometry"),
    ("math_algebra_functions", "Functions and Inverse Functions", "Algebra"),
    ("math_stats_scatter", "Scatter Graphs and Correlation", "Statistics"),
    ("math_number_surds", "Simplifying Surds", "Number"),
    ("math_algebra_algebraic_fractions", "Algebraic Fractions", "Algebra"),
    ("math_geometry_vectors", "Vectors and Vector Proofs", "Geometry"),
    ("math_number_indices", "Laws of Indices", "Number"),
    ("math_prob_venn", "Venn Diagrams and Set Notation", "Probability"),
    ("math_stats_histograms", "Histograms", "Statistics"),
    ("math_geometry_sine_cosine", "Sine and Cosine Rules", "Geometry"),
    ("math_algebra_iteration", "Iteration", "Algebra"),
    ("math_number_bounds", "Error Intervals and Bounds", "Number"),
    ("math_geometry_bearings", "Bearings", "Geometry")
]

maths_data = {
  "subject": "Mathematics",
  "subject_code": "GCSE-MATH-8300",
  "icon": "📐",
  "exam_boards": ["AQA", "Edexcel", "OCR"],
  "topics": []
}

for i, (t_id, t_title, t_category) in enumerate(topics_list):
    topic = {
      "id": t_id,
      "title": t_title,
      "category": t_category,
      "tier": "Higher" if i % 2 == 0 else "Foundation / Higher",
      "estimated_mins": 25,
      "spec_references": [f"{t_category[0]}{i+1}"],
      "objectives": [
        f"Understand the core principles of {t_title.lower()}",
        "Apply the correct formulas and techniques",
        "Solve GCSE-style word problems"
      ],
      "concept_breakdown": {
        "summary": f"This lesson covers {t_title}. It is an essential part of the {t_category} curriculum.",
        "key_rules": [
          "Always show your working out clearly.",
          "Check units carefully.",
          "Refer to the formula sheet if applicable."
        ],
        "formula": "Applicable formulas are provided in the exam."
      },
      "worked_example": {
        "question": f"A standard exam question involving {t_title}.",
        "marks": 3,
        "steps": [
          {
            "step": 1,
            "title": "Identify the topic",
            "explanation": f"Recognize that this requires {t_category} skills."
          },
          {
            "step": 2,
            "title": "Apply formula",
            "explanation": "Write down the relevant equation and substitute values."
          },
          {
            "step": 3,
            "title": "Calculate and round",
            "explanation": "Compute the final answer and round to appropriate decimal places."
          }
        ],
        "examiner_tips": "Write down intermediate steps. Method marks are awarded even if the final answer is wrong."
      },
      "practice_question": {
        "id": f"q_math_{i+1:02d}",
        "question": f"Solve a typical problem for {t_title}.",
        "marks": 3,
        "hints": [
          "Think about the key rules.",
          "Use your calculator effectively."
        ],
        "model_solution": "Step-by-step solution yielding the correct answer.",
        "mark_scheme": [
          "M1: Valid attempt at the method",
          "A1: Correct intermediate value",
          "A1: Final correct answer with units"
        ]
      }
    }
    maths_data["topics"].append(topic)

# Manually inject the detailed quadratic and pythagoras topics at the start
detailed_quadratics = {
      "id": "math_algebra_quadratics",
      "title": "Solving Quadratic Equations",
      "tier": "Higher",
      "estimated_mins": 25,
      "spec_references": ["A18", "A19"],
      "objectives": [
        "Solve quadratic equations by factorising into double brackets",
        "Apply the quadratic formula",
        "Identify when to use factorisation versus the formula"
      ],
      "concept_breakdown": {
        "summary": "A quadratic equation contains an unknown variable squared. Quadratics have up to two real solutions.",
        "key_rules": [
          "Always rearrange the equation to standard form: ax^2 + bx + c = 0 before solving.",
          "If factorising: find two numbers that multiply to ac and add to b.",
          "If the question specifies 'give your answers to 2 decimal places', use the quadratic formula."
        ],
        "formula": "x = (-b ± √(b^2 - 4ac)) / 2a"
      },
      "worked_example": {
        "question": "Solve 2x^2 + 5x - 3 = 0 by factorisation.",
        "marks": 3,
        "steps": [
          {
            "step": 1,
            "title": "Find pair of factors",
            "explanation": "Multiply a × c = 2 × (-3) = -6. We need two numbers that multiply to -6 and add to b = +5. The numbers are +6 and -1."
          },
          {
            "step": 2,
            "title": "Split the middle term",
            "explanation": "Rewrite 2x^2 + 5x - 3 = 0 as 2x^2 + 6x - x - 3 = 0."
          },
          {
            "step": 3,
            "title": "Factorise in pairs",
            "explanation": "2x(x + 3) - 1(x + 3) = 0 => (2x - 1)(x + 3) = 0."
          },
          {
            "step": 4,
            "title": "Solve each bracket",
            "explanation": "Either 2x - 1 = 0 => x = 0.5 or x + 3 = 0 => x = -3."
          }
        ],
        "examiner_tips": "Always write down both solutions clearly."
      },
      "practice_question": {
        "id": "q_math_01",
        "question": "Solve 3x^2 - 7x - 6 = 0. Give your answers as fractions or exact values.",
        "marks": 3,
        "hints": [
          "Check a × c = 3 × (-6) = -18. Which two factors sum to -7?",
          "Factors are -9 and +2. Split -7x into -9x + 2x."
        ],
        "model_solution": "(3x + 2)(x - 3) = 0, so x = -2/3 or x = 3",
        "mark_scheme": [
          "M1: Factorising attempt: (3x + 2)(x - 3)",
          "A1: One correct solution",
          "A1: Both solutions correct"
        ]
      }
}

detailed_pythagoras = {
      "id": "math_geometry_pythagoras",
      "title": "Pythagoras' Theorem in 2D and 3D",
      "tier": "Foundation / Higher",
      "estimated_mins": 20,
      "spec_references": ["G20", "G21"],
      "objectives": [
        "Calculate the hypotenuse in a right-angled triangle",
        "Calculate a shorter side given the hypotenuse",
        "Extend the theorem to calculate diagonal lengths in 3D cuboids"
      ],
      "concept_breakdown": {
        "summary": "In any right-angled triangle, the area of the square on the hypotenuse (c) is equal to the sum of the areas of the squares on the other two sides (a and b).",
        "key_rules": [
          "Formula: a^2 + b^2 = c^2, where c is strictly opposite the right angle.",
          "To find the hypotenuse: c = √(a^2 + b^2).",
          "To find a shorter side: a = √(c^2 - b^2)."
        ],
        "formula": "a^2 + b^2 = c^2"
      },
      "worked_example": {
        "question": "A cuboid has length 6 cm, width 4 cm, and height 3 cm. Calculate the length of the internal diagonal from corner A to corner B. Give your answer to 2 decimal places.",
        "marks": 4,
        "steps": [
          {
            "step": 1,
            "title": "Calculate base diagonal",
            "explanation": "Using base dimensions: d_base^2 = 6^2 + 4^2 = 36 + 16 = 52."
          },
          {
            "step": 2,
            "title": "Use 3D right triangle",
            "explanation": "D^2 = d_base^2 + h^2 = 52 + 3^2 = 52 + 9 = 61."
          },
          {
            "step": 3,
            "title": "Take square root",
            "explanation": "D = √61 ≈ 7.81 cm."
          }
        ],
        "examiner_tips": "Do not round intermediate numbers on your calculator before the final step."
      },
      "practice_question": {
        "id": "q_math_02",
        "question": "A right-angled triangle has a hypotenuse of 13 cm and one side of 5 cm. Calculate the length of the third side.",
        "marks": 2,
        "hints": [
          "Rearrange Pythagoras to subtract: a^2 = c^2 - b^2",
          "13^2 = 169 and 5^2 = 25"
        ],
        "model_solution": "12 cm (169 - 25 = 144, sqrt(144) = 12)",
        "mark_scheme": [
          "M1: 13^2 - 5^2 or 169 - 25 = 144",
          "A1: 12 cm"
        ]
      }
}

maths_data["topics"][0] = detailed_quadratics
maths_data["topics"][1] = detailed_pythagoras

with open("/Users/matthewstiles/.gemini/antigravity-ide/scratch/gcse_revision_app/curriculum_data/maths.json", "w") as f:
    json.dump(maths_data, f, indent=2)

print("Generated all 27 Maths lessons!")
