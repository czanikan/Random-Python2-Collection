#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randrange, randint
import win32api
import win32con
import os
import time

clear = lambda: os.system('cls')

player_x = 0
player_y = 0
vel_x = 0
vel_y = 0
fruit_x = 0
fruit_y = 0

w, h = 16, 9
a = [[]]
body = []
body_length = 0

def main():
    updateDisplay()

    while(True):
        inputManager()
        updatePosition()
        updateDisplay()
        manageFruit()

        time.sleep(0.1)
    
    term = input("Press [ENTER] to terminate.")

def updateDisplay():
    # Clear and redraw matrix
    clear()
    global a
    a = [["." for x in range(w)] for y in range(h)]

    a[fruit_y][fruit_x] = "O"

    a[player_y][player_x] = "@"

    for x in range(1, len(body)):
        a[body[x][1]][body[x][0]] = "#"

    for line in a:
        print("  ".join(map(str, line)))

def inputManager():
    global vel_x
    global vel_y
    global a

    # Move right
    if win32api.GetAsyncKeyState(win32con.VK_RIGHT):
        vel_x = 1
        vel_y = 0
        while (win32api.GetAsyncKeyState(win32con.VK_RIGHT) != 0):
            pass

    # Move left
    if win32api.GetAsyncKeyState(win32con.VK_LEFT):
        vel_x = -1
        vel_y = 0
        while (win32api.GetAsyncKeyState(win32con.VK_LEFT) != 0):
            pass

    # Move up
    if win32api.GetAsyncKeyState(win32con.VK_UP):
        vel_y = -1
        vel_x = 0
        while (win32api.GetAsyncKeyState(win32con.VK_UP) != 0):
            pass
    
    # Move down
    if win32api.GetAsyncKeyState(win32con.VK_DOWN):
        vel_y = 1
        vel_x = 0
        while (win32api.GetAsyncKeyState(win32con.VK_DOWN) != 0):
            pass

def updatePosition():
    global player_x
    global player_y
    global vel_x
    global vel_y
    global body

    player_x += vel_x
    player_y += vel_y

    if player_x > w-1:
        player_x = 0
    if player_x < 0:
        player_x = w-1
    if player_y > h-1:
        player_y = 0
    if player_y < 0:
        player_y = h-1

    head_pos = (player_x, player_y)
    body.insert(0, head_pos)
    last_n = len(body) - body_length
    body = body[:len(body)-last_n]

def manageFruit():
    global fruit_x
    global fruit_y
    global player_x
    global player_y
    global body_length

    if (fruit_x == player_x and fruit_y == player_y):
        body_length += 1
        placeFruit()

def placeFruit():
    global fruit_x
    global fruit_y
    global w
    global h

    fruit_x = randint(0, w)
    fruit_y = randint(0, h)


if __name__ == "__main__":
	main()
