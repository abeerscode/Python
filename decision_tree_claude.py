"""
Decision Tree Classifier — built from scratch
================================================
This mirrors the manual, step-by-step calculation you already learned:
    1. Compute Entropy of the current node
    2. For each feature, compute Information Gain (Entropy before - weighted Entropy after split)
    3. Pick the feature with the HIGHEST information gain
    4. Split the data on that feature, recurse on each branch
    5. Stop when a node is pure, out of features, or hits a depth limit

No sklearn used for the core algorithm — only plain Python + math,
so you can see every calculation happening.
"""

import math
from collections import Counter


# ----------------------------------------------------------------------
# 1. TOY DATASET  (classic "Play Tennis" example — easy to hand-verify)
# ----------------------------------------------------------------------
# Each row: (Outlook, Temperature, Humidity, Wind) -> PlayTennis (label)
data = [
    ("Sunny", "Hot", "High", "Weak", "No"),
    ("Sunny", "Hot", "High", "Strong", "No"),
    ("Overcast", "Hot", "High", "Weak", "Yes"),
    ("Rain", "Mild", "High", "Weak", "Yes"),
    ("Rain", "Cool", "Normal", "Weak", "Yes"),
    ("Rain", "Cool", "Normal", "Strong", "No"),
    ("Overcast", "Cool", "Normal", "Strong", "Yes"),
    ("Sunny", "Mild", "High", "Weak", "No"),
    ("Sunny", "Cool", "Normal", "Weak", "Yes"),
    ("Rain", "Mild", "Normal", "Weak", "Yes"),
    ("Sunny", "Mild", "Normal", "Strong", "Yes"),
    ("Overcast", "Mild", "High", "Strong", "Yes"),
    ("Overcast", "Hot", "Normal", "Weak", "Yes"),
    ("Rain", "Mild", "High", "Strong", "No"),
]

feature_names = ["Outlook", "Temperature", "Humidity", "Wind"]


# ----------------------------------------------------------------------
# 2. ENTROPY:  H(S) = - sum( p_i * log2(p_i) )
# ----------------------------------------------------------------------
def entropy(rows):
    labels = [row[-1] for row in rows]
    counts = Counter(labels)
    total = len(labels)
    ent = 0.0
    for label_count in counts.values():
        p = label_count / total
        ent -= p * math.log2(p)
    return ent


# ----------------------------------------------------------------------
# 3. INFORMATION GAIN for splitting on a given feature index
#    IG = Entropy(parent) - sum( |S_v|/|S| * Entropy(S_v) )
# ----------------------------------------------------------------------
def information_gain(rows, feature_index):
    parent_entropy = entropy(rows)
    total = len(rows)

    # group rows by the value of this feature
    subsets = {}
    for row in rows:
        key = row[feature_index]
        subsets.setdefault(key, []).append(row)

    weighted_entropy = 0.0
    for subset_rows in subsets.values():
        weight = len(subset_rows) / total
        weighted_entropy += weight * entropy(subset_rows)

    return parent_entropy - weighted_entropy, subsets


# ----------------------------------------------------------------------
# 4. TREE NODE
# ----------------------------------------------------------------------
class Node:
    def __init__(self, is_leaf=False, prediction=None,
                 feature_index=None, feature_name=None, branches=None):
        self.is_leaf = is_leaf
        self.prediction = prediction        # used if leaf
        self.feature_index = feature_index  # used if internal node
        self.feature_name = feature_name
        self.branches = branches or {}      # value -> child Node


# ----------------------------------------------------------------------
# 5. BUILD TREE (recursive, ID3-style)
# ----------------------------------------------------------------------
def majority_label(rows):
    labels = [row[-1] for row in rows]
    return Counter(labels).most_common(1)[0][0]


def build_tree(rows, available_features, depth=0, max_depth=None, indent=""):
    labels = [row[-1] for row in rows]

    # --- Stopping condition 1: node is pure ---
    if len(set(labels)) == 1:
        print(f"{indent}Leaf -> {labels[0]} (pure node)")
        return Node(is_leaf=True, prediction=labels[0])

    # --- Stopping condition 2: no features left, or depth limit hit ---
    if not available_features or (max_depth is not None and depth >= max_depth):
        pred = majority_label(rows)
        print(f"{indent}Leaf -> {pred} (majority vote, out of features/depth)")
        return Node(is_leaf=True, prediction=pred)

    # --- Try every remaining feature, compute info gain ---
    print(f"{indent}Node entropy = {entropy(rows):.4f}")
    best_gain = -1
    best_feature = None
    best_subsets = None

    for feature_index in available_features:
        gain, subsets = information_gain(rows, feature_index)
        print(f"{indent}  IG({feature_names[feature_index]}) = {gain:.4f}")
        if gain > best_gain:
            best_gain = gain
            best_feature = feature_index
            best_subsets = subsets

    # If best gain is 0, nothing more useful to split on -> leaf
    if best_gain <= 0:
        pred = majority_label(rows)
        print(f"{indent}Leaf -> {pred} (no useful split left)")
        return Node(is_leaf=True, prediction=pred)

    print(f"{indent}==> Split on '{feature_names[best_feature]}' "
          f"(gain={best_gain:.4f})")

    remaining_features = [f for f in available_features if f != best_feature]

    branches = {}
    for value, subset_rows in best_subsets.items():
        print(f"{indent}  Branch '{feature_names[best_feature]} = {value}':")
        child = build_tree(subset_rows, remaining_features,
                            depth + 1, max_depth, indent + "    ")
        branches[value] = child

    return Node(is_leaf=False, feature_index=best_feature,
                feature_name=feature_names[best_feature], branches=branches)


# ----------------------------------------------------------------------
# 6. PREDICT
# ----------------------------------------------------------------------
def predict(node, sample_dict):
    """sample_dict: {"Outlook": "Sunny", "Temperature": "Hot", ...}"""
    if node.is_leaf:
        return node.prediction
    value = sample_dict[node.feature_name]
    child = node.branches.get(value)
    if child is None:
        # unseen category at prediction time -> fall back to majority guess
        return "Unknown (unseen category during training)"
    return predict(child, sample_dict)


# ----------------------------------------------------------------------
# 7. PRETTY-PRINT THE TREE
# ----------------------------------------------------------------------
def print_tree(node, indent=""):
    if node.is_leaf:
        print(f"{indent}-> Predict: {node.prediction}")
        return
    for value, child in node.branches.items():
        print(f"{indent}[{node.feature_name} = {value}]")
        print_tree(child, indent + "    ")


# ----------------------------------------------------------------------
# 8. RUN IT
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("STEP-BY-STEP TREE BUILDING (trace of entropy / info gain)")
    print("=" * 60)

    all_feature_indices = list(range(len(feature_names)))
    tree = build_tree(data, all_feature_indices, max_depth=None)

    print("\n" + "=" * 60)
    print("FINAL TREE STRUCTURE")
    print("=" * 60)
    print_tree(tree)

    print("\n" + "=" * 60)
    print("TEST PREDICTIONS")
    print("=" * 60)
    test_samples = [
        {"Outlook": "Sunny", "Temperature": "Cool", "Humidity": "High", "Wind": "Strong"},
        {"Outlook": "Overcast", "Temperature": "Mild", "Humidity": "Normal", "Wind": "Weak"},
        {"Outlook": "Rain", "Temperature": "Mild", "Humidity": "Normal", "Wind": "Strong"},
    ]
    for sample in test_samples:
        result = predict(tree, sample)
        print(f"{sample} -> {result}")