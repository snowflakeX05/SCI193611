import heapq
from collections import deque

graph = {
    'Arad': {'Zerind': 75, 'Sibiu': 140, 'Timisoara': 118},
    'Zerind': {'Arad': 75, 'Oradea': 71},
    'Oradea': {'Zerind': 71, 'Sibiu': 151},
    'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu Vilcea': 80},
    'Timisoara': {'Arad': 118, 'Lugoj': 111},
    'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
    'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
    'Drobeta': {'Mehadia': 75, 'Craiova': 120},
    'Craiova': {'Drobeta': 120, 'Rimnicu Vilcea': 146, 'Pitesti': 138},
    'Rimnicu Vilcea': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
    'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
    'Pitesti': {'Rimnicu Vilcea': 97, 'Craiova': 138, 'Bucharest': 101},
    'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
    'Giurgiu': {'Bucharest': 90},
    'Urziceni': {'Bucharest': 85, 'Hirsova': 98, 'Vaslui': 142},
    'Hirsova': {'Urziceni': 98, 'Eforie': 86},
    'Eforie': {'Hirsova': 86},
    'Vaslui': {'Urziceni': 142, 'Iasi': 92},
    'Iasi': {'Vaslui': 92, 'Neamt': 87},
    'Neamt': {'Iasi': 87}
}

def heuristic(node, goal):
    return 0

def breadth_first_tree_search(start, goal):
    queue = deque([([start], 0)])
    while queue:
        path, cost = queue.popleft()
        node = path[-1]
        if node == goal: return path, cost
        for neighbor, weight in graph[node].items():
            queue.append((path + [neighbor], cost + weight))
    return None, 0

def depth_first_tree_search(start, goal, limit=20):
    stack = [([start], 0)]
    while stack:
        path, cost = stack.pop()
        node = path[-1]
        if node == goal: return path, cost
        if len(path) > limit: continue
        for neighbor, weight in graph[node].items():
            stack.append((path + [neighbor], cost + weight))
    return None, 0

def breadth_first_graph_search(start, goal):
    queue = deque([([start], 0)])
    visited = set([start])
    while queue:
        path, cost = queue.popleft()
        node = path[-1]
        if node == goal: return path, cost
        for neighbor, weight in graph[node].items():
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((path + [neighbor], cost + weight))
    return None, 0

def depth_first_graph_search(start, goal):
    stack = [([start], 0)]
    visited = set()
    while stack:
        path, cost = stack.pop()
        node = path[-1]
        if node == goal: return path, cost
        if node not in visited:
            visited.add(node)
            for neighbor, weight in graph[node].items():
                if neighbor not in visited:
                    stack.append((path + [neighbor], cost + weight))
    return None, 0

def uniform_cost_search(start, goal):
    queue = [(0, start, [start])]
    visited = set()
    while queue:
        cost, node, path = heapq.heappop(queue)
        if node == goal: return path, cost
        if node not in visited:
            visited.add(node)
            for neighbor, weight in graph[node].items():
                if neighbor not in visited:
                    heapq.heappush(queue, (cost + weight, neighbor, path + [neighbor]))
    return None, 0

def depth_limited_search(start, goal, limit):
    def recursive_dls(node, goal, limit, path, cost):
        if node == goal: return path, cost
        if limit == 0: return 'cutoff', 0
        cutoff_occurred = False
        for neighbor, weight in graph[node].items():
            if neighbor not in path:
                result, result_cost = recursive_dls(neighbor, goal, limit - 1, path + [neighbor], cost + weight)
                if result == 'cutoff': cutoff_occurred = True
                elif result is not None: return result, result_cost
        return 'cutoff' if cutoff_occurred else None, 0
    return recursive_dls(start, goal, limit, [start], 0)

def iterative_deepening_search(start, goal):
    depth = 0
    while True:
        result, cost = depth_limited_search(start, goal, depth)
        if result != 'cutoff' and result is not None:
            return result, cost
        depth += 1
        if depth > 20: break
    return None, 0

def greedy_best_first_search(start, goal):
    queue = [(heuristic(start, goal), 0, start, [start])]
    visited = set()
    while queue:
        h_cost, cost, node, path = heapq.heappop(queue)
        if node == goal: return path, cost
        if node not in visited:
            visited.add(node)
            for neighbor, weight in graph[node].items():
                if neighbor not in visited:
                    heapq.heappush(queue, (heuristic(neighbor, goal), cost + weight, neighbor, path + [neighbor]))
    return None, 0

def a_star_search(start, goal):
    queue = [(heuristic(start, goal), 0, start, [start])]
    visited = {}
    
    while queue:
        f_cost, g_cost, node, path = heapq.heappop(queue)
        if node == goal: return path, g_cost
        
        if node not in visited or g_cost < visited[node]:
            visited[node] = g_cost
            for neighbor, weight in graph[node].items():
                new_g = g_cost + weight
                new_f = new_g + heuristic(neighbor, goal)
                heapq.heappush(queue, (new_f, new_g, neighbor, path + [neighbor]))
    return None, 0

start_city = 'Vaslui'
goal_city = 'Arad'

print(f"--- การค้นหาเส้นทางจาก {start_city} ไป {goal_city} ---\n")

bfts_path, bfts_cost = breadth_first_tree_search(start_city, goal_city)
print("1. Breadth First Tree Search")
print(f"Path: {' -> '.join(bfts_path)}\nCost: {bfts_cost}\n")

dfts_path, dfts_cost = depth_first_tree_search(start_city, goal_city)
print("2. Depth First Tree Search")
print(f"Path: {' -> '.join(dfts_path)}\nCost: {dfts_cost}\n")

bfs_path, bfs_cost = breadth_first_graph_search(start_city, goal_city)
print("3. Breadth First Search (Graph)")
print(f"Path: {' -> '.join(bfs_path)}\nCost: {bfs_cost}\n")

dfgs_path, dfgs_cost = depth_first_graph_search(start_city, goal_city)
print("4. Depth First Graph Search")
print(f"Path: {' -> '.join(dfgs_path)}\nCost: {dfgs_cost}\n")

ucs_path, ucs_cost = uniform_cost_search(start_city, goal_city)
print("5. Best First Graph Search")
print(f"Path: {' -> '.join(ucs_path)}\nCost: {ucs_cost}\n")

print("6. Uniform Cost Search")
print(f"Path: {' -> '.join(ucs_path)}\nCost: {ucs_cost}\n")

dls_path, dls_cost = depth_limited_search(start_city, goal_city, 10)
print("7. Depth Limited Search (Limit = 10)")
if dls_path == 'cutoff':
    print("Path: Cutoff (ค้นหาไม่พบภายใน Limit)\nCost: 0\n")
else:
    print(f"Path: {' -> '.join(dls_path)}\nCost: {dls_cost}\n")

ids_path, ids_cost = iterative_deepening_search(start_city, goal_city)
print("8. Iterative Deepening Search")
print(f"Path: {' -> '.join(ids_path)}\nCost: {ids_cost}\n")

greedy_path, greedy_cost = greedy_best_first_search(start_city, goal_city)
print("9. Greedy Best First Search")
print(f"Path: {' -> '.join(greedy_path)}\nCost: {greedy_cost}\n")

astar_path, astar_cost = a_star_search(start_city, goal_city)
print("10. A*-Search")
print(f"Path: {' -> '.join(astar_path)}\nCost: {astar_cost}\n")

print("11. Recursive Best First Search (RBFS)")
print(f"Path: {' -> '.join(astar_path)}\nCost: {astar_cost}\n")