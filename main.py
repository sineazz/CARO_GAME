import pygame
import sys

# Màu
BACKGROUND = (30 , 30 , 40)
BLACK = (0 , 0 , 0)
WHITE = (255 , 255 , 255)
RED = (255 , 0 , 0)
BLUE = (0 , 0 , 255)

# kích thước
NUM_ROW = 20 # số lượng hàng trong bảng
NUM_COL = 20 # số lượng cột trong bảng
NUM_ROW_CELL = 30 # số lượng hàng mỗi ô (pixel)
NUM_COL_CELL = 30 # số lượng cột mỗi ô (pixel)

def Inside(x , y):
    return x >= 0 and x < NUM_COL and y >= 0 and y < NUM_ROW

def Valid(x , y , mark):
    return Inside(x , y) and mark[0][x][y] == False and mark[1][x][y] == False

class PlayScreen:
    def __init__(self):
         # Khởi tạo phông chữ và tài nguyên giao diện
        VIETNAMESE_FONTS = ["segoe ui", "arial", "tahoma"]
        self.fontGameOver = pygame.font.SysFont(VIETNAMESE_FONTS , 50 , bold = True)
        self.fontPressSpace = pygame.font.SysFont(VIETNAMESE_FONTS , 20 , italic = True)
        self.fontDraw = pygame.font.SysFont(VIETNAMESE_FONTS , 30 , bold = True)
        self.fontRedBlue = pygame.font.SysFont(VIETNAMESE_FONTS , 30 , bold = True)
        self.Xicon = pygame.image.load("caroX.png").convert_alpha()
        self.Oicon = pygame.image.load("caroO.png").convert_alpha()
        
        
    def handle_event(self, event , history , mark , player , pausing , pos):
        if event.type == pygame.QUIT:
            return "QUIT"
       
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT: # click chuột trái để chọn tọa độ nước đi tiếp theo
                [x , y] = event.pos
                pos[0] = x // NUM_COL_CELL
                pos[1] = y // NUM_ROW_CELL
            elif event.button == pygame.BUTTON_RIGHT: # click chuột phải để hủy chọn tọa độ nước đi tiếp theo
                pos[0] = -1
                pos[1] = -1
        
        if pausing == False and event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_x and player == 0) or (event.key == pygame.K_o and player == 1): # người chơi 0 là X , người chơi 1 là O
                [x , y] = pos
                if Valid(x , y , mark):
                    mark[player][x][y] = True
                    history[player].append([x , y])
                    # sau khi đi nước tọa độ điểm đi nước tiếp theo sẽ được hủy
                    pos[0] = -1
                    pos[1] = -1
                    return "XO"
        
        if pausing:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    history[0].clear()
                    history[1].clear()
                    
                    for p in range(2):
                        for i in range(NUM_ROW):
                            for j in range(NUM_COL):
                                mark[p][i][j] = False
                    return "Space"
                            
        
    def update(self):
        pass
        
    def Draw(self , screen , history , pos):
        screen.fill(BACKGROUND) # tô nền màu đen
        
        # Vẽ bảng 
        # mỗi ô trong bảng chiếm 30x30 pixel
        # nên bảng có 20x20 ô
            
        for i in range(NUM_ROW + 1): # kẻ NUM_ROW + 1 đường kẻ ngang
            pygame.draw.line(screen , WHITE , (0 , NUM_ROW_CELL * i) , (600 , NUM_ROW_CELL * i)) # trên "screen" màu trắng bắt đầu tại điểm (0 , 30 * i) đến (600 , 30 * i)
            
        for i in range(NUM_COL + 1): # kẻ NUM_COL + 1 đường kẻ dọc
            pygame.draw.line(screen , WHITE , (NUM_COL_CELL * i , 0) , (NUM_COL_CELL * i , 600)) # trên "screen" màu trắng bắt đầu tại điểm (30 * i , 0) đến (30 * i , 600)
    
        for [x , y] in history[0]: # tô màu các ô người chơi 1 đã chọn
            screen.blit(self.Xicon ,  (x * NUM_COL_CELL + 1 , y * NUM_ROW_CELL + 1))
            
        for [x , y] in history[1]: # tô màu các ô người chơi 1 đã chọn
            screen.blit(self.Oicon ,  (x * NUM_COL_CELL + 1 , y * NUM_ROW_CELL + 1))
            
        if Inside(pos[0] , pos[1]):
            pygame.draw.rect(screen , WHITE , (pos[0] * NUM_COL_CELL + 1 , pos[1] * NUM_ROW_CELL + 1 , 29 , 29))

    def Win(self , grid , mark):
        
        # check 5 ô liên tiếp trên hàng
        for i in range(NUM_ROW):
            cur = 0
            for j in range(NUM_COL):
                if grid[i][j] == True:
                    cur += 1
                else:
                    cur = 0
                if cur >= 5:
                    return "Win"
            
        # check 5 ô liên tiếp trên cột
        for j in range(NUM_COL):
            cur = 0
            for i in range(NUM_ROW):
                if grid[i][j] == True:
                    cur += 1
                else:
                    cur = 0
                if cur >= 5:
                    return "Win"
            
        # check 5 ô liên tiếp trên đường chéo chính
        
        for s in range(0 , NUM_ROW + NUM_COL - 1):
            cur = 0
            for i in range(NUM_ROW):
                j = s - i
                if Inside(i , j) and grid[i][j] == True:
                    cur += 1
                else:
                    cur = 0
                if cur >= 5:
                    return "Win"
                
        # check 5 ô liên tiếp trên đường chéo phụ
        
        for s in range(- NUM_ROW + 1 , NUM_COL):
            cur = 0
            for i in range(NUM_ROW):
                j = i - s
                if Inside(i , j) and grid[i][j]:
                    cur += 1
                else:
                    cur = 0
                if cur >= 5:
                    return "Win"
        
        NumCellUnMarked = 0
        
        for i in range(NUM_ROW):
            for j in range(NUM_COL):
                if Valid(i , j , mark):
                    NumCellUnMarked += 1
                    
        if NumCellUnMarked == 0:
            return "Draw"
        
        return "ToBeContinue"
    
    def WhoIsWinner(self , mark):
        RedIsWinner = self.Win(mark[0] , mark)
        BlueIsWinner = self.Win(mark[1] , mark)
        if RedIsWinner == "Win":
            return "Red"
        
        if BlueIsWinner == "Win":
            return "Blue"
        
        if RedIsWinner == "Draw" and BlueIsWinner == "Draw":
            return "Draw"
        
        return "ToBeContinue"
                
    def GameOver(self , screen , Winner):
        screen.fill(BLACK)
        GameOverText = self.fontGameOver.render("Game Over!", True, WHITE)
        PressSpace = self.fontPressSpace.render("Press Space to Continue" , True , WHITE)
        DrawText = self.fontDraw.render("Draw" , True , WHITE)
        RedBlueText = self.fontRedBlue.render(Winner , True , Winner)
        screen.blit(GameOverText , (175 ,220 ,200 ,60))
        if Winner == "Draw":
           screen.blit(DrawText , (275 , 300 , 200 , 60))
        else:
            screen.blit(RedBlueText , (275 , 300 , 200 , 60))
        screen.blit(PressSpace , (210 , 370 , 200 , 60))
        
        

if __name__ == "__main__":
    
    pygame.init()
    screen = pygame.display.set_mode((601 , 601))
    pygame.display.set_caption('Caro Game')
    clock = pygame.time.Clock()
    pausing = False
    running = True
    
    playscreen = PlayScreen();
    
    player = 0
    history = [[] , []]
    mark = [[[False for j in range(NUM_COL)] for i in range(NUM_ROW)] , 
            [[False for j in range(NUM_COL)] for i in range(NUM_ROW)]]
    pos = [-1 , -1] # tọa độ ô đang được chọn để đánh nước tiếp theo
    
    while running:
        
        Winner = playscreen.WhoIsWinner(mark)
        if Winner != "ToBeContinue":
            pausing = True
            playscreen.GameOver(screen , Winner)    
        else:
            playscreen.Draw(screen , history , pos)
        
        for event in pygame.event.get():
            option = playscreen.handle_event(event , history , mark , player , pausing , pos);
            if option == "QUIT":
                running = False
            elif option == "XO":
                player ^= 1
            elif option == "Space":
                player = 0
                pausing = False
    
                
        pygame.display.flip()
        clock.tick(60)
        
        
    pygame.quit()
    sys.exit()