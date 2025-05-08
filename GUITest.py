import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import radians, cos, sin
# ===== DH Matrix =====
def dh_matrix(theta, d, a, alpha):
    theta = radians(theta)
    alpha = radians(alpha)
    return np.array([
        [cos(theta), -sin(theta)*cos(alpha),  sin(theta)*sin(alpha), a*cos(theta)],
        [sin(theta),  cos(theta)*cos(alpha), -cos(theta)*sin(alpha), a*sin(theta)],
        [0,           sin(alpha),             cos(alpha),            d],
        [0,           0,                      0,                     1]
    ])
# ===== Draw Robot Arm =====
def draw_robot(joint_angles):
    dh_params = [
        [joint_angles[0], 0, 0, 90],
        [joint_angles[1], 0, 5, 0],
        [joint_angles[2], 0, 4, 0],
        [joint_angles[3], 0, 3, 90],
        [joint_angles[4], 0, 2, 0],
    ]
    T = np.eye(4)
    positions = [T[:3, 3]]
    for param in dh_params:
        T_next = dh_matrix(*param)
        T = T @ T_next
        positions.append(T[:3, 3])
    xs, ys, zs = zip(*positions)

    ax.clear()
    ax.plot(xs, ys, zs, '-o', linewidth=3, markersize=8, color='blue')
    ax.set_xlim([-15, 15])
    ax.set_ylim([-15, 15])
    ax.set_zlim([0, 15])
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("Control Robot Arm ")
    canvas.draw()

# ===== Slider Callback =====
def update_robot(*args):
    angles = [var.get() for var in sliders_vars]
    draw_robot(angles)

# ===== GUI Setup =====
root = tk.Tk()
root.title("Robotic Arm Control")

# Create matplotlib figure
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection='3d')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=1, rowspan=6)

# Create sliders
sliders_vars = []
for i in range(5):
    var = tk.DoubleVar()
    slider = ttk.Scale(root, from_=-180, to=180, orient='horizontal', variable=var, command=update_robot)
    slider.grid(row=i, column=0, padx=10, pady=10)
    sliders_vars.append(var)

# Initialize
draw_robot([0, 0, 0, 0, 0])
root.mainloop()
