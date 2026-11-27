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

# Lịch sử

history = [[[0 , 0] , [1 , 1]] , []] # lưu lịch sử tô màu các ô của người chơi 1 và người chơi 2

pygame.init()
screen = pygame.display.set_mode((601 , 601)) # màng hình 601x601 pixel
running = True


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

while running:
    
    Draw()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    pygame.display.flip()
    
pygame.quit() 