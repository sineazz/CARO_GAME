import pygame
import sys
import setting_screen,start_screen
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Caro Game")
    clock = pygame.time.Clock()

    start_page = start_screen.StartScreen()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            next_state = start_page.handle_event(event)
            if next_state == "START":
                start_page = start_screen.StartScreen()
            elif next_state == "SETTING":
                start_page = setting_screen.SettingsScreen()
            elif next_state == "QUIT":
                print("--> Click QUIT: Thoát game")
                running = False

        start_page.update()
        start_page.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()