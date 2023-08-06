import matplotlib.pyplot as plt
import numpy as np
import networkx as nx

from hypergz import hypergraph_layout
from hypergz.hypergraph_layout import hyperedge, hypergraph
from hypergz.our_layout import *


def draw_forest(num_of_trees, num_of_vxs, title1, title2, title3, title4):
    # Forest graph (5 tree of the size of 50 each)
    f: list[nx.Graph] = []
    for i in range(1, num_of_trees):
        f.append(nx.random_tree(num_of_vxs, i))
    pos_nx = nx.spring_layout(f[i - 1], iterations=700)
    plt.title(title1)
    nx.draw(f[i - 1], pos_nx, node_size=70)
    plt.show()
    pos = nx.force_directed(f[i - 1], 1, iterations=700, centrality=nx.closeness_centrality)
    plt.title(title2)
    nx.draw(f[i - 1], pos, node_size=70)
    plt.show()
    pos = nx.force_directed(f[i - 1], 1, iterations=700, centrality=nx.betweenness_centrality)
    plt.title(title3)
    nx.draw(f[i - 1], pos, node_size=70)
    plt.show()
    pos = nx.force_directed(f[i - 1], 1, iterations=700, centrality=nx.degree_centrality)
    plt.title(title4)
    nx.draw(f[i - 1], pos, node_size=70)
    plt.show()


def draw_graph(g, title1, title2, title3, title4):
    pos_nx = nx.spring_layout(g, iterations=700)
    plt.title(title1)
    nx.draw(g, pos_nx, node_size=70)
    plt.show()
    pos = nx.force_directed(g, 1, iterations=1000, centrality=nx.closeness_centrality)
    plt.title(title2)
    nx.draw(g, pos, node_size=70)
    plt.show()
    pos = nx.force_directed(g, 1, iterations=1000, centrality=nx.betweenness_centrality)
    plt.title(title3)
    nx.draw(g, pos, node_size=70)
    plt.show()
    pos = nx.force_directed(g, 1, iterations=1000, centrality=nx.degree_centrality)
    plt.title(title4)
    nx.draw(g, pos, node_size=70)
    plt.show()


def force_directed_tree():
    # Tree
    g: nx.Graph = nx.random_tree(70, 1)
    draw_graph(g, "Networkx tree", "Our tree with closeness centrality",
               "Our tree with betweenes centrality", "Our tree with degree centrality")


def force_directed_regular():
    # Regular graph
    # Note: gravity here is 0 therefore different centralities has no affect
    g: nx.Graph = nx.random_regular_graph(3, 90, 1)
    pos_nx = nx.spring_layout(g, iterations=700)
    plt.title('Networkx regular graph plot')
    nx.draw(g, pos_nx, node_size=70)
    plt.show()
    pos = nx.force_directed(g, 1, iterations=700, gravity=0, threshold=1e-4)
    pp = {}
    for i in range(len(pos)):
        pp[np.array(g.nodes)[i]] = np.array(pos[i])
    plt.title('Our regular graph plot')
    nx.draw(g, pp, node_size=70)
    plt.show()


def force_directed_small_forest():
    draw_forest(5, 70, "Networkx small forest", "Our small forest with closeness centrality",
                "Our small forest with betweenes centrality", "Our small forest with degree centrality")


def force_directed_large_forest():
    draw_forest(50, 100, "Networkx large forest", "Our large forest with closeness centrality",
                "Our large forest with betweenes centrality", "Our large forest with degree centrality")


def force_directed_hyper_graphs_using_social_and_gravity_scaling_drawing(G, iter):
    force_directed_hyper_graphs_using_social_and_gravity_scaling(G, iter,
                                                                 graph_type=hypergraph_layout.star_algorithm,
                                                                 seed=1, title="Star")
    force_directed_hyper_graphs_using_social_and_gravity_scaling(G, iter,
                                                                 graph_type=hypergraph_layout.complete_algorithm,
                                                                 seed=1, title="Complete")
    force_directed_hyper_graphs_using_social_and_gravity_scaling(G, iter,
                                                                 graph_type=hypergraph_layout.wheel_algorithm,
                                                                 seed=1, title="Wheel")
    force_directed_hyper_graphs_using_social_and_gravity_scaling(G, iter,
                                                                 graph_type=hypergraph_layout.cycle_algorithm,
                                                                 seed=1, title="Cycle")


def small_hyper_graph():
    E1 = hyperedge([1, 2, 3, 4])
    E2 = hyperedge([1, 3])
    E3 = hyperedge([1, 5, 6])
    E4 = hyperedge([1])
    G = hypergraph([1, 2, 3, 4, 5, 6], [E1, E2, E3, E4])
    force_directed_hyper_graphs_using_social_and_gravity_scaling_drawing(G, 1)


def medium_hyper_graph():
    # Note: in star layout 8 is inside [7,4,1] convex hull as expected
    E1 = hyperedge([10, 5, 8, 9])
    E2 = hyperedge([1])
    E3 = hyperedge([2, 6])
    E4 = hyperedge([2, 8, 7, 4, 1])
    E5 = hyperedge([7, 4, 1])
    E6 = hyperedge([11, 3])
    G = hypergraph([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], [E1, E2, E3, E4, E5, E6])
    force_directed_hyper_graphs_using_social_and_gravity_scaling_drawing(G, 10)


def large_hyper_graph():
    E1 = hyperedge([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    E2 = hyperedge([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    E3 = hyperedge([1, 2, 3, 4, 5, 6, 7, 8, 9])
    E4 = hyperedge([1, 2, 3, 4, 5, 6, 7])
    E5 = hyperedge([1, 2, 3, 4, 5, 6])
    E6 = hyperedge([1, 2, 3, 4, 5])
    E7 = hyperedge([1, 2, 3, 4])
    E8 = hyperedge([1, 2, 3])
    E9 = hyperedge([1, 2])
    E10 = hyperedge([1])
    G = hypergraph([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], [E1, E2, E3, E4, E5, E6, E7, E8, E9, E10])
    force_directed_hyper_graphs_using_social_and_gravity_scaling_drawing(G, 10)


def large_hyper_graph_with_tones_of_edges():
    E1 = hyperedge([1, 2, 3])
    E2 = hyperedge([5, 6, 7, 8, 9, 10])
    E3 = hyperedge([10, 6, 7, 8, 9])
    E4 = hyperedge([11, 2, 6, 7])
    E5 = hyperedge([1, 2, 3, 4])
    E6 = hyperedge([1, 4, 5])
    E7 = hyperedge([7, 8])
    E8 = hyperedge([9, 10])
    E9 = hyperedge([5, 7, 1, 3])
    E10 = hyperedge([9])
    E11 = hyperedge([7, 4, 1, 3])
    E12 = hyperedge([9, 4, 2])
    E13 = hyperedge([5, 6, 1, 8, 4, 10])
    E14 = hyperedge([7, 3])
    E15 = hyperedge([1, 8, 4])
    E16 = hyperedge([8])
    E17 = hyperedge([7, 4, 11])
    E18 = hyperedge([4, 1, 7])
    E19 = hyperedge([4, 8])
    E20 = hyperedge([6, 5, 2, 7, 8, 1])
    G = hypergraph([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], [E1, E2, E3, E4, E5, E6, E7, E8,
                                                         E9, E10, E11, E12, E13, E14, E15, E16, E17, E18, E19, E20])
    force_directed_hyper_graphs_using_social_and_gravity_scaling_drawing(G, 20)


if __name__ == '__main__':
    # regular graphs examples for the force_directed function (first article)
    # force_directed_tree()
    # force_directed_small_forest()
    # force_directed_large_forest()
    # force_directed_regular()
    # hyper graphs examples for the force_directed_hyper_graphs_using_social_and_gravity_scaling function
    # (second article)
    small_hyper_graph()
    # medium_hyper_graph()
    # large_hyper_graph()
    # large_hyper_graph_with_tones_of_edges()
