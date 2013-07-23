#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Author: Joao S. O. Bueno
# LGPL. v3.0

MAX_CASCADES = 400

import os, sys, time
from random import randrange, choice

sh = os.system
pr = sys.stdout.write
esqs = "\x1b["
getchars = lambda start, end: [unichr(i) for i in xrange(start, end)]

black, green, white = "30", "32", "37"

latin = getchars(0x30, 0x7e)
greek = getchars(0x390, 0x3cf)
hebrew = getchars(0x590, 0x5FF)

chars= latin + greek # + hebrew

def init():
    global cols, lines
    sh("setterm -cursor off")
    cols = int(os.popen("tput cols").read())
    lines = int(os.popen("tput lines").read())

def end():
    pr(esqs + "m")
    sh("clear")
    sh("setterm -cursor on")

def print_at(char, x, y, color="", bright="0"):
    pr("%s%d;%df" %(esqs, y, x))
    pr(esqs + bright + ";" + color + "m")
    pr(char.encode("utf-8"))

def update_line(speed, counter, line):
    counter += 1
    if counter >= speed:
        line += 1
        counter = 0
    return counter, line

def cascade(col):
    speed = randrange(0, 4) + 1
    espeed = randrange(0, 4) + 1
    line = counter = ecounter = 0
    oldline = eline = -1
    erasing = False
    bright = "1"
    limit = lines - randrange(lines)
    while True:
        counter, line = update_line(speed , counter, line)
        if randrange(10 * speed) < 1:
            bright = "0"
        if line > 1 and line <= limit and oldline != line:
            print_at(choice(chars),col, line-1, green, bright)
        if line < limit:
            print_at(choice(chars),col, line, white, "1")
        if erasing:
            ecounter, eline = update_line(espeed, ecounter, eline)
            print_at(" ",col, eline, black)
        else:
            erasing = randrange(line + 1) > (lines / 2)
            eline = 0
        yield None
        oldline = line
        if eline >= limit:
            print_at(" ",col, line, black)
            break

def main():
    cascading = set()
    while True:
        added_new = True
        while add_new(cascading): pass
        stopped = iterate(cascading)
        sys.stdout.flush()
        cascading.difference_update(stopped)
        time.sleep(.06)

def add_new(cascading):
    if randrange(MAX_CASCADES) > len(cascading):
        col = randrange(cols)
        for i in xrange(randrange(1, 20)):
            cascading.add(cascade((col + i - 1) % cols))
        return True
    return False

def iterate(cascading):
    stopped = set()
    for c in cascading:
        try:
            c.next()
        except StopIteration:
            stopped.add(c)
    return stopped

def doit():
    try:
        init()
        main()
    except KeyboardInterrupt:
        pass
    finally:
        end()

if __name__=="__main__":
    doit()