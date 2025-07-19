import pygame, sys, random

# Initialize Game
pygame.init()

# Game State
game_state = 1
score = 0
has_moved = False

# Window Setup
window_w = 400
window_h = 600
screen = pygame.display.set_mode((window_w, window_h))
pygame.display.set_caption("Flappython")
clock = pygame.time.Clock()
fps = 60

# Load Fonts
try:
    font = pygame.font.Font("fonts/BaiJamjuree-Bold.ttf", 60)
except:
    font = pygame.font.SysFont("Arial", 60)

# Load Sounds
try:
    slap_sfx = pygame.mixer.Sound("sounds/slap.wav")
    woosh_sfx = pygame.mixer.Sound("sounds/woosh.wav")
    score_sfx = pygame.mixer.Sound("sounds/score.wav")
except:
    slap_sfx = woosh_sfx = score_sfx = None

# Load Images
player_img = pygame.image.load("images/player.png").convert_alpha()
pipe_up_img = pygame.image.load("images/pipe_up.png").convert_alpha()
pipe_down_img = pygame.image.load("images/pipe_down.png").convert_alpha()
ground_img = pygame.image.load("images/ground.png").convert_alpha()
bg_img = pygame.image.load("images/background.png").convert()
bg_width = bg_img.get_width()

# Game Variables
bg_scroll_spd = 1
ground_scroll_spd = 2


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0

    def jump(self):
        self.velocity = -10

    def update(self):
        self.velocity += 0.75  # gravity
        self.y += self.velocity

    def draw(self):
        screen.blit(player_img, (self.x, self.y))


class Pipe:
    def __init__(self, x, height, gap, velocity):
        self.x = x
        self.height = height
        self.gap = gap
        self.velocity = velocity
        self.scored = False

    def update(self):
        self.x -= self.velocity

    def draw(self):
        screen.blit(pipe_down_img, (self.x, self.height - pipe_down_img.get_height()))
        screen.blit(pipe_up_img, (self.x, self.height + self.gap))


def scoreboard():
    show_score = font.render(str(score), True, (10, 40, 9))
    score_rect = show_score.get_rect(center=(window_w // 2, 64))
    screen.blit(show_score, score_rect)


def game():
    global game_state, score, has_moved

    # Initial setup
    bg_x_pos = 0
    ground_x_pos = 0
    player = Player(168, 300)
    pipes = [Pipe(600, random.randint(30, 250), 220, 2.4)]

    while game_state != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_state = 0
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                has_moved = True
                if woosh_sfx: woosh_sfx.play()
                player.jump()

        if has_moved:
            player.update()

            # Player rectangle for collision
            player_rect = pygame.Rect(player.x, player.y, player_img.get_width(), player_img.get_height())

            for pipe in pipes:
                # Pipe hitboxes
                top_rect = pygame.Rect(pipe.x, 0, pipe_up_img.get_width(), pipe.height)
                bottom_rect = pygame.Rect(pipe.x, pipe.height + pipe.gap, pipe_up_img.get_width(), window_h)

                if player_rect.colliderect(top_rect) or player_rect.colliderect(bottom_rect):
                    # Collision detected
                    if slap_sfx: slap_sfx.play()
                    player = Player(168, 300)
                    pipes = [Pipe(600, random.randint(30, 250), 220, 2.4)]
                    score = 0
                    has_moved = False
                    break

            # Ground or sky collision
            if player.y < -64 or player.y > 536:
                if slap_sfx: slap_sfx.play()
                player = Player(168, 300)
                pipes = [Pipe(600, random.randint(30, 250), 220, 2.4)]
                score = 0
                has_moved = False

            # Update and recycle pipes
            for pipe in pipes:
                pipe.update()

            if pipes[0].x < -pipe_up_img.get_width():
                pipes.pop(0)
                pipes.append(Pipe(400, random.randint(30, 280), 220, 2.4))

            # Score logic
            for pipe in pipes:
                if not pipe.scored and pipe.x + pipe_up_img.get_width() < player.x:
                    score += 1
                    if score_sfx: score_sfx.play()
                    pipe.scored = True

        # Scroll background
        bg_x_pos -= bg_scroll_spd
        if bg_x_pos <= -bg_width:
            bg_x_pos = 0

        ground_x_pos -= ground_scroll_spd
        if ground_x_pos <= -bg_width:
            ground_x_pos = 0

        # Draw background, ground
        screen.blit(bg_img, (bg_x_pos, 0))
        screen.blit(bg_img, (bg_x_pos + bg_width, 0))
        screen.blit(ground_img, (ground_x_pos, 536))
        screen.blit(ground_img, (ground_x_pos + bg_width, 536))

        # Draw pipes and player
        for pipe in pipes:
            pipe.draw()
        player.draw()

        # Draw score
        scoreboard()

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()


# Start game
game()
