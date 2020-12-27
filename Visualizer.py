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
        print(self.rows)
        if self.row < self.rows - 1 and not grid[self.row + 1][self.col].isWall(): #down
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].isWall(): #up
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.rows - 1 and not grid[self.row][self.col + 1].isWall(): #right
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].isWall(): #left
            self.neighbours.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

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
    
    return False

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
                
    pygame.quit()

main(win, width)

    



    



