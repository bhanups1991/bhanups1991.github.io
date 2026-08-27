### Reformulating Signorini Contact Conditions via the Positive Part Operator

In Signorini contact mechanics, unilateral contact constraints on the boundary $\Gamma_c$ are typically expressed through the classical complementarity conditions:

$$u_N \le g_N, \quad \sigma_N \le 0, \quad \sigma_N (u_N - g_N) = 0$$

where $g_N$ is the normal gap function and $\sigma_N$ is the normal contact pressure (defined negative in compression).

### Algebraic Reformulation with the Positive Part Operator

To implement these non-smooth constraints efficiently in computational frameworks (such as Nitsche-based formulations in FEniCS), the complementarity system can be equivalently rewritten using the positive part operator $(\cdot)_+ = \max(0, \cdot)$. 

For a given penalty parameter $\kappa > 0$, the contact condition is compactly satisfied when:

$$\sigma_N = - \left( \kappa (u_N - g_N) - \sigma_N \right)_+$$

$$\sigma_N = - \max\left( 0, \kappa (u_N - g_N) - \sigma_N \right)$$

This projection formulation maps the trial contact pressure onto the admissible region, avoiding explicit active-set search loops while ensuring thermodynamic and mechanical consistency.

### Visualization of the Projection Operator

To build intuition around how the positive part operator enforces the Signorini complementarity subset, we can refer to the following image.

![Signorini Conditions and Positive Part Operator](/images/signorini_conditions.png)