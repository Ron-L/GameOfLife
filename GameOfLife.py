'''
Conway's Game of Life:
    Any live cell with fewer than two live neighbours dies, as if by underpopulation.
    Any live cell with two or three live neighbours lives on to the next generation.
    Any live cell with more than three live neighbours dies, as if by overpopulation.
    Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
'''

import cv2
import numpy as np

IMG_TITLE = "Conway's Game of Life"
WH = 1000                           # window height
WW = 1000                           # window width
GRID_HEIGHT = 200                   # cell grid dimensions
GRID_WIDTH = 200
SEGMENT_COLOR = (148, 42, 24)       # (B,G,R)   Dark blue
BACKGROUND_COLOR = (255,255,255)    # (B,G,R)   White
SCALE = int(WH / GRID_HEIGHT)
WAIT_FOR_KEY_MS = 1                 # 1 is fast, 100 is slow
INITIAL_X = 10
INITIAL_Y = 10

# P
PATTERN = [
            [1, 1, 1, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 1, 1],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
]

# Gosper glider gun
PATTERN = [
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1],
]


# Population #5
PATTERN = [
            [0, 1, 0],
            [1, 1, 0],
            [0, 1, 1],
]

# R-Pentomino
PATTERN = [
            [0, 1, 1],
            [1, 1, 0],
            [0, 1, 0],
]

# Diehard
PATTERN = [
            [0, 0, 0, 0, 0, 0, 1, 0],
            [1, 1, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 1, 1],
]

# Acorn
PATTERN = [
            [0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0],
            [1, 1, 0, 0, 1, 1, 1],
]

# pi
PATTERN = [
            [1, 1, 1],
            [1, 0, 1],
            [1, 0, 1],
]


PATTERN = '''
000000000000000000001
00000000000000000001
0000000000000000001
000000000000000001
00000000000000001
0000000000000001
000000000000001
00000000000001
0000000000001
000000000001
00000000001
0000000001
000000001
00000001
0000001
000001
00001
0001
 111
1  1
 11
'''


# declare a grid row(y/GRID_HEIGHT) first by column(x/GRID_WIDTH)
# this means we vary the x/column for each y/row which is how I think of iterating
# through an array. The downside is that the reference of x and y is backwards
# of the normal coordinate specs (x,y):  grid[y][x], grid[column][row]. oh well
# we could iterate down the columns first (by row). It makes no difference to the
# rules. But I chose the other.
currGrid =  [[0 for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]
nextGrid =  [[0 for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]

img = None
gen = 0

def main():
    global img
    global currGrid
    global nextGrid


    # populate initial grid
    if type(PATTERN) is list:
        copy2DArray(PATTERN, currGrid, INITIAL_X, INITIAL_Y)
    else:
        textTo2DArray(PATTERN, currGrid, INITIAL_X, INITIAL_Y-1)  # y-1 since first line is empty

    # create the image
    # display the initial grid in the image
    # show the image
    # wait on a key
    createImg_displayGrid_show_wait(currGrid)

    while(True):
        # populate the next generation
        populateNextGen()

        # create the image
        # display the grid in the image
        # show the image
        # wait on a key
        createImg_displayGrid_show_wait(nextGrid)

        # move nextGrid to grid and reset nextGrid
        currGrid = nextGrid
        nextGrid = [[0 for x in range(GRID_WIDTH)] for y in range(GRID_HEIGHT)]


def createImg_displayGrid_show_wait(grid):
    global img
    global gen

    # Create an image with 3 channels for BGR
    img = np.zeros((WH, WW, 3), np.uint8)

    # blank the window
    img[:,0:WW] = BACKGROUND_COLOR

    # display next gen
    displayGrid(grid)

    # display built image
    cv2.imshow(IMG_TITLE, img)
    cv2.setWindowTitle(IMG_TITLE, IMG_TITLE+f': Generation {gen}')
    gen += 1

    # wait on input forever (any key)
    #cv2.waitKey(0)

    # wait on input 1 ms
    k = cv2.waitKey(WAIT_FOR_KEY_MS)
    if k == 27: #escape
        return


def populateNextGen():
    for y in range(len(nextGrid)):
        for x in range(len(nextGrid[y])):
            nc = countNeighbors(x, y)
            if currGrid[y][x] == 1:
                if 2 <= nc <= 3:
                    # Any live cell with two or three live neighbours lives on to the next generation.
                    nextGrid[y][x] = 1
                else:
                    # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
                    # Any live cell with more than three live neighbours dies, as if by overpopulation.
                    # i.e. 2 > nc > 3
                    # nextGrid[y][x] = 0  # no need to set to 0, nextGrid was initialized to 0
                    pass
            else:
                # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
                if nc == 3:
                    nextGrid[y][x] = 1


def displayGrid(grid):
    global img

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 1:
                img = cv2.rectangle(img, (x*SCALE, y*SCALE), ((x+1)*SCALE, (y+1)*SCALE), (0,0,0), -1)


# count the 1's in the 8 surrounding cells of current grid
# Note the inputs are in x, y order
def countNeighbors(x, y):
    count = 0
    for y1 in range(y-1, y+1+1):

        # don't go above top row
        if y1 < 0:
            continue

        # don't go below bottom row
        if y1 >= len(currGrid):
            break

        for x1 in range(x-1, x+1+1):

            # don't go left of left column
            if x1 < 0:
                continue

            # don't go right of right column
            if x1 >= len(currGrid[y1]):
                break

            # skip self
            if x1 == x and y1 == y:
                continue

            # count?
            if currGrid[y1][x1] != 0:
                count += 1
    return count


"""Copies a 2D array into another larger 2D array at a given position.

Args:
    src: The source 2D array.
    dest: The destination 2D array.
    x: The x-coordinate of the top-left corner where the source array
        should be copied in the destination array.
    y: The y-coordinate of the top-left corner where the source array
        should be copied in the destination array.
"""
def copy2DArray(src, dst, x, y):

    for y1 in range(len(src)):
        for x1 in range(len(src[y1])):
            dst[y + y1][x + x1] = src[y1][x1]
    pass


# let the user enter patterns as series of 0's (or blanks) and 1's in text
def textTo2DArray(text, dst, x, y):
    y1 = 0
    x1 = 0
    for l in text:
        if l == '1':
            dst[y + y1][x + x1] = 1
        elif l == '\n':
            x1 = -1  # below will increment to 0
            y1 += 1
        x1 += 1
    pass


if __name__ == '__main__':
    main()
    pass
