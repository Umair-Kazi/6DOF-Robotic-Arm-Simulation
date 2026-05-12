import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from ForwardKinematics import ForwardKinematics2D

def DrawAxes():
    glBegin(GL_LINES)

    glColor3f(1,0,0)
    glVertex3f(-10,0,0)
    glVertex3f(10,0,0)

    glColor3f(0,1,0)
    glVertex3f(0,-10,0)
    glVertex3f(0,10,0)

    glColor3f(0,0,1)
    glVertex3f(0,0,-10)
    glVertex3f(0,0,10)

    glEnd()

# joints = [
#     (0,0,0),
#     (0,1,0),
#     (0,2,0),
#     (0,3,0),
#     (0,4,0),
#     (0,5,0),
#     (0,6,0)
# ]

def DrawJoints(joints):
    glPointSize(8)

    glBegin(GL_LINES)
    glColor3f(1,1,1)
    for i in range(len(joints) - 1):
        glVertex3f(*joints[i])
        glVertex3f(*joints[i+1])
    glEnd()

    glBegin(GL_POINTS)
    for i in range(len(joints)):
        glVertex3f(*joints[i])
    glEnd()

def DrawJoints2D(joints):
    glPointSize(8)

    glBegin(GL_LINES)
    glColor3f(1,1,1)
    for i in range(len(joints) - 1):
        glVertex2f(*joints[i])
        glVertex2f(*joints[i+1])
    glEnd()

    glBegin(GL_POINTS)
    for i in range(len(joints)):
        glVertex2f(*joints[i])
    glEnd()

angles = [20, 40, -45, 50, 50, 30]
lengths = [1, 1, 2, 1, 1, 1]

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -20)
    glRotatef(30,1,0,0)
    glRotatef(45,0,1,0)

    mouse_held = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_held = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False

        if mouse_held:
            dx, dy = pygame.mouse.get_rel()
            glRotatef(dy, 1, 0, 0)
            glRotatef(dx, 0, 1, 0)
        else :
            pygame.mouse.get_rel()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        DrawAxes()
        # DrawJoints()
        x_pos, y_pos = ForwardKinematics2D(angles, lengths)
        joints = [(0, 0)] + list(zip(x_pos, y_pos))
        DrawJoints2D(joints)
        pygame.display.flip()
        pygame.time.wait(10)

main()