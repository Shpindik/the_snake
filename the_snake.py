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

    def __init__(self, position):
        self.position = position

    def draw(self):
        """Метод отрисовки обьекта на игровом поле"""
        pass


class Apple(GameObject):
    """Метод отрисовки яблока на игровом поле"""

    def draw(self):
        """Метод отрисовки яблока на игровом поле"""
        rect = pygame.Rect(
            self.position[0], self.position[1],
            GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(screen, APPLE_COLOR, rect)


class Snake(GameObject):
    """Конструктор класса змейки"""

    def __init__(self, position=(0,0)):
        super().__init__(position)
        self.positions = [position]
        self.direction = RIGHT
        self.next_direction = None

    def move(self, apple):
        """Метод перемещения змейки по игровому полю"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        # Получаем позицию змейки
        x, y = self.positions[0]

        # Вычисляем новую позицию змейки
        x += self.direction[0] * GRID_SIZE
        y += self.direction[1] * GRID_SIZE

        # Обновляем позицию змейки при пересечении границ экрана
        x %= SCREEN_WIDTH
        y %= SCREEN_HEIGHT

        # Проверяем столкновение с хвостом змейки
        if (x, y) in self.positions[1:]:
            print("Змейка съела сама себя!")
            pygame.quit()
            sys.exit()

        # Обновляем позицию головы змейки
        self.positions.insert(0, (x, y))

        # Проверяем, съела ли змейка яблоко
        if self.positions[0] == apple.position:
            apple.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            self.grow()

        # Удаляем последний сегмент, чтобы длина змейки оставалась постоянной
        else:
            self.positions.pop()

    def grow(self):
        """Метод увелечения длинны после съедания яблока"""
        tail = self.positions[-1]
        x, y = tail
        dx, dy = self.direction
        self.positions.append((x - dx * GRID_SIZE, y - dy * GRID_SIZE))
        # Удаляем последний сегмент, чтобы длина змейки оставалась постоянной
        self.positions.pop()

    def draw(self):
        """Метод отрисовки змейки на игровом поле"""
        for pos in self.positions:
            rect = pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(screen, SNAKE_COLOR, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_case(snake):
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


def main():
    """Описываем логику игры"""
    apple = Apple((randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                  randint(0, GRID_HEIGHT - 1) * GRID_SIZE))

    pygame.init()
    apple = Apple(
        (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
         randint(0, GRID_HEIGHT - 1) * GRID_SIZE))
    snake = Snake((20, 240))

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        handle_case(snake)

        # Двигаем змейку
        snake.move(apple)

# Проверяем на столкновения или другие игровые события (пока не реализовано)

        # Рисуем объекты
        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
