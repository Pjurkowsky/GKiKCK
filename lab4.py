#!/usr/bin/env python3
from math import cos, sin, pi
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *


viewer = [30.0, 0.0, 0.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0

scale = 1.0

left_mouse_button_pressed = False
right_mouse_button_pressed = False
middle_mouse_button_pressed = False

W_keyboard_button_pressed = False
A_keyboard_button_pressed = False
S_keyboard_button_pressed = False
D_keyboard_button_pressed = False
R_keyboard_button_pressed = False


mouse_x_pos_old = 0
delta_x = 0

mouse_y_pos_old = 0
delta_y = 0

R = 30.0

xangle = 30.0
yangle = 0
zangle = 0


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def shutdown():
    pass


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


def draw_pyramid(size, pos):
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])

    glBegin(GL_TRIANGLES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0 * size + pos[0], 1.0 * size + pos[1], 0.0 * size + pos[2])
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(-1.0 * size + pos[0], -1.0 * size + pos[1], 1.0 * size + pos[2])
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(1.0 * size + pos[0], -1.0 * size + pos[1], 1.0 * size + pos[2])

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0 * size + pos[0], 1.0 * size + pos[1], 0.0 * size + pos[2])
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0 * size + pos[0], -1.0 * size + pos[1], 1.0 * size + pos[2])
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(1.0 * size + pos[0], -1.0 * size + pos[1], -1.0 * size + pos[2])

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0 * size + pos[0], 1.0 * size + pos[1], 0.0 * size + pos[2])
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0 * size + pos[0], -1.0 * size + pos[1], -1.0 * size + pos[2])
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0 * size + pos[0], -1.0 *
               size + pos[1], -1.0 * size + pos[2])

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0 * size + pos[0], 1.0 * size + pos[1], 0.0 * size + pos[2])
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(-1.0 * size + pos[0], -1.0 *
               size + pos[1], -1.0 * size + pos[2])
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(-1.0 * size + pos[0], -1.0 * size + pos[1], 1.0 * size + pos[2])

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-1.0 * size + pos[0], -1.0 * size + pos[1], 1.0 * size + pos[2])
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(1.0 * size + pos[0], -1.0 * size + pos[1], 1.0 * size + pos[2])
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(1.0 * size + pos[0], -1.0 * size + pos[1], -1.0 * size + pos[2])

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-1.0 * size + pos[0], -1.0 * size + pos[1], 1.0 * size + pos[2])
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(1.0 * size + pos[0], -1.0 * size + pos[1], -1.0 * size + pos[2])
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(-1.0 * size + pos[0], -1.0 *
               size + pos[1], -1.0 * size + pos[2])

    glEnd()
    glPopMatrix()


def sierpinski_triangle_3d(size, pos, current_iter, iter):
    if current_iter == iter:
        draw_pyramid(size, pos)
    else:
        sierpinski_triangle_3d(size / 2, pos, current_iter + 1, iter)
        sierpinski_triangle_3d(
            size / 2, [pos[0] + size / 2, pos[1], pos[2]], current_iter + 1, iter)
        sierpinski_triangle_3d(
            size / 2, [pos[0] + size / 4, pos[1] + size / 2, pos[2] + size / 4], current_iter + 1, iter)
        sierpinski_triangle_3d(
            size / 2, [pos[0] + size / 2, pos[1],  pos[2] + size / 2], current_iter + 1, iter)
        sierpinski_triangle_3d(
            size / 2, [pos[0], pos[1], pos[2] + size / 2], current_iter + 1, iter)


def render(time):
    global theta
    global phi
    global scale
    global R

    global xangle
    global yangle
    global zangle

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if R_keyboard_button_pressed:
        gluLookAt(viewer[0], viewer[1], viewer[2],
                  viewer[0] - xangle, viewer[1] + yangle, viewer[2] - zangle, 0.0, 1.0, 0.0)
    elif not middle_mouse_button_pressed:
        theta %= 360
        phi %= 360

        s = 1.0
        if phi > 90 and phi < 270:
            s = -1.0
        x_eye = R * cos(theta * pi / 180.0) * cos(phi * pi / 180.0)
        y_eye = R * sin(phi * pi / 180.0)
        z_eye = R * sin(theta * pi / 180.0) * cos(phi * pi / 180.0)
        gluLookAt(x_eye, y_eye, z_eye,
                  0.0, 0.0, 0.0, 0.0, s, 0.0)
    else:
        gluLookAt(viewer[0], viewer[1], viewer[2],
                  0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
        glScalef(scale, scale, scale)
        glRotatef(theta, 0.0, 1.0, 0.0)
        glRotatef(phi, 1.0, 0.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    if right_mouse_button_pressed:
        scale += delta_y * 0.01
        R += delta_y * 0.1

    if W_keyboard_button_pressed:
        viewer[0] -= xangle * 0.5
        viewer[2] -= zangle * 0.5
    if A_keyboard_button_pressed:
        viewer[0] -= zangle * 0.5
        viewer[2] += xangle * 0.5
    if S_keyboard_button_pressed:
        viewer[0] += xangle * 0.5
        viewer[2] += zangle * 0.5
    if D_keyboard_button_pressed:
        viewer[0] += zangle * 0.5
        viewer[2] -= xangle * 0.5

    axes()
    sierpinski_triangle_3d(5.0, [0.0, 0.0, 0.0], 0, 2)

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def keyboard_key_callback(window, key, scancode, action, mods):
    global viewer
    global W_keyboard_button_pressed
    global A_keyboard_button_pressed
    global S_keyboard_button_pressed
    global D_keyboard_button_pressed
    global R_keyboard_button_pressed

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if action == GLFW_PRESS or action == GLFW_REPEAT:
        if key == GLFW_KEY_W:
            W_keyboard_button_pressed = True
        if key == GLFW_KEY_S:
            S_keyboard_button_pressed = True
        if key == GLFW_KEY_A:
            A_keyboard_button_pressed = True
        if key == GLFW_KEY_D:
            D_keyboard_button_pressed = True
        if key == GLFW_KEY_R:
            R_keyboard_button_pressed = not R_keyboard_button_pressed
    else:
        W_keyboard_button_pressed = False
        A_keyboard_button_pressed = False
        S_keyboard_button_pressed = False
        D_keyboard_button_pressed = False


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x
    global mouse_x_pos_old

    global delta_y
    global mouse_y_pos_old

    global xangle
    global yangle
    global zangle

    if R_keyboard_button_pressed:
        x_pos = (x_pos - 200) * 0.01
        y_pos = (y_pos - 200) * 0.01
        if y_pos <= -10.0:
            y_pos = -10.0
        if y_pos >= 10.0:
            y_pos = 10.0

    xangle = sin(x_pos)
    yangle = -y_pos
    zangle = -cos(x_pos)

    if yangle * pi / 180.0 > 45 or yangle * pi / 180.0 < -45:
        yangle = 45.0

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed
    global right_mouse_button_pressed
    global middle_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = True
    else:
        left_mouse_button_pressed = False

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = True
    else:
        right_mouse_button_pressed = False

    if button == GLFW_MOUSE_BUTTON_MIDDLE and action == GLFW_PRESS:
        middle_mouse_button_pressed = not middle_mouse_button_pressed


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)
    glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)
    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
