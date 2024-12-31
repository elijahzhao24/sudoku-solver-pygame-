# Elijah Zhao
# 2024/12/28
# Sudoku board player and solver (using recursive backtracking)
# uses api to fetch boards from given url

import copy
import pygame
from pip._vendor import requests
pygame.init()

WIDTH = 550
BG_COLOR = (251, 247, 244)
selected = 0

response = requests.get("https://sugoku.onrender.com/board?difficulty=easy")
grid = response.json()['board']
og_grid = copy.deepcopy(grid)
original = set()

for i in range(0, len(grid[0])):
    for j in range(0, len(grid[0])):
        if grid[i][j] != 0:
            original.add((i + 1, j + 1))
            


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

    row_invalid = check_row(g)
    column_invalid = check_column(g)
    cube_invalid = check_cube(g)

    if row_invalid != 0:
        pygame.draw.rect(win, (255, 153, 153), (50, (50 * row_invalid ), 450, 50))
    if column_invalid != 0:
        pygame.draw.rect(win, (255, 153, 153), ((50 * column_invalid), 50, 50, 450))
    if cube_invalid != 0:
        pygame.draw.rect(win, (255, 153, 153), ((((cube_invalid-1) % 3) * 150) + 50, (((cube_invalid-1 )//3) * 150) + 50, 150, 150))


    if (0 < selected < 10):
        pygame.draw.rect(win, (224, 224, 224), ((50 * selected), 550, 50, 50))
    elif selected == 11:
        pygame.draw.rect(win, (224, 224, 224), (50, 600, 50, 50))

    

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
    global grid
    if (0 < x < 10) and (0 < y < 10) and not ((y, x) in original):
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
    elif (y == 12) and (x == 2):
        selected = 0
        if solve(og_grid) != False:
            grid = solve(og_grid)
            print(grid)
        
def check_row(g):
    for i in range(0, len(g[0])):
        temp = {}
        for j in range(0, len(g[0])):
            if g[i][j] in temp.keys():
                return i + 1
            if g[i][j] != 0:
                temp[g[i][j]] = True
    return 0

def check_column(g):
    for i in range(0, len(g[0])):
        temp = {}
        for j in range(0, len(g[0])):
            if g[j][i] in temp.keys():
                return i + 1
            if g[j][i] != 0:
                temp[g[j][i]] = True
    return 0

def check_cube(g):
    for i in range(0, 7, 3):
        for j in range(0, 3):
            temp = {}
            for k in range(0, 3):
                for l in range(0, 3):
                    if g[i+k][(j *3)+l] in temp.keys():
                        return i + j + 1
                    if g[i+k][(j *3)+l] != 0:
                        temp[g[i+k][(j *3)+l]] = True
    return 0

def find_empty_location(g):
    for i in range(9):
        for j in range(9):
            if(g[i][j] == 0):
                return True
    return False

def find_first_spot(g):
    for i in range(9):
        for j in range(9):
            if(g[i][j] == 0):
                return [i, j]

def valid_location(g, num, y, x):
    g[y][x] = num

    row_invalid = check_row(g)
    column_invalid = check_column(g)
    cube_invalid = check_cube(g)

    if row_invalid != 0 or column_invalid != 0 or cube_invalid != 0:
        return False
    else:
        return True


def solve(g):
    if (not find_empty_location(g)):
        return g
    empty_spot = find_first_spot(g)

    for num in range(1, 10):
        tempg = copy.deepcopy(g)
        if valid_location(tempg, num, empty_spot[0], empty_spot[1]):
            tempg[empty_spot[0]][empty_spot[1]] = num
            solved = solve(tempg)
            if solved != False:
                return solved
            else:
                continue 
    return False

main()

