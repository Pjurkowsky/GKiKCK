#!/usr/bin/env python3
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *

import numpy as np
import math
import random

N = 20
rgb_values = np.random.rand(N, N, 3)


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


def x(u, v):
    return (
        -90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u
    ) * math.cos(math.pi * v)


def y(u, v):
    return 160 * u**4 - 320 * u**3 + 160 * u**2 - 5


def z(u, v):
    return (
        -90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u
    ) * math.sin(math.pi * v)


def spin(angle):
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


# 3.0
def egg_points():
    glBegin(GL_POINTS)
    tab = np.zeros((N, N, 3))

    u = np.linspace(0, 1, N)
    v = np.linspace(0, 1, N)

    for i in range(N):
        for j in range(N):
            tab[i][j][0] = x(u[i], v[j])
            tab[i][j][1] = y(u[i], v[j])
            tab[i][j][2] = z(u[i], v[j])

    glColor3f(1.0, 0.0, 0.0)
    for i in range(N - 1):
        for j in range(N - 1):
            glVertex3fv(tab[i][j])

    glEnd()


# 3.5
def egg_lines():
    glBegin(GL_LINES)
    tab = np.zeros((N, N, 3))

    u = np.linspace(0, 1, N)
    v = np.linspace(0, 1, N)

    for i in range(N):
        for j in range(N):
            tab[i][j][0] = x(u[i], v[j])
            tab[i][j][1] = y(u[i], v[j])
            tab[i][j][2] = z(u[i], v[j])

    glColor3f(1.0, 0.0, 0.0)
    for i in range(N - 1):
        for j in range(N - 1):
            glVertex3fv(tab[i][j])
            glVertex3fv(tab[i + 1][j])

            glVertex3fv(tab[i][j])
            glVertex3fv(tab[i][j + 1])

    glEnd()


# 4.0
def egg_triangles():
    glBegin(GL_TRIANGLES)
    tab = np.zeros((N, N, 3))

    u = np.linspace(0, 1, N)
    v = np.linspace(0, 1, N)

    for i in range(N):
        for j in range(N):
            tab[i][j][0] = x(u[i], v[j])
            tab[i][j][1] = y(u[i], v[j])
            tab[i][j][2] = z(u[i], v[j])

    for i in range(N - 1):
        for j in range(N - 1):
            glColor3fv(rgb_values[i][j])
            glVertex3fv(tab[i][j])

            glColor3fv(rgb_values[i + 1][j])
            glVertex3fv(tab[i + 1][j])

            glColor3fv(rgb_values[i][j + 1])
            glVertex3fv(tab[i][j + 1])

            glColor3fv(rgb_values[i + 1][j])
            glVertex3fv(tab[i + 1][j])

            glColor3fv(rgb_values[i + 1][j + 1])
            glVertex3fv(tab[i + 1][j + 1])

            glColor3fv(rgb_values[i][j + 1])
            glVertex3fv(tab[i][j + 1])
    glEnd()


# 4.5
def egg_triangle_strip():
    glBegin(GL_TRIANGLE_STRIP)
    tab = np.zeros((N, N, 3))

    u = np.linspace(0, 1, N)
    v = np.linspace(0, 1, N)

    for i in range(N):
        for j in range(N):
            tab[i][j][0] = x(u[i], v[j])
            tab[i][j][1] = y(u[i], v[j])
            tab[i][j][2] = z(u[i], v[j])

    for i in range(N - 1):
        for j in range(N - 1):
            glColor3fv(rgb_values[i][j])
            glVertex3fv(tab[i][j])

            glColor3fv(rgb_values[i + 1][j])
            glVertex3fv(tab[i + 1][j])

            glVertex3fv(tab[i][j + 1])

            glVertex3fv(tab[i + 1][j])

    glEnd()


def sierpinski_triangle_3d():
    glBegin(GL_TRIANGLES)
    glVertex3f(0.0, 0.0, 0.0)

    glVertex3f(1.0, 0.0, 0.0)

    glVertex3f(0.0, 1.0, 0.0)

    glEnd()


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    # spin(time * 180 / 3.1415)
    axes()

    sierpinski_triangle_3d()

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-7.5, 7.5, -7.5 / aspect_ratio, 7.5 / aspect_ratio, 7.5, -7.5)
    else:
        glOrtho(-7.5 * aspect_ratio, 7.5 * aspect_ratio, -7.5, 7.5, 7.5, -7.5)

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
