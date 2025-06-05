import pygame
import sys
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)

TOWER_COST = 100
TOWER_RADIUS = 20
TOWER_RANGE = 150
TOWER_FIRE_RATE = 1000
BULLET_SPEED = 4
BULLET_RADIUS = 5
BULLET_COLOR = BLACK
BULLET_DAMAGE = 10

ENEMY_SIZE = 20
ENEMY_COLOR = RED
ENEMY_HEALTH = 30
ENEMY_SPEED = 1.0
ENEMIES_PER_WAVE = 5
SPAWN_INTERVAL = 1000

COIN_REWARD_PER_WAVE = 50
PLAYER_MAX_HEALTH = 100
HEALTH_PENALTY_PER_LEAK = 10
PLACEMENT_TIME = 30000

PATH = [
    (0, SCREEN_HEIGHT // 2),
    (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2),
    (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3),
    (SCREEN_WIDTH * 2 // 3, SCREEN_HEIGHT // 3),
    (SCREEN_WIDTH * 2 // 3, SCREEN_HEIGHT * 2 // 3),
    (SCREEN_WIDTH, SCREEN_HEIGHT * 2 // 3),
]


class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.last_shot = 0

    def in_range(self, enemy):
        dx = enemy.x - self.x
        dy = enemy.y - self.y
        return dx * dx + dy * dy <= TOWER_RANGE * TOWER_RANGE

    def shoot(self, enemies, bullets, current_time):
        if current_time - self.last_shot < TOWER_FIRE_RATE:
            return
        for enemy in enemies:
            if self.in_range(enemy):
                dx = enemy.x - self.x
                dy = enemy.y - self.y
                dist = math.hypot(dx, dy)
                if dist == 0:
                    direction = (0, 0)
                else:
                    direction = (dx / dist, dy / dist)
                bullets.append(Bullet(self.x, self.y, direction))
                self.last_shot = current_time
                break


class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.dx = direction[0] * BULLET_SPEED
        self.dy = direction[1] * BULLET_SPEED

    def update(self):
        self.x += self.dx
        self.y += self.dy


class Enemy:
    def __init__(self):
        self.path = PATH
        self.path_index = 0
        self.x, self.y = self.path[0]
        self.health = ENEMY_HEALTH

    def update(self):
        if self.path_index + 1 >= len(self.path):
            return
        target_x, target_y = self.path[self.path_index + 1]
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            self.path_index += 1
        else:
            step = min(ENEMY_SPEED, dist)
            self.x += dx / dist * step
            self.y += dy / dist * step
            if step == dist:
                self.path_index += 1


def main():
    global ENEMY_SPEED
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tower Defense")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    big_font = pygame.font.SysFont(None, 48)

    state = "start"
    wave = 1
    coins = 300
    health = PLAYER_MAX_HEALTH

    towers = []
    enemies = []
    bullets = []

    placement_start = None

    enemies_to_spawn = 0
    spawned = 0
    last_spawn = 0

    running = True
    while running:
        dt = clock.tick(FPS)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == "start":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    start_rect = pygame.Rect(
                        SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50
                    )
                    if start_rect.collidepoint(mx, my):
                        state = "placing"
                        placement_start = current_time
            elif state == "placing":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    if coins >= TOWER_COST:
                        towers.append(Tower(mx, my))
                        coins -= TOWER_COST

        screen.fill(WHITE)

        if state == "start":
            title_surf = big_font.render("Tower Defense", True, BLACK)
            screen.blit(
                title_surf,
                title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)),
            )
            start_rect = pygame.Rect(
                SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 200, 50
            )
            pygame.draw.rect(screen, GREEN, start_rect)
            start_text = font.render("Start Game", True, BLACK)
            screen.blit(start_text, start_text.get_rect(center=start_rect.center))

        elif state == "placing":
            time_left = max(0, PLACEMENT_TIME - (current_time - placement_start))
            if time_left == 0 or coins < TOWER_COST:
                state = "wave"
                enemies_to_spawn = wave * ENEMIES_PER_WAVE
                spawned = 0
                last_spawn = current_time
            else:
                pygame.draw.lines(screen, GRAY, False, PATH, 5)
                for tower in towers:
                    pygame.draw.circle(screen, BLUE, (int(tower.x), int(tower.y)), TOWER_RADIUS)
                wave_text = font.render(f"Wave: {wave}", True, BLACK)
                coins_text = font.render(f"Coins: {coins}", True, BLACK)
                timer_text = font.render(
                    f"Time Left: {time_left // 1000}", True, BLACK
                )
                screen.blit(wave_text, (10, 10))
                screen.blit(coins_text, (10, 30))
                screen.blit(timer_text, (10, 50))

        elif state == "wave":
            if spawned < enemies_to_spawn and current_time - last_spawn >= SPAWN_INTERVAL:
                enemies.append(Enemy())
                spawned += 1
                last_spawn = current_time
            for enemy in enemies[:]:
                prev_index = enemy.path_index
                enemy.update()
                if prev_index + 1 >= len(enemy.path) and enemy.path_index + 1 >= len(enemy.path):
                    health -= HEALTH_PENALTY_PER_LEAK
                    enemies.remove(enemy)
                else:
                    pygame.draw.circle(screen, ENEMY_COLOR, (int(enemy.x), int(enemy.y)), ENEMY_SIZE)
            for tower in towers:
                tower.shoot(enemies, bullets, current_time)
                pygame.draw.circle(screen, BLUE, (int(tower.x), int(tower.y)), TOWER_RADIUS)
                pygame.draw.circle(screen, GRAY, (int(tower.x), int(tower.y)), TOWER_RANGE, 1)
            for bullet in bullets[:]:
                bullet.update()
                pygame.draw.circle(
                    screen, BULLET_COLOR, (int(bullet.x), int(bullet.y)), BULLET_RADIUS
                )
                for enemy in enemies[:]:
                    if math.hypot(bullet.x - enemy.x, bullet.y - enemy.y) <= ENEMY_SIZE:
                        enemy.health -= BULLET_DAMAGE
                        if enemy.health <= 0:
                            enemies.remove(enemy)
                        bullets.remove(bullet)
                        break
            pygame.draw.lines(screen, GRAY, False, PATH, 5)
            wave_text = font.render(f"Wave: {wave}", True, BLACK)
            coins_text = font.render(f"Coins: {coins}", True, BLACK)
            health_text = font.render(f"Health: {health}", True, BLACK)
            screen.blit(wave_text, (10, 10))
            screen.blit(coins_text, (10, 30))
            screen.blit(health_text, (10, 50))

            if spawned >= enemies_to_spawn and not enemies:
                if health > 0:
                    coins += COIN_REWARD_PER_WAVE
                    ENEMY_SPEED += 0.1
                    wave += 1
                    health = PLAYER_MAX_HEALTH
                    state = "placing"
                    placement_start = current_time
            if health <= 0:
                state = "gameover"

        elif state == "gameover":
            over_text = big_font.render("Game Over", True, RED)
            screen.blit(
                over_text,
                over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)),
            )
            sub_text = font.render("Press any key to exit", True, BLACK)
            screen.blit(
                sub_text,
                sub_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)),
            )
            pygame.display.flip()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.QUIT):
                        waiting = False
                        running = False
                clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()