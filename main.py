import networkx as nx


def ford_fulkerson_method(graph, source, sink):
    flow = 0
    # Создаем residual graph как копию исходного графа
    residual = graph.copy()

    def bfs(residual, source, sink):
        queue = [(source, [source])]
        visited = set()
        while queue:
            current, path = queue.pop(0)
            if current == sink:
                return path
            visited.add(current)
            for neighbor in list(residual[current]):
                if neighbor not in visited and residual[current][neighbor]['capacity'] > 0:
                    queue.append((neighbor, path + [neighbor]))
        return None

    while True:
        path = bfs(residual, source, sink)
        if not path:
            return flow  # Нет увеличивающего пути, возвращаем текущий поток
        # Находим минимальную пропускную способность в пути
        path_flow = float('Inf')
        for u, v in zip(path, path[1:]):
            path_flow = min(path_flow, residual[u][v]['capacity'])

        # Обновляем пропускные способности в residual graph
        for u, v in zip(path, path[1:]):
            residual[u][v]['capacity'] -= path_flow
            # Создаем или обновляем обратное ребро
            if residual.has_edge(v, u):
                residual[v][u]['capacity'] += path_flow
            else:
                residual.add_edge(v, u, capacity=path_flow)

        flow += path_flow


# Создание графа и добавление ребер с пропускной способностью
G = nx.DiGraph()
edges = [
    (1, 2, 32), (1, 3, 95), (1, 4, 75), (1, 5, 57), (2, 5, 23),
    (2, 3, 5), (2, 8, 16), (3, 4, 18), (3, 6, 6), (4, 5, 24),
    (4, 6, 9), (5, 7, 20), (5, 8, 94), (6, 7, 7),
    (6, 5, 11), (7, 8, 81)
]
for u, v, c in edges:
    G.add_edge(u, v, capacity=c)

max_flow = ford_fulkerson_method(G, 1, 8)
print("Максимальный поток из вершины 1 в вершину 8:", max_flow)
