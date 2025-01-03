import matplotlib.pyplot as plt
import networkx as nx

# Define the modules and their communication
edges = [
    ("Orchestrator", "GameState"),
    ("Orchestrator", "Reflection"),
    ("Orchestrator", "PromptBuilder"),
    ("Orchestrator", "GPTInteraction"),
    ("Orchestrator", "Voting"),
    ("Orchestrator", "ConsensusChecker"),
    ("Orchestrator", "GlobalHistory"),
    ("Orchestrator", "Moderator"),
    ("Moderator", "Voting"),
    ("Moderator", "Reflection"),
    ("GameState", "Reflection"),
    ("GameState", "PromptBuilder"),
    ("Reflection", "PromptBuilder"),
    ("Reflection", "GPTInteraction"),
    ("PromptBuilder", "GPTInteraction"),
    ("Voting", "ConsensusChecker"),
    ("Voting", "GlobalHistory"),
    ("ConsensusChecker", "GameState"),
    ("ConsensusChecker", "GlobalHistory"),
]

# Define node roles for categorization
module_roles = {
    "Orchestrator": "Koordinator",
    "GameState": "Zustandsmanager",
    "Reflection": "Entscheidungsfindung",
    "PromptBuilder": "Prompt-Generator",
    "GPTInteraction": "KI-Schnittstelle",
    "Voting": "Phasenmanager",
    "ConsensusChecker": "Konsensprüfer",
    "GlobalHistory": "Verlaufsspeicher",
    "Moderator": "Phasensteuerung",
}

# Short descriptions for roles in German
role_descriptions = {
    "Koordinator": "Steuert den gesamten Spielablauf",
    "Zustandsmanager": "Verwaltet Spielstatus und Daten",
    "Entscheidungsfindung": "Analysiert und trifft Entscheidungen",
    "Prompt-Generator": "Erstellt KI-Prompts",
    "KI-Schnittstelle": "Interagiert mit GPT",
    "Phasenmanager": "Verwaltet Spielphasen",
    "Konsensprüfer": "Validiert Entscheidungen",
    "Verlaufsspeicher": "Speichert Ereignisse",
    "Phasensteuerung": "Koordiniert Phasenübergänge",
}

# Create a directed graph
G = nx.DiGraph()
G.add_edges_from(edges)

# Set positions of nodes with smaller scale for reduced spacing
pos = nx.spring_layout(G, seed=42, k=1.5)  # Reduce `k` for closer nodes

# Define colors for the module roles
color_map = {
    "Koordinator": "gold",
    "Zustandsmanager": "lightblue",
    "Entscheidungsfindung": "lightgreen",
    "Prompt-Generator": "pink",
    "KI-Schnittstelle": "orange",
    "Phasenmanager": "violet",
    "Konsensprüfer": "red",
    "Verlaufsspeicher": "gray",
    "Phasensteuerung": "cyan",
}

# Map node colors based on roles
node_colors = [color_map[module_roles[node]] for node in G.nodes]

# Draw the graph with larger figure size and adjusted spacing
plt.figure(figsize=(30, 25))  # Large figure size
nx.draw_networkx_nodes(
    G, pos, node_size=9000, node_color=node_colors, edgecolors="black"  # Larger node size
)
nx.draw_networkx_edges(
    G,
    pos,
    arrowstyle="->",
    arrowsize=25,
    edge_color="gray",
    width=2,
    connectionstyle="arc3,rad=0",  # Straight arrows
)
# Add numbered labels to nodes
node_labels = {
    node: f"{i+1}. {node}\n({module_roles[node]})" for i, node in enumerate(G.nodes)
}
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=20, font_weight="bold")  # Larger font size

# Create a legend for node roles with descriptions in German
legend_handles = [
    plt.Line2D([0], [0], marker="o", color="w", label=f"{role}: {desc}",
               markersize=15, markerfacecolor=color)
    for role, color, desc in zip(color_map.keys(), color_map.values(), role_descriptions.values())
]
plt.legend(
    handles=legend_handles,
    title="Modulrollen & Beschreibungen",
    loc="upper left",  # Relative to `bbox_to_anchor`
    bbox_to_anchor=(0.01, 0.42),  # Adjust these values for finer control
    fontsize=20,
    title_fontsize=22,
    frameon=True  # Adds a frame for better visibility
)

# Add a title
plt.title("Modulkommunikation und -fluss in WerewolfIQ", fontsize=28, fontweight="bold")

# Display the plot
plt.axis("off")
plt.show()
