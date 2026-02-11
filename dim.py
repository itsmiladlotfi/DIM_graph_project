from itertools import combinations

# ==========================================================
# Convert adjacency matrix -> edge list
# ==========================================================
def get_edges(adj):
    n = len(adj)
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if adj[i][j] == 1:
                edges.append((i, j))
    return edges


# ==========================================================
# Matching condition
# No two edges share a vertex
# ==========================================================
def is_matching(matching):
    used_vertices = set()

    for u, v in matching:
        if u in used_vertices or v in used_vertices:
            return False
        used_vertices.add(u)
        used_vertices.add(v)

    return True


# ==========================================================
# Induced matching condition
# No endpoint of one matching edge is adjacent to
# an endpoint of another matching edge
# ==========================================================
def is_induced(matching, adj):

    # check pairwise edges in the matching
    for i in range(len(matching)):
        u1, v1 = matching[i]

        for j in range(i + 1, len(matching)):
            u2, v2 = matching[j]

            # any cross edge breaks induced property
            if adj[u1][u2] == 1:
                return False
            if adj[u1][v2] == 1:
                return False
            if adj[v1][u2] == 1:
                return False
            if adj[v1][v2] == 1:
                return False

    return True


# ==========================================================
# Dominating condition (CORRECT DEFINITION)
# Every NON-matching edge must be dominated by EXACTLY ONE
# matching edge (share one endpoint with exactly one edge in M)
# ==========================================================
def is_dominating(matching, edges):

    matching_set = set(matching)

    for (a, b) in edges:

        # skip edges that are in the matching itself
        if (a, b) in matching_set or (b, a) in matching_set:
            continue

        dominated_count = 0

        for (u, v) in matching:
            # shares a vertex
            if a == u or a == v or b == u or b == v:
                dominated_count += 1

        # must be dominated by exactly ONE matching edge
        if dominated_count != 1:
            return False

    return True


# ==========================================================
# MAIN FUNCTION
# ==========================================================
def has_DIM(adj):

    edges = get_edges(adj)

    # try every subset of edges
    for r in range(1, len(edges) + 1):
        for candidate in combinations(edges, r):

            if not is_matching(candidate):
                continue

            if not is_induced(candidate, adj):
                continue

            if not is_dominating(candidate, edges):
                continue

            return True, list(candidate)

    return False, None