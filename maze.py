import pygame
import sys
from random import choice
from typing import Tuple, List

'''
This program uses a random DFS on a 2D array to make a maze. Then after storing the paths it constructs
the soloution to the maze.


'''

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

MAZE_WIDTH = 100
MAZE_HEIGHT = 100



PURPLE = (113, 4, 196)
BLACK = (0,0,0)
DESERT_TAN = (196, 192, 167)
LIGHT_GREEN = (204,255,229)
END_RED = (255,12,12)


#(width, height)
MAZE_BLOCK_WIDTH = int(SCREEN_WIDTH/(MAZE_WIDTH))
MAZE_BLOCK_HEIGHT = int(SCREEN_HEIGHT/(MAZE_HEIGHT))


def rect_select(direction: str, x: int, y: int, width: int, height:int) -> pygame.Rect:
    match direction:
        case 'N':           # uptangle
            return pygame.Rect(x, y - height, width, 2*height)
        case 'S':           # downtangle
            return pygame.Rect(x, y, width, 2*height)
        case 'E':           # right-tangle
            return pygame.Rect(x, y, 2*width, height)
        case 'W':           # left-tangle
            return pygame.Rect(x-width, y, 2*width, height)    

def draw_start_end_blocks(surface: pygame.Surface):
    s = pygame.Rect(0, 0, MAZE_BLOCK_WIDTH-1, MAZE_BLOCK_HEIGHT-1)
    e = pygame.Rect((MAZE_WIDTH-1) * MAZE_BLOCK_WIDTH, (MAZE_HEIGHT-1)*MAZE_BLOCK_HEIGHT, MAZE_BLOCK_WIDTH-1, MAZE_BLOCK_HEIGHT-1)
    pygame.draw.rect(surface, LIGHT_GREEN, s)
    pygame.draw.rect(surface, END_RED, e)
def draw_maze_bg(surface: pygame.Surface):
    print("BG DRAW")
    for i in range(0,MAZE_HEIGHT):
        for j in range(0,MAZE_WIDTH):
            r = pygame.Rect(i*MAZE_BLOCK_WIDTH, j*MAZE_BLOCK_HEIGHT, MAZE_BLOCK_WIDTH-1, MAZE_BLOCK_HEIGHT-1)
            #if (i != 0 and j != 0) and (i % 2 == 0 or j % 2 == 0) :
            #    pygame.draw.rect(surface, PURPLE, r)
            #else:
            print(i,j)
            pygame.draw.rect(surface, DESERT_TAN, r)
            #pygame.time.wait(1)
            #pygame.display.update()
    draw_start_end_blocks(surface)


    print("BG DRAW COMPLETE")
  
def is_valid_move(status_arr, x,y):
    if (x >= 0 and y >= 0) and (x < MAZE_WIDTH and y < MAZE_HEIGHT) and  get_gridspace(status_arr, x, y) in (0,"E"):
        return True
    return False

def mock_valid_random_move(status_arr: List[List[int]], curr_x :int, curr_y:int) -> Tuple[int,int,str]:
    DIRECTIONS_SET = ["N","S","E","W"]
    while(True):
        if not DIRECTIONS_SET:
            return (-1,-1, None)
        direction = choice(DIRECTIONS_SET)
        match direction:
            case "N":
                if is_valid_move(status_arr, curr_x, curr_y - 1):                      #is_valid_move(status_arr, curr_x, curr_y - 1) == True:
                    #print("failed")
                    return (curr_x, curr_y - 1, direction)
            case "E":
                if is_valid_move(status_arr, curr_x + 1, curr_y):
                    return (curr_x + 1, curr_y, direction)
            case "S":
                if is_valid_move(status_arr, curr_x, curr_y +1):
                    return (curr_x, curr_y + 1, direction)
            case "W":
                if is_valid_move(status_arr, curr_x - 1, curr_y):  
                    return (curr_x - 1, curr_y, direction)  
            
        DIRECTIONS_SET.remove(direction)
def get_gridspace(status_arr: List[List[int]], curr_x: int, curr_y: int) -> int:
    return status_arr[curr_y][curr_x]

def set_gridspace(status_arr: List[List[int]], curr_x: int, curr_y: int):
    status_arr[curr_y][curr_x] = 1

def draw_solution(surface: pygame.Surface, path: List[Tuple[int,int]]):
    print("Drawing this path: ", path)
    for x,y in path:
        r = pygame.Rect(x*MAZE_BLOCK_WIDTH, y*MAZE_BLOCK_HEIGHT, MAZE_BLOCK_WIDTH-1, MAZE_BLOCK_HEIGHT-1)
        pygame.draw.rect(surface, LIGHT_GREEN, r)
        pygame.time.wait(1)
        pygame.display.update()
    print("solution drawn")

def do_dfs(surface: pygame.Surface):
    FINAL_PATH = None
    status = [[ 0 for j in range(MAZE_HEIGHT)] for i in range(MAZE_WIDTH)]
    stack = []
    curr_x, curr_y = 0,0
    stack.append([curr_x, curr_y, [(curr_x, curr_y)]])
    path_up_to = [(0,0)]
    status[0][0] = "S"
    status[MAZE_HEIGHT-1][MAZE_WIDTH-1] = "E"
    while(stack):
        new_curr_x, new_curr_y, direction = mock_valid_random_move(status, curr_x, curr_y)
        if (new_curr_x, new_curr_y) == (-1,-1): #aka no valid move, must backtrack4
            #print(f"no_valid_moves from x:{curr_x} y:{curr_y}")
                                         # go to last known valid point
            #print(stack)
            stack.pop()
            if stack: 
                new_curr_x, new_curr_y, path_up_to =  stack[-1]  # cont...
                curr_x, curr_y = new_curr_x, new_curr_y     #update the old to be the new, then continue
            continue
        path_up_to.append((new_curr_x, new_curr_y))
        stack.append([new_curr_x, new_curr_y, path_up_to.copy()])          #make that move
        set_gridspace(status, new_curr_x, new_curr_y)   #make that move cont

        # draw the lines here aka break the walls
        # depending on the move, which is known to be valid at this point
        # {N,S,E,W} ---> draw the corresponding rectangle {center-up, center-down, fcenter-right, center-left}

        r = rect_select(direction, curr_x * MAZE_BLOCK_WIDTH, curr_y * MAZE_BLOCK_HEIGHT, MAZE_BLOCK_WIDTH - 1, MAZE_BLOCK_HEIGHT - 1)
        pygame.draw.rect(surface, DESERT_TAN, r)    #draw the rect from old to new old location
        draw_start_end_blocks(surface)
        pygame.display.update()
        if (new_curr_x, new_curr_y) == (MAZE_WIDTH - 1, MAZE_HEIGHT - 1) and FINAL_PATH ==  None: #aka we hit the bottom right
            print("PATH to destination", path_up_to)
            FINAL_PATH = path_up_to.copy()
            #draw_solution(surface, path_up_to)
        #pygame.time.wait(0.1)

        curr_x, curr_y = new_curr_x, new_curr_y     #update the old to be the new, then continue
    draw_solution(surface, FINAL_PATH)
if __name__ == '__main__': 
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("hello")
    surface.fill(PURPLE)
    pygame.display.flip()




    running = True
    making_maze = True
    while(running):




        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        if making_maze:
            draw_maze_bg(surface)
            do_dfs(surface)
        making_maze = False
