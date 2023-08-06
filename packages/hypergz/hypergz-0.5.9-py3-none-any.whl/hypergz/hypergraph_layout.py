import networkx as nx
import numpy as np

__all__ = [
    "hypergraph",
    "complete_algorithm",
    "cycle_algorithm",
    "star_algorithm",
    "wheel_algorithm"
]


class hyperedge:
    def __init__(self, vertices: list[int]):
        self.vertices = np.array(vertices)


class hypergraph:
    def __init__(self, vertices: list[int], hyperedges: list[hyperedge]):
        self.vertices = np.array(vertices)
        self.hyperedges = np.array(hyperedges)


def complete_algorithm(h_graph: hypergraph):
    g = nx.Graph()
    for v in h_graph.vertices:
        g.add_node(v)
    for edge in h_graph.hyperedges:
        for i in range(len(edge.vertices)):
            for j in range(i + 1, len(edge.vertices)):
                g.add_edge(edge.vertices[i], edge.vertices[j])
    return g


def cycle_algorithm(h_graph: hypergraph):
    g = nx.Graph()
    for v in h_graph.vertices:
        g.add_node(v)
    for edge in h_graph.hyperedges:
        for i in range(len(edge.vertices) - 1):
            g.add_edge(edge.vertices[i], edge.vertices[i + 1])
        if len(edge.vertices) > 1:
            g.add_edge(edge.vertices[0], edge.vertices[-1])
    return g


def star_algorithm(h_graph: hypergraph):
    g = nx.Graph()
    for v in h_graph.vertices:
        g.add_node(v)
    for i, edge in enumerate(h_graph.hyperedges):
        center_vertex = f'center {i}'
        for v in edge.vertices:
            g.add_edge(v, center_vertex)
    return g


def wheel_algorithm(h_graph: hypergraph):
    g = nx.Graph()
    for v in h_graph.vertices:
        g.add_node(v)
    for i, edge in enumerate(h_graph.hyperedges):
        center_vertex = f'center {i}'
        for v in edge.vertices:
            g.add_edge(v, center_vertex)
    for edge in h_graph.hyperedges:
        for i in range(len(edge.vertices) - 1):
            g.add_edge(edge.vertices[i], edge.vertices[i + 1])
        if len(edge.vertices) > 1:
            g.add_edge(edge.vertices[0], edge.vertices[-1])
    return g


def print_edges(g: nx.Graph):
    for e in g.edges:
        print(f"{e[0]},{e[1]}")


if __name__ == '__main__':
    v1 = 1
    v2 = 2
    v3 = 3
    v4 = 4
    E1 = hyperedge([v1, v2, v3, v4])
    E2 = hyperedge([v3, v4])
    E3 = hyperedge([v1])
    G = hypergraph([v1, v2, v3, v4], [E1, E2, E3])
    g1 = complete_algorithm(G)
    print("complete graph:")
    print_edges(g1)
    print("cycle graph:")
    g2 = cycle_algorithm(G)
    print_edges(g2)
    print("star graph:")
    g3 = star_algorithm(G)
    print_edges(g3)
    print("wheel graph:")
    g4 = wheel_algorithm(G)
    print_edges(g4)