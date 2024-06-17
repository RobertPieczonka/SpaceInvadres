import pygame
import random

# Inicjalizacja pygame
pygame.init()

# Ustawienia okna gry
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Gracz
player_image = pygame.Surface((50, 50))
player_image.fill(WHITE)
player_rect = player_image.get_rect(center=(WIDTH // 2, HEIGHT - 50))
player_speed = 5

# Obcy
enemy_image = pygame.Surface((50, 50))
enemy_image.fill(WHITE)
enemies = []
for _ in range(10):
    enemy_rect = enemy_image.get_rect(x=random.randint(0, WIDTH - 50), y=random.randint(50, 200))
    enemies.append(enemy_rect)
enemy_speed = 2

# Strzały gracza
bullet_image = pygame.Surface((5, 20))
bullet_image.fill(WHITE)
bullets = []
bullet_speed = 7

# Funkcje pomocnicze
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

# Główna pętla gry
clock = pygame.time.Clock()
running = True
game_over = False
while running:
    WINDOW.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and player_rect.x < WIDTH - player_rect.width:
            player_rect.x += player_speed
        elif keys[pygame.K_LEFT] and player_rect.x > 0:
            player_rect.x -= player_speed

        # Ruch obcych
        for enemy in enemies:
            enemy.y += enemy_speed
            if enemy.y >= HEIGHT:
                enemy.y = random.randint(-200, -50)
                enemy.x = random.randint(0, WIDTH - 50)

        # Strzały obcych (fikcyjne, w tej wersji nie ma strzałów obcych)
        for enemy in enemies:
            if random.randint(0, 1000) < 10:
                bullet_rect = pygame.Rect(enemy.x + 25, enemy.y + 50, 5, 20)
                bullets.append(bullet_rect)

        # Ruch strzałów
        for bullet in bullets:
            bullet.y += bullet_speed
            if bullet.y > HEIGHT:
                bullets.remove(bullet)

        # Kolizje strzałów gracza z obcymi
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)

        # Kolizja gracza z obcymi
        for enemy in enemies:
            if enemy.colliderect(player_rect):
                game_over = True

        # Rysowanie elementów gry
        WINDOW.blit(player_image, player_rect)
        for enemy in enemies:
            WINDOW.blit(enemy_image, enemy)
        for bullet in bullets:
            pygame.draw.rect(WINDOW, WHITE, bullet)

    else:
        draw_text("GAME OVER", pygame.font.Font(None, 64), WHITE, WINDOW, WIDTH // 2, HEIGHT // 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
