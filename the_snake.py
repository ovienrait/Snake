from random import choice, randint

import pygame

# Инициализация PyGame
pygame.init()

# Константы для размеров
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Константы для цветов
BOARD_BACKGROUND_COLOR = (69, 71, 54)
APPLE_COLOR = (228, 138, 70)
MUSHROOM_1_COLOR = (143, 82, 152)
MUSHROOM_2_COLOR = (41, 108, 149)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)

# Скорость движения змейки
SPEED = 15

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля
pygame.display.set_caption('Змейка')

# Настройка времени
clock = pygame.time.Clock()


# Описание всех классов игры
class GameObject:
    """Базовый класс игры"""

    def __init__(self, position_x=None, position_y=None, body_color=None):
        """Конструктор базового класса"""
        self.position = (position_x, position_y)
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовывания на экране"""
        pass


class Apple(GameObject):
    """Дочерний класс для экземпляров яблока"""

    def __init__(self, body_color=None):
        """Конструктор дочернего класса для экземпляра яблока"""
        self.body_color = body_color
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод определения случайного положения яблока"""
        position_x = randint(0, GRID_WIDTH - 1)
        position_y = randint(0, GRID_HEIGHT - 1)
        return (position_x * GRID_SIZE), (position_y * GRID_SIZE)

    def draw(self, surface):
        """Метод для отрисовывания яблока на экране"""
        x_axis = self.position[0]
        y_axis = self.position[1]
        rect = (
            pygame.Rect((x_axis, y_axis), (GRID_SIZE, GRID_SIZE))
        )
        pygame.draw.rect(surface, self.body_color, rect, 0, 4)
        apple = pygame.image.load('./images/PixelApple.png')
        apple.set_colorkey((0, 0, 0))
        surface.blit(apple, (x_axis + GRID_SIZE / 20, y_axis + GRID_SIZE / 20))
        pygame.draw.rect(surface, (255, 255, 255), rect, 1, 4)


class Mushroom(Apple):
    """Дочерний класс для экземпляров гриба"""

    def draw(self, surface):
        """Метод для отрисовывания яблока на экране"""
        x_axis = self.position[0]
        y_axis = self.position[1]
        rect = (
            pygame.Rect((x_axis, y_axis), (GRID_SIZE, GRID_SIZE))
        )
        pygame.draw.rect(surface, self.body_color, rect, 0, 4)
        mushroom = pygame.image.load('./images/PixelMushroom.png')
        mushroom.set_colorkey(BLACK_COLOR)
        surface.blit(mushroom,
                     (x_axis + GRID_SIZE / 20, y_axis + GRID_SIZE / 20)
                     )
        pygame.draw.rect(surface, WHITE_COLOR, rect, 1, 4)


class Snake(GameObject):
    """Дочерний класс для экземпляров змейки"""

    def __init__(self):
        """Конструктор дочернего класса для экземпляра змейки"""
        self.length = 1
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = (56, 142, 60)

    def update_direction(self):
        """Метод для обновления направления движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод для обновления позиции змейки"""
        head_position = self.get_head_position()
        dx = self.direction[0] * GRID_SIZE
        dy = self.direction[1] * GRID_SIZE
        new_x = head_position[0] + dx
        if new_x >= SCREEN_WIDTH:
            new_x -= SCREEN_WIDTH
        elif new_x < 0:
            new_x += SCREEN_WIDTH
        new_y = head_position[1] + dy
        if new_y >= SCREEN_HEIGHT:
            new_y -= SCREEN_HEIGHT
        elif new_y < 0:
            new_y += SCREEN_HEIGHT
        new_head_position = (new_x, new_y)
        if new_head_position in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, (new_x, new_y))
            if len(self.positions) > self.length:
                self.positions.pop()

    def draw(self, surface):
        """Метод для отрисовывания змейки на экране"""
        for position in self.positions:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect, 0, 6)
            pygame.draw.rect(surface, (255, 255, 255), rect, 1, 6)

        # Отрисовка головы змейки
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect, 0, 6)
        pygame.draw.rect(surface, (255, 255, 255), head_rect, 1, 6)

    def get_head_position(self):
        """Метод для возвращения позиции головы змейки"""
        return self.positions[0]

    def reset(self):
        """Метод для сбрасывания змейки в начальное состояние"""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Функция для обработки нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():  # noqa: max-complexity=13
    """Основной игровой цикл"""
    # Создание экземпляров классов
    snake = Snake()
    apple = Apple(APPLE_COLOR)
    mushroom_1 = Mushroom(MUSHROOM_1_COLOR)
    mushroom_2 = Mushroom(MUSHROOM_2_COLOR)
    pos_1, pos_2 = snake.positions[0], apple.position
    pos_3, pos_4 = mushroom_1.position, mushroom_2.position
    pos_list_1 = [pos_2, pos_3, pos_4]
    pos_list_2 = [pos_3, pos_4]
    while pos_1 in pos_list_1 or pos_2 in pos_list_2 or pos_3 == pos_4:
        apple.position = apple.randomize_position()
        mushroom_1.position = mushroom_1.randomize_position()
        mushroom_2.position = mushroom_2.randomize_position()
    occupied_positions = pos_list_1

    while True:
        # Присваивание и изменение скорости змейки
        if snake.length < 15:
            a = 0
        elif 15 <= snake.length < 30:
            a = 5
        elif 30 <= snake.length < 50:
            a = 10
        else:
            a = 15
        clock.tick(SPEED + a)

        # Отрисовка всех элементов
        pygame.display.update()
        screen.fill(BOARD_BACKGROUND_COLOR)
        background = pygame.image.load('./images/PixelBackground.png')
        screen.blit(background, (0, 0))
        apple.draw(screen)
        mushroom_1.draw(screen)
        mushroom_2.draw(screen)
        snake.move()
        snake.draw(screen)
        handle_keys(snake)
        snake.update_direction()

        # Обработка события столкновения с яблоком
        if snake.positions[0] == apple.position:
            occupied_positions.remove(apple.position)
            while apple.position in occupied_positions + snake.positions:
                apple.position = apple.randomize_position()
            occupied_positions.insert(0, apple.position)
            snake.length += 1

        # Обработка события столкновения с mushroom_1
        if snake.positions[0] == mushroom_1.position:
            occupied_positions.remove(mushroom_1.position)
            while mushroom_1.position in occupied_positions + snake.positions:
                mushroom_1.position = mushroom_1.randomize_position()
            occupied_positions.insert(1, mushroom_1.position)
            if snake.length > 1:
                snake.length -= 1
                snake.positions.pop()

        # Обработка события столкновения с mushroom_2
        if snake.positions[0] == mushroom_2.position:
            occupied_positions.remove(mushroom_2.position)
            while mushroom_2.position in occupied_positions + snake.positions:
                mushroom_2.position = mushroom_2.randomize_position()
            occupied_positions.insert(1, mushroom_2.position)
            if 1 < snake.length < 3:
                snake.length -= 1
                snake.positions.pop()
            elif snake.length >= 3:
                snake.length -= 2
                snake.positions.pop()
                snake.positions.pop()


if __name__ == '__main__':
    main()
