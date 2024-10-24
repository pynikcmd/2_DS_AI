from collections import deque

class Problem:
    def __init__(self, initial, goal, maze):
        self.initial = initial
        self.goal = goal
        self.maze = maze

    def actions(self, state):
        row, col = state
        actions = []
        if row > 0 and self.maze[row - 1][col] == 1:  # вверх
            actions.append(('UP', (row - 1, col)))
        if row < len(self.maze) - 1 and self.maze[row + 1][col] == 1:  # вниз
            actions.append(('DOWN', (row + 1, col)))
        if col > 0 and self.maze[row][col - 1] == 1:  # влево
            actions.append(('LEFT', (row, col - 1)))
        if col < len(self.maze[0]) - 1 and self.maze[row][col + 1] == 1:  # вправо
            actions.append(('RIGHT', (row, col + 1)))
        return actions

    def result(self, state, action):
        return action[1]  # возвращает новое состояние после действия

    def is_goal(self, state):
        return state == self.goal


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __repr__(self):
        return f"<{self.state}>"

    def __lt__(self, other):
        return self.path_cost < other.path_cost

def breadth_first_search(problem):
    node = Node(problem.initial)
    if problem.is_goal(node.state):
        return node

    frontier = deque([node])  # очередь для BFS
    reached = {problem.initial}

    while frontier:
        node = frontier.popleft()
        for action, child_state in problem.actions(node.state):
            if child_state not in reached:
                child_node = Node(child_state, node, action)
                if problem.is_goal(child_state):
                    return child_node
                frontier.append(child_node)
                reached.add(child_state)

    return None  # если решение не найдено

def path_actions(node):
    actions = []
    while node.parent is not None:
        actions.append(node.action)
        node = node.parent
    return actions[::-1]

# Пример лабиринта
maze = [
    [1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [0, 0, 1, 0, 1, 1, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 1, 0, 0, 1, 1, 0, 0, 1]
]

initial = (0, 0)  # начальная позиция
goal = (7, 5)  # целевая позиция

problem = Problem(initial, goal, maze)
solution = breadth_first_search(problem)

if solution:
    actions = path_actions(solution)
    print("Длина кратчайшего пути:", len(actions))
else:
    print("Путь не найден.")
