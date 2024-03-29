import pygame
from .dot import Dot

# Values to encode information in internal logic
EMPTY_BLOCK = 0
WALL_BLOCK = 1
GHOST_ONLY_BLOCK = 2

BLINKY_SPAWN_BLOCK = 3
PINKY_SPAWN_BLOCK = 4
INKY_SPAWN_BLOCK = 5
CLYDE_SPAWN_BLOCK = 6

PACMAN_SPAWN_BLOCK = 7
DOT_BLOCK = 8
SUPER_DOT_BLOCK = 9

# Colors used to encode the information in the level descriptor image
EMPTY_BLOCK_COLOR = (255, 255, 255)
WALL_BLOCK_COLOR = (0, 0, 0)
GHOST_ONLY_BLOCK_COLOR = (136, 136, 136)

BLINKY_SPAWN_BLOCK_COLOR = (221, 0, 0)
PINKY_SPAWN_BLOCK_COLOR = (255, 153, 153)
INKY_SPAWN_BLOCK_COLOR = (102, 255, 255)
CLYDE_SPAWN_BLOCK_COLOR = (255, 153, 0)

PACMAN_SPAWN_BLOCK_COLOR = (255, 255, 51)

SUPER_DOT_BLOCK_COLOR = (51, 255, 0)

spawn_blocks = [BLINKY_SPAWN_BLOCK, PINKY_SPAWN_BLOCK, INKY_SPAWN_BLOCK,
                CLYDE_SPAWN_BLOCK, PACMAN_SPAWN_BLOCK]

# Dictionaries from blocks to colors and viceversa
block_to_color_mapping = {EMPTY_BLOCK: EMPTY_BLOCK_COLOR,
                          WALL_BLOCK: WALL_BLOCK_COLOR,
                          GHOST_ONLY_BLOCK: GHOST_ONLY_BLOCK_COLOR,
                          BLINKY_SPAWN_BLOCK: BLINKY_SPAWN_BLOCK_COLOR,
                          PINKY_SPAWN_BLOCK: PINKY_SPAWN_BLOCK_COLOR,
                          INKY_SPAWN_BLOCK: INKY_SPAWN_BLOCK_COLOR,
                          CLYDE_SPAWN_BLOCK: CLYDE_SPAWN_BLOCK_COLOR,
                          PACMAN_SPAWN_BLOCK: PACMAN_SPAWN_BLOCK_COLOR,
                          SUPER_DOT_BLOCK: SUPER_DOT_BLOCK_COLOR}

color_to_block_mapping = {v: k for k, v in block_to_color_mapping.items()}

DISPLAY_WALL_BLOCK_COLOR = (0, 51, 255)
DISPLAY_EMPTY_BLOCK_COLOR = (0, 0, 0)

NUM_DIRECTIONS = 4

class Level():
    # Matrix that holds the level details
    arena = []
    arena_width = None
    arena_height = None
    screen_size = None
    dots = None

    def __init__(self, screen_size, level_file):
        self.screen_size = screen_size

        level_image = pygame.image.load(level_file)
        px_array = pygame.PixelArray(level_image)

        width = len(px_array[0])
        height = len(px_array)

        # PixelArrays are addressed [column][row]
        # arena is addressed [row][column]
        # That's why things are flipped
        self.arena_width = height
        self.arena_height = width

        self.dots = pygame.sprite.Group()

        # Read and decode level descriptor
        for row in range(self.arena_height):
            self.arena.append([])
            for col in range(self.arena_width):
                try:
                    # Have to do this "unboxing" because pygame.Color is not
                    # hashable, so it cannot be put in a dictionary
                    current_color = level_image.unmap_rgb(px_array[col][row])
                    color_tuple = (current_color.r, current_color.g,
                                   current_color.b)

                    self.arena[row].append(color_to_block_mapping[color_tuple])

                    # Puts dots in all empty blocks
                    if color_to_block_mapping[color_tuple] == EMPTY_BLOCK:
                        self.dots.add(Dot(self, 'sprites/dot.png', (row, col)))
                    if color_to_block_mapping[color_tuple] == SUPER_DOT_BLOCK:
                        self.dots.add(Dot(self, 'sprites/super-dot.png', (row, col), is_super=True))

                except KeyError:
                    raise ValueError("{0} is not a valid level descriptor\
                            image: encountered color {1}\n" .format(level_file,
                            px_array[row][col]))

    def get_position_from_arena_position(self, arena_position):
        width, height = self.screen_size
        arena_row, arena_col = arena_position

        aspect_ratio = width/self.arena_width

        return (aspect_ratio*arena_col, aspect_ratio * arena_row)

    def is_accessible(self, arena_position):
        arena_row, arena_col = arena_position
        is_wall = True if (self.arena[arena_row][arena_col] == WALL_BLOCK) else False

        return (not is_wall)

    def is_turning_point(self, arena_position):
        accessible = []
        for dir in range(NUM_DIRECTIONS):
            accessible.append(self.is_accessible(self.get_next_cell_in_direction(arena_position, dir)))

        if accessible.count(True) >= 3 or (accessible.count(True) == 2 and not((accessible[0] and accessible[2]) or (accessible[1] and accessible[3]))):
            return True
        return False

    def get_next_cell_in_direction(self, arena_position, direction):
        arena_row, arena_col = arena_position
        if direction == 0:
            arena_col += 1
        elif direction == 1:
            arena_row -= 1
        elif direction == 2:
            arena_col -= 1
        elif direction == 3:
            arena_row += 1

        # Handle loop around
        if arena_row < 0:
            arena_row = self.arena_height - 1
        elif arena_row >= self.arena_height:
            arena_row = 0

        if arena_col < 0:
            arena_col = self.arena_width - 1
        elif arena_col >= self.arena_width:
            arena_col = 0

        return (arena_row, arena_col)

    def get_pacman_spawn_position(self):
        for row in range(self.arena_height):
            for col in range(self.arena_width):
                if self.arena[row][col] == PACMAN_SPAWN_BLOCK:
                    return (row, col)

        assert False, "Pacman spawn position does not exist.\n"

    def get_blinky_spawn_position(self):
        for row in range(self.arena_height):
            for col in range(self.arena_width):
                if self.arena[row][col] == BLINKY_SPAWN_BLOCK:
                    return (row, col)

        assert False, "Blinky (red ghost) spawn position does not exist.\n"

    def get_pinky_spawn_position(self):
        for row in range(self.arena_height):
            for col in range(self.arena_width):
                if self.arena[row][col] == PINKY_SPAWN_BLOCK:
                    return (row, col)

        assert False, "Pinky (pink ghost) spawn position does not exist.\n"

    def get_inky_spawn_position(self):
        for row in range(self.arena_height):
            for col in range(self.arena_width):
                if self.arena[row][col] == INKY_SPAWN_BLOCK:
                    return (row, col)

        assert False, "Inky (blue ghost) spawn position does not exist.\n"

    def get_clyde_spawn_position(self):
        for row in range(self.arena_height):
            for col in range(self.arena_width):
                if self.arena[row][col] == CLYDE_SPAWN_BLOCK:
                    return (row, col)

        assert False, "Clyde (orange ghost) spawn position does not exist.\n"

    def get_dots(self):
        return self.dots

    def get_surface(self):

        width, height = self.screen_size
        surface = pygame.Surface((width, height))
        px_array = pygame.PixelArray(surface)

        # Sprite and arena must have same aspect ratio
        assert ((width % self.arena_width == 0) and
                (height % self.arena_height == 0) and
                (width/self.arena_width == height/self.arena_height)
               ), "Requested sprite size is incompatible with arena size.\n"

        aspect_ratio = width/self.arena_width

        # For each block in the arena
        for row in range(self.arena_height):
            for col in range(self.arena_width):
                # Use this for all blocks, unless otherwise specified
                color = DISPLAY_EMPTY_BLOCK_COLOR

                if self.arena[row][col] == WALL_BLOCK:
                    color = DISPLAY_WALL_BLOCK_COLOR

                # Draw the pixels
                for p_row in range(aspect_ratio):
                    for p_col in range(aspect_ratio):
                        px_array[aspect_ratio*col + p_col][aspect_ratio*row + p_row] = color

        return px_array.make_surface()

