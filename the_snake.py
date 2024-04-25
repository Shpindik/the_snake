from random import randint

import pygame
import sys

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

# Тут опишите все классы игры.


class GameObject:
    """Конструктор класса"""

    def __init__(self, position=(0, 0)):
        self.position = position
        self.body_color = (0, 0, 0)

    def draw(self):
        """Метод отрисовки обьекта на игровом поле"""
        raise NotImplementedError

    def get_rectangle(self, position, color, width):
        """Метод возвращает прямоугольник"""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect, width)


class Apple(GameObject):
    """Метод отрисовки яблока на игровом поле"""

    def __init__(self, position=(0, 0)):
        super().__init__(position)
        self.body_color = APPLE_COLOR

    def draw(self):
        """Метод отрисовки яблока на игровом поле"""
        self.get_rectangle(self.position, self.body_color, 0)

    def randomize_position(self, occupied_positions):
        """Метод рандомизации позиции яблока"""
        while True:
            pos = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                   randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if (pos) not in occupied_positions:
                self.position = (pos)
                break


class Snake(GameObject):
    """Конструктор класса змейки"""

    def __init__(self, position=(0, 0)):
        super().__init__(position)
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR

    def move(self, apple):
        """Метод перемещения змейки по игровому полю"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        # Получаем позицию змейки
        position = self.get_head_position()

        # Вычисляем новую позицию змейки
        dx, dy = self.direction
        position = (position[0] + dx * GRID_SIZE,
                    position[1] + dy * GRID_SIZE)

        # Обновляем позицию змейки при пересечении границ экрана
        position = (position[0] % SCREEN_WIDTH, position[1] % SCREEN_HEIGHT)

        # Обновляем позицию головы змейки
        self.positions.insert(0, (position))

    def grow(self):
        """Метод увелечения длинны после съедания яблока"""
        tail = self.positions[-1]
        x, y = tail
        dx, dy = self.direction
        self.positions.append((x - dx * GRID_SIZE, y - dy * GRID_SIZE))
        self.positions.pop()

    def draw(self):
        """Метод отрисовки змейки на игровом поле"""
        for pos in self.positions:
            rect = pygame.Rect(pos, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def reset(self):
        """Метод сброса змейки"""
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Метод обновления направления движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Метод получения позиции головы змейки"""
        return self.positions[0]


def handle_keys(snake):
    """Описываем логику обработки событий"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


def main():
    """Описываем логику игры"""
    pygame.init()
    apple = Apple()
    snake = Snake((20, 240))
    apple.randomize_position(snake.position)

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_keys(snake)

        # Двигаем змейку
        snake.move(apple)

        # Проверяем, съела ли змейка яблоко
        if snake.get_head_position() == apple.position:
            apple.randomize_position(snake.position)
            snake.grow()
        # Удаляем последний сегмент, чтобы длина змейки оставалась постоянной
        else:
            snake.positions.pop()

        # Проверяем, столкнулась ли змейка с собой
        if snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            apple.randomize_position(snake.position)


# Проверяем на столкновения или другие игровые события (пока не реализовано)

        # Рисуем объекты
        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
