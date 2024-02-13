"""
2 task (Artem)

Algorithm Bellman-Ford
"""
import networkx as nx
import random
import matplotlib.pyplot as plt
from itertools import combinations, groupby

def gnp_random_connected_graph(num_of_nodes: int,
                               completeness: int,
                               directed: bool = False,
                               draw: bool = False):
    """
    Generates a random graph, similarly to an Erdős-Rényi 
    graph, but enforcing that the resulting graph is conneted (in case of undirected graphs)
    """

    
    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    edges = combinations(range(num_of_nodes), 2)
    G.add_nodes_from(range(num_of_nodes))
    
    for _, node_edges in groupby(edges, key = lambda x: x[0]):
        node_edges = list(node_edges)
        random_edge = random.choice(node_edges)
        if random.random() < 0.5:
            random_edge = random_edge[::-1]
        G.add_edge(*random_edge)
        for e in node_edges:
            if random.random() < completeness:
                G.add_edge(*e)
                
    for (u,v,w) in G.edges(data=True):
        w['weight'] = random.randint(-5, 20)
                
    if draw: 
        plt.figure(figsize=(10,6))
        if directed:
            # draw with edge weights
            pos = nx.arf_layout(G)
            nx.draw(G,pos, node_color='lightblue', 
                    with_labels=True,
                    node_size=500, 
                    arrowsize=20, 
                    arrows=True)
            labels = nx.get_edge_attributes(G,'weight')
            nx.draw_networkx_edge_labels(G, pos,edge_labels=labels)
            
        else:
            nx.draw(G, node_color='lightblue', 
                with_labels=True, 
                node_size=500)
        
    return G

G = gnp_random_connected_graph(10, 0.5, True)

def bellman_ford(G, start):
    """
    Bellman-Ford algorithm
    """
    dist = {node: float('infinity') for node in G.nodes}
    dist[start] = 0
    
    for _ in range(len(G.nodes)-1):
        for u, v, w in G.edges(data=True):
            if dist[u] + w['weight'] < dist[v]:
                dist[v] = dist[u] + w['weight']
                
    for u, v, w in G.edges(data=True):
        if dist[u] + w['weight'] < dist[v]:
            raise ValueError("Graph contains a negative-weight cycle")
            
    return dist

# print(bellman_ford(G, 0))


"""
Algorithm Floyd-Warshall
"""

def floyd_warshall(G):
    """
    Floyd-Warshall algorithm
    """
    dist = {node: {node: float('infinity') for node in G.nodes} for node in G.nodes}
    omegas = {node: {node: None for node in G.nodes} for node in G.nodes}

    for nd in G.nodes:
        dist[nd][nd] = 0
        omegas[nd][nd] = nd

    for u, v, w in G.edges(data=True):
        dist[u][v] = w['weight']
        omegas[u][v] = u

    for k in G.nodes:
        for i in G.nodes:
            for j in G.nodes:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    omegas[i][j] = omegas[k][j]

    return dist, omegas

print(floyd_warshall(G))







