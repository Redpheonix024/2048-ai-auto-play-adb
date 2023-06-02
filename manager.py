
import ai
import time
import bridge


# d = {0:"u",1:"d",2:"l",3:"r"}

def runa(grid):
    #print("the grid is",grid)
    start_time = time.time()
    best = bridge.getbestmove(grid)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Function get best move took {execution_time:.6f} seconds.")
    # best['move'] = d[best['move']]
    # print("best move is hfy",best)
    return best
    



