# NOTE: This code was generated entirely by an AI model (Gemini), in several iterations, based on the initial prompt and subsequent refinements.
#       I have reviewed the code and made necessary adjustments to ensure it is consistent with our current discussion.
#       If you find any issues or have suggestions for improvement, please let me know.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

# Set LaTeX-style Computer Modern fonts and dark background
plt.rcParams['font.family'] = 'serif'
plt.rcParams['mathtext.fontset'] = 'cm'
plt.style.use('dark_background')

# Define F with a significant rotation (40 degrees) combined with stretch
theta = np.radians(40)
c, s = np.cos(theta), np.sin(theta)
R = np.array([[c, -s], [s, c]])
S = np.array([[1.2, 0.1], [0.1, 0.9]])
F = R @ S

# Compute tensor transformations and their inverses/transposes
F_T = F.T
F_inv = np.linalg.inv(F)
F_inv_T = np.linalg.inv(F).T

# Initial reference vector v_0 (Tail A at origin, Head B_0)
A = np.array([0.0, 0.0])
v_0 = np.array([2.5, 1.5])

# Transformations & intermediate argument vectors
v_F = F @ v_0                 
v_FT_Fv = F_T @ v_F         
v_Finv_Fv = F_inv @ v_F     
v_FinvT_v = F_inv_T @ v_0     

operations = [
    # 1. F v_0 -> v
    ("vector_transform_F.svg", None, v_0, v_F, 
     r'$\mathbf{v} = \mathbf{F}\mathbf{v}_0$', 
     r'Reference Basis ($\mathbf{E}_i$) $\rightarrow$ Current Basis ($\mathbf{e}_i$)',
     r'$v_i \mathbf{e}_i = (F_{ij} \mathbf{e}_i \otimes \mathbf{E}_j) \cdot (v_{0k} \mathbf{E}_k)$' + '\n' +
     r'$v_i \mathbf{e}_i = F_{ij} v_{0j} \mathbf{e}_i$', 
     '#00f3ff', (0.05, 0.95)),
    
    # 2. F^T (F v_0) -> u (Using correct components F_{ij} with flipped bases)
    ("vector_transform_FT.svg", v_F, v_0, v_FT_Fv, 
     r'$\mathbf{u} = \mathbf{F}^T(\mathbf{F}\mathbf{v}_0)$', 
     r'Current Basis ($\mathbf{e}_i$) $\rightarrow$ Reference Basis ($\mathbf{E}_i$)',
     r'$U_j \mathbf{E}_j = (F_{ij} \mathbf{E}_j \otimes \mathbf{e}_i) \cdot (v_k \mathbf{e}_k)$' + '\n' +
     r'$U_j \mathbf{E}_j = F_{ij} v_i \mathbf{E}_j$', 
     '#ff007f', (0.05, 0.95)),
    
    # 3. F^-1 (F v_0) -> v_0
    ("vector_transform_Finv.svg", v_F, v_0, v_Finv_Fv, 
     r'$\mathbf{v}_0 = \mathbf{F}^{-1}(\mathbf{F}\mathbf{v}_0)$', 
     r'Current Basis ($\mathbf{e}_i$) $\rightarrow$ Reference Basis ($\mathbf{E}_i$)',
     r'$v_{0j} \mathbf{E}_j = (F^{-1}_{ji} \mathbf{E}_j \otimes \mathbf{e}_i) \cdot (v_k \mathbf{e}_k)$' + '\n' +
     r'$v_{0j} \mathbf{E}_j = F^{-1}_{ji} v_i \mathbf{E}_j$', 
     '#00ff66', (0.05, 0.95)),
    
    # 4. F^-T v_0 -> w
    ("vector_transform_FinvT.svg", None, v_0, v_FinvT_v, 
     r'$\mathbf{w} = \mathbf{F}^{-T}\mathbf{v}_0$', 
     r'Reference Basis ($\mathbf{E}_i$) $\rightarrow$ Current Basis ($\mathbf{e}_i$)',
     r'$w_i \mathbf{e}_i = (F^{-T}_{ij} \mathbf{e}_i \otimes \mathbf{E}_j) \cdot (v_{0k} \mathbf{E}_k)$' + '\n' +
     r'$w_i \mathbf{e}_i = F^{-T}_{ij} v_{0j} \mathbf{e}_i$', 
     '#ffe600', (0.05, 0.95))
]

for filename, v_arg, v_start, v_trans, vec_name, space_transition, derivation_text, color, box_pos in operations:
    fig, ax = plt.subplots(figsize=(9, 7.5))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    # Trimmed axes limits: x from -1 to 5, y from -1 to 5
    ax.set_xlim(-1, 5)
    ax.set_ylim(-1, 5)
    ax.set_xticks(np.arange(-1, 6, 1))
    ax.set_yticks(np.arange(-1, 6, 1))
    
    # Gridlines and axes lines
    ax.grid(True, color='#222222', linewidth=0.8, linestyle='-')
    ax.axhline(0, color='#444444', linewidth=1.2)
    ax.axvline(0, color='#444444', linewidth=1.2)
    
    # Plot primary initial reference vector v_0
    ax.quiver(A[0], A[1], v_start[0], v_start[1], angles='xy', scale_units='xy', scale=1, 
              color='#ffffff', width=0.005, headwidth=4, headlength=6)
    
    # Plot secondary argument vector if present (e.g., F v_0)
    if v_arg is not None:
        ax.quiver(A[0], A[1], v_arg[0], v_arg[1], angles='xy', scale_units='xy', scale=1, 
                  color='#00f3ff', alpha=0.6, width=0.005, headwidth=4, headlength=6)
        ax.scatter([v_arg[0]], [v_arg[1]], color='#00f3ff', zorder=5, alpha=0.6)
        ax.text(v_arg[0] + 0.2, v_arg[1] + 0.2, r'$\mathbf{F}\mathbf{v}_0$', color='#00f3ff', fontsize=16.5)

    # Plot final transformed vector
    ax.quiver(A[0], A[1], v_trans[0], v_trans[1], angles='xy', scale_units='xy', scale=1, 
              color=color, width=0.007, headwidth=5, headlength=7)
    
    # Midpoint-to-midpoint serpentine snake-like routing for the curved arrow
    from_vec = v_arg if v_arg is not None else v_start
    mid_from = 0.5 * from_vec
    mid_to = 0.5 * v_trans
    
    arrow = FancyArrowPatch(
        (mid_from[0], mid_from[1]), (mid_to[0], mid_to[1]),
        connectionstyle="angle3,angleA=45,angleB=-45", color='white', alpha=0.7,
        arrowstyle="simple,head_length=8,head_width=6", lw=1.5, zorder=6
    )
    ax.add_patch(arrow)

    # Markers and labels
    ax.scatter([A[0]], [A[1]], color='#888888', zorder=5)
    ax.scatter([v_start[0]], [v_start[1]], color='#ffffff', zorder=5)
    ax.scatter([v_trans[0]], [v_trans[1]], color=color, zorder=5)
    
    ax.text(A[0] - 0.3, A[1] - 0.3, r'$O\ (0,0)$', color='#aaaaaa', fontsize=15)
    ax.text(v_start[0] + 0.2, v_start[1] + 0.2, r'$\mathbf{v}_0$', color='#ffffff', fontsize=16.5)
    ax.text(v_trans[0] + 0.2, v_trans[1] + 0.2, vec_name, color=color, fontsize=16.5)
    
    ax.set_aspect('equal')
    ax.set_title(space_transition, fontsize=19.5, color='white', pad=15)
    
    # Overlay mathematical derivation box with bright white text
    ax.text(box_pos[0], box_pos[1], derivation_text, transform=ax.transAxes, color='#ffffff', fontsize=15, 
             bbox=dict(boxstyle='round,pad=0.8', facecolor='#111111', edgecolor=color, alpha=0.9),
             horizontalalignment='left', verticalalignment='top', zorder=10)
    
    for spine in ax.spines.values():
        spine.set_edgecolor('#444444')
        
    plt.tight_layout()
    plt.savefig(filename, format='svg', facecolor=fig.get_facecolor(), edgecolor='none', pad_inches=0.1)
    plt.close()

print("Successfully generated and saved final SVG figures with corrected F^T index notation.")