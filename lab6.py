#!/usr/bin/env python3
from math import cos, sin, pi
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image
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

X_keyboard_button_pressed = False

mouse_x_pos_old = 0
delta_x = 0

mouse_y_pos_old = 0
delta_y = 0

N = 20

R = 30.0

xangle = 30.0
yangle = 0
zangle = 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

image = Image.open("tekstura.tga")
image2 = Image.open("tekstura2.tga")

txt = np.zeros((N, N, 2))
for u in range(N):
    for v in range(N):
        txt[u, v] = [v/N, u/(N/2)]


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)
    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_TEXTURE_2D)
    glEnable(GL_CULL_FACE)
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, image.size[0], image.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1)
    )


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


def x(u, v):
    return (
        -90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u
    ) * cos(pi * v)


def y(u, v):
    return 160 * u**4 - 320 * u**3 + 160 * u**2 - 5


def z(u, v):
    return (
        -90 * u**5 + 225 * u**4 - 270 * u**3 + 180 * u**2 - 45 * u
    ) * sin(pi * v)


def egg_points(u, v):
    tab = np.zeros((N, N, 3))
    for i in range(N):
        for j in range(N):
            tab[i][j][0] = x(u[i], v[j])
            tab[i][j][1] = y(u[i], v[j])
            tab[i][j][2] = z(u[i], v[j])
    return tab


def egg_triangle_strip():
    glBegin(GL_TRIANGLE_STRIP)

    u = np.linspace(0, 1, N)
    v = np.linspace(0, 1, N)

    tab = egg_points(u, v)

    for i in range(N - 1):
        for j in range(N - 1):
            glTexCoord2fv(txt[i][j + 1])
            glVertex3fv(tab[i][j + 1])

            glTexCoord2fv(txt[i + 1][j + 1])
            glVertex3fv(tab[i + 1][j + 1])

            glTexCoord2fv(txt[i + 1][j])
            glVertex3fv(tab[i + 1][j])

            glTexCoord2fv(txt[i][j])
            glVertex3fv(tab[i][j])

            glTexCoord2fv(txt[i][j + 1])
            glVertex3fv(tab[i][j + 1])

            glTexCoord2fv(txt[i + 1][j])
            glVertex3fv(tab[i + 1][j])

    glEnd()


def rectangle():
    glBegin(GL_TRIANGLES)

    glTexCoord2f(0.0, 0.0)
    glVertex3f(-5.0, -5.0, 0.0)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(5.0, -5.0, 0.0)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(-5.0, 5.0, 0.0)

    glTexCoord2f(1.0, 0.0)
    glVertex3f(5.0, -5.0, 0.0)

    glTexCoord2f(1.0, 1.0)
    glVertex3f(5.0, 5.0, 0.0)

    glTexCoord2f(0.0, 1.0)
    glVertex3f(-5.0, 5.0, 0.0)

    glEnd()


def draw_pyramid(size, pos):
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])

    glBegin(GL_TRIANGLES)

    if not X_keyboard_button_pressed:
        glTexCoord2f(0.25, 0.5)
        glVertex3f(0.0 * size + pos[0], 1.0 *
                   size + pos[1], 0.0 * size + pos[2])
        glTexCoord2f(0, 1)
        glVertex3f(-1.0 * size + pos[0], -1.0 *
                   size + pos[1], 1.0 * size + pos[2])
        glTexCoord2f(0.0, 0.0)
        glVertex3f(1.0 * size + pos[0], -1.0 *
                   size + pos[1], 1.0 * size + pos[2])

    glTexCoord2f(0.25, 0.5)
    glVertex3f(0.0 * size + pos[0], 1.0 * size + pos[1], 0.0 * size + pos[2])
    glTexCoord2f(0.0, 0.0)
    glVertex3f(1.0 * size + pos[0], -1.0 * size + pos[1], 1.0 * size + pos[2])
    glTexCoord2f(1, 0.0)
    glVertex3f(1.0 * size + pos[0], -1.0 * size + pos[1], -1.0 * size + pos[2])

    glTexCoord2f(0.25, 0.5)
    glVertex3f(0.0 * size + pos[0], 1.0 * size + pos[1], 0.0 * size + pos[2])
    glTexCoord2f(1, 0.0)
    glVertex3f(1.0 * size + pos[0], -1.0 * size + pos[1], -1.0 * size + pos[2])
    glTexCoord2f(1, 1)
    glVertex3f(-1.0 * size + pos[0], -1.0 *
               size + pos[1], -1.0 * size + pos[2])

    glTexCoord2f(0.25, 0.5)
    glVertex3f(0.0 * size + pos[0], 1.0 * size + pos[1], 0.0 * size + pos[2])
    glTexCoord2f(1, 1)
    glVertex3f(-1.0 * size + pos[0], -1.0 *
               size + pos[1], -1.0 * size + pos[2])
    glTexCoord2f(0, 1)
    glVertex3f(-1.0 * size + pos[0], -1.0 * size + pos[1], 1.0 * size + pos[2])

    # texture rectangle

    glTexCoord2f(0.0, 1.0)
    glVertex3f(1.0 * size + pos[0], -1.0 * size + pos[1], 1.0 * size + pos[2])
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0 * size + pos[0], -1.0 * size + pos[1], 1.0 * size + pos[2])
    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0 * size + pos[0], -1.0 * size + pos[1], -1.0 * size + pos[2])

    glTexCoord2f(1.0, 1.0)
    glVertex3f(1.0 * size + pos[0], -1.0 * size + pos[1], -1.0 * size + pos[2])
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-1.0 * size + pos[0], -1.0 * size + pos[1], 1.0 * size + pos[2])
    glTexCoord2f(1.0, 0.0)
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


def render(window, time):
    global theta
    global phi
    global scale
    global R

    global xangle
    global yangle
    global zangle

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

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

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    if right_mouse_button_pressed:
        scale += delta_y * 0.01
        R += delta_y * 0.1

    if glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS:
        viewer[0] -= xangle * 0.5
        viewer[2] -= zangle * 0.5
    if glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS:
        viewer[0] -= zangle * 0.5
        viewer[2] += xangle * 0.5
    if glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS:
        viewer[0] += xangle * 0.5
        viewer[2] += zangle * 0.5
    if glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS:
        viewer[0] += zangle * 0.5
        viewer[2] -= xangle * 0.5

    # sierpinski_triangle_3d(5.0, [0.0, 0.0, 0.0], 0, 0)
    egg_triangle_strip()
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
    global R_keyboard_button_pressed
    global X_keyboard_button_pressed

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_R and action == GLFW_PRESS:
        R_keyboard_button_pressed = not R_keyboard_button_pressed

    if key == GLFW_KEY_X and action == GLFW_PRESS:
        X_keyboard_button_pressed = not X_keyboard_button_pressed


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
    global image
    global image2

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

    if middle_mouse_button_pressed:
        glTexImage2D(
            GL_TEXTURE_2D, 0, 3, image2.size[0], image2.size[1], 0,
            GL_RGB, GL_UNSIGNED_BYTE, image2.tobytes("raw", "RGB", 0, -1)
        )
    else:
        glTexImage2D(
            GL_TEXTURE_2D, 0, 3, image.size[0], image.size[1], 0,
            GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1)
        )


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
        render(window, glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
