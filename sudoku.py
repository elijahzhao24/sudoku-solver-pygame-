# Elijah Zhao
# 2024/12/28
# Sudoku board player and solver (using recursive backtracking)
# uses api to fetch boards from given url

import pygame
from pip._vendor import requests
pygame.init()

WIDTH = 550
BG_COLOR = (251, 247, 244)
selected = 0

response = requests.get("https://sugoku.onrender.com/board?difficulty=easy")
grid = response.json()['board']
original = []

for i in range(0, len(grid[0])):
    for j in range(0, len(grid[0])):
        if grid[i][j] != 0:
            original.append([i + 1, j + 1])
            


font = pygame.font.SysFont('Comic Sans MS', 35)
font2 = pygame.font.SysFont('Comic Sans MS', 12)


def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, WIDTH + 150))
    window.fill(BG_COLOR)
    drawboard(window, grid)
    pygame.display.update()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked(pos[0]//50, pos[1]//50)
                window.fill(BG_COLOR)
                drawboard(window, grid)
                pygame.display.update()
            
def drawboard(win, g):
    for i in range(0, 10):
        if (i%3 == 0):
            pygame.draw.line(win, (0, 0, 0), (50 + 50*i, 50), (50 + 50*i, 500), 4)
            pygame.draw.line(win, (0, 0, 0), (50, 50 + 50*i), (500, 50 + 50*i), 4)
        else:
            pygame.draw.line(win, (0, 0, 0), (50 + 50*i, 50), (50 + 50*i, 500), 2)
            pygame.draw.line(win, (0, 0, 0), (50, 50 + 50*i), (500, 50 + 50*i), 2)

    for i in range(0, len(g[0])):
        for j in range(0, len(g[0])):
            if(0 < g[i][j] < 10):
                val = font.render(str(g[i][j]), True, (0, 0, 0))
                win.blit(val, ((j + 1)*50 + 15, (i+1)*50))
    
    pygame.draw.line(win, (0, 0, 0), (50, 550), (500, 550), 4)
    pygame.draw.line(win, (0, 0, 0), (50, 600), (500, 600), 4)
    for i in range(1, 10):
        val = font.render(str(i), True, (0, 0, 0))
        win.blit(val, ((i)*50 + 15, 550))
        pygame.draw.line(win, (0, 0, 0), (50 + 50*i, 550), (50 + 50*i, 600), 4)
    pygame.draw.line(win, (0, 0, 0), (50 , 550), (50, 600), 4)
    pygame.draw.line(win, (0, 0, 0), (50 , 600), (50, 650), 4)
    pygame.draw.line(win, (0, 0, 0), (100 , 600), (100, 650), 4)
    pygame.draw.line(win, (0, 0, 0), (150 , 600), (150, 650), 4)
    win.blit(font2.render("remove", True, (0, 0, 0)), (50 + 5, 600+15))
    win.blit(font2.render("solve", True, (0, 0, 0)), (100 + 10, 600+15))
    pygame.draw.line(win, (0, 0, 0), (50, 650), (150, 650), 4)
    
def clicked(x, y):
    global selected
    if (0 < x < 10) and (0 < y < 10) and not ([y, x] in original):
        if selected == 11:
            grid[y-1][x-1] = 0
        elif (0< selected< 10):
            grid[y-1][x-1] = selected
    elif (y == 11) and (0 < x < 10):
        if selected == x:
            selected = 0
        else:
            selected = x
    elif (y == 12) and (x == 1):
        if selected == 11:
            selected = 0
        else:
            selected = 11
        

main()

