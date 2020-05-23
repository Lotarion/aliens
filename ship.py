import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, game_settngs, screen):
        """Инициализирует корабль и задает его начальную позицию"""
        super().__init__()
        self.screen = screen
        self.game_settings = game_settngs

        # Загрузка изображения корабля
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # Каждый новый корабль появляется у нижнего экрана
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # Сохранение вещественной координаты центра корабля
        self.center = float(self.rect.centerx)
        # флаг перемещения
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Обновляет позицию корабля с учетом флага"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.game_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.game_settings.ship_speed_factor
        # Обновление атрибута rect на основании self.center
        self.rect.centerx = int(self.center)

    def blitme(self):
        """Рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)
        
    def center_ship(self):
        """ Размещает корабль в центре нижней стороны"""
        self.center = self.screen_rect.centerx
        