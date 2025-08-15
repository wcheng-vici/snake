import pygame
import random
import sys

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

FPS = 10

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow_flag = False
        
    def move(self):
        head = self.positions[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        if new_head[0] < 0 or new_head[0] >= GRID_WIDTH:
            return False
        if new_head[1] < 0 or new_head[1] >= GRID_HEIGHT:
            return False
            
        if new_head in self.positions[1:]:
            return False
            
        self.positions.insert(0, new_head)
        
        if not self.grow_flag:
            self.positions.pop()
        else:
            self.grow_flag = False
            
        return True
        
    def change_direction(self, direction):
        if direction[0] * -1 != self.direction[0] or direction[1] * -1 != self.direction[1]:
            self.direction = direction
            
    def grow(self):
        self.grow_flag = True
        
    def get_head(self):
        return self.positions[0]

class Food:
    def __init__(self):
        self.position = None
        self.randomize_position()
        
    def randomize_position(self, snake_positions=None):
        while True:
            self.position = (random.randint(0, GRID_WIDTH - 1), 
                           random.randint(0, GRID_HEIGHT - 1))
            if snake_positions is None or self.position not in snake_positions:
                break

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Retro Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.reset_game()
        
    def reset_game(self):
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.speed = FPS
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                    elif event.key == pygame.K_ESCAPE:
                        return False
                else:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction((1, 0))
                    elif event.key == pygame.K_ESCAPE:
                        return False
        return True
        
    def update(self):
        if not self.game_over:
            if not self.snake.move():
                self.game_over = True
                return
                
            if self.snake.get_head() == self.food.position:
                self.snake.grow()
                self.score += 10
                self.food.randomize_position(self.snake.positions)
                
                if self.score % 50 == 0 and self.speed < 20:
                    self.speed += 1
                    
    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, DARK_GREEN, (x, 0), (x, WINDOW_HEIGHT), 1)
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            pygame.draw.line(self.screen, DARK_GREEN, (0, y), (WINDOW_WIDTH, y), 1)
            
    def draw(self):
        self.screen.fill(BLACK)
        
        self.draw_grid()
        
        for position in self.snake.positions:
            rect = pygame.Rect(position[0] * CELL_SIZE, position[1] * CELL_SIZE,
                              CELL_SIZE - 2, CELL_SIZE - 2)
            pygame.draw.rect(self.screen, GREEN, rect)
            pygame.draw.rect(self.screen, DARK_GREEN, rect, 2)
            
        food_rect = pygame.Rect(self.food.position[0] * CELL_SIZE,
                               self.food.position[1] * CELL_SIZE,
                               CELL_SIZE - 2, CELL_SIZE - 2)
        pygame.draw.rect(self.screen, RED, food_rect)
        pygame.draw.rect(self.screen, WHITE, food_rect, 2)
        
        score_text = f"Score: {self.score}"
        for i, char in enumerate(score_text):
            if i < self.screen.cell_width:
                self.screen.buffer[0][i] = char
        
        if self.game_over:
            game_over_text = "GAME OVER"
            restart_text = "Press SPACE to restart or ESC to quit"
            
            y_center = self.screen.cell_height // 2
            x_center = self.screen.cell_width // 2
            
            go_start = x_center - len(game_over_text) // 2
            for i, char in enumerate(game_over_text):
                if 0 <= go_start + i < self.screen.cell_width and y_center - 1 >= 0:
                    self.screen.buffer[y_center - 1][go_start + i] = char
                    
            restart_start = x_center - len(restart_text) // 2
            for i, char in enumerate(restart_text):
                if 0 <= restart_start + i < self.screen.cell_width and y_center + 1 < self.screen.cell_height:
                    self.screen.buffer[y_center + 1][restart_start + i] = char
            
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.speed)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()