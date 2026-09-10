# NOTE: This code was generated entirely by an AI model (ChatGPT), in 2 iterations, based on the initial prompt and subsequent refinement.
#       I have reviewed the code and made necessary adjustments to ensure it is consistent with our current discussion.
#       If you find any issues or have suggestions for improvement, please let me know.

import numpy as np
import matplotlib.pyplot as plt

# Rotation angle
theta = np.deg2rad(45)

# Rotation matrix
R = np.array([
            [np.cos(theta), -np.sin(theta)],
            [np.sin(theta),  np.cos(theta)]
            ])

# Reference coordinates of a square
X = np.array([
            [0.0, 0.0],
            [1.0, 0.0],
            [1.0, 1.0],
            [0.0, 1.0]
            ])

# Pure rigid-body rotation: x = R X
x = X @ R.T

# Displacement: u = x - X
u = x - X

# Displacement gradient (constant for rigid rotation)
# since u = x - X = RX - X = (R - I) X, 
# therefore we have Grad(u) = (R - I)Grad(X) = R - I, 
# because Grad(X) = I (identity matrix), and R - I is constant.
H = R - np.eye(2)

# Infinitesimal strain
epsilon = 0.5 * (H + H.T)

# Deformation gradient, F = Grad(x) = Grad(RX) = R Grad(X) = R I = R
F = R

# Green-Lagrange strain
C = F.T @ F
E = 0.5 * (C - np.eye(2))

print("Rotation matrix R:\n", R)
print("\nDisplacement gradient H:\n", H)
print("\nInfinitesimal strain epsilon:\n", epsilon)
print("\nGreen-Lagrange strain E:\n", E)

# -------------------------------------------------------------------------
# Plot reference and rotated configurations
# -------------------------------------------------------------------------

# Match the plotting style used on the tensors_with_bases page
plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'cm'
plt.style.use('dark_background')

fig, ax = plt.subplots(figsize=(9, 7.5))

fig.patch.set_facecolor('black')
ax.set_facecolor('black')

# Reference configuration
ax.plot(np.r_[X[:, 0], X[0, 0]],np.r_[X[:, 1], X[0, 1]],'o-',color='#ffffff',linewidth=2.0,markersize=7,label=r'Reference configuration')

# Rigid-body rotated configuration
ax.plot(np.r_[x[:, 0], x[0, 0]],np.r_[x[:, 1], x[0, 1]],'o-',color='#00f3ff',linewidth=2.5,markersize=7,label=r'Rigid-body rotation')

# Axes limits
ax.set_xlim(-1.2, 2.0)
ax.set_ylim(-1.2, 2.0)

# Grid and axes
ax.grid(True, color='#222222', linewidth=0.8, linestyle='-')
ax.axhline(0, color='#444444', linewidth=1.2)
ax.axvline(0, color='#444444', linewidth=1.2)

# Labels and title
ax.set_xlabel(r'$X / x$', fontsize=17, color='white')
ax.set_ylabel(r'$Y / y$', fontsize=17, color='white')
ax.set_title(r'Pure Rigid-Body Rotation ($45^\circ$)',fontsize=19.5,color='white',pad=15)

# Legend
legend = ax.legend(fontsize=14,frameon=True,facecolor='#111111',edgecolor='#444444')

for text in legend.get_texts():
    text.set_color('white')

# Spines
for spine in ax.spines.values():
    spine.set_edgecolor('#444444')

ax.set_aspect('equal')
plt.tight_layout()
plt.show()