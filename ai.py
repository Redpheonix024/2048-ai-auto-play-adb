from copy import deepcopy
import random
import helper
import time


def getbestmove(grid, runs):
    if not validate_grid(grid):
        raise ValueError("Invalid grid format")

    if not isinstance(runs, int) or runs <= 0:
        raise ValueError("Number of runs must be a positive integer")

    bestscore = 0
    bestmove = -1
    prev_grid = None
    free_squares = countFreeSquares(grid)
    print("Number of free squares:", free_squares)
    runs = calculate_runs(free_squares)
    print("Number of runs:", runs)
    for i in range(4):
        res, new_grid = multiplerandom(grid, i, runs, prev_grid)
        score = res['score']
        if score >= bestscore:
            bestscore = score
            bestmove = i
            bestmoveavg = res['avgmoves']
        prev_grid = new_grid

    return {'move': bestmove, 'score': bestscore, 'bestmoveavg': bestmoveavg}


def validate_grid(grid):
    if not isinstance(grid, list) or len(grid) != 4:
        return False
    for row in grid:
        if not isinstance(row, list) or len(row) != 4:
            return False
        for value in row:
            if not isinstance(value, int):
                return False
    return True


def calculate_runs(free_squares):
    #if free_squares <= 0:
    #    return 100
    #elif free_squares >= 15:
    #    return 1
    #else:
    #    # Linear interpolation formula
        return 1 #int((100 - free_squares * 100 / 15))

def countFreeSquares(grid):
    count = 0
    for row in grid:
        count += row.count(0)
        
    return count

def multiplerandom(grid, move, runs, prev_grid=None):
    total = 0
    min_score = float('inf')
    max_score = 0
    total_moves = 0
    for i in range(runs):
        res, new_grid = randRuns(grid, move, prev_grid)
        if res == -1:
            continue
        score = res['score']
        if score == -1:
            break
        total += score
        total_moves += res['moves']
        if score < min_score:
            min_score = score
        if score > max_score:
            max_score = score
    avg_score = total / runs if runs > 0 else 0
    avg_moves = total_moves / runs if runs > 0 else 0
    return {'score': avg_score, 'avgmoves': avg_moves}, new_grid


def randRuns(grid, move, prev_grid=None):
    g = deepcopy(grid)
    score = 0
    res = moveandaddrandtiles(g, move)
    if not res['moved']:
        return -1, None
    score += res['score']
    moves = 1
    prev_board = deepcopy(g)
    prev_move = move
    max_tile_pos = None
    while True:
        if not helper.movesavilable(g) or g == prev_board:
            new_move = chooseNewMove(g, prev_move, prev_grid)
            if new_move is None:
                break
            prev_move = new_move
        else:
            new_move = prev_move
        temp_grid = deepcopy(g)
        res = helper.move(new_move, temp_grid)
        if not res['moved']:
            continue
        score += res['score']
        max_tile_pos = findMaxTilePosition(temp_grid)
        helper.addRandomData(temp_grid)
        g = deepcopy(temp_grid)
        moves += 1
        prev_board = deepcopy(g)
    return {'moves': moves, 'score': score, 'max_tile_pos': max_tile_pos}, deepcopy(g)


def stackCorners(grid):
    corners = [(0, 0), (0, 3), (3, 0), (3, 3)]
    edges = [(0, 1), (0, 2), (1, 0), (1, 3), (2, 0), (2, 3), (3, 1), (3, 2)]
    
    available_tiles = []
    for i in range(4):
        for j in range(4):
            if grid[i][j] == 0:
                available_tiles.append((i, j))
    
    min_distance = float('inf')
    corner_pos = None
    
    for tile in available_tiles:
        i, j = tile
        if tile in corners and grid[i][j] == 0:
            grid[i][j] = getRandomTile()
            return
        elif tile in edges and grid[i][j] == 0:
            if abs(i - j) < min_distance:
                min_distance = abs(i - j)
                corner_pos = (i, j)
    
    if corner_pos is not None:
        grid[corner_pos[0]][corner_pos[1]] = getRandomTile()



def getRandomTile():
    # Returns a random tile based on the distribution of tile values
    # in the original game (90% chance for 2, 10% chance for 4)
    return 2 if random.random() < 0.9 else 4

def calculateSnakeScore(grid, snake_move):
    # Copy the grid to avoid modifying the original grid
    temp_grid = deepcopy(grid)
    
    # Make the snake move on the temporary grid
    makeSnakeMove(temp_grid, snake_move)
    
    # Calculate the score based on the snake algorithm
    score = 0
    for i in range(4):
        for j in range(4):
            # Assign higher scores to tiles near the corners
            if (i == 0 or i == 3) and (j == 0 or j == 3):
                score += temp_grid[i][j] * 10
            # Assign lower scores to tiles near the edges
            elif i == 0 or i == 3 or j == 0 or j == 3:
                score += temp_grid[i][j] * 5
    
    return score


def chooseNewMove(grid, prev_move, prev_grid):
    available_moves = [0, 1, 2, 3]
    if prev_grid is not None and grid == prev_grid:
        available_moves.remove(prev_move)
    random.shuffle(available_moves)
    max_tile_pos = findMaxTilePosition(grid)
    best_move = None
    max_combined_score = 0
    scores = []  # Store scores for threshold calculation
    for move in available_moves:
        temp_grid = deepcopy(grid)
        res = helper.move(move, temp_grid)
        if res['moved']:
            score = calculateMergeScore(temp_grid, max_tile_pos)
            logicscorce=calculateScore(temp_grid)
            monotonicity = calculateMonotonicity(temp_grid)
            freesqurescore=countFreeSquares(temp_grid)*2
            # Combine the score and monotonicity heuristics to determine the move score
            move_score = score + monotonicity * 5 + logicscorce * 5 + freesqurescore
            #print(move,"the scorce is",move_score)
            #time.sleep(1)

            # Check if a snake move is possible
            snake_move = snake_algorithm(temp_grid)
            if snake_move is not None:
                #print("using snake move")
                snake_score = calculateSnakeScore(temp_grid, snake_move)
                # Combine the snake score with the move score
                combined_score = move_score + snake_score*2
            else:
                combined_score = move_score

            # Prioritize moves with higher combined score
            if combined_score > max_combined_score:
                max_combined_score = combined_score
                best_move = move

            scores.append(combined_score)  # Store scores for threshold calculation

    # Calculate the threshold based on a percentage of the maximum combined score achieved
    if scores:
        threshold = max(scores) * 0.8  # Adjust the percentage as needed
    else:
        threshold = 0

    # Additional Functionality - Game Over Detection
    if best_move is None and not helper.movesavilable(grid):
        # No available moves and game-over situation
        # Implement game-over logic here if needed
        return None

    # Early termination if a satisfactory move is found
    if max_combined_score >= threshold:
        return best_move

    return None  # Return None when the grid is the same as the previous grid



#def chooseNewMove(grid, prev_move, prev_grid):
#    available_moves = [0, 1, 2, 3]
#    if prev_grid is not None and grid == prev_grid:
#        available_moves.remove(prev_move)
#    random.shuffle(available_moves)
#    max_tile_pos = findMaxTilePosition(grid)
#    best_move = None
#    max_combined_score = 0
#    max_monotonicity = -1
#    scores = []  # Store scores for threshold calculation
#    for move in available_moves:
#        temp_grid = deepcopy(grid)
#        res = helper.move(move, temp_grid)
#        if res['moved']:
#            score = calculateMergeScore(temp_grid, max_tile_pos)
#            monotonicity = calculateMonotonicity(temp_grid)
#             Combine the score and monotonicity heuristics to determine the move score
#            combined_score = score + monotonicity * 0.5 + calculateSnakeScore(temp_grid) * 2

#             Prioritize moves with higher combined score
#            if combined_score > max_combined_score:
#                max_combined_score = combined_score
#                best_move = move
#                max_monotonicity = monotonicity
#             If the move has the same combined score, prefer the one with higher monotonicity
#            elif combined_score == max_combined_score and monotonicity > max_monotonicity:
#                best_move = move
#                max_monotonicity = monotonicity

#            scores.append(combined_score)  # Store scores for threshold calculation

#     Calculate the threshold based on a percentage of the maximum score achieved
#    if scores:
#        threshold = max(scores) * 0.8  # Adjust the percentage as needed
#    else:
#        threshold = 0

#     Additional Functionality - Game Over Detection
#    if best_move is None and not helper.movesavilable(grid):
#         No available moves and game-over situation
#         Implement game-over logic here if needed
#        return None

#     Early termination if a satisfactory move is found
#    if max_combined_score >= threshold:
#        return best_move

#    return None  # Return None when the grid is the same as the previous grid



def moveandaddrandtiles(grid, dir):
    res = helper.move(dir, grid)
    if res['moved']:
        helper.addRandomData(grid)
        stackCorners(grid)
    return res

def stackCorners(grid):
    corners = [(0, 0), (0, 3), (3, 0), (3, 3)]
    edges = [(0, 1), (0, 2), (1, 0), (1, 3), (2, 0), (2, 3), (3, 1), (3, 2)]
    
    available_tiles = []
    for i in range(4):
        for j in range(4):
            if grid[i][j] == 0:
                available_tiles.append((i, j))
    
    min_distance = float('inf')
    corner_pos = None
    
    for tile in available_tiles:
        i, j = tile
        if tile in corners and grid[i][j] == 0:
            grid[i][j] = getRandomTile()
            return
        elif tile in edges and grid[i][j] == 0:
            if abs(i - j) < min_distance:
                min_distance = abs(i - j)
                corner_pos = (i, j)
    
    if corner_pos is not None:
        grid[corner_pos[0]][corner_pos[1]] = getRandomTile()
    
    pileUpBottomRight(grid)


def pileUpBottomRight(grid):
    empty_positions = []
    for i in range(4):
        for j in range(4):
            if grid[i][j] == 0:
                empty_positions.append((i, j))

    # Sort empty positions based on their distance from the bottom right corner
    empty_positions.sort(key=lambda pos: abs(pos[0] - 3) + abs(pos[1] - 3))

    for pos in empty_positions:
        i, j = pos
        if grid[i][j] == 0:
            grid[i][j] = getRandomTile()
            break


def calculateScore(grid):
    corners = [(0, 0), (0, 3), (3, 0), (3, 3)]
    edges = [(0, 1), (0, 2), (1, 0), (1, 3), (2, 0), (2, 3), (3, 1), (3, 2)]
    center = [(1, 1), (1, 2), (2, 1), (2, 2)]
    
    score = 0
    for i in range(4):
        for j in range(4):
            if (i, j) in corners and grid[i][j] != 0:
                score += grid[i][j] * 2
            elif (i, j) in edges and grid[i][j] != 0:
                score += grid[i][j] * 3
            elif (i, j) in center and grid[i][j] != 0:
                score -= grid[i][j]
    
    return score

# Pre-calculate distance values for the calculateMergeScore function
distance_lookup = [[abs(i - j) + 1e-6 for j in range(4)] for i in range(4)]

def calculateMonotonicity(grid):
    monotonicity = 0
    for i in range(4):
        row_values = [grid[i][j] for j in range(4)]
        monotonicity += calculateRowMonotonicity(row_values)
    return monotonicity


def calculateRowMonotonicity(row):
    # Calculate the monotonicity of a row
    increasing = all(row[i] <= row[i + 1] for i in range(len(row) - 1))
    decreasing = all(row[i] >= row[i + 1] for i in range(len(row) - 1))
    return 1 if increasing or decreasing else 0


def calculateBalance(grid):
    balance = 0
    for i in range(4):
        for j in range(4):
            if i > 0:
                balance += abs(grid[i][j] - grid[i - 1][j])
            if j > 0:
                balance += abs(grid[i][j] - grid[i][j - 1])
    return balance


def findMaxTilePosition(grid):
    max_tile = 0
    max_pos = (0, 0)
    for i in range(4):
        for j in range(4):
            if grid[i][j] > max_tile:
                max_tile = grid[i][j]
                max_pos = (i, j)
    return max_pos


EPSILON = 1e-6

def calculateMergeScore(grid, max_tile_pos):
    max_tile = grid[max_tile_pos[0]][max_tile_pos[1]]
    score = 0
    for i in range(4):
        for j in range(4):
            if grid[i][j] > 0:
                distance = distance_lookup[i][j]
                score += grid[i][j] / distance
    return score

def snake_algorithm(grid):
    max_value = max(max(row) for row in grid)  # Find the maximum value in the grid
    max_tile_pos = None
    corner_tiles = []
    edge_tiles = []

    # Iterate over the grid to find the positions of maximum value, corners, and edges
    for i in range(4):
        for j in range(4):
            if grid[i][j] == max_value:
                max_tile_pos = (i, j)
            if (i == 0 or i == 3) and (j == 0 or j == 3):
                corner_tiles.append((i, j))
            elif i == 0 or i == 3 or j == 0 or j == 3:
                edge_tiles.append((i, j))

    # Sort the corner and edge tiles in descending order based on their values
    corner_tiles.sort(key=lambda pos: grid[pos[0]][pos[1]], reverse=True)
    edge_tiles.sort(key=lambda pos: grid[pos[0]][pos[1]], reverse=True)

    # Move the maximum value to the first corner tile
    if max_tile_pos not in corner_tiles:
        if corner_tiles:
            corner = corner_tiles[0]
            move = calculate_move(max_tile_pos, corner)
            return move

    # Move the next maximum value to the nearest edge tile
    if len(corner_tiles) >= 2 and edge_tiles:
        next_max_value = grid[corner_tiles[1][0]][corner_tiles[1][1]]
        nearest_edge = find_nearest_edge(edge_tiles)
        move = calculate_move(corner_tiles[1], nearest_edge)
        return move

    # If the above conditions are not met, choose a random available move
    available_moves = [0, 1, 2, 3]
    random.shuffle(available_moves)
    return available_moves[0]  # Return a random move


def calculate_move(start_pos, end_pos):
    # Calculate the move direction based on the start and end positions
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    if dx == 1:
        return 2  # Down
    elif dx == -1:
        return 0  # Up
    elif dy == 1:
        return 3  # Right
    elif dy == -1:
        return 1  # Left


def find_nearest_edge(edge_tiles):
    distances = [sum((abs(tile[0] - 1.5), abs(tile[1] - 1.5))) for tile in edge_tiles]
    min_distance = min(distances)
    min_distance_indices = [i for i, distance in enumerate(distances) if distance == min_distance]
    return edge_tiles[random.choice(min_distance_indices)]



def makeSnakeMove(grid, snake_move):
    if snake_move == 0:  # Move up
        for j in range(4):
            for i in range(1, 4):
                if grid[i][j] != 0:
                    moveTile(grid, i, j, -1, 0)
    elif snake_move == 1:  # Move down
        for j in range(4):
            for i in range(2, -1, -1):
                if grid[i][j] != 0:
                    moveTile(grid, i, j, 1, 0)
    elif snake_move == 2:  # Move left
        for i in range(4):
            for j in range(1, 4):
                if grid[i][j] != 0:
                    moveTile(grid, i, j, 0, -1)
    elif snake_move == 3:  # Move right
        for i in range(4):
            for j in range(2, -1, -1):
                if grid[i][j] != 0:
                    moveTile(grid, i, j, 0, 1)

def moveTile(grid, i, j, di, dj):
    while 0 <= i + di < 4 and 0 <= j + dj < 4 and grid[i + di][j + dj] == 0:
        grid[i][j], grid[i + di][j + dj] = grid[i + di][j + dj], grid[i][j]
        i += di
        j += dj

#grid = [
#    [0, 2, 0, 0],
#    [0, 4, 0, 0],
#    [8, 0, 0, 0],
#    [0, 0, 0, 0]
#]
#runs=3
#best = getbestmove(grid,runs)
#print(best)