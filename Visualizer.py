import pygame
import math
import random
from queue import PriorityQueue

pygame.init()
width = 800
win = pygame.display.set_mode((width, width))
pygame.display.set_caption("Pathfinding Algorithm Visualizer")
clock = pygame.time.Clock()

click = False

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
        return self.color == pygame.Color('orchid3')
    
    def isOpen(self):
        return self.color == pygame.Color('plum1')

    def isWall(self):
        return self.color == pygame.Color('black')
    
    def isStart(self):
        return self.color == pygame.Color('green')
    
    def isEnd(self):
        return self.color == pygame.Color('red')

    def reset(self):
        self.color = pygame.Color('white')

    def makeClosed(self):
        self.color = pygame.Color('orchid3')
    
    def makeOpen(self):
        self.color = pygame.Color('plum1')

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
        self.neighbours = []
        if self.row < self.rows - 1 and not grid[self.row + 1][self.col].isWall(): #down
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].isWall(): #up
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.rows - 1 and not grid[self.row][self.col + 1].isWall(): #right
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].isWall(): #left
            self.neighbours.append(grid[self.row][self.col - 1])

def dist(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1-y2)

def reconstructPath(cameFrom, end, draw):
    while end in cameFrom:
        end = cameFrom[end]
        end.makePath()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    openSet = PriorityQueue()
    openSet.put((0, count, start))
    cameFrom = {}
    gScore = {node: float("inf") for row in grid for node in row}
    gScore[start] = 0

    fScore = {node: float("inf") for row in grid for node in row}
    fScore[start] = dist(start.getPos(), end.getPos())

    openSetHash = {start}

    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = openSet.get()[2]
        openSetHash.remove(current)

        if current == end: #make path
            reconstructPath(cameFrom, end, draw)
            end.makeEnd()
            start.makeStart()

            return True

        for neighbour in current.neighbours:
            temp_gScore = gScore[current] + 1
            if temp_gScore < gScore[neighbour]:
                cameFrom[neighbour] = current
                gScore[neighbour] = temp_gScore
                fScore[neighbour] = temp_gScore + dist(neighbour.getPos(), end.getPos())
                if neighbour not in openSetHash:
                    count += 1
                    openSet.put((fScore[neighbour], count, neighbour))
                    openSetHash.add(neighbour)
                    neighbour.makeOpen()
                
        draw()

        if current != start:
            current.makeClosed()
    
    print("No Solution")

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

def main(win, width, randomWalls):
    rows = 50
    grid = makeGrid(rows, width)
    howManyWalls = 500
    start = None
    end = None
    run = True

    if randomWalls:
        for i in range(howManyWalls):
            randX = random.randint(1, rows - 1)
            randY = random.randint(1, rows - 1)
            grid[randX][randY].makeWall()

    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = getClickedPos(pos, rows, width)
                node = grid[row][col]
                if not start and node != end:
                    start = node
                    start.makeStart()
                elif not end and node != start:
                    end = node
                    end.makeEnd()
                elif node != start and node != end:
                    node.makeWall()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = getClickedPos(pos, rows, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.updateNeighbours(grid)
                    algorithm(lambda: draw(win, grid, rows, width), grid, start, end)

                if event.key == pygame.K_BACKSPACE:
                    start = None
                    end = None
                    grid = makeGrid(rows, width)
                    menu(click)
                
    pygame.quit()

font = pygame.font.SysFont('Century Gothic', 50)
font2 = pygame.font.SysFont('Calibri', 20)
font3 = pygame.font.SysFont('Arial', 22)
def renderText(text, font, colour, window, x, y):
    render = font.render(text, True, colour)
    textRect = render.get_rect()
    textRect.center = (x, y)
    window.blit(render, textRect)


def menu(click):
    run = True
    generateWalls = False
    while run:
        win.fill(pygame.Color('DeepSkyBlue'))

        astarButton = pygame.Rect(100,250,600,100)
        pygame.draw.rect(win, pygame.Color('grey'), astarButton)

        dijkstraButton = pygame.Rect(100,400,600,100)
        pygame.draw.rect(win, pygame.Color('grey'), dijkstraButton)

        renderText("Pathfinding Visualizer", font, pygame.Color('red'), win, width/2, 75)
        renderText("Select an Algorithm", font2, pygame.Color('red'), win, width/2, 150)
        renderText("A* Search", font, pygame.Color('red'), win, width/2, 300)
        renderText("Generate random walls?", font3, pygame.Color('black'), win, 680, 660)
        renderText("Dijkstra's Algorithm", font, pygame.Color('red'), win, width/2, 450)

        randomWallButton = pygame.Rect(700,700,50,50)
        if generateWalls == False:
            pygame.draw.rect(win, pygame.Color('grey'), randomWallButton)
        elif generateWalls == True:
            pygame.draw.rect(win, pygame.Color('green'), randomWallButton)
        
        

        mx, my = pygame.mouse.get_pos()
        if astarButton.collidepoint((mx, my)):
            if click:
                main(win, width, generateWalls)
                
        if randomWallButton.collidepoint((mx,my)):
            if click:
                if generateWalls == False:
                    generateWalls = True
                else:
                    generateWalls = False

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]:
                click = True

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

menu(click)

    



    



