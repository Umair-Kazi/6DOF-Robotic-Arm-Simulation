import pygame
from pygame.locals import *
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *

from ForwardKinematics import ForwardKinematics2D
from ForwardKinematics import ForwardKinematics3D

from InverseKinematics import NumericalInverseKinematics

def DrawAxes():
    glBegin(GL_LINES)

    glColor3f(1,0,0)
    glVertex3f(-30,0,0)
    glVertex3f(30,0,0)

    glColor3f(0,1,0)
    glVertex3f(0,-30,0)
    glVertex3f(0,30,0)

    glColor3f(0,0,1)
    glVertex3f(0,0,-30)
    glVertex3f(0,0,30)

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

def DrawText(display, text, y_offset=30):
    font = pygame.font.SysFont("monospace", 20)
    surface = font.render(text, True, (255, 255, 255))
    text_data = pygame.image.tostring(surface, "RGBA", True)
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glWindowPos2d(10, display[1] - y_offset)
    glDrawPixels(surface.get_width(), surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)
    glDisable(GL_BLEND)

# angles = [20, 40, -45, 50, 50, 30]
# lengths = [1, 1, 2, 1, 1, 1]

angles = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ]
lengths = [3.625, 4.25, 5.875, 3.0, 4.375]
joint_limits = [
    (-90, 90),
    (-90, 90),
    (-90, 90),
    (-90, 90),
    (-90, 90)
]
joint_axes = [1, 0, 0, 0, 1] # +1 last servo not included, manipulates claw open/close position
claw_angle = 70

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    gluPerspective(45, (display[0]/display[1]), 0.1, 200.0)
    glTranslatef(0.0, 0.0, -75)
    glRotatef(30,1,0,0)
    glRotatef(45,0,1,0)

    mouse_held = False
    selected_joint = 0
    kinematics_type = 0

    total_length = sum(lengths)
    target = np.array([0.0, total_length, 0.0])

    # TODO: implement real-time control with keyboard, then XBOX controller
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_held = True
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_held = False
            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_5:
                    selected_joint = event.key - pygame.K_1
                if event.key == pygame.K_f:
                    kinematics_type = 0
                if event.key == pygame.K_i:
                    kinematics_type = 1

        if kinematics_type == 0: # FORWARD KINEMATICS
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                if (angles[selected_joint][joint_axes[selected_joint]] < 90):
                        angles[selected_joint][joint_axes[selected_joint]] += 5
                        pygame.time.wait(10)
            if keys[pygame.K_LEFT]:
                if (angles[selected_joint][joint_axes[selected_joint]] > -90):
                        angles[selected_joint][joint_axes[selected_joint]] -= 5
                        pygame.time.wait(10)
        elif kinematics_type == 1: # INVERSE KINEMATICS
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                target[0] += 0.1
            if keys[pygame.K_LEFT]:
                target[0] -= 0.1
            if keys[pygame.K_UP]:
                target[1] += 0.1
            if keys[pygame.K_DOWN]:
                target[1] -= 0.1
            if keys[pygame.K_a]:
                target[2] += 0.1
            if keys[pygame.K_d]:
                target[2] -= 0.1

        base_height = lengths[0]
        max_reach = sum(lengths[1:]) * 0.95

        target[1] = max(0, target[1])

        offset = target - np.array([0, base_height, 0])
        dist = np.linalg.norm(offset)
        if dist > max_reach:
            target = np.array([0, base_height, 0]) + (offset / dist) * max_reach

        if mouse_held:
            dx, dy = pygame.mouse.get_rel()
            glRotatef(dy, 1, 0, 0)
            glRotatef(dx, 0, 1, 0)
        else :
            pygame.mouse.get_rel()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        DrawAxes()
        # DrawJoints()
        # x_pos, y_pos = ForwardKinematics2D(angles, lengths)
        # joints = [(0, 0)] + list(zip(x_pos, y_pos))
        # DrawJoints2D(joints)

        if kinematics_type == 0:
            DrawText(display, "Mode: Forward Kinematics [F/I to switch]")
            positions = ForwardKinematics3D(angles, lengths)
        elif kinematics_type == 1:
            DrawText(display, "Mode: Inverse Kinematics [F/I to switch]")
            DrawText(display, f"Target: ({target[0]:.2f}, {target[1]:.2f}, {target[2]:.2f})", y_offset=55)
            solved_angles = NumericalInverseKinematics(target, angles, lengths, joint_axes)
            positions  = ForwardKinematics3D(solved_angles, lengths)

        joints = [(0, 0, 0)] + list(positions)
        DrawJoints(joints)

        pygame.display.flip()
        pygame.time.wait(10)

main()