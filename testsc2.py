import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((600, 480))
pygame.display.set_caption("Screen 2 Game Caro")
clock = pygame.time.Clock()


class OptionSelector:

    def __init__(
        self, title, options, x, y, btn_width=140, btn_height=45, gap=15
    ):
        self.title = title
        self.options = options
        self.selected_index = 0
        self.font = pygame.font.SysFont("Arial", 22, bold=True)
        self.rects = []
        for i in range(len(options)):
            btn_x = x + i * (btn_width + gap)
            btn_y = y + 35
            self.rects.append(pygame.Rect(btn_x, btn_y, btn_width, btn_height))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.rects):
                if rect.collidepoint(event.pos):
                    self.selected_index = i

    def draw(self, screen):
        title_surf = self.font.render(self.title, True, (30, 30, 30))
        screen.blit(title_surf, (self.rects[0].x, self.rects[0].y - 35))
        for i, rect in enumerate(self.rects):
            bg_color = (
                (46, 204, 113) if i == self.selected_index else (220, 220, 220)
            )
            text_color = (
                (255, 255, 255) if i == self.selected_index else (50, 50, 50)
            )
            pygame.draw.rect(screen, bg_color, rect, border_radius=8)
            pygame.draw.rect(screen, (80, 80, 80), rect, 2, border_radius=8)
            text_surf = self.font.render(self.options[i], True, text_color)
            screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def get_value(self):
        return self.options[self.selected_index]


# ==========================================
# LỚP NHẬP TÊN NGƯỜI CHƠI
# ==========================================
class Nhapten:

    def __init__(self, x, y, box_width=300, box_height=42, gap=75):
        """
        x, y: Tọa độ bắt đầu vẽ khu vực nhập tên
        gap: Khoảng cách dọc giữa ô nhập 1 và ô nhập 2
        """
        self.x = x
        self.y = y
        self.box_width = box_width
        self.box_height = box_height
        self.gap = gap

        self.font_label = pygame.font.SysFont("Arial", 20, bold=True)
        self.font_text = pygame.font.SysFont("Arial", 20)

        # Lưu tên mặc định cho 2 người chơi
        self.names = ["Player 1", "Player 2"]
        self.max_length = 18  # Giới hạn số ký tự tối đa

        # Chỉ số ô đang được chọn để gõ (-1 nghĩa là không chọn ô nào)
        self.active_index = 0
        self.num_boxes = 1

        # Tạo sẵn 2 khung hình chữ nhật (Rect)
        self.rects = [
            pygame.Rect(x, y + 28, box_width, box_height),
            pygame.Rect(x, y + 28 + gap, box_width, box_height),
        ]

    def set_mode(self, mode):
        """Cập nhật số lượng khung nhập dựa trên chế độ chơi"""
        if mode == "1 Player":
            self.num_boxes = 1
            if self.active_index == 1:
                self.active_index = 0
        else:
            self.num_boxes = 2

    def handle_event(self, event):
        # 1. Xử lý click chuột để chọn ô muốn nhập
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.active_index = -1  # Reset trạng thái chọn
            for i in range(self.num_boxes):
                if self.rects[i].collidepoint(event.pos):
                    self.active_index = i

        # 2. Xử lý gõ bàn phím khi có một ô đang được chọn
        if event.type == pygame.KEYDOWN and self.active_index != -1:
            idx = self.active_index
            if event.key == pygame.K_BACKSPACE:
                # Xóa 1 ký tự cuối
                self.names[idx] = self.names[idx][:-1]
            elif event.key in (pygame.K_RETURN, pygame.K_TAB):
                # Nhấn Enter hoặc Tab để chuyển sang ô tiếp theo (nếu có)
                if self.num_boxes == 2:
                    self.active_index = (idx + 1) % 2
            else:
                # Thêm ký tự vừa gõ nếu chưa vượt quá độ dài tối đa
                if (
                    len(self.names[idx]) < self.max_length
                    and event.unicode.isprintable()
                ):
                    self.names[idx] += event.unicode

    def draw(self, screen):
        labels = ["Player 1 (X):", "Player 2 (O):"]

        for i in range(self.num_boxes):
            rect = self.rects[i]

            # Vẽ nhãn phía trên ô nhập
            label_surf = self.font_label.render(labels[i], True, (30, 30, 30))
            screen.blit(label_surf, (rect.x, rect.y - 26))

            # Đổi màu viền nếu ô này đang được chọn để gõ
            if i == self.active_index:
                border_color = (41, 128, 185)  # Xanh dương đậm
                bg_color = (255, 255, 255)
                border_thickness = 3
            else:
                border_color = (150, 150, 150)  # Xám
                bg_color = (238, 238, 238)
                border_thickness = 2

            # Vẽ nền và viền khung nhập
            pygame.draw.rect(screen, bg_color, rect, border_radius=6)
            pygame.draw.rect(
                screen, border_color, rect, border_thickness, border_radius=6
            )

            # Hiển thị tên (thêm dấu nháy "|" nếu đang gõ ở ô này)
            display_text = self.names[i] + (
                "|" if i == self.active_index else ""
            )
            text_surf = self.font_text.render(display_text, True, (20, 20, 20))
            screen.blit(text_surf, (rect.x + 12, rect.y + 9))

    def get_names(self):
        """Trả về danh sách tên tương ứng với chế độ chơi"""
        if self.num_boxes == 1:
            return [self.names[0], "Bot (AI)"]
        return [self.names[0], self.names[1]]

class Am_thanh:
    def __init__(
            self, image, x = 10, y = 500
    ):
        self.x = 10
        self.y = 500
        self.image = []
        self.scale_image = []
        self.rect_image = []
        for i in range(len(image)):
            self.image.append(pygame.image.load(image[i]).convert())
            self.scale_image.append(pygame.transform.scale(self.image[i], (40, 40)))
            self.rect_image.append(self.scale_image[i].get_rect(topleft = (10, 550)))

    def draw(self, screen):
        i = 2
        current_image = self.scale_image[i]
        current_rect_image = self.rect_image[i]
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if current_rect_image.collidepoint(mouse_pos):
                current_image = self.scale_image[i+1 % 3]
                current_rect_image = self.rect_image[i + 1 % 3]
        screen.blit(current_image, (10, 500))
        screen.blit(current_image, current_rect_image)

class nut_start:
    def __init__(
            self, x, y, width = 200, height = 80, normal_color = (46, 204, 113), hover_color = (39, 174, 96)
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("Arial", 35, bold = True)
        self.name = "Start Game"
        self.rect = pygame.Rect( x, y, width, height)
        self.normal_color = normal_color
        self.hover_color = hover_color

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            current_color = self.hover_color
        else:
            current_color = self.normal_color
        pygame.draw.rect(screen, current_color, self.rect, border_radius = 10)
        pygame.draw.rect(screen, (30, 45, 60), self.rect, 2, border_radius = 10)

        text_suf = self.font.render(self.name, True, (0, 0, 0))
        text_rect = text_suf.get_rect(center = self.rect.center)
        screen.blit(text_suf, text_rect)

    def is_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(self.rect):
                return True
        return False

                
# ==========================================
# CHẠY THỬ NGHIỆM TRÊN CỬA SỔ PYGAME
# ==========================================


# Khởi tạo bảng chọn chế độ và khung nhập tên
mode_selector = OptionSelector(
    "Game mode:", ["1 Player", "2 Player"], x=150, y=50
)
name_input = Nhapten(x=150, y=170, box_width=300)
vol = Am_thanh(
    ["image/tat_am.jpg", "image/am_tb.jpg", "image/am_lon.jpg"],
    x = 10,
    y = 500
)

start_button = nut_start(
    x = 200,
    y = 350,
    width = 200,
    height = 80, 
    normal_color = (46, 204, 113),
    hover_color = (39, 174, 96)
)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Bắt sự kiện cho cả 2 thành phần
        mode_selector.handle_event(event)
        name_input.set_mode(
            mode_selector.get_value()
        )  
        # Cập nhật số ô theo chế độ
        name_input.handle_event(event)

    screen.fill((245, 195, 205))

    # Vẽ giao diện
    mode_selector.draw(screen)
    name_input.draw(screen)
    vol.draw(screen)
    start_button.draw(screen)
    #chu Setting
    font = pygame.font.SysFont("Arial", 30, (0, 0, 0))
    text_suf = font.render("SETTING", True, (0, 0, 0))
    rect_text = text_suf.get_rect(center = (300, 25))
    screen.blit(text_suf, rect_text)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()