# main.py

import pygame
import sys
import random
import os

# Importar los módulos del juego
import settings
import sprites
import game_functions

# --- Inicialización ---
pygame.init()
pygame.mixer.init()

# Configurar la pantalla
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
pygame.display.set_caption("AstroBlast")

# Reloj para controlar la velocidad del juego
clock = pygame.time.Clock()

# --- Carga de Recursos (Imágenes y Sonidos) ---
def load_assets():
    assets = {}
    # Directorios
    img_dir = os.path.join(os.path.dirname(__file__), "assets", "img")
    snd_dir = os.path.join(os.path.dirname(__file__), "assets", "snd")

    # Cargar imágenes
    assets["player_img"] = pygame.image.load(os.path.join(img_dir, "player_ship.png")).convert_alpha()
    assets["player_img"] = pygame.transform.scale(assets["player_img"], (50, 50)) # Ajusta el tamaño si es necesario

    assets["bullet_img"] = pygame.image.load(os.path.join(img_dir, "laser_red.png")).convert_alpha()
    assets["bullet_img"] = pygame.transform.scale(assets["bullet_img"], (10, 30))

    assets["enemy_img_basic"] = pygame.image.load(os.path.join(img_dir, "enemy_ship.png")).convert_alpha()
    assets["enemy_img_basic"] = pygame.transform.scale(assets["enemy_img_basic"], (40, 40))

    assets["background"] = pygame.image.load(os.path.join(img_dir, "background.jpeg")).convert()
    assets["background"] = pygame.transform.scale(assets["background"], (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    # Cargar sonidos
    assets["shoot_sound"] = pygame.mixer.Sound(os.path.join(snd_dir, "laser_sound.mp3"))
    assets["explosion_sound"] = pygame.mixer.Sound(os.path.join(snd_dir, "explosion_sound.mp3"))
    # Música de fondo
    pygame.mixer.music.load(os.path.join(snd_dir, "background_music.mp3"))
    pygame.mixer.music.set_volume(0.4) # Ajusta el volumen

    return assets

ASSETS = load_assets()

# --- Función Principal del Juego ---
def game_loop():
    # Grupos de sprites
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    # Jugador
    player = sprites.Player(ASSETS["player_img"], all_sprites, bullets, ASSETS["bullet_img"], ASSETS["shoot_sound"])
    all_sprites.add(player)

    score = 0
    game_over = False
    last_enemy_spawn_time = pygame.time.get_ticks()

    pygame.mixer.music.play(-1) # Reproducir música de fondo en bucle

    while not game_over:
        # Controlar la velocidad de fotogramas
        clock.tick(settings.FPS)

        # 1. Procesamiento de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT" # Señal para salir del juego
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # 2. Actualizar
        # Generar enemigos automáticamente
        now = pygame.time.get_ticks()
        if now - last_enemy_spawn_time > settings.ENEMY_SPAWN_INTERVAL:
            enemy_x = random.randrange(settings.SCREEN_WIDTH - ASSETS["enemy_img_basic"].get_width())
            enemy = sprites.Enemy(ASSETS["enemy_img_basic"], enemy_x, -ASSETS["enemy_img_basic"].get_height(), settings.ENEMY_SPEED_MIN)
            all_sprites.add(enemy)
            enemies.add(enemy)
            last_enemy_spawn_time = now

        all_sprites.update()

        # Colisiones: Balas vs Enemigos
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 10 # Puntos por cada enemigo destruido
            ASSETS["explosion_sound"].play()
            # Crear un nuevo enemigo para reemplazar al destruido (o dejar que el spawn lo haga)
            # enemy_x = random.randrange(settings.SCREEN_WIDTH - ASSETS["enemy_img_basic"].get_width())
            # enemy = sprites.Enemy(ASSETS["enemy_img_basic"], enemy_x, -ASSETS["enemy_img_basic"].get_height(), settings.ENEMY_SPEED_MIN)
            # all_sprites.add(enemy)
            # enemies.add(enemy)

        # Colisiones: Jugador vs Enemigos
        hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
        if hits:
            game_over = True # El juego termina si el jugador colisiona con un enemigo

        # 3. Dibujar
        screen.fill(settings.BLACK)
        screen.blit(ASSETS["background"], (0, 0)) # Dibujar fondo

        all_sprites.draw(screen)

        # Dibujar puntuación
        game_functions.display_text(screen, f"Score: {score}", 24, settings.SCREEN_WIDTH // 2, 10)

        # Actualizar la pantalla
        pygame.display.flip()

    return "GAME_OVER", score # Devolver el estado y la puntuación final

# --- Bucle Principal del Juego (Gestión de Estados) ---
def main():
    game_state = "MENU"
    final_score = 0

    while True:
        if game_state == "MENU":
            game_state = game_functions.show_main_menu(screen, ASSETS["background"])
        elif game_state == "PLAYING":
            result, score = game_loop() # Iniciar el bucle de juego
            if result == "QUIT":
                break # Salir del bucle principal si se pide salir del juego
            game_state = result
            final_score = score
        elif game_state == "GAME_OVER":
            game_state = game_functions.show_game_over_screen(screen, final_score, ASSETS["background"])

        if game_state == "QUIT":
            break # Salir completamente si el estado es QUIT

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()