import pygame
import sys
import random

pygame.init()  # pygame Başlat

# müzik ayarları
pygame.mixer.init()  # mixer başlat
pygame.mixer.music.load('snake.mp3')  # arka plan müziği yükle
pygame.mixer.music.play(-1)  # müziği sonsuz döngüde çal
pygame.mixer.music.set_volume(0.5)  # müzik ses seviyesi

# ekran boyutu
width, height = 600, 400  # boyutu
screen = pygame.display.set_mode((width, height))  # ekran oluştur
pygame.display.set_caption("🐍 Snake Game")  # pencere başlığı

# renk tanımlamaları
GREEN = (170, 215, 81)  # açık yeşil
DARK_GREEN = (0, 100, 0)  # koyu yeşil
RED = (255, 0, 0)  # kırmızı
WHITE = (255, 255, 255)  # beyaz
BLACK = (0, 0, 0)  # siyah
GRAY = (60, 60, 60)  # gri

# FPS
clock = pygame.time.Clock()  # saat oluştur
snake_speed = 10  # yılan hızı

# yılanın başlangıç konumu ve boyutu
snake_pos = [100, 50]  # yılanın kafa pozisyonu
snake_body = [[100, 50], [90, 50], [80, 50]]  # yılanın vücut parçaları
snake_direction = 'RIGHT'  # yılanın ilk yönü

# yem tanımlama
food_pos = [random.randrange(1, (width//10)) * 10,
            random.randrange(1, (height//10)) * 10]  # rastgele yem pozisyonu
food_spawn = True  # yem mevcut mu

score = 0  # skor başlangıcı

font = pygame.font.SysFont('arial', 25)  # normal yazı tipi
game_over_font = pygame.font.SysFont('arial', 40, True)  # kalın yazı tipi


def show_score():
    """Skoru ekrana yazdırma"""
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, [10, 10])


def draw_button(text, x, y, w, h, color, hover_color):
    """Buton oluşturma fonksiyonu"""
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
        if click[0] == 1:
            return True
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + w / 2, y + h / 2))
    screen.blit(text_surface, text_rect)
    return False


def game_over():
    """Oyun bittiğinde ekrana mesaj ve yeniden başlatma seçeneği"""
    pygame.mixer.music.stop()  # müzik durdur
    while True:
        screen.fill(GRAY)
        text = game_over_font.render(f"Game Over! Score: {score}", True, WHITE)
        text_rect = text.get_rect(center=(width / 2, height / 3))
        screen.blit(text, text_rect)

        # Yeniden oyna butonu
        again = draw_button("PLAY AGAIN", width / 2 - 100,
                            height / 2, 200, 50, DARK_GREEN, GREEN)
        # Çıkış butonu
        exit_game = draw_button("EXIT", width / 2 - 100,
                                height / 2 + 70, 200, 50, RED, (255, 100, 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if again:  # yeniden oyna seçildi
            main_game()  # oyunu yeniden başlat
        if exit_game:  # çıkış seçildi
            pygame.quit()
            sys.exit()

        pygame.display.update()
        clock.tick(15)


def main_game():
    """Ana oyun döngüsü"""
    global snake_pos, snake_body, snake_direction, food_pos, food_spawn, score

    # oyun değişkenlerini sıfırla
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    snake_direction = 'RIGHT'
    food_pos = [random.randrange(1, (width//10)) * 10,
                random.randrange(1, (height//10)) * 10]
    food_spawn = True
    score = 0

    pygame.mixer.music.play(-1)  # müziği yeniden başlat

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # yön kontrolü
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != "DOWN":
                    snake_direction = 'UP'
                elif event.key == pygame.K_DOWN and snake_direction != "UP":
                    snake_direction = 'DOWN'
                elif event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                    snake_direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                    snake_direction = 'RIGHT'

        # hareket
        if snake_direction == 'UP':
            snake_pos[1] -= 10
        if snake_direction == 'DOWN':
            snake_pos[1] += 10
        if snake_direction == 'LEFT':
            snake_pos[0] -= 10
        if snake_direction == 'RIGHT':
            snake_pos[0] += 10

        # yeni kafa ekle
        snake_body.insert(0, list(snake_pos))

        # yem yeme kontrolü
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 10  # skor artır
            food_spawn = False  # yeni yem oluşturulacak
        else:
            snake_body.pop()  # son parçayı sil (hareket efekti)

        # yeni yem oluştur
        if not food_spawn:
            food_pos = [random.randrange(1, (width // 10)) * 10,
                        random.randrange(1, (height // 10)) * 10]
        food_spawn = True

        # DUVARA ÇARPTI MI?
        if snake_pos[0] < 0 or snake_pos[0] >= width or snake_pos[1] < 0 or snake_pos[1] >= height:
            game_over()

        # KENDİNE ÇARPTI MI?
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over()

        # arka plan
        screen.fill(GREEN)

        # yılanı çiz
        for block in snake_body:
            pygame.draw.rect(screen, DARK_GREEN, pygame.Rect(
                block[0], block[1], 10, 10))

        # yemi çiz
        pygame.draw.rect(screen, RED, pygame.Rect(
            food_pos[0], food_pos[1], 10, 10))

        # skoru göster
        show_score()

        pygame.display.update()
        clock.tick(snake_speed)


# oyunu başlat
main_game()
