from random import choice, randint

import pygame

# Инициализация PyGame
pygame.init()

# Константы для размеров
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

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
SNAKE_COLOR = (56, 142, 60)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)

# Скорость движения змейки
SPEED = 15

# Путь к фоновому изображению
BACKGROUND_IMAGE = './images/PixelBackground.png'

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля
pygame.display.set_caption('Змейка')

# Настройка времени
clock = pygame.time.Clock()


# Описание всех классов игры
class GameObject:
    """Базовый класс игры"""

    def __init__(self, body_color=None, position=SCREEN_CENTER):
        """Конструктор базового класса"""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовывания на экране"""
        pass


class Food(GameObject):
    """Дочерний класс для экземпляров еды"""

    ICON = ''

    def randomize_position(self):
        """Метод определения случайного положения еды"""
        position_x = randint(0, GRID_WIDTH - 1)
        position_y = randint(0, GRID_HEIGHT - 1)
        self.position = (position_x * GRID_SIZE, position_y * GRID_SIZE)

    def draw(self, surface):
        """Метод для отрисовывания еды на экране"""
        x_axis, y_axis = self.position
        rect = (
            pygame.Rect((x_axis, y_axis), (GRID_SIZE, GRID_SIZE))
        )
        pygame.draw.rect(surface, self.body_color, rect, 0, 4)
        food = pygame.image.load(self.ICON)
        food.set_colorkey(BLACK_COLOR)
        surface.blit(food, (x_axis + GRID_SIZE / 20, y_axis + GRID_SIZE / 20))
        pygame.draw.rect(surface, WHITE_COLOR, rect, 1, 4)


class Apple(Food):
    """Дочерний класс для экземпляров яблока"""

    ICON = './images/PixelApple.png'


class Mushroom(Food):
    """Дочерний класс для экземпляров гриба"""

    ICON = './images/PixelMushroom.png'


class Snake(GameObject):
    """Дочерний класс для экземпляров змейки"""

    def __init__(self, body_color=None, position=SCREEN_CENTER):
        """Конструктор дочернего класса для экземпляра змейки"""
        super().__init__(body_color, position)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

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


def start_position(snake, apple, mushroom_1, mushroom_2):
    """Функция определения начальных координат объектов"""
    position_list = []
    while snake.position == apple.position:
        apple.randomize_position()
    position_list.append(snake.position)
    position_list.append(apple.position)
    while mushroom_1.position in position_list:
        mushroom_1.randomize_position()
    position_list.append(mushroom_1.position)
    while mushroom_2.position in position_list:
        mushroom_2.randomize_position()
    position_list.append(mushroom_2.position)
    position_list.pop(0)
    return position_list


def speed_tweaking(length, speed):
    """Функция изменения скорости змейки"""
    if length < 15:
        a = 0
    elif 15 <= length < 30:
        a = 5
    elif 30 <= length < 50:
        a = 10
    else:
        a = 15
    clock.tick(speed + a)


def crossing_apple(snake, apple, occupied_positions):
    """Функция обработки события столкновения с яблоком"""
    if snake.positions[0] == apple.position:
        occupied_positions.remove(apple.position)
        while apple.position in occupied_positions + snake.positions:
            apple.randomize_position()
        occupied_positions.insert(0, apple.position)
        snake.length += 1


def crossing_mushroom_1(snake, mushroom_1, occupied_positions):
    """Функция обработки события столкновения с mushroom_1"""
    if snake.positions[0] == mushroom_1.position:
        occupied_positions.remove(mushroom_1.position)
        while mushroom_1.position in occupied_positions + snake.positions:
            mushroom_1.randomize_position()
        occupied_positions.insert(1, mushroom_1.position)
        if snake.length > 1:
            snake.length -= 1
            snake.positions.pop()


def crossing_mushroom_2(snake, mushroom_2, occupied_positions):
    """Функция обработки события столкновения с mushroom_2"""
    if snake.positions[0] == mushroom_2.position:
        occupied_positions.remove(mushroom_2.position)
        while mushroom_2.position in occupied_positions + snake.positions:
            mushroom_2.randomize_position()
        occupied_positions.insert(1, mushroom_2.position)
        if 1 < snake.length < 3:
            snake.length -= 1
            snake.positions.pop()
        elif snake.length >= 3:
            snake.length -= 2
            snake.positions.pop()
            snake.positions.pop()


def main():
    """Основной игровой цикл"""
    # Создание экземпляров классов
    snake = Snake(SNAKE_COLOR)
    apple = Apple(APPLE_COLOR)
    mushroom_1 = Mushroom(MUSHROOM_1_COLOR)
    mushroom_2 = Mushroom(MUSHROOM_2_COLOR)
    occupied_positions = start_position(snake, apple, mushroom_1, mushroom_2)
    while True:
        # Присваивание и изменение скорости змейки
        speed_tweaking(snake.length, SPEED)

        # Отрисовка всех элементов
        pygame.display.update()
        screen.fill(BOARD_BACKGROUND_COLOR)
        background = pygame.image.load(BACKGROUND_IMAGE)
        screen.blit(background, (0, 0))
        apple.draw(screen)
        mushroom_1.draw(screen)
        mushroom_2.draw(screen)
        snake.move()
        snake.draw(screen)
        handle_keys(snake)
        snake.update_direction()

        # Обработка событий столкновения с объектами
        crossing_apple(snake, apple, occupied_positions)
        crossing_mushroom_1(snake, mushroom_1, occupied_positions)
        crossing_mushroom_2(snake, mushroom_2, occupied_positions)


if __name__ == '__main__':
    main()
