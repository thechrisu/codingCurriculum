import pygame
from .level import NUM_DIRECTIONS

ROTATION_ANGLE = (360/NUM_DIRECTIONS)


class Character(pygame.sprite.Sprite):
    image = None
    rect = None
    next_direction = None  # right = 0, up = 1, left = 2, down = 3
    curr_direction = None
    arena_position = None  # (row, col)

    radius = 2  # For circle collision detection, do not remove;

    speed = None
    time_since_last_update = None 

    def __init__(self, level, image, scale_factor, arena_position, direction, speed):
        pygame.sprite.Sprite.__init__(self)

        self.level = level
        self.speed = speed
        self.time_since_last_update = 0

        self.image = pygame.image.load(image)
        image_width, image_height = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(image_width * scale_factor), int(image_height * scale_factor)))
        self.image = pygame.transform.rotate(self.image, direction * ROTATION_ANGLE)
        self.curr_direction = direction

        self.arena_position = arena_position
        self.rect = self.image.get_rect().move(level.get_position_from_arena_position(arena_position))

    def set_direction(self, direction):
        assert direction in range(NUM_DIRECTIONS), "pacman.character: tried to set invalid direction {}.\n".format(direction)
        self.next_direction = direction

    def get_next_cell_in_direction(self, direction):
        return self.level.get_next_cell_in_direction(self.arena_position, direction)

    def get_update_frequency(self):
        return (1000.0/self.speed)

    def update(self):
        self.update_direction()
        next_cell = self.get_next_cell_in_direction(self.curr_direction)

        if self.level.is_accessible(next_cell):
            self.arena_position = next_cell
            self.rect = self.image.get_rect().move(self.level.get_position_from_arena_position(self.arena_position))
