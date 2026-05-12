import numpy
from OpenGL.GL import *
from OpenGL.GLU import *

def ForwardKinematics2D(angles, lengths):
    world_angle = 0

    x_pos = []
    y_pos = []

    for i in range(len(angles)):
        angle = angles[i]
        world_angle += angle
        
        rad_angle = numpy.radians(world_angle)

        if i == 0:
            x = lengths[i] * numpy.cos(rad_angle)
            y = lengths[i] * numpy.sin(rad_angle)
        else:
            x = x_pos[i-1] + lengths[i] * numpy.cos(rad_angle)
            y = y_pos[i-1] + lengths[i] * numpy.sin(rad_angle)
        
        x_pos.append(x)
        y_pos.append(y)

    return x_pos, y_pos

# angles = [20, 40, -45, -10, 5, 5]
# lengths = [1, 1, 2, 1, 1, 1]
# 
# x_pos, y_pos = ForwardKinematics2D(angles, lengths)
# for i in range(len(x_pos)):
#     print(f"Joint {i+1}: ({x_pos[i]:.3f}, {y_pos[i]:.3f})")