import json

detailed_slides = [
    "### Slide 1: Expanding Quadratics\n\n*   **The FOIL Method:** When expanding two binomials like (x + a)(x + b), use the FOIL method: First, Outer, Inner, Last. Multiply the First terms, then the Outer terms, then the Inner terms, and finally the Last terms.\n*   **Collecting Like Terms:** After multiplying out the brackets, you will usually have two terms involving 'x' (the Outer and Inner products). Always collect and add these together to simplify the expression into the standard ax² + bx + c format.\n*   **Perfect Squares:** For expressions like (x + a)², remember that it means (x + a)(x + a). Do not just square the x and square the a; you must expand the full double brackets to avoid missing the middle term.\n*   **Difference of Two Squares:** Be on the lookout for patterns like (x + a)(x - a). When expanded, the middle terms cancel out (+ax and -ax), leaving just x² - a². This is a highly examinable shortcut.",
    "### Slide 2: Factorising Simple Quadratics (a = 1)\n\n*   **The Goal of Factorisation:** Factorising is the reverse process of expanding. You are trying to put an expression of the form x² + bx + c back into double brackets: (x + p)(x + q).\n*   **Finding the Numbers:** To find the values of p and q, you need two numbers that multiply together to give the constant term (c) and add together to give the coefficient of x (b).\n*   **Sign Rules:** Pay close attention to the signs. If c is positive, both numbers have the same sign (either both positive or both negative). If c is negative, the numbers must have different signs (one positive, one negative).\n*   **Checking Your Work:** You can always check if you have factorised correctly by expanding your double brackets using the FOIL method and ensuring you get back to the original expression.",
    "### Slide 3: Solving by Factorisation\n\n*   **Setting to Zero:** To solve a quadratic equation, it must first be set equal to zero. If you are given an equation like x² + 5x = 6, you must rearrange it to x² + 5x - 6 = 0 before attempting to solve.\n*   **The Zero Product Property:** Once factorised into the form (x + p)(x + q) = 0, we use a fundamental rule of math: if two things multiply to make zero, at least one of them must be zero.\n*   **Finding the Solutions:** Set each bracket equal to zero individually. If (x + p)(x + q) = 0, then either x + p = 0 or x + q = 0.\n*   **Interpreting the Answers:** These solutions represent the 'roots' of the quadratic equation. Graphically, these are the x-intercepts, or the points where the parabola crosses the x-axis on a graph.",
    "### Slide 4: Using the Quadratic Formula\n\n*   **When to use it:** The quadratic formula is used when a quadratic equation ax² + bx + c = 0 cannot be easily factorised. The exam question will often give a clue by asking for the answer to \"2 decimal places\" or \"3 significant figures\".\n*   **The Formula:** You must memorize the formula: x = [-b ± √(b² - 4ac)] / 2a. Ensure that the division line goes under the entire numerator, not just the square root.\n*   **The Discriminant (b² - 4ac):** The value under the square root is called the discriminant. If it is positive, there are two distinct real solutions. If it is exactly zero, there is one repeated real solution. If it is negative, there are no real solutions.\n*   **Common Mistakes:** Be extremely careful with negative numbers, especially when substituting a negative 'b' into the '-b' part of the formula, or when squaring a negative number for 'b²' (it should always become positive)."
]

quiz_bank = [
    {
        "question": "What is the result of expanding the brackets (x + 3)(x + 5)?",
        "options": ["x² + 15", "x² + 8x + 15", "x² + 15x + 8", "2x + 8"],
        "answer_index": 1,
        "explanation": "Using FOIL: x*x (x²) + 5*x (5x) + 3*x (3x) + 3*5 (15). Collecting the like terms 5x + 3x gives x² + 8x + 15."
    },
    {
        "question": "Which of the following is the correct expansion of the perfect square (x - 4)²?",
        "options": ["x² - 16", "x² + 16", "x² - 8x + 16", "x² - 4x + 16"],
        "answer_index": 2,
        "explanation": "(x - 4)(x - 4) expands to x² - 4x - 4x + 16. Collecting like terms yields x² - 8x + 16."
    },
    {
        "question": "Expand and simplify the expression: (2x + 1)(x - 3)",
        "options": ["2x² - 6x - 3", "2x² - 5x - 3", "2x² - 7x - 3", "3x - 2"],
        "answer_index": 1,
        "explanation": "FOIL gives: 2x² - 6x + 1x - 3. This simplifies to 2x² - 5x - 3."
    },
    {
        "question": "What is the factorised form of x² + 7x + 10?",
        "options": ["(x + 5)(x + 2)", "(x + 10)(x + 1)", "(x - 5)(x - 2)", "(x + 7)(x + 3)"],
        "answer_index": 0,
        "explanation": "We need two numbers that multiply to 10 and add to 7. These numbers are 5 and 2. Thus, (x + 5)(x + 2)."
    },
    {
        "question": "Factorise the quadratic expression: x² - 2x - 15",
        "options": ["(x - 5)(x + 3)", "(x + 5)(x - 3)", "(x - 15)(x + 1)", "(x - 3)(x - 5)"],
        "answer_index": 0,
        "explanation": "We need numbers that multiply to -15 and add to -2. The numbers are -5 and +3."
    },
    {
        "question": "Which expression represents the difference of two squares for x² - 49?",
        "options": ["(x - 7)²", "(x + 7)(x - 7)", "(x - 49)(x + 1)", "(x - 7)(x - 7)"],
        "answer_index": 1,
        "explanation": "A difference of two squares takes the form a² - b² = (a+b)(a-b). Here, b is 7, so it's (x + 7)(x - 7)."
    },
    {
        "question": "What are the solutions to the equation (x - 8)(x + 4) = 0?",
        "options": ["x = 8, x = 4", "x = -8, x = -4", "x = 8, x = -4", "x = -8, x = 4"],
        "answer_index": 2,
        "explanation": "By the zero product property, set each bracket to zero: x - 8 = 0 -> x = 8, and x + 4 = 0 -> x = -4."
    },
    {
        "question": "Solve the equation x² - 9x + 20 = 0",
        "options": ["x = 5, x = 4", "x = -5, x = -4", "x = -10, x = 2", "x = 10, x = -2"],
        "answer_index": 0,
        "explanation": "Factorising gives (x - 5)(x - 4) = 0. Therefore, the solutions are x = 5 and x = 4."
    },
    {
        "question": "Before solving x² = 6x - 8, what is the correct first step?",
        "options": ["Divide everything by x", "Square root both sides", "Subtract x² from both sides", "Rearrange to x² - 6x + 8 = 0"],
        "answer_index": 3,
        "explanation": "A quadratic equation must be set to zero before solving by factorisation or using the formula."
    },
    {
        "question": "What is the correct quadratic formula for solving ax² + bx + c = 0?",
        "options": ["x = [-b ± √(b² + 4ac)] / 2a", "x = [-b ± √(b² - 4ac)] / 2a", "x = [b ± √(b² - 4ac)] / 2a", "x = [-b ± √(b² - 4ac)] / a"],
        "answer_index": 1,
        "explanation": "The standard quadratic formula is x = [-b ± √(b² - 4ac)] / 2a."
    },
    {
        "question": "If you are solving 2x² + 5x - 3 = 0 using the quadratic formula, what is the value of 'a'?",
        "options": ["2", "5", "-3", "0"],
        "answer_index": 0,
        "explanation": "In the standard form ax² + bx + c = 0, 'a' is the coefficient of x², which is 2."
    },
    {
        "question": "What does the discriminant (b² - 4ac) tell you about a quadratic equation if it equals -4?",
        "options": ["There are two positive solutions", "There is one repeated solution", "There are no real solutions", "There are two negative solutions"],
        "answer_index": 2,
        "explanation": "If the discriminant is negative (less than zero), you cannot take its square root in the real number system, meaning there are no real solutions."
    },
    {
        "question": "Solve x² - 25 = 0",
        "options": ["x = 5", "x = -5", "x = 5 or x = -5", "x = 25"],
        "answer_index": 2,
        "explanation": "Rearranging gives x² = 25. Taking the square root gives both the positive and negative roots: x = ±5."
    },
    {
        "question": "Factorise 3x² + 12x",
        "options": ["3x(x + 4)", "x(3x + 12)", "3(x² + 4x)", "(3x + 4)(x + 3)"],
        "answer_index": 0,
        "explanation": "Take out the highest common factor of both terms, which is 3x. This leaves x in the first term and 4 in the second: 3x(x + 4)."
    },
    {
        "question": "Which of the following equations has a repeated root (only one real solution)?",
        "options": ["x² - 4 = 0", "x² - 6x + 9 = 0", "x² + 5x + 6 = 0", "x² + 1 = 0"],
        "answer_index": 1,
        "explanation": "x² - 6x + 9 factorises to (x - 3)(x - 3) = 0, or (x - 3)² = 0. Because both brackets are identical, it yields only one unique solution: x = 3."
    }
]

def patch_quadratics():
    with open('curriculum_data/maths.json', 'r') as f:
        data = json.load(f)
    
    for topic in data.get('topics', []):
        if topic['id'] == 'math_algebra_quadratics':
            topic['detailed_slides'] = detailed_slides
            topic['quiz_bank'] = quiz_bank
            break
            
    with open('curriculum_data/maths.json', 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    patch_quadratics()
    print("Quadratics lesson upgraded successfully!")
