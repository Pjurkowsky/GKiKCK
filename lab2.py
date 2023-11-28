#!/usr/bin/env python3
from math import pi, sin
import sys
import random
from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


red = random.random()
green = random.random()
blue = random.random()


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.5, 0.5, 0.5, 1.0)


def shutdown():
    pass


def draw_rectangle(x, y, a, b, d=0, color=(0.0, 0.0, 0.0)):
    glColor3fv(color)

    glBegin(GL_TRIANGLES)
    glVertex2f(x, y + d)

    glVertex2f(x + d, y + b)

    glVertex2f(x + a, y + d)
    glEnd()

    glBegin(GL_TRIANGLES)
    glVertex2f(x + a, y + b)

    glVertex2f(x, y + b + d)

    glVertex2f(x + d + a, y)
    glEnd()


def draw_carpet(x, y, size, current_iter, iter, d=0):
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                continue

            step = 3 ** (iter - current_iter)
            n_x = x + i * step
            n_y = y + j * step

            if current_iter == iter:
                draw_rectangle(n_x * size / 3, n_y * size / 3, size / 3, size / 3, d)
            else:
                draw_carpet(n_x, n_y, size / 3, current_iter + 1, iter, d)


def draw_triangle_1():
    glBegin(GL_TRIANGLES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(25.0, 75.0)


    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(50.0, 25.0)
    
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(75.0, 75.0)
    glEnd()


def draw_triangle(x, y, l, color=(0.0, 0.0, 0.0)):
    glColor3fv(color)

    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)

    glVertex2f(x - l, y)

    glVertex2f(x - l / 2, y - sin(pi / 3) * l)
    glEnd()


def draw_sierp_trianagle(x, y, l, curr_iter, iter, color=(0.0, 0.0, 0.0)):
    if curr_iter == iter:
        draw_triangle(x, y, l, color)
    else:
        draw_sierp_trianagle(x, y, l / 2, curr_iter + 1, iter, color)
        draw_sierp_trianagle(x - l / 2, y, l / 2, curr_iter + 1, iter,color)
        draw_sierp_trianagle(
            x - l / 4, y - sin(pi / 3) * l / 2, l / 2, curr_iter + 1, iter , color
        )


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    #3.0
    #draw_triangle_1()   

    #3.5
    #draw_rectangle(25, 25, 50, 50, 0, (red, green, blue))

    #4.0
    #draw_rectangle(25, 25, 50, 50, 5, (red, green, blue))

    #4.5
    #draw_carpet(0, 0, 100, 1, 6, 1)
    
    #5.0
    draw_sierp_trianagle(100, 100, 100, 1, 5, (red, green, blue))

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1

    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 400 - height, width, height)

    glLoadIdentity()

    if width <= height:
        glOrtho(0, 100.0, 100.0 / aspect_ratio, 0, 1.0, -1.0) 
    else:
        glOrtho(0, 100.0 * aspect_ratio, 100.0, 0, 1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == "__main__":
    main()
