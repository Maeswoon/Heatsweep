
GRID_SIZE = 6
EMPTY = 0
HOTSPOT = 3
GRID = [ 
    [3, 0, 0, 0, 2, 2],
    [1, 1, 0, 0, 2, 0],
    [0, 1, 1, 2, 0, 2],
    [0, 2, 2, 1, 2, 0],
    [2, 1, 1, 0, 1, 0],
    [0, 2, 2, 0, 2, 0]
]

# grid of 0s of size gridSize
def emptyGrid(gridSize):
    return [[0]*gridSize for _ in range(gridSize)]

# return a list of all the coords within a 3x3 square around (x,y) if in the grid
# I'm sure there's a cleaner way to do this but honestly this is the most readable I can do
def getAdjacent(x, y, gridSize):
    coords = []
    for xi in [x-1, x, x+1]:
        for yi in [y-1, y, y+1]:
            if 0 <= xi < gridSize and 0 <= yi < gridSize: # make sure coords within grid
                coords.append((xi, yi))
    return coords

def processAdjacent(x, y, player, grid, checked):
    checked[y][x] = 1 # mark current coord as checked
    for (xi, yi) in getAdjacent(x, y, GRID_SIZE):
        # base case: hotspot is adjacent to us
        if grid[yi][xi] == HOTSPOT:
            return True
        
        if checked[yi][xi] == 0 and grid[yi][xi] == player:
            # recurse on adjacent un-checked squares owned by player
            if processAdjacent(xi, yi, player, grid, checked):
                return True
    
    # base case: no path to hotspot
    return False

def checkWinHardcoded(grid, player: int):
    # hardcoded; these would come from the board
    (hx, hy) = (0, 0) # hotspot x, hotspot y
    (p1x, p1y) = (0, 1)
    (p2x, p2y) = (5, 0)

    # step 0: check if the hotspot is flipped
    if grid[hy][hx] == 0:
        return False
    
    # recursively build out pathway from hotspot 
    checked = emptyGrid(GRID_SIZE) # initialize matrix of 0s
    if player == 1:
        return processAdjacent(p1x, p1y, 1, grid, checked)
    else:
        return processAdjacent(p2x, p2y, 2, grid, checked)

def generateHeatMap(hx, hy, gridSize):
    # validate arguments
    if not (0 <= hx < gridSize and 0 <= hy < gridSize):
        raise ValueError("Heat location outside of grid")
    
    # generate a grid of heats with 255 at hx, hy


if __name__ == "__main__":
    print("GRID:")
    for row in GRID:
        print(row)

    print("P1 win: ", checkWinHardcoded(GRID, 1))
    print("P2 win: ", checkWinHardcoded(GRID, 2))