import sys
import tkinter as tk
import random
from tkinter import messagebox

root = tk.Tk()
root.title("Ouroboros")

if len(sys.argv) >= 2:
    HEIGHT = int(sys.argv[1]) 
    WIDTH = int(sys.argv[2])
else:
    HEIGHT = 500 
    WIDTH = 500

x1 = y1 = HEIGHT/2
foodx = foody = 200

direc = "none"
last_direc = "none"
delay = 100
start_loop = 1

list_of_rects = []
max_size = 5

score = 0
walls = [f"{HEIGHT/2} {WIDTH/2}"]
foodloc = f"{foodx} {foody}"

score_box = tk.Label(root, text=score)
score_box.pack()

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

starting_rect = canvas.create_rectangle(x1, y1, x1+10, y1+10, fill="green")

def generate_food():
    global HEIGHT, WIDTH, foodloc, foodx, foody, food
    foodx = float(random.randint(0, WIDTH/10) * 10)
    foody = float(random.randint(0, HEIGHT/10) * 10)
    if foodx == HEIGHT or 0:
        foodx = float(HEIGHT - 50)
    if foody == WIDTH or 0:
        foody = float(WIDTH - 50)
    foodloc = f"{foodx} {foody}"
    food = canvas.create_rectangle(foodx, foody, foodx+10, foody+10, fill="blue")
    print(f"f {foodloc}")

generate_food()

def draw_rect():
    list_of_rects.append(canvas.create_rectangle(x1, y1, x1+10, y1+10, fill="green"))
    if len(list_of_rects) > max_size:
        canvas.delete(list_of_rects[0])
        list_of_rects.pop(0)

def score_add():
    global score, x1, y1, foodx, foody, walls, foodloc, max_size, delay
    coords = str(x1) + " " + str(y1)
    if coords == foodloc:
        canvas.delete(food)
        max_size += 1
        score += 1
        if delay > 50:
            delay -= 5
        score_box["text"] = score
        generate_food()
    if coords in walls:
        messagebox.showinfo("you lose!", f"you lose! your final score was {score}")
        root.destroy()
    walls.append(coords)
    if len(walls) > max_size:
        walls.pop(0)


def move():
    global x1, y1, direc, delay
    if direc == "d":
        x1 += 10
        if x1 > WIDTH:
            x1 = 0
    elif direc == "a":
        x1 -= 10
        if x1 < 0:
            x1 = WIDTH
    elif direc == "s":
        y1 += 10
        if y1 > HEIGHT:
            y1 = 0
    elif direc == "w":
        y1 -= 10
        if y1 < 0:
            y1 = HEIGHT
    draw_rect()
    score_add()
    root.after(delay, move)

def direction(event):
    global direc, start_loop, starting_rect, last_direc
    if last_direc == "a" and event.char == "d":
        print("can't move in that direction")
    elif last_direc == "d" and event.char == "a":
        print("can't move in that direction")
    elif last_direc == "w" and event.char == "s":
        print("can't move in that direction")
    elif last_direc == "s" and event.char == "w":
        print("can't move in that direction")
    else:
        direc = event.char
        last_direc = direc
    canvas.delete(starting_rect)
    if start_loop == 1:
        move()
        start_loop = 0



root.bind("<Key>", direction)

root.mainloop()