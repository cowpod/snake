# librarys
import random
import typing
#import math
from time import time
#import ctypes
from uuid import UUID
from collections import deque

# custom modules
from Position import *
from Colors import *

PAD=4
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
'''
my methods
'''

def in_bounds(game_state, x,y):
    if x<0 or x>=game_state["board"]["width"] or y<0 or y>=game_state["board"]["height"]:
        return False
    return True
    
def millis():
    return round(time() * 1000)

def build_matrix(game_state:{})->[]:
    '''
    builds matrix, populates with class Position and sublasses
    '''
    matrix=[[Position(x, y, 0) for x in range(game_state["board"]["height"])] for y in range(game_state["board"]["width"])]
    
    # set Foods in matrix
    for food in game_state["board"]["food"]:
        matrix[food["x"]][food["y"]] = Food(food["x"], food["y"])
    # set Hazards in matrix
    for hazard in game_state["board"]["hazards"]:
        matrix[hazard["x"]][hazard["y"]] = Hazard(hazard["x"], hazard["y"])
    # set Snakes in matrix
    for snake in game_state["board"]["snakes"]:
        for i,xy in enumerate(snake["body"]):
            new = Snake(xy["x"], xy["y"], UUID(snake["id"]), snake["length"], snake["health"], i==0)
            new.addWeight(i)
            matrix[xy["x"]][xy["y"]] = new
            
    return matrix
    
def print_matrix(game_state:{}, matrix:[])->None:
    '''
    print matrix
    '''
    for x_row in matrix:
        for y in x_row:
            if isinstance(y, Food):
                print(Colors.GREEN+str(y).ljust(PAD),end="")
            elif isinstance(y, Hazard):
                print(Colors.RED+str(y).ljust(PAD),end="")
            elif isinstance(y, Snake):
                if UUID(game_state["you"]["id"])==y.id:
                    print(Colors.BLUE+str(y).ljust(PAD),end="")
                else:
                    print(Colors.RED+str(y).ljust(PAD),end="")
            else:
                print(Colors.NONE+str(y).ljust(PAD),end="")
        print("")


#def bfs(matrix, start_row, start_col, weight):
#    visited = set() # keep track of visited cells
#    stack = [(start_row, start_col)] # initialize the stack with the starting cell
#
#    def bfs_recursive():
#        nonlocal weight,matrix
#        if not stack: # stop recursion if the stack is empty
#            return matrix
#
#        row, col = stack.pop() # pop a cell from the top of the stack
#        if (row, col) not in visited:
#            # mark the cell as visited
#            visited.add((row, col))
#
#            position=matrix[row][col]
#            if isinstance(position, Position):
#                if weight<=0:
#                    return matrix
#                print("bfs(): expanding food at:", position.tuple())
#                position.setWeight(weight)
#                weight=weight-1
#                matrix[row][col]=position
#
#            # check all four neighbors
#            for row_offset, col_offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
#                neighbor_row, neighbor_col = row + row_offset, col + col_offset
#                if (0 <= neighbor_row < len(matrix) and 0 <= neighbor_col < len(matrix[0]) and
#                    (neighbor_row, neighbor_col) not in visited):
#                    # push the neighbor onto the stack if it is within bounds and hasn't been visited yet
#                    stack.append((neighbor_row, neighbor_col))
#
#        # recurse on the remaining cells in the stack
#        bfs_recursive()
#
#    bfs_recursive()

def bfs(matrix, start_row, start_col, weight):
    # Define the queue and enqueue the starting node
    queue = deque([(start_row, start_col)])
    
    # Define the visited set and mark the starting node as visited
    visited = set([(start_row, start_col)])
    
    # Define the DIRECTIONS to traverse
      # right, down, left, up
    
    # Loop until the queue is empty
    while queue:
        # Dequeue the next node to visit
        current_row, current_col = queue.popleft()
                
        p=matrix[current_row][current_col]
        if weight>=0 and not isinstance(p,Snake) and not isinstance(p,Hazard) and not  isinstance(p,Food) and (current_row,current_col):
            weight=weight-1
            p.setWeight(weight)
            matrix[current_row][current_col]=p
            assert(matrix[current_row][current_col]==p)
        
        # Traverse all the neighboring nodes
        for direction in DIRECTIONS:
            next_row = current_row + direction[0]
            next_col = current_col + direction[1]
            
            # Check if the neighboring node is valid and unvisited
            if (next_row >= 0 and next_row < len(matrix) and
                next_col >= 0 and next_col < len(matrix[0]) and
                (next_row, next_col) not in visited):
                
                # Enqueue the neighboring node and mark it as visited
                queue.append((next_row, next_col))
                visited.add((next_row, next_col))
    return matrix
    
def mark_food(game_state:{}, matrix:[])->[]:
    '''
    marks matrix positions according to position contents
    '''
    
    for xy in game_state["board"]["food"]:
        position = matrix[xy["x"]][xy["y"]]
        if isinstance(position,Food):
            print("mark_food(): got food at "+str(position.tuple())+", "+str(position.weight()))
            matrix=bfs(matrix, xy["x"], xy["y"], position.weight())
    return matrix

'''
given game methods
'''

def info() -> typing.Dict:
    print("INFO")
    return {
        "apiversion": "1",
        "author": "cowpod",
        "color": "#ffcc00",
        "head": "sand-worm",
        "tail": "replit-notmark",
    }

def start(game_state: typing.Dict):
    print("GAME START")

def end(game_state: typing.Dict):
    print("GAME OVER\n")

# https://docs.battlesnake.com/api/example-move
def move(game_state: typing.Dict) -> typing.Dict:
    print("\nTurn:", game_state["turn"])
    
    # build matrix
    # Position: Food, Hazard, Snake
    matrix = build_matrix(game_state)
    
    
    # mark
    matrix = mark_food(game_state, matrix)
        
    # print matrix
    print_matrix(game_state, matrix)
    
    max_weight=0
    max_pos=None
    for direction in DIRECTIONS:
        x_n=game_state["you"]["head"]["x"]+direction[0]
        y_n=game_state["you"]["head"]["y"]+direction[1]
        if in_bounds(game_state, x_n, y_n):
            p = matrix[x_n][y_n]
            if p.weight()>max_weight:
                max_weight=p.weight()
                max_pos=p
            
    if max_pos == None:
        move=random.choice(["up", "down", "left", "right"])
        print("locked in? random!")
    else:
        m_x=game_state["you"]["head"]["x"]
        m_y=game_state["you"]["head"]["y"]
        print(max_pos.tuple(), max_pos.weight())
        
        if m_x < max_pos.x():
            move="right"
        elif m_x > max_pos.x():
            move="down"
        elif m_y < max_pos.y():
            move="up"
        elif m_y > max_pos.y():
            move="left"
        else:
            move=random.choice(["up", "down", "left", "right"])
            print("error? random!")
            
        print(move)
        return {"move": move}

if __name__ == "__main__":
    from server import run_server
    run_server({"info": info, "start": start, "move": move, "end": end})
