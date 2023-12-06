#!/usr/bin/env python3
from math import cos, sin, pi
import sys

from glfw.GLFW import *

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

N = 20

viewer = [0.0, 0.0, 10.0]

theta = 0.0
phi = 0.0
pix2angle = 1.0

scale = 1.0

left_mouse_button_pressed = False
right_mouse_button_pressed = False
middle_mouse_button_pressed = False

R_keyboard_button_pressed = False

mouse_x_pos_old = 0
delta_x = 0

mouse_y_pos_old = 0
delta_y = 0

R = 10.0

xangle = 0.0
yangle = 0.0
zangle = 0.0

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

i = 0
elapsedTime = 0.0


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


def x_u(u, v):
    return (
        -450 * u**4 + 900 * u**3 - 810 * u**2 + 360 * u - 45
    ) * cos(pi * v)


def x_v(u, v):
    return pi * (
        90 * u**5 - 225 * u**4 + 270 * u**3 - 180 * u**2 + 45 * u
    ) * sin(pi * v)


def y_u(u, v):
    return 640 * u**3 - 960 * u**2 + 320 * u


def y_v(u, v):
    return 0


def z_u(u, v):
    return (
        -450 * u**4 + 900 * u**3 - 810 * u**2 + 360 * u - 45
    ) * sin(pi * v)


def z_v(u, v):
    return -pi * (
        90 * u**5 - 225 * u**4 + 270 * u**3 - 180 * u**2 + 45 * u
    ) * cos(pi * v)


def normalize_vector(vector):
    length = np.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
    return np.array([vector[0] / length, vector[1] / length, vector[2] / length])


def egg_points(u, v):
    tab = np.zeros((N, N, 3))
    for i in range(N):
        for j in range(N):
            tab[i][j][0] = x(u[i], v[j])
            tab[i][j][1] = y(u[i], v[j])
            tab[i][j][2] = z(u[i], v[j])
    return tab


def create_normalized_vectors(u, v):
    vectors = np.zeros((N, N, 3))

    for i in range(N):
        for j in range(N):
            vectors[i][j][0] = y_u(u[i], v[j]) * z_v(u[i], v[j]) - \
                z_u(u[i], v[j]) * y_v(u[i], v[j])
            vectors[i][j][1] = z_u(u[i], v[j]) * x_v(u[i], v[j]) - \
                x_u(u[i], v[j]) * z_v(u[i], v[j])
            vectors[i][j][2] = x_u(u[i], v[j]) * y_v(u[i], v[j]) - \
                y_u(u[i], v[j]) * x_v(u[i], v[j])

            vectors[i][j] = normalize_vector(vectors[i][j])

            if i >= N / 2:
                vectors[i][j] = -1 * vectors[i][j]

    vectors[0] = np.array([0, -1, 0])
    vectors[N - 1] = np.array([0, 1, 0])

    return vectors


def egg_triangles():
    glBegin(GL_TRIANGLES)

    u = np.linspace(0, 1, N)
    v = np.linspace(0, 1, N)

    tab = egg_points(u, v)

    normalized_vectors = create_normalized_vectors(u, v)

    for i in range(N - 1):
        for j in range(N - 1):
            glNormal3fv(normalized_vectors[i][j])
            glVertex3fv(tab[i][j])

            glNormal3fv(normalized_vectors[i + 1][j])
            glVertex3fv(tab[i + 1][j])

            glNormal3fv(normalized_vectors[i][j + 1])
            glVertex3fv(tab[i][j + 1])

            glNormal3fv(normalized_vectors[i + 1][j])
            glVertex3fv(tab[i + 1][j])

            glNormal3fv(normalized_vectors[i + 1][j + 1])
            glVertex3fv(tab[i + 1][j + 1])

            glNormal3fv(normalized_vectors[i][j + 1])
            glVertex3fv(tab[i][j + 1])
    glEnd()


def draw_lines():
    glBegin(GL_LINES)

    u = np.linspace(0, 1, N)
    v = np.linspace(0, 1, N)

    tab = egg_points(u, v)

    normalized_vectors = create_normalized_vectors(u, v)

    for i in range(N):
        for j in range(N):
            glVertex3fv(tab[i][j])
            glVertex3fv(normalized_vectors[i][j] + tab[i][j])
    glEnd()


def render(window, time):
    global theta
    global phi
    global scale
    global R

    global xangle
    global yangle
    global zangle

    global i
    global elapsedTime

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if R_keyboard_button_pressed:
        gluLookAt(viewer[0], viewer[1], viewer[2],
                  viewer[0] - xangle, viewer[1] + yangle, viewer[2] - zangle, 0.0, 1.0, 0.0)
    else:
        gluLookAt(viewer[0], viewer[1], viewer[2],
                  0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

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

    if glfwGetKey(window, GLFW_KEY_T) and time - elapsedTime > 0.5:
        elapsedTime = time
        i += 1
        i %= 16
        print("i: ", i)
    if glfwGetKey(window, GLFW_KEY_F) and time - elapsedTime > 0.2:
        elapsedTime = time
        if i < 4:
            light_ambient[i] += 0.1
            if light_ambient[i] >= 0.99:
                light_ambient[i] = 1.0
            glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
            print("light_ambient: ", light_ambient)

        elif i < 8:
            light_diffuse[i - 4] += 0.1
            if light_diffuse[i - 4] >= 0.99:
                light_diffuse[i - 4] = 1.0
            glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
            print("light_diffuse: ", light_diffuse)

        elif i < 12:
            light_specular[i - 8] += 0.1
            if light_specular[i - 8] >= 0.99:
                light_specular[i - 8] = 1.0
            glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
            print("light_specular: ", light_specular)

        else:
            light_position[i - 12] += 0.1
            glLightfv(GL_LIGHT0, GL_POSITION, light_position)
            print("light_position: ", light_position)

    if glfwGetKey(window, GLFW_KEY_G) and time - elapsedTime > 0.2:
        elapsedTime = time
        if i < 4:
            light_ambient[i] -= 0.1
            if light_ambient[i] < 0.1:
                light_ambient[i] = 0.0
            glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
            print("light_ambient: ", light_ambient)

        elif i < 8:
            light_diffuse[i - 4] -= 0.1
            if light_diffuse[i - 4] < 0.1:
                light_diffuse[i - 4] = 0.0
            glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
            print("light_diffuse: ", light_diffuse)

        elif i < 12:
            light_specular[i - 8] -= 0.1
            if light_specular[i - 8] < 0.1:
                light_specular[i - 8] = 0.0
            glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
            print("light_specular: ", light_specular)

        else:
            light_position[i - 12] -= 0.1
            if light_position[i - 12] < 0.1:
                light_position[i - 12] = 0.0
            glLightfv(GL_LIGHT0, GL_POSITION, light_position)
            print("light_position: ", light_position)

    axes()
    light_source(theta, phi)
    egg_triangles()
    if middle_mouse_button_pressed:
        draw_lines()
    glFlush()


def light_source(theta, phi):
    theta %= 360
    phi %= 360

    x_eye = R * cos(theta * pi / 180.0) * cos(phi * pi / 180.0)
    y_eye = R * sin(phi * pi / 180.0)
    z_eye = R * sin(theta * pi / 180.0) * cos(phi * pi / 180.0)

    light_position = [x_eye, y_eye, z_eye, 1.0]

    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glTranslatef(light_position[0], light_position[1], light_position[2])
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    glTranslatef(-light_position[0], -light_position[1], -light_position[2])


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

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    if key == GLFW_KEY_R and action == GLFW_PRESS:
        R_keyboard_button_pressed = not R_keyboard_button_pressed


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
        render(window, glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
