import os
import json

path = "curriculum_data/maths.json"
with open(path, "r") as f:
    data = json.load(f)

for t in data.get("topics", []):
    if t["id"] == "math_algebra_quadratics":
        t["detailed_slides"] = [
            "### Slide 1: What is a Quadratic Equation?\n\n- A quadratic equation takes the form **ax² + bx + c = 0**.\n- The highest power of the unknown variable (usually *x*) is a square (2).\n- Unlike linear equations, quadratics typically have **two** real solutions, though they can have one repeated solution or no real solutions.\n- Example: $2x^2 + 5x - 3 = 0$. Here, $a=2, b=5, c=-3$.",
            "### Slide 2: Solving by Factorisation\n\n- **Step 1:** Ensure the equation equals zero ($ax^2 + bx + c = 0$).\n- **Step 2:** Find two numbers that multiply to give $a \\times c$ and add to give $b$.\n- **Step 3:** Split the middle term ($bx$) using these two numbers.\n- **Step 4:** Factorise in pairs to get two brackets (e.g., $(2x-1)(x+3)=0$).\n- **Step 5:** Solve by setting each bracket to zero. Either $2x-1=0$ or $x+3=0$.",
            "### Slide 3: The Quadratic Formula\n\n- Use the formula when you cannot easily factorise, or when the question asks for answers to a specific number of decimal places or significant figures.\n- **Formula:** $x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}$\n- **The Discriminant ($b^2 - 4ac$):**\n  - If positive: Two distinct solutions.\n  - If zero: One repeated solution.\n  - If negative: No real solutions.",
            "### Slide 4: Common Examiner Traps\n\n- **Forgetting the $\\pm$ sign:** When taking a square root manually, remember there is a positive and negative root.\n- **Sign errors in the formula:** If $b$ is negative, $-b$ becomes positive. Be very careful computing $b^2$ when $b$ is negative; $(-3)^2$ is $+9$, not $-9$.\n- **Not rearranging first:** You *must* get all terms on one side equal to zero before identifying $a, b, c$ or factorising."
        ]
        
        t["quiz_bank"] = [
            {
                "question": "What is the standard form of a quadratic equation?",
                "options": ["y = mx + c", "ax^2 + bx + c = 0", "a/x + b = c", "x^3 + bx^2 + c = 0"],
                "answer_index": 1,
                "explanation": "A quadratic equation must have an x-squared term as its highest power and be set to zero to solve."
            },
            {
                "question": "Solve the equation: (x - 3)(x + 4) = 0",
                "options": ["x = 3, x = 4", "x = -3, x = 4", "x = 3, x = -4", "x = -3, x = -4"],
                "answer_index": 2,
                "explanation": "Set each bracket to zero: x - 3 = 0 means x = 3. x + 4 = 0 means x = -4."
            },
            {
                "question": "What is the value of the discriminant in the quadratic formula?",
                "options": ["b^2 - 4ac", "2a", "-b", "sqrt(b^2 - 4ac)"],
                "answer_index": 0,
                "explanation": "The discriminant is the part under the square root: b^2 - 4ac."
            },
            {
                "question": "If a quadratic equation factorises to x(x - 5) = 0, what are the solutions?",
                "options": ["x = 0, x = -5", "x = 0, x = 5", "x = 1, x = 5", "x = 5 only"],
                "answer_index": 1,
                "explanation": "Set x = 0 and x - 5 = 0. Therefore x = 0 and x = 5."
            },
            {
                "question": "Which of these is the correct quadratic formula?",
                "options": ["x = (-b ± sqrt(b^2 + 4ac)) / 2a", "x = (-b ± sqrt(b^2 - 4ac)) / 2a", "x = (b ± sqrt(b^2 - 4ac)) / a", "x = (-b ± sqrt(b - 4ac)) / 2a"],
                "answer_index": 1,
                "explanation": "The formula requires -b and b^2 - 4ac all divided by 2a."
            },
            {
                "question": "How many real solutions does a quadratic equation have if b^2 - 4ac < 0?",
                "options": ["0", "1", "2", "Infinite"],
                "answer_index": 0,
                "explanation": "You cannot take the square root of a negative number in real mathematics, so there are 0 real solutions."
            },
            {
                "question": "Factorise x^2 + 7x + 10.",
                "options": ["(x+2)(x+5)", "(x-2)(x-5)", "(x+1)(x+10)", "(x+3)(x+4)"],
                "answer_index": 0,
                "explanation": "We need two numbers that multiply to 10 and add to 7. 2 and 5 work."
            },
            {
                "question": "What are the values of a, b, and c in: 3x^2 - x + 4 = 0?",
                "options": ["a=3, b=1, c=4", "a=3, b=0, c=4", "a=3, b=-1, c=4", "a=3, b=-x, c=4"],
                "answer_index": 2,
                "explanation": "The coefficient of x is -1, so b = -1."
            },
            {
                "question": "Factorise x^2 - 9 (Difference of two squares).",
                "options": ["(x-3)(x-3)", "(x+3)(x+3)", "(x-9)(x+1)", "(x-3)(x+3)"],
                "answer_index": 3,
                "explanation": "Difference of two squares a^2 - b^2 factorises to (a-b)(a+b). Here, a=x, b=3."
            },
            {
                "question": "Solve x^2 = 16.",
                "options": ["x = 4 only", "x = -4 only", "x = 4 and x = -4", "x = 8"],
                "answer_index": 2,
                "explanation": "Taking the square root gives both a positive and negative answer: ±4."
            },
            {
                "question": "Solve 2x^2 = 50.",
                "options": ["x = 5", "x = ±5", "x = 25", "x = ±25"],
                "answer_index": 1,
                "explanation": "First divide by 2 to get x^2 = 25. Then square root to get x = ±5."
            },
            {
                "question": "What is the next step to solve (x+1)^2 = 9?",
                "options": ["Expand the brackets", "Square root both sides", "Subtract 9 from both sides", "Divide by 9"],
                "answer_index": 1,
                "explanation": "Square rooting both sides gives x + 1 = ±3, which is the fastest way to solve this."
            }
        ]
        break

with open(path, "w") as f:
    json.dump(data, f, indent=2)

print("Quadratics patched.")
