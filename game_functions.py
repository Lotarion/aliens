import sys

import pygame

from bullet import Bullet
from alien import Alien

def check_keydown_events(event, game_settings, screen, ship, bullets):
    """Реагирует на нажатие клавиш"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(game_settings, screen, ship, bullets)    
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(game_settings, screen, ship, bullets):
    """ Выпускает пулю, если максимум еще не достигнут"""
    # Создание новой пули и включение ее в группу bullets
    if len(bullets) < game_settings.bullets_allowed:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    """Реагирует на отпускание клавиш """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(game_settings, screen, ship, bullets):
    """Обрабатывает нажатия клавиш и события мыши"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def update_screen(game_settings, screen, ship, aliens, bullets):
    """Обновляет изображения на экране и отображает новый экран"""
    # При каждом проходе цикла перерисовывается экран
    screen.fill(game_settings.bg_color)
    # Все пули выводятся позади изображений корабля и пришельцев
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # Отображение последнего прорисованного экрана
    pygame.display.flip()

def update_bullets(game_settings, screen, ship, aliens, bullets):
    """ Обновляет позиции пуль и уничтожает старые пули"""
    bullets.update()

    # Удаление пуль вышедших за край экрана
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(game_settings, screen, ship, aliens, bullets)

def check_bullet_alien_collisions(game_settings, screen, ship, aliens, bullets):    
    """ Обработка коллизий пуль с пришельцами"""
    # Проверка попаданий в пришельцев
    # при обнаружении попадания удалить пулю и пришельца
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
        # Уничтожение существующих пуль и создание нового флота
        bullets.empty()
        create_fleet(game_settings, screen, ship, aliens)

def get_number_aliens_x(game_settings, alien_width):
    """ Вычисляет количество пришельцев в ряду"""
    available_space_x = game_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x

def get_number_rows(game_settings, ship_height, alien_height):
    """ Определяет количество рядов, помещающихся на экране"""
    available_space_y = (game_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(game_settings, screen, aliens, alien_number, row_number):
    """ Создает пришельца и размещает его в ряду"""
    alien = Alien(game_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(game_settings, screen, ship, aliens):
    """ Создает флот пришельцев"""
    # Создание пришельца и вычисление количества пришельцев в ряду
    # Интервал между соседними пришельцами равен одной ширине пришелшьца

    alien = Alien(game_settings, screen)
    number_aliens_x = get_number_aliens_x(game_settings, alien.rect.width)
    number_rows = get_number_rows(game_settings, ship.rect.height, alien.rect.height)

    # Создание первого ряда пришельцев
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Создание пришельца и размещеение его в ряду
            create_alien(game_settings, screen, aliens, alien_number, row_number)        

def check_fleet_edges(game_settings, aliens):
    """ Реагирует на достижение флотом края экрана"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game_settings, aliens)
            break

def change_fleet_direction(game_settings, aliens):
    """ Опускает фесь флот и меняет направление флота"""
    for alien in aliens.sprites():
        alien.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1

def update_aliens(game_settings, ship, aliens):
    """ Обновляет позиции всех пришельцев во флоте"""
    check_fleet_edges(game_settings, aliens)
    aliens.update()

    # Проверка коллизий "пришелец-корабль"
    if pygame.sprite.spritecollideany(ship, aliens):
        print("Ship hit!!!")
        