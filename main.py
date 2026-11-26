import pygame

pygame.init()
screen = pygame.display.set_mode((601 , 601))
pygame.display.set_caption('CARO_GAME')
running = True
BLACK = (0 , 0 , 0)
WHITE = (255 , 255 , 255)
BLUE = (0 , 0 , 255)
RED = (255 , 0 , 0)
Red_win = False
Blue_win = False
cur = 0
history = [[] , []]
table = [
    [[0 for j in range(20)] for i in range(20)],
    [[0 for j in range(20)] for i in range(20)]
]
end = False
font_big = pygame.font.SysFont("sans" , 50)

press_space_to_continue = font_big.render("Press space to continue", True , BLACK)
Red_win_txt = font_big.render("Red win" , True , RED)
Blue_win_txt = font_big.render("Blue win" , True , BLUE)

def check(a):
    
    for i in range(0 , 20):
        cur = 0
        for j in range(0 , 20):
            if a[i][j]:
                cur += 1
            else:
                cur = 0
            if cur >= 5:
                return 1
    
    
    for j in range(0 , 20):
        cur = 0
        for i in range(0 , 20):
            if a[i][j]:
                cur += 1
            else:
                cur = 0
            if cur >= 5:
                return 1
    
    for s in range(0 , 39):
        cur = 0
        for i in range(0 , 20):
            if s - i >= 0 and s - i < 20:
                if a[i][s - i]:
                    cur += 1
                else:
                    cur = 0
            else:
                cur = 0
            if cur >= 5:
                return 1
    
    for s in range(-19, 20):
        cur = 0
        for i in range(0 , 20):
            if i - s >= 0 and i - s < 20:
                if a[i][i - s]:
                    cur += 1
                else:
                    cur = 0
            else:
                cur = 0
                
            if cur >= 5:
                return 1
    
    return 0

while running:
    screen.fill(BLACK)
    
    for i in range(0 , 21):
        pygame.draw.line(screen , WHITE , (0 , i * 30) , (600 , i * 30))
        
    for i in range(0 , 21):
        pygame.draw.line(screen , WHITE , (i * 30 , 0) , (i * 30 , 600))
        
    for [x , y] in history[0]:
        pygame.draw.rect(screen , RED , (x * 30 , y * 30 , 30 , 30))
    
    for [x , y] in history[1]:
            pygame.draw.rect(screen , BLUE , (x * 30 , y * 30 , 30 , 30))


    if end:
        
        pygame.draw.rect(screen , WHITE , (0 , 200 , 601 , 200))
        
        screen.blit(press_space_to_continue , (50 , 200)) 
        if Blue_win:
            screen.blit(Blue_win_txt , (50 , 300))
        if Red_win:
            screen.blit(Red_win_txt , (50 , 300))    
             
    if end == False and check(table[0]):
        Red_win = True
        end = True
    
    if end == False and check(table[1]):
        Blue_win = True
        end = True
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                running = False
        if end and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                history = [[] , []]
                table = [
                            [[0 for j in range(20)] for i in range(20)],
                            [[0 for j in range(20)] for i in range(20)]
                        ]
                end = False
                cur = 0
                Blue_win = False
                Red_win = False
                
        if end == False and event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and table[0][event.pos[0] // 30][event.pos[1] // 30] == False and table[1][event.pos[0] // 30][event.pos[1] // 30] == False:
                history[cur].append([event.pos[0] // 30 , event.pos[1] // 30])
                table[cur][event.pos[0] // 30][event.pos[1] // 30] = 1
                cur ^= 1
    
    pygame.display.flip()
    
pygame.quit()