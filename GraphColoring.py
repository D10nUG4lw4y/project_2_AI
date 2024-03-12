import networkx as nx
import random
import matplotlib.pyplot as plt
import numpy as np

def generate_graph(n, p):
    # generate a random graph with n nodes and edge probability p
    G = nx.Graph()
    for i in range(n):
        G.add_node(i)
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < p:
                G.add_edge(i, j)
    return G

def erdos_renyi_graph(n, p):
    # generate a random graph using the Erdos-Renyi model
    graph = nx.erdos_renyi_graph(n, p)
    return graph

def random_color(graph, num_colors):
    # generate a random color in hexadecimal
    colors = {node: random.randint(1, num_colors) for node in graph.nodes}
    return colors

def conflict_count(graph, colors):
    # count the number of conflicts in the given coloring
    conflicts = 0
    for edge in graph.edges:
        if colors[edge[0]] == colors[edge[1]]:
            conflicts += 1
    return conflicts

def draw_graph(graph, colors):
    # draw the graph with the given coloring
    pos = nx.spring_layout(graph, seed = 42)
    nx.draw_networkx_nodes(graph, pos, node_color=list(colors.values()), cmap=plt.get_cmap('jet'), node_size=500)
    nx.draw_networkx_edges(graph, pos)
    nx.draw_networkx_labels(graph, pos)

    plt.show()

def decentralized_coloring(graph, colors, num_colors, max_iter=100, hold=20):
    iterations = 0
    nodes = list(graph.nodes)
    num_conflicts = conflict_count(graph, colors)
    elite_conflicts = num_conflicts
    elite_colors = colors
    while num_conflicts > 0 and iterations < max_iter:
        iterations += 1
        random.shuffle(nodes)
        # for each node, try a new color and see if it reduces the number of conflicts
        for node in nodes:
            old_color = colors[node]
            new_color = random.randint(1, num_colors)
            colors[node] = new_color
            new_conflicts = conflict_count(graph, colors)
            # if the new color reduces the number of conflicts, keep it
            if new_conflicts < num_conflicts:
                num_conflicts = new_conflicts
            # otherwise, revert to the old color
            else:
                colors[node] = old_color
        print('Iteration:', iterations, 'Number of conflicts:', num_conflicts)
        # if the new coloring is better than the elite coloring, keep it
        if num_conflicts < elite_conflicts:
            elite_conflicts = num_conflicts
            elite_colors = colors
        # if we have reached the hold iteration, use the elite coloring
        if iterations % hold == 0:
            colors = elite_colors
            num_conflicts = elite_conflicts
    return elite_colors

def color_vs_conflicts(num_nodes, edge_prob, start_num_colors, end_num_colors):
    results = []
    # for each number of colors, generate a random graph and find the number of conflicts
    for num_colors in range(start_num_colors, end_num_colors + 1):
        conflicts_per_color = []

        graph = erdos_renyi_graph(num_nodes, edge_prob)
        colors = random_color(graph, num_colors)
        draw_graph(graph, colors)

        final_colors = decentralized_coloring(graph, colors, num_colors)

        num_conflicts = conflict_count(graph, final_colors)
        conflicts_per_color.append(num_conflicts)

        print('Number of conflicts for {} colors: {}'.format(num_colors, num_conflicts))

        draw_graph(graph, final_colors)

        results.append(conflicts_per_color)

    # plot the results
    x = np.arange(start_num_colors, end_num_colors + 1)
    y = np.array(results)
    plt.plot(x, y)
    plt.xlabel('Number of colors')
    plt.ylabel('Number of conflicts')
    plt.title('Final number of conflicts for different number of colors after 100 iterations')
    plt.show()

num_nodes = 50
edge_prob = 0.3
start_num_colors = 2
end_num_colors = 10

color_vs_conflicts(num_nodes, edge_prob, start_num_colors, end_num_colors)