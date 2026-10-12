import json

maths_cats = {
    "Number": ["Fraction", "Percentage", "Interest", "Surds", "Indices", "Bounds", "Error"],
    "Algebra": ["Equation", "Inequalities", "Nth Term", "Line Graphs", "Inverse", "Quadratic", "Iteration", "Algebraic", "Sequence"],
    "Geometry and Measures": ["Pythagoras", "Circle", "Area", "Volume", "Transformations", "Vectors", "Sine", "Cosine", "Bearings", "Trigonometry"],
    "Probability": ["Probability", "Tree Diagrams", "Venn"],
    "Statistics": ["Mean", "Median", "Mode", "Range", "Scatter", "Histograms", "Correlation"],
    "Ratio and Proportion": ["Ratio", "Proportion"]
}

def get_maths_category(title):
    for cat, keywords in maths_cats.items():
        for kw in keywords:
            if kw.lower() in title.lower():
                return cat
    return "Number" # fallback

with open("curriculum_data/maths.json", "r") as f:
    data = json.load(f)

for t in data.get("topics", []):
    t["category"] = get_maths_category(t["title"])

with open("curriculum_data/maths.json", "w") as f:
    json.dump(data, f, indent=2)

print("Maths explicitly fixed.")
