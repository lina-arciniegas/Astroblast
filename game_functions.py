# -*- coding: utf-8 -*-
"""
game_functions.py
Funciones auxiliares para AstroBlast (menús, HUD, fondo y utilidades).
Compatible con main.py / settings.py / sprites.py.
"""

import pygame
import settings

# -----------------------------------------------------------------------------
# Tipografías y texto
# -----------------------------------------------------------------------------
_font_cache = {}

def _get_font(size):
    """Devuelve/cacha una fuente del sistema (Arial o por defecto)."""
    f = _font_cache.get(size)
    if f is None:
        try:
            f = pygame.font.SysFont("arial", size)
        except Exception:
            f = pygame.font.Font(None, size)
        _font_cache[size] = f
    return f

def display_text(screen, text, size, x, y, color=settings.WHITE, center=True):
    """Renderiza texto en (x, y). Si center=True centra en ese punto; si no, usa topleft."""
    font = _get_font(size)
    surf = font.render(text, True, color)
    rect = surf.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surf, rect)
    return rect


# -----------------------------------------------------------------------------
# Fondo (estático o con scroll vertical)
# -----------------------------------------------------------------------------
def draw_background(screen, background_image, scroll_y=None, speed=0.0):
    """
    Dibuja el fondo. Si se pasa scroll_y y speed>0, crea efecto de scroll vertical.
    Devuelve el nuevo valor de scroll_y (o el mismo si no se usa scroll).
    """
    if scroll_y is None or speed <= 0.0:
        screen.blit(background_image, (0, 0))
        return scroll_y

    h = background_image.get_height()
    scroll_y = (scroll_y + speed) % h
    screen.blit(background_image, (0, scroll_y - h))
    screen.blit(background_image, (0, scroll_y))
    return scroll_y


# -----------------------------------------------------------------------------
# Menús
# -----------------------------------------------------------------------------
def _menu_loop(screen, background_image, title, lines, title_color, enter_result, esc_result):
    """Bucle genérico para pantallas tipo menú (devuelve enter_result o esc_result)."""
    clock = pygame.time.Clock()
    blink = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return enter_result
                if event.key == pygame.K_ESCAPE:
                    return esc_result
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return enter_result  # click también inicia

        # Dibujo
        screen.blit(background_image, (0, 0))
        display_text(screen, title, 64, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 4, title_color)
        y = settings.SCREEN_HEIGHT // 2 - 20 * len(lines)
        for ln in lines:
            display_text(screen, ln, 22, settings.SCREEN_WIDTH // 2, y, settings.WHITE)
            y += 32

        # Pista parpadeante
        blink = (blink + 1) % 60
        if blink < 30:
            display_text(
                screen,
                "ENTER para continuar  |  ESC para salir",
                16,
                settings.SCREEN_WIDTH // 2,
                settings.SCREEN_HEIGHT - 28,
                (210, 210, 210),
            )

        pygame.display.flip()
        clock.tick(settings.FPS)

def show_main_menu(screen, background_image):
    """Muestra el menú principal y devuelve 'PLAYING' o 'QUIT'."""
    lines = ["Presiona ENTER para Jugar", "Presiona ESC para Salir", "Click Izquierdo también inicia"]
    return _menu_loop(screen, background_image, "ASTROBLAST", lines, settings.YELLOW, "PLAYING", "QUIT")

def show_game_over_screen(screen, score, background_image):
    """Muestra la pantalla de fin de juego y devuelve 'PLAYING' o 'QUIT'."""
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return "PLAYING"
                if event.key == pygame.K_ESCAPE:
                    return "QUIT"

        screen.blit(background_image, (0, 0))
        display_text(screen, "GAME OVER", 64, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 4, settings.RED)
        display_text(screen, f"Puntuación Final: {score}", 32, settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 - 10)
        display_text(screen, "ENTER: Reintentar    |    ESC: Salir", 20,
                     settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2 + 50, (230, 230, 230))

        pygame.display.flip()
        clock.tick(settings.FPS)


# -----------------------------------------------------------------------------
# Opcionales para refactor (si quieres mover lógica fuera del main)
# -----------------------------------------------------------------------------
def check_events(player):
    """
    Maneja eventos básicos. Devuelve 'QUIT' si se cierra la ventana; None en caso contrario.
    Dispara con ESPACIO (delegado a player.shoot()).
    NOTA: tu main.py ya procesa eventos; úsalo solo si decides refactorizar.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "QUIT"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.shoot()
    return None

def update_game_elements(all_sprites, player, enemies, bullets, score, assets=None):
    """
    Actualiza sprites y gestiona colisiones.
    Devuelve (estado, score_actualizado), donde estado es 'PLAYING' o 'GAME_OVER'.
    *No* genera enemigos (eso ya lo hace tu main.py).
    """
    # Actualización estándar
    all_sprites.update()

    # Colisión balas ↔ enemigos
    destroyed = pygame.sprite.groupcollide(enemies, bullets, True, True)
    if destroyed:
        score += 10 * len(destroyed)  # 10 puntos por enemigo destruido
        if assets and "explosion_sound" in assets:
            try:
                assets["explosion_sound"].play()
            except Exception:
                pass  # evita crashear si el mixer no está disponible

    # Colisión jugador ↔ enemigos (rectangular por defecto)
    hit_player = pygame.sprite.spritecollide(player, enemies, True)  # collide_rect
    if hit_player:
        return "GAME_OVER", score

    return "PLAYING", score

