import pygame
import math
from queue import PriorityQueue

width = 800
win = pygame.display.set_mode((width, width))
pygame.display.set_caption("Pathfinding Algorithm Visualizer")

class Node:
    def __init__(self, row, col, width, rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = pygame.Color('white')
        self.neighbours = []
        self.width = width
        self.rows = rows

    def getPos(self):
        return self.row, self.col

    def isClosed(self):
        return self.color == pygame.Color('purple')
    
    def isOpen(self):
        return self.color == pygame.Color('orange')

    def isWall(self):
        return self.color == pygame.Color('black')
    
    def isStart(self):
        return self.color == pygame.Color('green')
    
    def isEnd(self):
        return self.color == pygame.Color('red')

    def reset(self):
        self.color = pygame.Color('white')

    def makeClosed(self):
        self.color = pygame.Color('purple')
    
    def makeOpen(self):
        self.color = pygame.Color('orange')

    def makeWall(self):
        self.color = pygame.Color('black')
    
    def makeStart(self):
        self.color = pygame.Color('green')
    
    def makeEnd(self):
        self.color = pygame.Color('red')
    
    def makePath(self):
        self.color = pygame.Color('yellow')

    def draw(self,win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def updateNeighbours(self, grid):
        pass

    def __lt__(self, other):
        return False

def dist(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def makeGrid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    
    return grid

def drawGrid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, pygame.Color('grey'), (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, pygame.Color('grey'), (j * gap, 0), (j * gap, width))
    
def draw(win, grid, rows, width):
    win.fill(pygame.Color('white'))

    for row in grid:
        for node in row:
            node.draw(win)

    drawGrid(win, rows, width)

    pygame.display.update()

def getClickedPos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    rows = 50
    grid = makeGrid(rows, width)
    
    start = None
    end = None

    run = True
    searching = False
    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if searching:
                continue
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = getClickedPos(pos, rows, width)
                node = grid[row][col]
                if not start:
                    start = node
                    start.makeStart()
                elif not end:
                    end = node
                    end.makeEnd()
                elif (node != start) and (node != end):
                    node.makeWall()

            elif pygame.mouse.get_pressed()[2]:
                pass

                

    pygame.quit()

main(win, width)

    



    



