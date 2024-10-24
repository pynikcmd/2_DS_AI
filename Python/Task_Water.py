from collections import deque

class PourProblem:
    def __init__(self, start, goal, sizes):
        self.start = start  # начальное состояние кувшинов (объемы воды)
        self.goal = goal  # целевой объем воды
        self.sizes = sizes  # максимальные размеры кувшинов

    def is_goal(self, state):
        return self.goal in state  # проверка, содержит ли один из кувшинов целевой объем

    def actions(self, state):
        actions = []
        num_jugs = len(self.sizes)
        # Наполнение каждого кувшина до максимума
        for i in range(num_jugs):
            if state[i] < self.sizes[i]:
                actions.append(('Fill', i))

        # Выливание содержимого каждого кувшина
        for i in range(num_jugs):
            if state[i] > 0:
                actions.append(('Dump', i))

        # Переливание воды из одного кувшина в другой
        for i in range(num_jugs):
            for j in range(num_jugs):
                if i != j and state[i] > 0 and state[j] < self.sizes[j]:
                    actions.append(('Pour', i, j))

        return actions

    def result(self, state, action):
        state = list(state)  # создаем копию состояния
        if action[0] == 'Fill':
            i = action[1]
            state[i] = self.sizes[i]  # наполняем кувшин до максимума
        elif action[0] == 'Dump':
            i = action[1]
            state[i] = 0  # опустошаем кувшин
        elif action[0] == 'Pour':
            i, j = action[1], action[2]
            transfer = min(state[i], self.sizes[j] - state[j])
            state[i] -= transfer  # переливаем воду из i в j
            state[j] += transfer

        return tuple(state)

def bfs(problem):
    # Инициализируем начальный узел
    start_node = problem.start
    if problem.is_goal(start_node):
        return start_node, []  # Если стартовое состояние уже является целевым

    frontier = deque([start_node])
    explored = set([start_node])
    paths = {start_node: []}

    while frontier:
        current_state = frontier.popleft()

        for action in problem.actions(current_state):
            new_state = problem.result(current_state, action)

            if new_state not in explored:
                explored.add(new_state)
                frontier.append(new_state)
                paths[new_state] = paths[current_state] + [action]

                if problem.is_goal(new_state):
                    return new_state, paths[new_state]

    return None, []  # если решение не найдено

# Примеры для проверки
test_cases = [
    ((1, 2, 1), 2, (3, 2, 5)),  # Начальное состояние с доступным решением
    ((1, 0, 0), 2, (3, 5, 8)),  # Начальное состояние с другим объемом
    ((1, 1, 1), 3, (3, 5, 7)),  # Начальное состояние для получения 3
    ((1, 0, 1), 2, (2, 3, 5))   # Начальное состояние с 1 литром
]

# Выполняем все тесты
for start_state, goal, sizes in test_cases:
    problem = PourProblem(start_state, goal, sizes)
    final_state, solution_path = bfs(problem)

    print(f"Начальное состояние: {start_state}, Цель: {goal}, Размеры: {sizes}")
    if final_state:
        print("Последовательность действий:", solution_path)
        current_state = start_state
        states = [current_state]
        for action in solution_path:
            current_state = problem.result(current_state, action)
            states.append(current_state)
        print("Состояния:", states)
    else:
        print("Решение не найдено.")
    print()
