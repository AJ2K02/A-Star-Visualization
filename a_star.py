import tkinter as tk
from math import sqrt
import time
from random import randint


sps = 60
root_side = 720
# size of a side in px

square_side = root_side / sps
# size of the side of a square in px


walls = []

click_mode = "start"


start = (-1, -1)
end = (-1, -1)


def display_squares():
    global w
    x = 0
    y = 0
    while y < sps:
        while x < sps:
            w.create_rectangle(x * square_side, y * square_side, (x + 1) * square_side, (y + 1) * square_side, fill="white")
            x += 1
        x = 0
        y += 1



def color_square(sq, type):
    global w, sps
    if type == "open":
        w.itemconfigure(sq[1] * sps + sq[0] + 1, fill="blue")
    if type == "closed":
        w.itemconfigure(sq[1] * sps + sq[0] + 1, fill="red")
    if type == "path":
        w.itemconfigure(sq[1] * sps + sq[0] + 1, fill="green")



def h(current, end):
    return sqrt((current[0] - end[0]) ** 2 + (current[1] - end[1]) ** 2)

def ha(current, end):
    return abs(current[0] - end[0]) + abs(current[1] - end[1])


def get_neighbors(node):
    neighbors = []
    if node[0] > 0:
        neighbors.append((node[0] - 1, node[1]))
        if node[1] > 0:
            neighbors.append((node[0] - 1, node[1] - 1))
        if node[1] < sps - 1:
            neighbors.append((node[0] - 1, node[1] + 1))
    if node[0] < sps - 1:
        neighbors.append((node[0] + 1, node[1]))
        if node[1] > 0:
            neighbors.append((node[0] + 1, node[1] - 1))
        if node[1] < sps - 1:
            neighbors.append((node[0] + 1, node[1] + 1))
    if node[1] > 0:
        neighbors.append((node[0], node[1] - 1))
    if node[1] < sps - 1:
        neighbors.append((node[0], node[1] + 1))

    return neighbors


def get_path(came_from):
    global end, start
    current = end
    path = []
    while current != start:
        path.append(current)
        color_square(current, "path")
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


def get_best_node(open, f, g, h):
    best_node = open[0]
    for node in open:
        if f[node] < f[best_node]:
            best_node = node
        elif f[node] <= f[best_node] and h[node] < h[best_node]:
            best_node = node
        elif f[node] <= f[best_node] and h[node] <= h[best_node] and g[node] < g[best_node]:
            best_node = node
    return best_node



def a_star():

    global start, end, walls, sps
    closed_set = []
    open_set = [start]
    came_from = {start:None}
    gscore = {start:0}
    hscore = {start:h(start,end)}
    fscore = {start:gscore[start] + hscore[start]}
    while len(open_set) != 0:
        current = get_best_node(open_set, fscore, gscore, hscore)
        if current == end:
            print("end")
            return get_path(came_from)
        for neighbor in get_neighbors(current):
            if neighbor in closed_set or neighbor in walls:
                continue
            g_to_add = 1.4
            if neighbor[0] == current[0] or neighbor[1] == current[1]:
                g_to_add = 1
            if neighbor not in open_set:
                open_set.append(neighbor)
                color_square(neighbor, "open")
                came_from[neighbor] = current
                gscore[neighbor] = gscore[came_from[neighbor]] + g_to_add
                hscore[neighbor] = h(neighbor, end)
                fscore[neighbor] = gscore[neighbor] + hscore[neighbor]
            if gscore[neighbor] > gscore[came_from[neighbor]] + g_to_add:
                came_from[neighbor] = current
                gscore[neighbor] = gscore[came_from[neighbor]] + g_to_add
                hscore[neighbor] = h(neighbor, end)
                fscore[neighbor] = gscore[neighbor] + hscore[neighbor]

        open_set.remove(current)
        color_square(current, "closed")
        closed_set.append(current)
        root.update()
        #time.sleep(0.4)
        #input("Next?")



def key_press(event):
    global root, click_mode, w, sps
    if repr(event.char) == repr("a"):
        print(a_star())
    elif repr(event.char) == repr("s"):
        click_mode = "start"
    elif repr(event.char) == repr("e"):
        click_mode = "end"
    elif repr(event.char) == repr("w"):
        click_mode = "wall"
    elif repr(event.char) == repr("r"):
        for i in range(sps):
            for j in range(sps):
                if randint(0, 100) < 60:
                    walls.append((j, i))
                    w.itemconfigure(i * sps + j + 1, fill="black")


def click(event):
    global w
    index_x = int(event.x * sps / root_side)
    index_y = int(event.y * sps / root_side)
    if click_mode == "start":
        global start
        if start[0] != -1:
            print("2 starting nodes, error")
        w.itemconfigure(index_y * sps + index_x + 1, fill="orange")
        start = (index_x, index_y)
    elif click_mode == "end":
        global end
        if end[0] != -1:
            print("2 starting nodes, error")
        w.itemconfigure(index_y * sps + index_x + 1, fill="purple")
        end = (index_x, index_y)
    elif click_mode == "wall":
        w.itemconfigure(index_y * sps + index_x + 1, fill="black")
        walls.append((index_x, index_y))



root = tk.Tk()
root.title("A* Visualization")
root.geometry(str(root_side) + "x" + str(root_side))
w = tk.Canvas(root, width=root_side, height=root_side)
w.pack()
w.bind("<Key>", key_press)
w.bind("<Button-1>", click)
w.focus_set()


display_squares()

root.mainloop()
