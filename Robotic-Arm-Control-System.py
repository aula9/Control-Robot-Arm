"""
Robotic Arm Control System - Working Version
-------------------------------------------
This version has been tested and verified to work properly.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from math import radians, cos, sin
import logging
from datetime import datetime

# ===== Initial Setup =====
logging.basicConfig(filename='robot_arm.log', level=logging.INFO)

# ===== DH Matrix Computation =====
def dh_matrix(theta, d, a, alpha):
    theta = radians(theta)
    alpha = radians(alpha)
    return np.array([
        [cos(theta), -sin(theta)*cos(alpha), sin(theta)*sin(alpha), a*cos(theta)],
        [sin(theta), cos(theta)*cos(alpha), -cos(theta)*sin(alpha), a*sin(theta)],
        [0, sin(alpha), cos(alpha), d],
        [0, 0, 0, 1]
    ])

# ===== Robot Arm Visualization =====
def draw_robot(joint_angles):
    try:
        # DH parameters for a 5-joint arm
        dh_params = [
            [joint_angles[0], 0, 0, 90],
            [joint_angles[1], 0, 5, 0],
            [joint_angles[2], 0, 4, 0],
            [joint_angles[3], 0, 3, 90],
            [joint_angles[4], 0, 2, 0],
        ]
        
        # Compute positions
        T = np.eye(4)
        positions = [T[:3, 3]]
        for param in dh_params:
            T = T @ dh_matrix(*param)
            positions.append(T[:3, 3])
        
        # Extract coordinates
        xs, ys, zs = zip(*positions)
        
        # Update plot
        ax.clear()
        ax.plot(xs, ys, zs, '-o', linewidth=2, markersize=5, color='blue')
        ax.set_xlim([-10, 10])
        ax.set_ylim([-10, 10])
        ax.set_zlim([0, 15])
        ax.set_xlabel('X Axis')
        ax.set_ylabel('Y Axis')
        ax.set_zlabel('Z Axis')
        ax.set_title('Robotic Arm Simulation')
        
        canvas.draw()
    
    except Exception as e:
        logging.error(f"Drawing error: {str(e)}")
        messagebox.showerror("Error", f"Failed to update visualization: {str(e)}")

# ===== GUI Functions =====
def update_robot(*args):
    angles = [var.get() for var in joint_vars]
    draw_robot(angles)

def emergency_stop():
    for var in joint_vars:
        var.set(0)
    update_robot()
    messagebox.showwarning("Emergency Stop", "Robot arm has been reset to default position")

# ===== Main Window Setup =====
root = tk.Tk()
root.title("Robotic Arm Controller")
root.geometry("900x700")

# Create matplotlib figure
fig = plt.figure(figsize=(6, 6))
ax = fig.add_subplot(111, projection='3d')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# ===== Control Panel =====
control_frame = ttk.Frame(root, padding="10")
control_frame.pack(side=tk.LEFT, fill=tk.Y)

# Joint sliders
joint_vars = []
for i in range(5):
    frame = ttk.Frame(control_frame)
    frame.pack(fill=tk.X, pady=5)
    
    label = ttk.Label(frame, text=f"Joint {i+1}:")
    label.pack(side=tk.LEFT)
    
    var = tk.DoubleVar(value=0)
    joint_vars.append(var)
    
    scale = ttk.Scale(
        frame,
        from_=-180,
        to=180,
        orient=tk.HORIZONTAL,
        variable=var,
        command=update_robot
    )
    scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
    
    value_label = ttk.Label(frame, text="0.0°")
    value_label.pack(side=tk.LEFT, padx=5)
    
    # Update label when slider changes
    def make_lambda(v, l): 
        return lambda *_: l.config(text=f"{v.get():.1f}°")
    
    var.trace_add('write', make_lambda(var, value_label))

# Emergency stop button
stop_btn = ttk.Button(
    control_frame,
    text="⛔ EMERGENCY STOP",
    command=emergency_stop,
    style='Emergency.TButton'
)
stop_btn.pack(fill=tk.X, pady=20)

# Style configuration
style = ttk.Style()
style.configure('Emergency.TButton', foreground='white', background='red', font=('Arial', 12, 'bold'))

# Initialize the robot visualization
draw_robot([0]*5)

# Start the application
root.mainloop()
