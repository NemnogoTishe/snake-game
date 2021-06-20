import pygame
import sys
import random

pygame.init()

block_size = 20
count_rect = 20

"""background color"""
bkcolor = (0, 255, 144)
rect_color = (255, 255, 255)
BLUE = (204, 255, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
snake_color = (0, 0, 255)
margin = 2
head_margin = 50
"""screensize"""
size = [block_size * count_rect + 2 * block_size + margin * count_rect,
        block_size * count_rect + 2 * block_size + margin * count_rect + head_margin]
""""""
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Змейка')

timer = pygame.time.Clock()
courier = pygame.font.SysFont('courier', 36)


class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def inside(self):
        return 0 <= self.x < block_size and 0 <= self.y < block_size

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


def rand_emp_block():
    x = random.randint(0, count_rect - 1)
    y = random.randint(0, count_rect - 1)
    emp_block = SnakeBlock(x, y)
    while emp_block in snake_blocks:
        emp_block.x = random.randint(0, count_rect - 1)
        emp_block.y = random.randint(0, count_rect - 1)
    return emp_block


def draw_block(color, row, column):
    pygame.draw.rect(screen, color, [block_size + column * block_size + margin * (column + 1),
                                     head_margin + block_size + row * block_size + margin * (row + 1),
                                     block_size,
                                     block_size])


snake_blocks = [SnakeBlock(9, 8), SnakeBlock(9, 9)]
apple = rand_emp_block()
d_row = 0
d_col = 1
total = 0
# start game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and d_col != 0:
                d_row = -1
                d_col = 0
            elif event.key == pygame.K_DOWN and d_col != 0:
                d_row = 1
                d_col = 0
            elif event.key == pygame.K_LEFT and d_row != 0:
                d_row = 0
                d_col = -1
            elif event.key == pygame.K_RIGHT and d_row != 0:
                d_row = 0
                d_col = 1

    screen.fill(bkcolor)
    text_total = courier.render(f'Total: {total}', 0, WHITE)
    screen.blit(text_total, (block_size, block_size))
    for row in range(count_rect):
        for column in range(count_rect):
            if (row + column) % 2 == 0:
                color = BLUE
            else:
                color = rect_color
            draw_block(color, row, column)

    head = snake_blocks[-1]
    if not head.inside():
        print('exit')
        pygame.quit()

    draw_block(RED, apple.x, apple.y)
    for block in snake_blocks:
        draw_block(snake_color, block.x, block.y)

    if apple == head:
        total += 1
        snake_blocks.append(apple)
        apple = rand_emp_block()

    for block in snake_blocks:
        draw_block(snake_color, block.x, block.y)

    new_head = SnakeBlock(head.x + d_row, head.y + d_col)
    snake_blocks.append(new_head)
    snake_blocks.pop(0)

    pygame.display.flip()
    timer.tick(10)
