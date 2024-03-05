import json

# Define a class to store traversal context
class Context:
    def __init__(self):
        self.count = 0               # Initialize node count to 0
        self.changes = {}            # Initialize dictionary to track changes

    # Method to increment node count
    def increment_count(self):
        self.count += 1

# Function for depth-first traversal and counting of nodes
def dfs_traversal_count(node, context):
    # If the node is a dictionary
    if isinstance(node, dict):
        context.increment_count()         # Increment node count
        # Iterate over key-value pairs in the dictionary
        for key, value in node.items():
            # If the value is another dictionary or a list, recursively call the function
            if isinstance(value, (dict, list)):
                dfs_traversal_count(value, context)
            else:
                # Track changes to attributes
                if key not in context.changes:
                    context.changes[key] = []           # Initialize list for attribute changes
                context.changes[key].append(value)     # Add value to the list of changes for the attribute
    # If the node is a list
    elif isinstance(node, list):
        # Iterate over items in the list
        for item in node:
            # Recursively call the function for each item in the list
            dfs_traversal_count(item, context)

# Read and parse the JSON file
with open('output.json', 'r') as file:
    data = json.load(file)

# Create a context object to store traversal state
context = Context()

# Traverse the AST using DFS and count the total number of nodes
dfs_traversal_count(data, context)

# Print the total number of nodes
print("Total Number of Nodes:", context.count)

print("context.count before calling the function:", context.count)

# context is a heap object, so it's passed by reference, not by value
dfs_traversal_count(None, context)

print("context.count after calling the function:", context.count)
