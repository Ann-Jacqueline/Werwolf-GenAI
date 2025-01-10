import matplotlib.pyplot as plt
import networkx as nx

# Define a directed graph for the workflow
G_workflow = nx.DiGraph()

# Define nodes with numbers and descriptions for clarity
nodes_workflow = [
    "1. Orchestrator",
    "2. Reflection Model",
    "3. LLAMA",
    "4. Token Scoring Model",
    "5. Tentative Global History Model",
    "6. Voting Model",
    "7. Persistent Global History Model"
]

# Add nodes to the graph
G_workflow.add_nodes_from(nodes_workflow)

# Define edges to represent interactions and feedback loops
edges_workflow = [
    # Start of a new phase
    ("7. Persistent Global History Model", "1. Orchestrator"),  # Step 1: Final state informs Orchestrator
    ("1. Orchestrator", "2. Reflection Model"),  # Step 2: Orchestrator triggers Reflection Model
    ("2. Reflection Model", "3. LLAMA"),  # Step 3: Reflection generates dynamic prompt for LLAMA

    # Discussion phase
    ("3. LLAMA", "4. Token Scoring Model"),  # Step 4: LLAMA generates output -> Scoring
    ("4. Token Scoring Model", "5. Tentative Global History Model"),  # Step 5: Add output to Tentative History
    ("5. Tentative Global History Model", "2. Reflection Model"),  # Step 6: Tentative History triggers reprompt

    # Feedback loops during discussion
    ("5. Tentative Global History Model", "6. Voting Model"),  # Step 7: Discussion log sent to Voting Model

    # End of discussion phase
    ("6. Voting Model", "7. Persistent Global History Model"),  # Step 8: Voting sends summary to Persistent History
]

# Add edges to the graph
G_workflow.add_edges_from(edges_workflow)

# Define positions for the nodes
pos_workflow = {
    "1. Orchestrator": (-3, 0),
    "2. Reflection Model": (0, 2),
    "3. LLAMA": (3, 0),
    "4. Token Scoring Model": (1, -2),
    "5. Tentative Global History Model": (0, -4),
    "6. Voting Model": (2, -6),
    "7. Persistent Global History Model": (-2, -6),
}

# Create the plot
plt.figure(figsize=(14, 10))

# Draw nodes and edges
nx.draw(
    G_workflow, pos_workflow, with_labels=True, node_size=3500, node_color="lightblue",
    font_size=10, font_weight="bold", arrowsize=20, edge_color="gray"
)

# Define edge labels for better explanation
edge_labels_workflow = {
    ("7. Persistent Global History Model", "1. Orchestrator"): "Step 1: Inform Orchestrator",
    ("1. Orchestrator", "2. Reflection Model"): "Step 2: Trigger Reflection",
    ("2. Reflection Model", "3. LLAMA"): "Step 3: Generate Prompt",
    ("3. LLAMA", "4. Token Scoring Model"): "Step 4: Output -> Scoring",
    ("4. Token Scoring Model", "5. Tentative Global History Model"): "Step 5: Update Tentative History",
    ("5. Tentative Global History Model", "2. Reflection Model"): "Step 6: Reprompt Reflection",
    ("5. Tentative Global History Model", "6. Voting Model"): "Step 7: Send Log to Voting",
    ("6. Voting Model", "7. Persistent Global History Model"): "Step 8: Finalize History",
}

# Add edge labels to the plot
nx.draw_networkx_edge_labels(
    G_workflow, pos_workflow, edge_labels=edge_labels_workflow,
    font_size=8, font_color="darkgreen", label_pos=0.6, bbox=dict(facecolor="white", alpha=0.7)
)

# Add title
plt.title("Model Workflow and Feedback Loops", fontsize=14, fontweight="bold")
plt.show()


