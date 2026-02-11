import streamlit as st
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from dim import has_DIM

st.set_page_config(layout="wide")
st.title("Dominating Induced Matching (DIM)")
st.caption("Student: Milad Lotfi")
st.caption("Instructor: Dr. Behmaram")
st.caption("Course: Graph Theory Project")
st.divider()
# --------------------------------------------------
# UTILITIES
# --------------------------------------------------

def random_graph(n, p):
    mat = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i + 1, n):
            if np.random.rand() < p:
                mat[i][j] = 1
                mat[j][i] = 1
    return mat


def generate_until_dim(n, p, max_attempts=300):
    for _ in range(max_attempts):
        mat = random_graph(n, p)
        has_dim, _ = has_DIM(mat)
        if has_dim:
            return mat
    return None


def enforce_graph_rules(mat):
    n = mat.shape[0]

    # remove self loops
    for i in range(n):
        mat[i][i] = 0

    # make symmetric (undirected)
    for i in range(n):
        for j in range(n):
            val = max(mat[i][j], mat[j][i])
            mat[i][j] = val
            mat[j][i] = val

    return mat


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("Graph Controls")

n = st.sidebar.slider("Number of vertices", 2, 10, 4)
p = st.sidebar.slider("Edge probability", 0.0, 1.0, 0.3, 0.05)

btn_random = st.sidebar.button("Generate Random Graph")
btn_dim = st.sidebar.button("Generate Graph WITH DIM")
btn_clear = st.sidebar.button("Clear Graph")

# --------------------------------------------------
# SESSION STATE INITIALIZATION
# --------------------------------------------------

if "matrix" not in st.session_state:
    st.session_state.matrix = np.zeros((n, n), dtype=int)

# resize matrix if n changes
if st.session_state.matrix.shape[0] != n:
    st.session_state.matrix = np.zeros((n, n), dtype=int)

# buttons
if btn_random:
    st.session_state.matrix = random_graph(n, p)

if btn_clear:
    st.session_state.matrix = np.zeros((n, n), dtype=int)

if btn_dim:
    mat = generate_until_dim(n, p)
    if mat is not None:
        st.session_state.matrix = mat
    else:
        st.sidebar.warning("Could not find DIM graph")

# --------------------------------------------------
# LAYOUT (2 COLUMNS)
# --------------------------------------------------

col1, col2 = st.columns(2)

# --------------------------------------------------
# MATRIX EDITOR
# --------------------------------------------------

with col1:
    st.subheader("Adjacency Matrix")

    df = pd.DataFrame(
        st.session_state.matrix,
        columns=[f"v{i}" for i in range(n)],
        index=[f"v{i}" for i in range(n)],
    )

    edited_df = st.data_editor(
        df,
        num_rows="fixed",
        use_container_width=True,
        key="matrix_editor"
    )

    matrix = edited_df.to_numpy().astype(int)
    matrix = enforce_graph_rules(matrix)
    st.session_state.matrix = matrix

    st.caption("Matrix automatically corrected to a simple undirected graph")

# --------------------------------------------------
# GRAPH VISUALIZATION
# --------------------------------------------------

with col2:
    st.subheader("Graph Visualization")

    G = nx.Graph()

    for i in range(n):
        G.add_node(i)

    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] == 1:
                G.add_edge(i, j)

    fig, ax = plt.subplots()
    pos = nx.spring_layout(G, seed=7)

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightblue",
        edge_color="gray",
        node_size=900,
        font_size=12,
        ax=ax
    )

    st.pyplot(fig)

    edges_count = int(np.sum(matrix) // 2)
    density = edges_count / (n * (n - 1) / 2)
    st.info(f"Vertices: {n} | Edges: {edges_count} | Density: {density:.2f}")

# --------------------------------------------------
# DIM CHECKER
# --------------------------------------------------

st.divider()
st.subheader("DIM Checker")

check = st.button("Check Dominating Induced Matching")

if check:
    has_dim, matching = has_DIM(matrix)

    if has_dim:
        st.success(f"Graph HAS a DIM: {matching}")

        # highlight matching edges
        fig2, ax2 = plt.subplots()

        edge_colors = []
        for edge in G.edges():
            if edge in matching or (edge[1], edge[0]) in matching:
                edge_colors.append("red")
            else:
                edge_colors.append("gray")

        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color="lightgreen",
            edge_color=edge_colors,
            node_size=900,
            font_size=12,
            width=2.5,
            ax=ax2
        )

        st.pyplot(fig2)

    else:
        st.error("Graph does NOT have a Dominating Induced Matching")
