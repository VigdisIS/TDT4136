from Map import Map_Obj
import heapq

# Using the steps listed in https://www.geeksforgeeks.org/a-search-algorithm/ as source for the A* algorithm

# Class to represent a node in the search tree
class Node:
    def __init__(self, x, y, weight):
        self.x = x # x coordinate
        self.y = y # y coordinate
        self.weight = weight # weight of the node
        self.g = float('inf')  # Cost from start to this node
        self.h = 0  # Heuristic cost from this node to goal
        self.f = float('inf')  # Total cost from start to goal through this node
        self.parent = None # Parent node

    # Python lt method to compare the node with another node
    # https://www.geeksforgeeks.org/python-__lt__-magic-method/
    def __lt__(self, other):
        return self.f < other.f

def heuristic(current, goal):
    # We're only allowed to move in four directions, so we'll use Manhattan distance
    return abs(current.x - goal.x) + abs(current.y - goal.y)

def a_star(grid, start, goal):
    # Create a 2D array of Node objects from the grid
    nodes = []
    for x in range(len(grid)):
        nodes.append([])
        for y in range(len(grid[0])):
            nodes[x].append(Node(x, y, grid[x][y]))

    # Define the start and goal nodes from our 2D array of nodes
    start_node = nodes[start[0]][start[1]]
    goal_node = nodes[goal[0]][goal[1]]

    # Intialilze the open and closed list
    open_list = []
    closed_list = set()

    # Add the start node to the open list
    heapq.heappush(open_list, start_node)

    # Set the g and f-cost of the start node to 0
    start_node.g = 0
    start_node.f = 0

    # While the open list is not empty
    while open_list:
        # Find the node with the least f in the open list and pop it off the list
        q = heapq.heappop(open_list)

        # Push q to the closed list
        closed_list.add(q)

        # Check if we have reached the goal node
        if q == goal_node:
            # Retrieve the path
            path = []
            while q.parent:
                path.append((q.x, q.y))
                q = q.parent
            path.append((start_node.x, start_node.y))
            return path[::-1]

        # Generate the current node's 4 successors from the 2D array of nodes
        successor_tuples = [((q.x - 1), q.y), ((q.x + 1), q.y), (q.x, (q.y - 1)), (q.x, (q.y + 1))]
        successors = []
        for x, y in successor_tuples:
            # Only add coordinates that are inside the grid and non-negative (weight >= 0)
            if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] >= 0:
                successors.append(nodes[x][y])
            
        # Iterate through the successors of the current node
        for successor in successors:            
            # If the successor is in the closed list, skip it
            if successor in closed_list:
                continue

            # Calculate the tentative g-cost of the successor
            succ_tentative_g = q.g + successor.weight 

            # If this path to the successor is shorter than any previous paths, update the successor's details
            if succ_tentative_g < successor.g:
                successor.g = succ_tentative_g
                successor.h = heuristic(successor, goal_node)
                successor.f = successor.g + successor.h
                successor.parent = q

                # If the successor is not in the open list, add it
                if successor not in open_list:
                    heapq.heappush(open_list, successor)

    # If we get here, it means there's no path from start to goal
    return None    

def task1(): 
     map1 = Map_Obj()
     map1.show_map()
     path1 = a_star(map1.int_map , map1.start_pos, map1.end_goal_pos)
     for cell in path1:
        map1.set_cell_value(pos=cell, value="#")
     map1.show_map()    

def task2():
        map2 = Map_Obj(task=2)
        map2.show_map()
        path2 = a_star(map2.int_map, map2.start_pos, map2.end_goal_pos)
        for col in path2:
            map2.set_cell_value(pos=col, value="#")
        map2.show_map()    

def task3():
    map3 = Map_Obj(task=3)
    map3.show_map()
    path3 = a_star(map3.int_map, map3.start_pos, map3.end_goal_pos)
    for col in path3:
        map3.set_cell_value(pos=col, value="#")
    map3.show_map()

def task4():
    map4 = Map_Obj(task=4)
    map4.show_map()
    path4 = a_star(map4.int_map, map4.start_pos, map4.end_goal_pos)
    for col in path4:
        map4.set_cell_value(pos=col, value="#")
    map4.show_map()

def main():
    task1()
    task2()
    task3()
    task4()

if __name__ == "__main__":
    main()
