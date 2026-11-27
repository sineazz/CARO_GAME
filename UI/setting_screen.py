import pygame
import sys

# =======================================================
# 1. COMPONENT: Ô NHẬP TÊN USERNAME (INPUT BOX)
# =======================================================
class InputBox:
    def __init__(self, x, y, width, height, initial_text="Player 1"):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = initial_text
        self.active = False  # Trạng thái đang con trỏ gõ chữ
        
        self.color_inactive = (180, 180, 180)
        self.color_active = (41, 128, 185)
        
        fonts = ["segoe ui", "arial", "tahoma"]
        self.font = pygame.font.SysFont(fonts, 20)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Nếu click vào ô -> Active, click ra ngoài -> Inactive
            self.active = self.rect.collidepoint(event.pos)

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < 20:
                self.text += event.unicode

    def draw(self, surface):
        # Vẽ ô màu trắng
        pygame.draw.rect(surface, (255, 255, 255), self.rect, border_radius=6)
        
        # Vẽ viền (Đổi màu xanh khi đang gõ)
        color = self.color_active if self.active else self.color_inactive
        pygame.draw.rect(surface, color, self.rect, width=2, border_radius=6)

        # Vẽ chữ inside ô
        text_surf = self.font.render(self.text, True, (30, 30, 30))
        surface.blit(text_surf, (self.rect.x + 10, self.rect.y + (self.rect.height - text_surf.get_height()) // 2))


# =======================================================
# 2. COMPONENT: THANH TRƯỢT ÂM LƯỢNG (SLIDER)
# =======================================================
class Slider:
    def __init__(self, x, y, width, height, initial_val=0.7):
        self.rect = pygame.Rect(x, y, width, height)
        self.value = initial_val
        self.is_dragging = False

        self.handle_radius = height // 2 + 5
        self.handle_x = x + int(self.value * width)
        self.handle_y = y + height // 2

        fonts = ["segoe ui", "arial", "tahoma"]
        self.font = pygame.font.SysFont(fonts, 18, bold=True)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            handle_rect = pygame.Rect(
                self.handle_x - self.handle_radius,
                self.handle_y - self.handle_radius,
                self.handle_radius * 2,
                self.handle_radius * 2
            )
            if handle_rect.collidepoint(event.pos) or self.rect.collidepoint(event.pos):
                self.is_dragging = True
                self._update_val(event.pos[0])

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging = False

        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            self._update_val(event.pos[0])

    def _update_val(self, mouse_x):
        self.handle_x = max(self.rect.left, min(mouse_x, self.rect.right))
        self.value = (self.handle_x - self.rect.left) / self.rect.width
        # Cập nhật trực tiếp âm lượng Pygame Mixer
        try:
            pygame.mixer.music.set_volume(self.value)
        except Exception:
            pass

    def draw(self, surface):
        # Vẽ thanh ray nền
        pygame.draw.rect(surface, (200, 200, 200), self.rect, border_radius=6)
        
        # Vẽ phần đã kéo
        filled_w = self.handle_x - self.rect.left
        if filled_w > 0:
            filled_rect = pygame.Rect(self.rect.left, self.rect.top, filled_w, self.rect.height)
            pygame.draw.rect(surface, (46, 204, 113), filled_rect, border_radius=6)

        # Vẽ núm tròn
        knob_color = (39, 174, 96) if self.is_dragging else (255, 255, 255)
        pygame.draw.circle(surface, knob_color, (self.handle_x, self.handle_y), self.handle_radius)
        pygame.draw.circle(surface, (100, 100, 100), (self.handle_x, self.handle_y), self.handle_radius, width=2)

        # In số %
        text_surf = self.font.render(f"{int(self.value * 100)}%", True, (50, 50, 50))
        surface.blit(text_surf, (self.rect.right + 12, self.rect.top - 2))


# =======================================================
# 3. CLASS MÀN HÌNH SETTINGS (SETTINGS SCREEN)
# =======================================================
class SettingsScreen:
    def __init__(self):
        fonts = ["segoe ui", "arial", "tahoma"]
        self.title_font = pygame.font.SysFont(fonts, 36, bold=True)
        self.label_font = pygame.font.SysFont(fonts, 20, bold=True)
        self.btn_font = pygame.font.SysFont(fonts, 18, bold=True)

        # 1. Ô nhập Tên người chơi
        self.input_username = InputBox(x=230, y=180, width=220, height=40, initial_text="Player 1")

        # 2. Thanh trượt Âm lượng
        self.volume_slider = Slider(x=230, y=260, width=220, height=12, initial_val=0.7)

        # 3. Chế độ chơi ("PVP" hoặc "PVE")
        self.game_mode = "PVP"
        self.rect_pvp = pygame.Rect(230, 320, 105, 40)
        self.rect_pve = pygame.Rect(345, 320, 105, 40)

        # 4. Nút TRỞ VỀ (BACK)
        self.rect_back = pygame.Rect(200, 440, 201, 50)

    def handle_event(self, event):
        # Lắng nghe sự kiện cho Input box và Slider
        self.input_username.handle_event(event)
        self.volume_slider.handle_event(event)

        # Click chọn chế độ chơi
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect_pvp.collidepoint(event.pos):
                self.game_mode = "PVP"
            elif self.rect_pve.collidepoint(event.pos):
                self.game_mode = "PVE"

            # Click nút TRỞ VỀ -> Trả về dictionary cấu hình và chuyển màn hình
            elif self.rect_back.collidepoint(event.pos):
                config_data = {
                    "username": self.input_username.text,
                    "volume": self.volume_slider.value,
                    "mode": self.game_mode
                }
                return "START"

        return None

    def update(self):
        pass

    def draw(self, surface):
        surface.fill((240, 242, 245))  # Tô nền màu xám xanh

        # Tiêu đề
        title = self.title_font.render("CÀI ĐẶT GAME", True, (41, 128, 185))
        surface.blit(title, ((601 - title.get_width()) // 2, 80))

        # --- MỤC 1: USERNAME ---
        lbl_user = self.label_font.render("Tên người chơi:", True, (50, 50, 50))
        surface.blit(lbl_user, (70, 188))
        self.input_username.draw(surface)

        # --- MỤC 2: ÂM LƯỢNG ---
        lbl_vol = self.label_font.render("Âm lượng:", True, (50, 50, 50))
        surface.blit(lbl_vol, (70, 255))
        self.volume_slider.draw(surface)

        # --- MỤC 3: CHẾ ĐỘ CHƠI ---
        lbl_mode = self.label_font.render("Chế độ chơi:", True, (50, 50, 50))
        surface.blit(lbl_mode, (70, 328))

        # Nút PvP (2 Người)
        color_pvp = (41, 128, 185) if self.game_mode == "PVP" else (200, 200, 200)
        text_color_pvp = (255, 255, 255) if self.game_mode == "PVP" else (80, 80, 80)
        pygame.draw.rect(surface, color_pvp, self.rect_pvp, border_radius=8)
        txt_pvp = self.btn_font.render("2 Người", True, text_color_pvp)
        surface.blit(txt_pvp, txt_pvp.get_rect(center=self.rect_pvp.center))

        # Nút PvE (Với Bot)
        color_pve = (41, 128, 185) if self.game_mode == "PVE" else (200, 200, 200)
        text_color_pve = (255, 255, 255) if self.game_mode == "PVE" else (80, 80, 80)
        pygame.draw.rect(surface, color_pve, self.rect_pve, border_radius=8)
        txt_pve = self.btn_font.render("Với Máy", True, text_color_pve)
        surface.blit(txt_pve, txt_pve.get_rect(center=self.rect_pve.center))

        # --- NÚT TRỞ VỀ ---
        mouse_pos = pygame.mouse.get_pos()
        back_color = (39, 174, 96) if self.rect_back.collidepoint(mouse_pos) else (46, 204, 113)
        pygame.draw.rect(surface, back_color, self.rect_back, border_radius=10)
        txt_back = self.label_font.render("LƯU & TRỞ VỀ", True, (255, 255, 255))
        surface.blit(txt_back, txt_back.get_rect(center=self.rect_back.center))


# =======================================================
# KHỐI TEST CHẠY THỬ ĐỘC LẬP (TEST FILE)
# =======================================================
if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((601, 601))
    pygame.display.set_caption("Test Settings Screen (601x601)")
    clock = pygame.time.Clock()

    setting_page = SettingsScreen()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            res = setting_page.handle_event(event)
            if res:
                next_state, config = res
                print(f"--> Đã bấm LƯU & TRỞ VỀ!")
                print(f"    Tên: {config['username']}")
                print(f"    Volume: {int(config['volume']*100)}%")
                print(f"    Chế độ: {config['mode']}")

        setting_page.update()
        setting_page.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()