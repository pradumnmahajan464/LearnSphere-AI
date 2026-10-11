"""
Seed script — populates the database with sample educational content.
Run once: python seed.py (from backend/)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal, Base
from app.models.models import Subject, Topic, Quiz, Question

# ── Create all tables ─────────────────────────────────────────────────────────
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Skip if already seeded
if db.query(Subject).count() > 0:
    print("Database already seeded. Skipping.")
    db.close()
    sys.exit(0)

# ─────────────────────────────────────────────────────────────────────────────
# SUBJECTS + TOPICS
# ─────────────────────────────────────────────────────────────────────────────

subjects_data = [
    {
        "name": "Python Programming",
        "description": "Learn Python from basics to object-oriented programming.",
        "icon": "🐍",
        "topics": [
            {
                "title": "Introduction to Python",
                "difficulty": "Beginner",
                "notes": """Python is a high-level, interpreted programming language known for its simplicity and readability.

**Key Facts:**
- Created by Guido van Rossum in 1991.
- Uses indentation to define code blocks — no curly braces.
- Dynamically typed: you don't declare variable types.

**Hello World:**
```python
print("Hello, World!")
```

**Variables:**
```python
name = "Alice"
age = 21
gpa = 3.8
is_student = True
```

Python supports integers, floats, strings, booleans, lists, tuples, dictionaries, and sets as built-in types.""",
            },
            {
                "title": "Control Flow",
                "difficulty": "Beginner",
                "notes": """Control flow lets you make decisions and repeat actions in your code.

**If / Elif / Else:**
```python
score = 75
if score >= 90:
    print("A grade")
elif score >= 70:
    print("B grade")
else:
    print("Below B")
```

**For Loop:**
```python
for i in range(5):
    print(i)   # prints 0 1 2 3 4
```

**While Loop:**
```python
count = 0
while count < 3:
    print(count)
    count += 1
```

Use `break` to exit a loop early and `continue` to skip the current iteration.""",
            },
            {
                "title": "Functions and Modules",
                "difficulty": "Intermediate",
                "notes": """Functions let you reuse blocks of code with different inputs.

**Defining a Function:**
```python
def greet(name):
    return f"Hello, {name}!"

print(greet("Bob"))   # Hello, Bob!
```

**Default Arguments:**
```python
def power(base, exponent=2):
    return base ** exponent

print(power(3))    # 9
print(power(2, 3)) # 8
```

**Modules:**
Python's standard library provides many built-in modules.
```python
import math
print(math.sqrt(16))  # 4.0

import random
print(random.randint(1, 10))
```

You can also create your own modules by saving functions in a `.py` file and importing them.""",
            },
            {
                "title": "Lists and Dictionaries",
                "difficulty": "Beginner",
                "notes": """Lists and dictionaries are the two most important data structures in Python.

**Lists:**
```python
fruits = ["apple", "banana", "cherry"]
fruits.append("date")
print(fruits[0])   # apple
print(len(fruits)) # 4
```

**List Comprehension:**
```python
squares = [x**2 for x in range(6)]
# [0, 1, 4, 9, 16, 25]
```

**Dictionaries:**
```python
student = {"name": "Alice", "gpa": 3.9}
student["major"] = "CS"
print(student["name"])  # Alice
```

Dictionaries store key-value pairs and provide O(1) average-case lookups.""",
            },
        ],
    },
    {
        "name": "Machine Learning",
        "description": "Understand ML concepts, algorithms, and practical applications.",
        "icon": "🤖",
        "topics": [
            {
                "title": "What is Machine Learning?",
                "difficulty": "Beginner",
                "notes": """Machine Learning (ML) is a branch of Artificial Intelligence where computers learn from data without being explicitly programmed for every task.

**Three Main Types:**
1. **Supervised Learning** — the model learns from labelled examples (e.g., email spam detection).
2. **Unsupervised Learning** — the model finds patterns in unlabelled data (e.g., customer segmentation).
3. **Reinforcement Learning** — an agent learns by interacting with an environment and receiving rewards.

**The ML Pipeline:**
1. Collect and clean data.
2. Choose and train a model.
3. Evaluate performance on a test set.
4. Deploy and monitor.

Common applications: image recognition, recommendation systems, fraud detection, language translation.""",
            },
            {
                "title": "Linear Regression",
                "difficulty": "Beginner",
                "notes": """Linear Regression predicts a continuous numerical output from one or more input features.

**Equation:**
```
y = w₁x₁ + w₂x₂ + ... + b
```
where `w` values are weights (learned from data) and `b` is the bias term.

**Example with scikit-learn:**
```python
from sklearn.linear_model import LinearRegression
import numpy as np

X = np.array([[1], [2], [3], [4]])
y = np.array([2, 4, 6, 8])

model = LinearRegression()
model.fit(X, y)
print(model.predict([[5]]))  # [10.]
```

**Key Metric — R² Score:** Measures how well the line fits the data. R² = 1.0 is a perfect fit.""",
            },
            {
                "title": "Classification and Decision Trees",
                "difficulty": "Intermediate",
                "notes": """Classification assigns inputs to discrete categories (classes).

**Decision Trees** split data by asking questions about features:
```
Is petal length > 2.5 cm?
  Yes → Is petal width > 1.8 cm?
        Yes → Virginica
        No  → Versicolor
  No  → Setosa
```

**Example:**
```python
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_iris

X, y = load_iris(return_X_y=True)
clf = DecisionTreeClassifier(max_depth=3)
clf.fit(X, y)
print(clf.score(X, y))  # accuracy
```

**Overfitting:** A tree that is too deep memorises training data and generalises poorly. Limit depth with `max_depth`.""",
            },
            {
                "title": "Model Evaluation",
                "difficulty": "Intermediate",
                "notes": """Evaluating your model correctly prevents overoptimistic results.

**Train / Test Split:**
```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
```

**Key Classification Metrics:**
- **Accuracy** = correct predictions / total predictions
- **Precision** = TP / (TP + FP) — how many positives are truly positive
- **Recall** = TP / (TP + FN) — how many actual positives were caught
- **F1 Score** = harmonic mean of precision and recall

**Confusion Matrix:** A table showing TP, TN, FP, FN counts for each class.

Always evaluate on a held-out **test set** that was never used during training.""",
            },
        ],
    },
    {
        "name": "Data Structures",
        "description": "Master arrays, linked lists, trees, graphs, and algorithms.",
        "icon": "🌲",
        "topics": [
            {
                "title": "Arrays and Searching",
                "difficulty": "Beginner",
                "notes": """An **array** stores elements of the same type in contiguous memory locations, accessible by index in O(1) time.

**Python list (dynamic array):**
```python
arr = [10, 20, 30, 40, 50]
print(arr[2])   # 30  — O(1) access
arr.append(60)  # O(1) amortised
```

**Linear Search — O(n):**
```python
def linear_search(arr, target):
    for i, val in enumerate(arr):
        if val == target:
            return i
    return -1
```

**Binary Search — O(log n) on sorted arrays:**
```python
def binary_search(arr, target):
    lo, hi = 0, len(arr) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if arr[mid] == target: return mid
        elif arr[mid] < target: lo = mid + 1
        else: hi = mid - 1
    return -1
```""",
            },
            {
                "title": "Stacks and Queues",
                "difficulty": "Beginner",
                "notes": """**Stack — Last In, First Out (LIFO):**
Imagine a stack of plates — you always add/remove from the top.

```python
stack = []
stack.append(1)  # push
stack.append(2)
top = stack.pop()  # 2 — O(1)
```

Use cases: undo/redo, function call stack, expression evaluation.

**Queue — First In, First Out (FIFO):**
```python
from collections import deque
queue = deque()
queue.append("A")  # enqueue
queue.append("B")
first = queue.popleft()  # "A" — O(1)
```

Use cases: BFS traversal, task scheduling, print spooler.

Both stacks and queues support push/pop (or enqueue/dequeue) in **O(1)** time with the right implementation.""",
            },
            {
                "title": "Linked Lists",
                "difficulty": "Intermediate",
                "notes": """A **Linked List** is a sequence of nodes where each node stores a value and a pointer to the next node.

```
[10 | →] → [20 | →] → [30 | None]
 head
```

**Node class:**
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
```

**Advantages over arrays:**
- O(1) insertion/deletion at the head.
- No need to pre-allocate size.

**Disadvantages:**
- O(n) access by index (no random access).
- Extra memory for pointers.

Types: Singly linked, Doubly linked (has `.prev` pointer), Circular linked.""",
            },
            {
                "title": "Trees and Binary Search Trees",
                "difficulty": "Advanced",
                "notes": """A **tree** is a hierarchical data structure with a root node and children.

**Binary Tree:** each node has at most 2 children (left, right).

**Binary Search Tree (BST):** for every node:
- All values in the left subtree are **smaller**.
- All values in the right subtree are **larger**.

```
       8
      / \\
     3   10
    / \\    \\
   1   6    14
```

**BST Operations (average O(log n), worst O(n)):**
```python
class BST:
    def insert(self, root, val):
        if root is None: return Node(val)
        if val < root.data: root.left = self.insert(root.left, val)
        else: root.right = self.insert(root.right, val)
        return root
```

**Traversals:** In-order (sorted), Pre-order, Post-order.""",
            },
        ],
    },
    {
        "name": "Mathematics",
        "description": "Explore algebra, calculus, statistics, and discrete math.",
        "icon": "📐",
        "topics": [
            {
                "title": "Algebra Fundamentals",
                "difficulty": "Beginner",
                "notes": """Algebra uses symbols (variables) to represent numbers and express relationships.

**Solving Linear Equations:**
```
2x + 5 = 13
2x = 8
x = 4
```

**Quadratic Formula:**
For ax² + bx + c = 0:
```
x = (-b ± √(b² - 4ac)) / 2a
```
The **discriminant** (b² - 4ac) tells you:
- > 0 → two real roots
- = 0 → one real root (repeated)
- < 0 → no real roots (complex)

**Systems of Equations:**
Use substitution or elimination to solve two equations with two unknowns simultaneously.""",
            },
            {
                "title": "Probability and Statistics",
                "difficulty": "Beginner",
                "notes": """Statistics summarises data; probability quantifies uncertainty.

**Measures of Central Tendency:**
- **Mean** = sum of values / count
- **Median** = middle value when sorted
- **Mode** = most frequent value

**Spread:**
- **Variance** σ² = average of squared differences from the mean
- **Standard Deviation** σ = √variance

**Probability:**
- P(event) = favourable outcomes / total outcomes
- P(A ∪ B) = P(A) + P(B) − P(A ∩ B)
- **Conditional probability:** P(A|B) = P(A ∩ B) / P(B)

**Normal Distribution:** Bell-shaped curve; 68% of data within 1σ, 95% within 2σ, 99.7% within 3σ.""",
            },
            {
                "title": "Calculus — Derivatives",
                "difficulty": "Intermediate",
                "notes": """A **derivative** measures how fast a function changes at a given point — the slope of the tangent line.

**Notation:** f'(x) or dy/dx

**Basic Rules:**
| Function | Derivative |
|----------|------------|
| xⁿ       | n·xⁿ⁻¹    |
| eˣ       | eˣ         |
| ln x     | 1/x        |
| sin x    | cos x      |
| cos x    | −sin x     |

**Chain Rule:**
If y = f(g(x)), then dy/dx = f'(g(x)) · g'(x)

**Example:**
d/dx [x³ + 2x] = 3x² + 2

**Applications:** Finding maxima/minima of functions, gradient descent in ML, optimisation problems.""",
            },
            {
                "title": "Discrete Mathematics",
                "difficulty": "Intermediate",
                "notes": """Discrete math deals with countable, distinct structures — essential for computer science.

**Logic Gates:**
- AND: T ∧ T = T; otherwise F
- OR: F ∨ F = F; otherwise T
- NOT: ¬T = F, ¬F = T

**Set Theory:**
- Union: A ∪ B — all elements in A or B
- Intersection: A ∩ B — elements in both
- Difference: A − B — elements in A but not B

**Graph Theory Basics:**
A graph G = (V, E) has vertices V and edges E.
- **Degree** of a vertex = number of edges connected to it.
- **Path** = sequence of vertices connected by edges.
- **Cycle** = path that starts and ends at the same vertex.

**Counting (Combinatorics):**
- Permutations: P(n,r) = n! / (n-r)!
- Combinations: C(n,r) = n! / (r! · (n-r)!)""",
            },
        ],
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# QUIZZES + QUESTIONS
# ─────────────────────────────────────────────────────────────────────────────

quizzes_data = {
    "Python Programming": [
        {
            "title": "Python Basics Quiz",
            "questions": [
                {
                    "question_text": "Which keyword is used to define a function in Python?",
                    "options": ["func", "def", "function", "define"],
                    "correct_answer": 1,
                    "explanation": "'def' is the keyword used to define a function in Python. Example: def my_function(): ..."
                },
                {
                    "question_text": "What is the output of: print(type(3.14))?",
                    "options": ["<class 'int'>", "<class 'str'>", "<class 'float'>", "<class 'number'>"],
                    "correct_answer": 2,
                    "explanation": "3.14 is a floating-point literal, so type(3.14) returns <class 'float'>."
                },
                {
                    "question_text": "Which of the following is used to add an item to the end of a list?",
                    "options": ["add()", "insert()", "append()", "push()"],
                    "correct_answer": 2,
                    "explanation": "list.append(item) adds an item to the end of the list in O(1) amortised time."
                },
                {
                    "question_text": "What does the 'range(3)' function produce?",
                    "options": ["[1, 2, 3]", "[0, 1, 2]", "[0, 1, 2, 3]", "[1, 2]"],
                    "correct_answer": 1,
                    "explanation": "range(3) produces values 0, 1, 2 — it starts at 0 and stops before 3."
                },
                {
                    "question_text": "How do you create a dictionary in Python?",
                    "options": ["[key: value]", "(key, value)", "{key: value}", "<key: value>"],
                    "correct_answer": 2,
                    "explanation": "Dictionaries use curly braces with key-value pairs: {'name': 'Alice', 'age': 21}."
                },
            ],
        },
        {
            "title": "Python Functions Quiz",
            "questions": [
                {
                    "question_text": "What keyword returns a value from a function?",
                    "options": ["send", "output", "return", "yield_value"],
                    "correct_answer": 2,
                    "explanation": "The 'return' statement exits a function and optionally passes back a value to the caller."
                },
                {
                    "question_text": "Which built-in function gives the length of a list?",
                    "options": ["size()", "count()", "length()", "len()"],
                    "correct_answer": 3,
                    "explanation": "len(obj) returns the number of items in a sequence or collection."
                },
                {
                    "question_text": "What is a lambda function?",
                    "options": [
                        "A function imported from a library",
                        "An anonymous single-expression function",
                        "A recursive function",
                        "A function that returns None"
                    ],
                    "correct_answer": 1,
                    "explanation": "Lambda functions are anonymous functions defined with the 'lambda' keyword: lambda x: x*2."
                },
                {
                    "question_text": "What does *args allow in a function?",
                    "options": [
                        "Keyword arguments only",
                        "Exactly two arguments",
                        "Any number of positional arguments",
                        "No arguments"
                    ],
                    "correct_answer": 2,
                    "explanation": "*args collects extra positional arguments into a tuple, allowing flexible argument counts."
                },
                {
                    "question_text": "Which module provides math functions like sqrt()?",
                    "options": ["numpy", "math", "calc", "numbers"],
                    "correct_answer": 1,
                    "explanation": "Python's built-in 'math' module provides sqrt(), floor(), ceil(), pi, and more."
                },
            ],
        },
    ],
    "Machine Learning": [
        {
            "title": "ML Fundamentals Quiz",
            "questions": [
                {
                    "question_text": "Which type of ML uses labelled training data?",
                    "options": ["Unsupervised", "Reinforcement", "Supervised", "Transfer"],
                    "correct_answer": 2,
                    "explanation": "Supervised learning trains on labelled examples — each input has a corresponding correct output."
                },
                {
                    "question_text": "What does overfitting mean in machine learning?",
                    "options": [
                        "The model is too simple",
                        "The model memorises training data but fails on new data",
                        "The model has too few parameters",
                        "The training data is too large"
                    ],
                    "correct_answer": 1,
                    "explanation": "Overfitting occurs when a model learns the training data too well, including noise, and cannot generalise."
                },
                {
                    "question_text": "What is the purpose of a test set?",
                    "options": [
                        "To train the model",
                        "To tune hyperparameters",
                        "To evaluate the model on unseen data",
                        "To preprocess features"
                    ],
                    "correct_answer": 2,
                    "explanation": "The test set simulates real-world performance — it must never be seen during training or hyperparameter tuning."
                },
                {
                    "question_text": "Which metric measures classification correctness as a fraction?",
                    "options": ["RMSE", "R² Score", "Accuracy", "Entropy"],
                    "correct_answer": 2,
                    "explanation": "Accuracy = correct predictions / total predictions. It's the most intuitive classification metric."
                },
                {
                    "question_text": "Linear Regression predicts which type of output?",
                    "options": ["A category", "A continuous number", "A probability only", "A boolean"],
                    "correct_answer": 1,
                    "explanation": "Linear regression outputs a continuous numerical value (e.g., house price, temperature)."
                },
            ],
        },
        {
            "title": "ML Algorithms Quiz",
            "questions": [
                {
                    "question_text": "What does a Decision Tree split on at each node?",
                    "options": [
                        "A random threshold",
                        "A feature that best separates the classes",
                        "The mean of all features",
                        "The last feature in the dataset"
                    ],
                    "correct_answer": 1,
                    "explanation": "Decision trees choose the feature and threshold that best separates classes (e.g., maximising information gain)."
                },
                {
                    "question_text": "What is the k-Nearest Neighbours (kNN) algorithm based on?",
                    "options": [
                        "Mathematical equations",
                        "Tree structures",
                        "Similarity to nearby training examples",
                        "Gradient descent"
                    ],
                    "correct_answer": 2,
                    "explanation": "kNN classifies a point based on the majority class of its k closest neighbours in the feature space."
                },
                {
                    "question_text": "Which Python library is most commonly used for classical ML?",
                    "options": ["TensorFlow", "PyTorch", "scikit-learn", "Keras"],
                    "correct_answer": 2,
                    "explanation": "scikit-learn provides a consistent API for classical ML algorithms, preprocessing, and evaluation."
                },
                {
                    "question_text": "What does train_test_split do in scikit-learn?",
                    "options": [
                        "Normalises the data",
                        "Trains the model automatically",
                        "Divides data into training and testing subsets",
                        "Removes missing values"
                    ],
                    "correct_answer": 2,
                    "explanation": "train_test_split randomly divides the dataset into training and testing portions (e.g., 80/20 split)."
                },
                {
                    "question_text": "What is the F1 score?",
                    "options": [
                        "The arithmetic mean of precision and recall",
                        "The harmonic mean of precision and recall",
                        "Accuracy minus error rate",
                        "The area under the ROC curve"
                    ],
                    "correct_answer": 1,
                    "explanation": "F1 = 2 · (Precision · Recall) / (Precision + Recall). It balances both metrics, useful for imbalanced classes."
                },
            ],
        },
    ],
    "Data Structures": [
        {
            "title": "Arrays and Basic DS Quiz",
            "questions": [
                {
                    "question_text": "What is the time complexity of accessing an array element by index?",
                    "options": ["O(n)", "O(log n)", "O(1)", "O(n²)"],
                    "correct_answer": 2,
                    "explanation": "Arrays store elements contiguously in memory, so index-based access is O(1) — a direct memory calculation."
                },
                {
                    "question_text": "Which data structure follows LIFO (Last In, First Out)?",
                    "options": ["Queue", "Stack", "Linked List", "Graph"],
                    "correct_answer": 1,
                    "explanation": "A stack is a LIFO structure — the last element pushed is the first one popped. Like a stack of plates."
                },
                {
                    "question_text": "What is the time complexity of binary search?",
                    "options": ["O(n)", "O(n log n)", "O(1)", "O(log n)"],
                    "correct_answer": 3,
                    "explanation": "Binary search halves the search space each step, giving O(log n) comparisons on a sorted array."
                },
                {
                    "question_text": "Which data structure is best for implementing a printer queue?",
                    "options": ["Stack", "Queue", "Tree", "Hash Table"],
                    "correct_answer": 1,
                    "explanation": "A queue (FIFO) is perfect for a printer — documents are printed in the order they were submitted."
                },
                {
                    "question_text": "In a singly linked list, each node contains:",
                    "options": [
                        "Only a value",
                        "A value and a pointer to the next node",
                        "A value and pointers to both next and previous nodes",
                        "An index and a value"
                    ],
                    "correct_answer": 1,
                    "explanation": "A singly linked list node stores data and one next pointer. Doubly linked lists have both next and prev."
                },
            ],
        },
        {
            "title": "Trees and Algorithms Quiz",
            "questions": [
                {
                    "question_text": "In a Binary Search Tree, where are smaller values stored?",
                    "options": ["Right subtree", "Left subtree", "Root only", "Random position"],
                    "correct_answer": 1,
                    "explanation": "BST property: values smaller than the root go in the left subtree; larger values go in the right subtree."
                },
                {
                    "question_text": "What traversal of a BST gives elements in sorted order?",
                    "options": ["Pre-order", "Post-order", "In-order", "Level-order"],
                    "correct_answer": 2,
                    "explanation": "In-order traversal (left → root → right) of a BST visits nodes in ascending sorted order."
                },
                {
                    "question_text": "What is the height of a balanced binary tree with n nodes?",
                    "options": ["O(n)", "O(n²)", "O(log n)", "O(1)"],
                    "correct_answer": 2,
                    "explanation": "A balanced binary tree has height O(log n), making search, insert, and delete O(log n) operations."
                },
                {
                    "question_text": "Which algorithm uses a queue for graph traversal?",
                    "options": ["DFS (Depth-First Search)", "BFS (Breadth-First Search)", "Dijkstra's Algorithm", "Binary Search"],
                    "correct_answer": 1,
                    "explanation": "BFS uses a queue to explore nodes level by level — all neighbours first, then their neighbours."
                },
                {
                    "question_text": "What is a leaf node in a tree?",
                    "options": [
                        "The root node",
                        "Any node with two children",
                        "A node with no children",
                        "A node with only a left child"
                    ],
                    "correct_answer": 2,
                    "explanation": "A leaf node has no children — it is at the bottom of the tree with no further branches."
                },
            ],
        },
    ],
    "Mathematics": [
        {
            "title": "Algebra and Statistics Quiz",
            "questions": [
                {
                    "question_text": "If 3x + 6 = 21, what is x?",
                    "options": ["3", "5", "7", "9"],
                    "correct_answer": 1,
                    "explanation": "3x + 6 = 21 → 3x = 15 → x = 5."
                },
                {
                    "question_text": "What is the mean of [2, 4, 4, 4, 5, 5, 7, 9]?",
                    "options": ["4", "5", "5.5", "4.5"],
                    "correct_answer": 1,
                    "explanation": "Sum = 40, count = 8, mean = 40/8 = 5."
                },
                {
                    "question_text": "What does the discriminant b² - 4ac determine in a quadratic?",
                    "options": [
                        "The vertex of the parabola",
                        "The y-intercept",
                        "The number and type of roots",
                        "The axis of symmetry"
                    ],
                    "correct_answer": 2,
                    "explanation": "Discriminant > 0: two real roots; = 0: one real root; < 0: no real roots (complex)."
                },
                {
                    "question_text": "What is the probability of rolling a 6 on a fair die?",
                    "options": ["1/3", "1/4", "1/6", "1/2"],
                    "correct_answer": 2,
                    "explanation": "A fair die has 6 equally likely outcomes. Only one is a 6, so P(6) = 1/6."
                },
                {
                    "question_text": "What percentage of data falls within 2 standard deviations of the mean in a normal distribution?",
                    "options": ["68%", "95%", "99.7%", "50%"],
                    "correct_answer": 1,
                    "explanation": "The empirical rule: ~68% within 1σ, ~95% within 2σ, ~99.7% within 3σ."
                },
            ],
        },
        {
            "title": "Calculus and Discrete Math Quiz",
            "questions": [
                {
                    "question_text": "What is the derivative of x³?",
                    "options": ["x²", "3x²", "3x³", "x⁴/4"],
                    "correct_answer": 1,
                    "explanation": "Power rule: d/dx[xⁿ] = n·xⁿ⁻¹. So d/dx[x³] = 3x²."
                },
                {
                    "question_text": "What is the derivative of sin(x)?",
                    "options": ["-cos(x)", "tan(x)", "cos(x)", "-sin(x)"],
                    "correct_answer": 2,
                    "explanation": "d/dx[sin(x)] = cos(x). This is a fundamental trigonometric derivative."
                },
                {
                    "question_text": "How many ways can you choose 2 items from 5 (order doesn't matter)?",
                    "options": ["20", "10", "15", "5"],
                    "correct_answer": 1,
                    "explanation": "C(5,2) = 5! / (2! · 3!) = 120 / 12 = 10 combinations."
                },
                {
                    "question_text": "In logic, what is the result of T AND F?",
                    "options": ["True", "False", "Undefined", "True only if T > F"],
                    "correct_answer": 1,
                    "explanation": "AND (conjunction) is True only when BOTH operands are True. T AND F = False."
                },
                {
                    "question_text": "What is the degree of a vertex in a graph?",
                    "options": [
                        "Its position in a sorted list",
                        "The number of edges connected to it",
                        "Its distance from the root",
                        "The number of vertices in its subtree"
                    ],
                    "correct_answer": 1,
                    "explanation": "The degree of a vertex is the count of edges incident to it. In directed graphs, we distinguish in-degree and out-degree."
                },
            ],
        },
    ],
}

# ─────────────────────────────────────────────────────────────────────────────
# INSERT INTO DATABASE
# ─────────────────────────────────────────────────────────────────────────────

for s_data in subjects_data:
    subject = Subject(
        name=s_data["name"],
        description=s_data["description"],
        icon=s_data["icon"],
    )
    db.add(subject)
    db.flush()  # get subject.id

    for order, t_data in enumerate(s_data["topics"]):
        topic = Topic(
            subject_id=subject.id,
            title=t_data["title"],
            notes=t_data["notes"],
            difficulty=t_data["difficulty"],
            order_index=order,
        )
        db.add(topic)

    for q_data in quizzes_data.get(s_data["name"], []):
        quiz = Quiz(subject_id=subject.id, title=q_data["title"])
        db.add(quiz)
        db.flush()

        for question_data in q_data["questions"]:
            question = Question(
                quiz_id=quiz.id,
                question_text=question_data["question_text"],
                options=question_data["options"],
                correct_answer=question_data["correct_answer"],
                explanation=question_data["explanation"],
            )
            db.add(question)

db.commit()
db.close()
print("Database seeded successfully!")
print("   Subjects: Python Programming, Machine Learning, Data Structures, Mathematics")
print("   Each subject has 4 topics and 2 quizzes (5 questions each).")
print("\n   Demo: Register a new account at http://localhost:5173")
