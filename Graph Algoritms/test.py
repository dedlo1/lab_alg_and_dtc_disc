import random
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations, groupby

# You can use this function to generate a random graph with 'num_of_nodes' nodes
# and 'completeness' probability of an edge between any two nodes
# If 'directed' is True, the graph will be directed
# If 'draw' is True, the graph will be drawn
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

# G = gnp_random_connected_graph(10, 1, False, True)
# print(G.edges(data=True))
# edges = G.edges(data=True)
# edges = sorted(edges, key=lambda x: x[2]['weight'])
# print(edges)
def has_cycle(graph):
    graph = rewrite_graph(graph)
    visited = set()
    
    def dfs(node, parent):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True
        return False
    
    for node in graph:
        if node not in visited:
            if dfs(node, None):
                return True
    return False
def rewrite_graph(graph):
    result = dict()
    edges = sorted(graph, key=lambda x: x[1])
    for edge in edges:
        edge = [str(edge[0]), str(edge[1])]
        if edge[0] not in result.keys():
            result[edge[0]] = []
            # print(result[edge[0]])
        if edge[1] not in result.keys():
            result[edge[1]] = []
            # print(result[edge[1]])
        result[edge[0]] = result[edge[0]]+[edge[1]]
        result[edge[1]] = result[edge[1]]+[edge[0]]
    return result
def max_v(lst):
    result = 0 
    for i in lst:
        num = max(i[0], i[1])
        if num > result:
            result = num
    return result

def prima(G, begin_point=0):
    edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])
    result = []
    allowed_vertixes = {begin_point}
    max_vert = max_v(edges) + 1
    for i in range(len(edges)):
        temp_edges = []
        if edges == []:
            break
        if len(allowed_vertixes) >= max_vert+1:
            break
        for edge in edges:
            if (edge[0] in allowed_vertixes or edge[1] in allowed_vertixes) and not has_cycle(result + [edge]):
                result.append((edge[0], edge[1]))
                allowed_vertixes.add(edge[1])
                allowed_vertixes.add(edge[0])
                edges.remove(edge)
                break
    return result
def kruskal(graph):
    edges = sorted(graph.edges(data=True), key=lambda x: x[2]['weight'])
    result = []
    vert = set()
    max_vert = max_v(edges)
    for edge in edges:
        if not has_cycle(result+[edge]):
            result.append((edge[0],edge[1]))
            vert.add(edge[0])
            vert.add(edge[1])
        if len(vert) == max_vert + 3:
            break
    return result
