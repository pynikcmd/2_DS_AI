from Problem import Problem
from Node import Node, failure, expand, path_states
import heapq

# Список городов и расстояний между ними
distances = {
    ('Ставрополь', 'Михайловск'): 14,
    ('Михайловск', 'Московское'): 25,
    ('Московское', 'Донское'): 20,
    ('Донское', 'Изобильный'): 22,
    ('Михайловск', 'Изобильный'): 46,
    ('Изобильный', 'Новотроицкая'): 14,
    ('Новотроицкая', 'Новоалександровск'): 17,
    ('Новоалександровск', 'Кропоткин'): 56,
    ('Кропоткин', 'Новоивановский'): 25,
    ('Кропоткин', 'Восточный'): 32,
    ('Новоивановский', 'Мирный'): 7,
    ('Мирный', 'Тбилисская'): 14,
    ('Тбилисская', 'Ладожская'): 25,
    ('Восточный', 'Ладожская'): 41,
    ('Ладожская', 'Двубратский'): 14,
    ('Двубратский', 'Васюринская'): 39,
    ('Васюринская', 'Знаменский'): 37,
    ('Васюринская', 'Старокорсунская'): 12,
    ('Старокорсунская', 'Хутор Ленина'): 10,
    ('Хутор Ленина', 'Краснодар'): 25,
    ('Знаменский', 'Краснодар'): 17,
}


# Функция для получения расстояния между городами
def get_distance(city1, city2):
    return distances.get((city1, city2)) or distances.get((city2, city1), float('inf'))


class TSPProblem(Problem):
    """Класс для решения задачи коммивояжёра."""

    def __init__(self, initial, goal):
        super().__init__(initial=initial, goal=goal)
        self.cities = list(distances.keys())

    def actions(self, state):
        """Возвращает возможные действия - соседние города."""
        return [city for city in distances.keys() if state in city]

    def result(self, state, action):
        """Возвращает следующий город, в который переходит коммивояжер."""
        return action[1] if state == action[0] else action[0]

    def action_cost(self, state, action, result):
        """Возвращает стоимость перехода между городами."""
        return get_distance(state, result)


# Функция поиска в ширину

def breadth_first_search(problem):
    node = Node(problem.initial)
    if problem.is_goal(problem.initial):
        return path_states(node), 0, 1  # 1 сгенерированный узел (начальный)

    frontier = [(0, node)]  # Приоритетная очередь: (стоимость, узел)
    reached = {problem.initial: 0}  # Отслеживаем минимальную стоимость до каждой вершины
    node_count = 1  # Счётчик узлов (начальный узел уже сгенерирован)

    while frontier:
        cost, node = heapq.heappop(frontier)  # Извлекаем узел с наименьшей стоимостью

        # Если цель достигнута
        if problem.is_goal(node.state):
            return path_states(node), cost, node_count

        # Расширяем узлы
        for child in expand(problem, node):
            s = child.state
            new_cost = cost + problem.action_cost(node.state, None, child.state)

            # Если это новый узел или более дешевый путь
            if s not in reached or new_cost < reached[s]:
                reached[s] = new_cost
                heapq.heappush(frontier, (new_cost, child))  # Добавляем узел с его стоимостью
                node_count += 1  # Увеличиваем счётчик узлов

    return failure, float('inf'), node_count  # Если решение не найдено


# Инициализация задачи
problem = TSPProblem(initial='Ставрополь', goal='Краснодар')

# Запуск поиска в ширину
route, distance, generated_nodes = breadth_first_search(problem)

print(f"Минимальный маршрут: {route}")
print(f"Расстояние: {distance} км")
print(f"Сгенерировано узлов: {generated_nodes}")
