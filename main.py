import pygame

# Màu
BLACK = (0 , 0 , 0)
WHITE = (255 , 255 , 255)
RED = (255 , 0 , 0)
BLUE = (0 , 0 , 255)

# kích thước
NUM_ROW = 20 # số lượng hàng trong bảng
NUM_COL = 20 # số lượng cột trong bảng
NUM_ROW_CELL = 30 # số lượng hàng mỗi ô (pixel)
NUM_COL_CELL = 30 # số lượng cột mỗi ô (pixel)

# Game

player = 0 # lượt của người chơi nào 
history = [[] , []] # lưu lịch sử tô màu các ô của người chơi 1 và người chơi 2
mark = [[[0 for j in range(20)] for i in range(20)] ,
        [[0 for j in range(20)] for i in range(20)]] # bảng đánh dấu các ô người chơi 1 và người chơi 2 đã đi

pygame.init()
screen = pygame.display.set_mode((601 , 601)) # màng hình 601x601 pixel
running = True
pausing = False
Winner = 0

def ins(x , y): # check nằm trong bảng
    return x >= 0 and x < NUM_COL and y >= 0 and y < NUM_ROW

def check(x , y): # check nằm trong bảng và ô (x , y) chưa được tô trước đó
    return ins(x , y) and mark[0][x][y] == False and mark[1][x][y] == False

def Draw():
    screen.fill(BLACK) # tô nền màu đen

    # Vẽ bảng 
    # mỗi ô trong bảng chiếm 30x30 pixel
    # nên bảng có 20x20 ô
    
    for i in range(NUM_ROW + 1): # kẻ NUM_ROW + 1 đường kẻ ngang
        pygame.draw.line(screen , WHITE , (0 , NUM_ROW_CELL * i) , (600 , NUM_ROW_CELL * i)) # trên "screen" màu trắng bắt đầu tại điểm (0 , 30 * i) đến (600 , 30 * i)
        
    for i in range(NUM_COL + 1): # kẻ NUM_COL + 1 đường kẻ dọc
        pygame.draw.line(screen , WHITE , (NUM_COL_CELL * i , 0) , (NUM_COL_CELL * i , 600)) # trên "screen" màu trắng bắt đầu tại điểm (30 * i , 0) đến (30 * i , 600)

    for [x , y] in history[0]: # tô màu các ô người chơi 1 đã chọn
        pygame.draw.rect(screen , RED , (x * NUM_COL_CELL + 1 , y * NUM_ROW_CELL + 1 , NUM_COL_CELL - 1 , NUM_ROW_CELL - 1)) # tô màu đỏ hình chữ nhật có điểm trái trên là (x * NUM_COL_CELL + 1 , y * NUM_ROW_CELL + 1) với số lượng cột là NUM_COL_CELL - 1 và số lượng hàng là NUM_ROW_CELL - 1
    
    for [x , y] in history[1]: # tô màu các ô người chơi 1 đã chọn
        pygame.draw.rect(screen , BLUE , (x * NUM_COL_CELL + 1 , y * NUM_ROW_CELL + 1 , NUM_COL_CELL - 1 , NUM_ROW_CELL - 1)) # tô màu xanh hình chữ nhật có điểm trái trên là (x * NUM_COL_CELL + 1 , y * NUM_ROW_CELL + 1) với số lượng cột là NUM_COL_CELL - 1 và số lượng hàng là NUM_ROW_CELL - 1
        
    # điểm (x , y) trong bảng có tọa độ điểm trái trên là (x * NUM_COL_CELL , y * NUM_ROW_CELL)
    # mỗi ô có NUM_COL_CELL cột và NUM_ROW_CELL hàng
    # để giữa các ô được tô có đường kẻ màu trắng nên
    # dời điểm (x * NUM_COL_CELL , y * NUM_ROW_CELL) thành (x * NUM_COL_CELL + 1 , y * NUM_ROW_CELL + 1)
    # số lượng hàng cột mỗi ô trừ đi 1

def Win(grid):
    
    # check 5 ô liên tiếp trên hàng
    for i in range(NUM_ROW):
        cur = 0
        for j in range(NUM_COL):
            if grid[i][j] == True:
                cur += 1
            else:
                cur = 0
            if cur >= 5:
                return True
        
    # check 5 ô liên tiếp trên cột
    for j in range(NUM_COL):
        cur = 0
        for i in range(NUM_ROW):
            if grid[i][j] == True:
                cur += 1
            else:
                cur = 0
            if cur >= 5:
                return True
        
    # check 5 ô liên tiếp trên đường chéo chính
    
    for s in range(0 , 39):
        cur = 0
        for i in range(NUM_ROW):
            j = s - i
            if ins(i , j) and grid[i][j] == True:
                cur += 1
            else:
                cur = 0
            if cur >= 5:
                return True
            
    # check 5 ô liên tiếp trên đường chéo phụ
    
    for s in range(-19 , 20):
        cur = 0
        for i in range(NUM_ROW):
            j = i - s
            if ins(i , j) and grid[i][j]:
                cur += 1
            else:
                cur = 0
            if cur >= 5:
                return True
    
    return False
             

while running:
    
    if(pausing):
        if Winner == 1:
            screen.fill(RED)
        else:
            screen.fill(BLUE)
    else:
        Draw()
    
    if Win(mark[0]):
        pausing = True
        Winner = 1
    if Win(mark[1]):
        pausing = True
        Winner = 2
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if pausing:
            continue
            
        if event.type == pygame.MOUSEBUTTONDOWN: # click chuột
            if event.button == 1: # click chuột trái
                
                [x , y] = event.pos # lấy tọa độ điểm chuột click
                x = x // NUM_COL_CELL # đưa x về tọa độ trên bảng 20x20 
                y = y // NUM_ROW_CELL # đưa y về tọa độ trên bảng 20x20
                
                if check(x , y): # check điểm x y có thõa hay không
                    history[player].append([x , y])
                    mark[player][x][y] = True
                    player = player ^ 1
            
    pygame.display.flip()
    
pygame.quit() 