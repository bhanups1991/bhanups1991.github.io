# Reformulating Signorini Contact Conditions via the Positive Part Operator

In Signorini contact mechanics, unilateral contact constraints on the boundary $\Gamma_c$ are typically expressed through the classical complementarity conditions:

$$g_n \ge 0, \quad p_n \ge 0, \quad p_n g_n = 0$$

where $g_n$ is the normal gap function and $p_n$ is the normal contact pressure (defined positive in compression). 

## Algebraic Reformulation with the Positive Part Operator

To implement these non-smooth constraints efficiently in computational frameworks (such as Nitsche-based formulations in FEniCS), the complementarity system can be equivalently rewritten using the positive part operator $(\cdot)_+ = \max(0, \cdot)$. 

For a given penalty parameter $\gamma > 0$, the contact condition is compactly satisfied when:

$$p_n = \left( p_n - \gamma g_n \right)_+$$

This projection formulation maps the trial contact pressure onto the admissible positive cone, avoiding explicit active-set search loops while ensuring thermodynamic and mechanical consistency.

## Visualization of the Projection Operator

To build intuition around how the positive part operator enforces the Signorini complementarity subset, we can visualize the mapping of the unconstrained intermediate state to the valid mechanical contact response:

```python
import numpy as np
import matplotlib.pyplot as plt

# Define range of intermediate gap-pressure states
x = np.linspace(-3, 3, 400)
# Positive part operator projection: p_n = max(0, x)
proj_positive = np.maximum(0, x)

plt.figure(figsize=(8, 5))
plt.plot(x, proj_positive, label=r'$p_n = (p_n - \gamma g_n)_+$', color='indigo', lw=2.5)
plt.axhline(0, color='black', lw=1)
plt.axvline(0, color='black', lw=1)
plt.title('Signorini Projection via Positive Part Operator', fontsize=12)
plt.xlabel('Intermediate State ($p_n - \gamma g_n$)', fontsize=10)
plt.ylabel('Projected Contact Pressure ($p_n$)', fontsize=10)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.show()
```