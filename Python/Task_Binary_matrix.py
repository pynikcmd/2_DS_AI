from collections import deque


def count_islands(grid):
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    islands_count = 0

    def breadth_first_search(start_row, start_col):
        # Направления для перемещения (включая диагонали)
        directions = [
            (-1, -1), (-1, 0), (-1, 1),  # Верхние строки
            (0, -1), (0, 1),  # Горизонтально
            (1, -1), (1, 0), (1, 1)  # Нижние строки
        ]

        queue = deque([(start_row, start_col)])
        visited[start_row][start_col] = True

        while queue:
            row, col = queue.popleft()
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                # Проверка границ и посещения
                if 0 <= new_row < rows and 0 <= new_col < cols and not visited[new_row][new_col] and grid[new_row][
                    new_col] == 1:
                    visited[new_row][new_col] = True
                    queue.append((new_row, new_col))

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1 and not visited[i][j]:  # Найти новый остров
                breadth_first_search(i, j)  # Запустить BFS для данного острова
                islands_count += 1  # Увеличить счетчик островов

    return islands_count


# Пример ввода
grid1 = [
    [1, 1, 0, 0, 0],
    [0, 1, 0, 0, 1],
    [1, 0, 0, 1, 1],
    [0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1]
]

grid2 = [
    [1, 0, 0, 1],
    [0, 0, 0, 0],
    [1, 1, 0, 1],
    [0, 0, 1, 1]
]

grid3 = [
    [1, 0, 0, 0],
    [1, 0, 1, 1],
    [0, 0, 0, 0],
    [0, 1, 1, 0],
    [1, 0, 0, 1]
]

grid4 = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
]

# Подсчет островов
# Тестирование различных матриц
grids = [grid1, grid2, grid3, grid4]

for index, grid in enumerate(grids, start=1):
    result = count_islands(grid)
    print(f'Матрица {index}, Общее количество островов: {result}')
