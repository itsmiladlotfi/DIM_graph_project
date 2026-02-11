import streamlit as st

st.set_page_config(layout="wide")



st.title("Dominating Induced Matching (DIM)")

st.markdown("### Student: Milad Lotfi")
st.markdown("### Instructor: Dr. Behmaram")
st.markdown("### Course: Graph Theory")

st.divider()


st.header("What is a Dominating Induced Matching?")

st.write("""
In a graph G = (V,E), a matching is a set of edges such that no two edges share a common vertex.

A Dominating Induced Matching (DIM) is a special type of matching that satisfies THREE conditions simultaneously.
""")


st.header("1) Matching Condition")
st.write("""
No two selected edges touch each other.

Each vertex can belong to at most one selected edge.
""")

st.header("2) Induced Condition")
st.write("""
If we take all vertices that belong to the selected edges,
the subgraph formed by those vertices must contain only those edges.

Meaning:
There are no extra edges between endpoints of different matching edges.
""")

st.header("3) Dominating Condition")
st.write("""
Every edge in the graph must be "controlled" by exactly one chosen edge.

An edge is dominated if it shares at least one endpoint with a matching edge.
""")

st.divider()


st.header("Intuition")

st.write("""
You can think of DIM as placing "guards" on some edges:

• Guards cannot stand next to each other
• Guards cannot see each other directly
• Every edge in the graph must be watched by exactly one guard
""")

st.divider()


st.header("Complexity")

st.write("""
The Dominating Induced Matching problem is NP-Complete in general graphs.

This means:
There is no known efficient (polynomial-time) algorithm that solves the problem for all graphs.

Therefore, in this project we use a brute-force verification algorithm
to experimentally check whether a graph admits a DIM.
""")

st.divider()


st.header("How to Use the Interactive Demo")

st.write("""
Go to the Interactive DIM Demo page from the sidebar.

There you can:
• Manually create a graph using the adjacency matrix
• Generate random graphs
• Automatically generate graphs that contain a DIM
• Visually verify the matching

If a DIM exists, its edges will be highlighted in RED.
""")