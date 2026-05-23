import numpy as np
from ForwardKinematics import ForwardKinematics3D
import copy

def compute_jacobian(angles, lengths, joint_axes):
    jacobian = []
    degree_perturbation = 0.001
    current_end = ForwardKinematics3D(angles, lengths)[-1]

    for i in range(len(angles)):
        nudged_angles = copy.deepcopy(angles)
        nudged_angles[i][joint_axes[i]] += degree_perturbation

        nudged_end = ForwardKinematics3D(nudged_angles, lengths)[-1]
        column_i = (nudged_end - current_end) / degree_perturbation

        jacobian.append(column_i)

    return np.array(jacobian).T

def NumericalInverseKinematics(target, angles, lengths, joint_axes, iterations=100, tolerance=0.01):
    for i in range(iterations):
        current_end_effector_pos = ForwardKinematics3D(angles, lengths)[-1]
        error = target - current_end_effector_pos
        if np.linalg.norm(error) <= tolerance: break

        J = compute_jacobian(angles, lengths, joint_axes)
        pseudoinverse_jacobian = np.linalg.pinv(J)

        delta_angles = pseudoinverse_jacobian @ error
        for j in range(len(angles)):
            angles[j][joint_axes[j]] += delta_angles[j]

    return angles

# angles = [
#     [0, 0, 0],
#     [0, 0, 0],
#     [0, 0, 0],
#     [0, 0, 0],
#     [0, 0, 0],
#     [0, 0, 0]
# ]
# lengths = [1, 1, 2, 1, 1, 1]
# joint_axes = [1, 0, 0, 0, 1, 2]
# target = np.array([2.0, 5.0, 1.0])

# solved_angles = numerical_IK(target, angles, lengths, joint_axes)

# from ForwardKinematics import ForwardKinematics3D
# final_pos = ForwardKinematics3D(solved_angles, lengths)[-1]
# print(f"Target:   {target}")
# print(f"Achieved: {final_pos}")
# print(f"Error:    {np.linalg.norm(target - final_pos):.4f}")