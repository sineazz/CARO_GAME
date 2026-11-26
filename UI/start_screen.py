import pygame
import sys

class StartScreen:
    def __init__(self):
        # Khởi tạo phông chữ và tài nguyên giao diện màn hình Start
        VIETNAMESE_FONTS = ["segoe ui", "arial", "tahoma"]
        self.font = pygame.font.SysFont(VIETNAMESE_FONTS, 28, bold=True)

        # Tạo 2 hình chữ nhật của 2 nút play và quit
        self.play_rect = pygame.Rect(200,220,200,60)
        self.quit_rect = pygame.Rect(200,300,200,60)

    # Kiểm tra xem con trỏ chuột click vào ô play hay quit
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (self.play_rect.collidepoint(event.pos)): return "SETTING"
            if (self.quit_rect.collidepoint(event.pos)): return "QUIT"
        return "START"

    def update(self):
        # Cập nhật logic hiệu ứng (nếu có)
        pass

    # Vẽ ra màn hình 2 nút bấm
    def draw(self, surface):
        surface.fill((240, 240, 240))
        play_color = (46, 204, 113)
        pygame.draw.rect(surface, play_color, self.play_rect, border_radius=8)
        
        play_text = self.font.render("CHƠI", True, (255, 255, 255))
        play_text_rect = play_text.get_rect(center=self.play_rect.center)
        surface.blit(play_text, play_text_rect)

        quit_color = (231, 76, 60)
        pygame.draw.rect(surface, quit_color, self.quit_rect, border_radius=8)

        quit_text = self.font.render("THOÁT", True, (255, 255, 255))
        quit_text_rect = quit_text.get_rect(center=self.quit_rect.center)
        surface.blit(quit_text, quit_text_rect)


# =======================================================
# KHỐI TEST CHẠY ĐỘC LẬP (CHỈ CHẠY KHI BẤM RUN FILE NÀY)
# =======================================================
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Caro Game - Start Screen Simple")
    clock = pygame.time.Clock()

    start_page = StartScreen()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            next_state = start_page.handle_event(event)
            if next_state == "SETTING":
                print("--> Click PLAY: Chuyển sang màn hình GAME")
            elif next_state == "QUIT":
                print("--> Click QUIT: Thoát game")
                running = False

        start_page.update()
        start_page.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()