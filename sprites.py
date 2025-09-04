# sprites.py

import pygame
import settings

class Player(pygame.sprite.Sprite):
    def __init__(self, image, all_sprites_group, bullets_group, bullet_image, shoot_sound):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = settings.SCREEN_WIDTH // 2
        self.rect.bottom = settings.SCREEN_HEIGHT - 10
        self.speedx = 0
        self.bullets_group = bullets_group
        self.all_sprites_group = all_sprites_group # Para añadir balas al grupo general
        self.bullet_image = bullet_image
        self.shoot_sound = shoot_sound
        self.last_shot = pygame.time.get_ticks()
        self.shoot_delay = 250 # Milisegundos entre disparos

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -settings.PLAYER_SPEED
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = settings.PLAYER_SPEED

        self.rect.x += self.speedx

        # Limitar el movimiento para que no salga de la pantalla
        if self.rect.right > settings.SCREEN_WIDTH:
            self.rect.right = settings.SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.bullet_image, self.rect.centerx, self.rect.top)
            self.all_sprites_group.add(bullet)
            self.bullets_group.add(bullet)
            self.shoot_sound.play()

    def draw(self, screen):
        # Esta función es en realidad manejada por all_sprites.draw(screen) en main.py
        # pero la incluimos para completar el requisito.
        screen.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedy = speed # La velocidad inicial se pasa como parámetro
        self.hp = 1 # Puntos de vida, se puede variar por tipo de enemigo

    def update(self):
        self.rect.y += self.speedy
        # Si el enemigo sale de la pantalla por abajo, lo eliminamos
        if self.rect.top > settings.SCREEN_HEIGHT:
            self.kill() # Elimina el sprite de todos los grupos a los que pertenece

    def draw(self, screen):
        # Esta función es en realidad manejada por all_sprites.draw(screen) en main.py
        screen.blit(self.image, self.rect)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y # Inicia desde la parte superior de la nave
        self.speedy = settings.BULLET_SPEED # Velocidad negativa para ir hacia arriba

    def update(self):
        self.rect.y += self.speedy
        # Si la bala sale de la pantalla por arriba, la eliminamos
        if self.rect.bottom < 0:
            self.kill()

    def draw(self, screen):
        # Esta función es en realidad manejada por all_sprites.draw(screen) en main.py
        screen.blit(self.image, self.rect)