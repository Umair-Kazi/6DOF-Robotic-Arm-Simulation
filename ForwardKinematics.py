import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *

def ForwardKinematics2D(angles, lengths):
    world_angle = 0

    x_pos = []
    y_pos = []

    for i in range(len(angles)):
        angle = angles[i]
        world_angle += angle
        
        rad_angle = np.radians(world_angle)

        if i == 0:
            x = lengths[i] * np.cos(rad_angle)
            y = lengths[i] * np.sin(rad_angle)
        else:
            x = x_pos[i-1] + lengths[i] * np.cos(rad_angle)
            y = y_pos[i-1] + lengths[i] * np.sin(rad_angle)
        
        x_pos.append(x)
        y_pos.append(y)

    return x_pos, y_pos

# angles = [20, 40, -45, -10, 5, 5]
# lengths = [1, 1, 2, 1, 1, 1]
# 
# x_pos, y_pos = ForwardKinematics2D(angles, lengths)
# for i in range(len(x_pos)):
#     print(f"Joint {i+1}: ({x_pos[i]:.3f}, {y_pos[i]:.3f})")

def rotation_matrix_X(angle):
    radians = np.radians(angle)

    R = np.array([
        [1, 0,                  0               ],
        [0, np.cos(radians),    -np.sin(radians)],
        [0, np.sin(radians),    np.cos(radians) ],

    ])

    return R

def rotation_matrix_Y(angle):
    radians = np.radians(angle)

    R = np.array([
        [np.cos(radians),   0,  -np.sin(radians)],
        [0,                 1,  0               ],
        [np.sin(radians),   0,  np.cos(radians) ]
    ])

    return R

def rotation_matrix_Z(angle):
    radians = np.radians(angle)

    R = np.array([
        [np.cos(radians),   -np.sin(radians),   0],
        [np.sin(radians),   np.cos(radians),    0],
        [0,                 0,                  1]
    ])

    return R

# angles = [
#         (0, 0, 45),
#         (0, 30, 0),
#         (0, 0, -45),
#         (90, 0, 0),
#         (30, 0, 0),
#         (0, -45, 0)
#     ]
# lengths = [1, 1, 2, 1, 1, 1]

def ForwardKinematics3D(angles, lengths):
    world_rotation = np.eye(3)

    positions = []

    for i in range(len(angles)):
        rx = angles[i][0]
        ry = angles[i][1]
        rz = angles[i][2]

        R_joint = rotation_matrix_X(rx) @ rotation_matrix_Y(ry) @ rotation_matrix_Z(rz)
        world_rotation = world_rotation @ R_joint
        direction = world_rotation @ np.array([0, 1, 0])

        if i == 0:
            pos = lengths[i] * direction
        else:
            pos = positions[i - 1] + lengths[i] * direction
        
        positions.append(pos)

    return positions

# test = ForwardKinematics3D(angles, lengths)
# for i in range(len(test)):
#     print(f"Joint {i+1}: {test[i]}")