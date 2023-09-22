from Map import Map_Obj
import heapq


class Node:
    def __init__(self, x, y, weight):
        self.x = x
        self.y = y
        self.weight = weight
        self.g = float('inf')  # Cost from start to this node
        self.h = 0  # Heuristic cost from this node to goal
        self.f = float('inf')  # Total cost from start to goal through this node
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f

def heuristic(node, goal):
    # Using Manhattan distance heuristic
    return abs(node.x - goal.x) + abs(node.y - goal.y)

def a_star(grid, start, goal):
    # Create a 2D array of Node objects from the grid
    nodes = [[Node(x, y, grid[x][y]) for y in range(len(grid[0]))] for x in range(len(grid))]

    # Define the start and goal nodes
    start_node = nodes[start[0]][start[1]]
    goal_node = nodes[goal[0]][goal[1]]

    # Initialize the open list as a min-heap and add the start node
    open_list = []
    heapq.heappush(open_list, start_node)

    # Set the g-cost of the start node to 0
    start_node.g = 0
    start_node.f = heuristic(start_node, goal_node)

    # Initialize a set for the closed list
    closed_list = set()

    # Start the search loop
    while open_list:
        # Get the node with the lowest f-cost from the open list
        current_node = heapq.heappop(open_list)

        # Add the current node to the closed list
        closed_list.add(current_node)

        # Check if we have reached the goal node
        if current_node == goal_node:
            # Retrieve the path
            path = []
            while current_node.parent:
                path.append((current_node.x, current_node.y))
                current_node = current_node.parent
            path.append((start_node.x, start_node.y))
            return path[::-1]

        # Generate the neighbors of the current node
        neighbors = [
            nodes[x][y]
            for x, y in [
                (current_node.x - 1, current_node.y),
                (current_node.x + 1, current_node.y),
                (current_node.x, current_node.y - 1),
                (current_node.x, current_node.y + 1),
            ]
            if 0 <= x < len(grid) and 0 <= y < len(grid[0]) and grid[x][y] >= 0
        ]

        for neighbor in neighbors:
            # If the neighbor is in the closed list, skip it
            if neighbor in closed_list:
                continue

            # Calculate the tentative g-cost of the neighbor
            tentative_g = current_node.g + neighbor.weight 

            # If this path to the neighbor is shorter than any previous paths, update the neighbor's details
            if tentative_g < neighbor.g:
                neighbor.g = tentative_g
                neighbor.h = heuristic(neighbor, goal_node)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.parent = current_node

                # If the neighbor is not in the open list, add it
                if neighbor not in open_list:
                    heapq.heappush(open_list, neighbor)

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
        path2 = a_star(map2.int_map, map2.start_pos, map2.end_goal_pos)
        for col in path2:
            map2.set_cell_value(pos=col, value="#")
        map2.show_map()    

def task3():
    map3 = Map_Obj(task=3)
    path3 = a_star(map3.int_map, map3.start_pos, map3.end_goal_pos)
    map3.show_map()

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