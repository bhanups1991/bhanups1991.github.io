The simplest way to remove the confusion is to keep just one central question in mind:

> At each load/time step, **what unknowns must be found, and do we solve them directly or iteratively?**

```markdown
# Finite-Element Analysis: From Weak Form to Solution

## 0. Governing problem

Strong form:
- Balance law in the continuum
- Constitutive law
- Kinematics
- Boundary conditions
- Initial conditions for dynamics

Example structural dynamics:

\[
\rho \ddot{\mathbf u} - \nabla \cdot \boldsymbol{\sigma}
= \mathbf b
\]

with:
- \(\mathbf u\): displacement
- \(\boldsymbol{\sigma}\): stress from the material model
- \(\mathbf b\): body force

---

## 1. Weak formulation

Purpose:
- Reduce differentiability requirements on the solution
- Introduce test functions
- Obtain the form used for finite-element discretization

Virtual-work form:

\[
\delta W_{\mathrm{int}}
+
\delta W_{\mathrm{inertia}}
=
\delta W_{\mathrm{ext}}
\]

Discrete semi-discrete equation:

\[
\mathbf M\ddot{\mathbf u}
+
\mathbf C\dot{\mathbf u}
+
\mathbf f_{\mathrm{int}}(\mathbf u,\text{state})
=
\mathbf f_{\mathrm{ext}}(t)
\]

Important:
- The weak form may already be nonlinear.
- Nonlinearity can come from material behavior, geometry, contact, or boundary conditions.

---

## 2. Spatial discretization

Approximate the unknown field using FE shape functions:

\[
\mathbf u(\mathbf x,t)
\approx
\mathbf N(\mathbf x)\mathbf d(t)
\]

Produces finite-dimensional equations:

\[
\mathbf R(\mathbf d,\dot{\mathbf d},\ddot{\mathbf d},t)
=
\mathbf 0
\]

where:

\[
\mathbf R
=
\mathbf f_{\mathrm{ext}}
-
\mathbf f_{\mathrm{int}}
-
\mathbf C\dot{\mathbf d}
-
\mathbf M\ddot{\mathbf d}
\]

Key outputs:
- Global displacement vector \(\mathbf d\)
- Global mass matrix \(\mathbf M\)
- Damping matrix \(\mathbf C\), if used
- Internal force vector \(\mathbf f_{\mathrm{int}}\)
- Residual vector \(\mathbf R\)

---

## 3. Classify the FE problem

### Linear versus nonlinear

Linear:
- Small deformation
- Linear elastic material
- Fixed boundary/contact conditions
- Constant stiffness matrix

\[
\mathbf K\mathbf d=\mathbf f
\]

Nonlinear:
- Material nonlinearity: plasticity, hyperelasticity, viscoelasticity, damage
- Geometric nonlinearity: large deformation/rotation
- Contact nonlinearity
- Nonlinear loads or constraints

\[
\mathbf R(\mathbf d)=\mathbf 0
\]

### Quasi-static versus dynamic

Quasi-static:

\[
\mathbf f_{\mathrm{int}}(\mathbf d)
=
\mathbf f_{\mathrm{ext}}(\lambda)
\]

Dynamic:

\[
\mathbf M\ddot{\mathbf d}
+
\mathbf C\dot{\mathbf d}
+
\mathbf f_{\mathrm{int}}(\mathbf d)
=
\mathbf f_{\mathrm{ext}}(t)
\]

---

## 4. Discretize the evolution

### Quasi-static: load increments

\[
\lambda_n
\rightarrow
\lambda_{n+1}
\]

At each load increment, solve for:

\[
\mathbf d_{n+1}
\]

### Dynamics: time increments

\[
t_n
\rightarrow
t_{n+1}=t_n+\Delta t
\]

At each time step, solve for some combination of:

\[
\mathbf d_{n+1},
\quad
\dot{\mathbf d}_{n+1},
\quad
\ddot{\mathbf d}_{n+1}
\]

The time integrator determines whether this step requires a global nonlinear iteration.

---

## 5. Choose the time-integration method

### Explicit dynamics

Typical method:
- Central difference / leapfrog

Core idea:
- Compute acceleration from known forces at \(t_n\)
- Update velocity
- Update displacement
- No global Newton iteration

\[
\ddot{\mathbf d}_n
=
\mathbf M^{-1}
\left(
\mathbf f_{\mathrm{ext},n}
-
\mathbf f_{\mathrm{int},n}
\right)
\]

\[
\dot{\mathbf d}_{n+1/2}
=
\dot{\mathbf d}_{n-1/2}
+
\Delta t\,\ddot{\mathbf d}_n
\]

\[
\mathbf d_{n+1}
=
\mathbf d_n
+
\Delta t\,\dot{\mathbf d}_{n+1/2}
\]

Requirements:
- Usually lumped/diagonal mass matrix
- Stable only if:

\[
\Delta t < \Delta t_{\mathrm{critical}}
\]

Main computational cost:
- Element/material update
- Internal-force assembly
- Very many small time steps

Key point:

> Explicit dynamics avoids a global equilibrium iteration, but it still performs a local constitutive update at every integration point.

### Implicit dynamics

Typical methods:
- Newmark-\(\beta\)
- HHT-\(\alpha\)
- Generalized-\(\alpha\)

At \(t_{n+1}\), the unknown displacement appears inside the internal force:

\[
\mathbf f_{\mathrm{int}}(\mathbf d_{n+1})
\]

Therefore the time-discrete equation is generally nonlinear:

\[
\mathbf R_{n+1}(\mathbf d_{n+1})
=
\mathbf 0
\]

Requirement:
- Global Newton–Raphson iterations at each time step for nonlinear problems

Advantages:
- Usually stable for larger time steps
- Better for slower/quasi-static response

Cost:
- Repeated global tangent-matrix assembly
- Repeated global linear-system solves

---

## 6. Nonlinear solution: Newton–Raphson

Used when the discrete equation is nonlinear:

\[
\mathbf R(\mathbf x)=\mathbf 0
\]

where \(\mathbf x\) may contain displacement only, or displacement/velocity/acceleration/contact variables.

At Newton iteration \(i\):

\[
\mathbf R(\mathbf x^{(i)})
\neq
\mathbf 0
\]

Linearize the residual:

\[
\mathbf R(\mathbf x^{(i)}+\Delta\mathbf x)
\approx
\mathbf R(\mathbf x^{(i)})
+
\mathbf J^{(i)}\Delta\mathbf x
\]

Solve:

\[
\mathbf J^{(i)}
\Delta\mathbf x^{(i)}
=
-\mathbf R^{(i)}
\]

Update:

\[
\mathbf x^{(i+1)}
=
\mathbf x^{(i)}
+
\Delta\mathbf x^{(i)}
\]

Stop when:
- Residual is sufficiently small
- Increment is sufficiently small
- Energy criterion is satisfied
- Maximum iteration count is reached

Key point:

> Newton iterations are global iterations within one load increment or one implicit time step.

---

## 7. Linearization and tangent matrix

The matrix in the Newton step is the Jacobian:

\[
\mathbf J
=
\frac{\partial \mathbf R}{\partial \mathbf x}
\]

For structural mechanics, it is commonly called the tangent stiffness:

\[
\mathbf K_{\mathrm{T}}
=
\frac{\partial \mathbf f_{\mathrm{int}}}{\partial \mathbf d}
\]

Typical contributions:

\[
\mathbf K_{\mathrm{T}}
=
\mathbf K_{\mathrm{material}}
+
\mathbf K_{\mathrm{geometric}}
+
\mathbf K_{\mathrm{contact}}
+
\mathbf K_{\mathrm{constraint}}
\]

Material contribution:
- Comes from the constitutive tangent

\[
\mathbb C_{\mathrm{alg}}
=
\frac{\partial\boldsymbol{\sigma}}
{\partial\boldsymbol{\varepsilon}}
\]

Geometric contribution:
- Comes from stress-dependent changes in equilibrium under large deformation

Contact contribution:
- Comes from the derivative of contact forces with respect to displacement

Key point:

> Linearization produces a linear problem. It does not solve the original nonlinear problem by itself.

---

## 8. Linear system solve

Each Newton iteration requires a linear solve:

\[
\mathbf K_{\mathrm{T}}
\Delta \mathbf d
=
-\mathbf R
\]

This is the level where a matrix inverse is conceptually involved.

In practice, one almost never computes:

\[
\mathbf K_{\mathrm{T}}^{-1}
\]

explicitly.

Instead, solve the system using:

### Direct solvers

\[
\mathbf K_{\mathrm{T}}
=
\mathbf L\mathbf U
\]

or, for suitable symmetric systems:

\[
\mathbf K_{\mathrm{T}}
=
\mathbf L\mathbf D\mathbf L^T
\]

Examples:
- LU
- Cholesky
- LDL\(^T\)

### Iterative solvers

Examples:
- Conjugate gradient
- GMRES
- BiCGSTAB

Usually combined with:
- Preconditioning
- Domain decomposition
- Multigrid

Key point:

> A linear solver may perform many algebraic iterations, but these are different from Newton iterations.

---

## 9. Local material-point update

At every element integration point:

\[
\Delta\boldsymbol{\varepsilon}
\rightarrow
\boldsymbol{\sigma}_{n+1},
\;
\mathbf q_{n+1}
\]

where \(\mathbf q\) denotes internal variables, for example:
- Plastic strain
- Equivalent plastic strain
- Hardening variables
- Damage variables
- Viscoelastic variables

### Elastic material

Direct update:

\[
\boldsymbol{\sigma}_{n+1}
=
\mathbb C
:
\boldsymbol{\varepsilon}_{n+1}
\]

### Inelastic material

Usually involves a local return-mapping problem:

\[
\text{Given }
\Delta\boldsymbol{\varepsilon},
\text{ find }
\Delta\lambda,
\boldsymbol{\sigma}_{n+1},
\mathbf q_{n+1}
\]

This may require a local Newton iteration.

Key distinction:

> Local Newton iteration: solves a constitutive update at one Gauss point.

> Global Newton iteration: solves equilibrium for all nodal unknowns.

---

## 10. Full algorithmic hierarchy

```text
CONTINUUM MODEL
│
├── Strong form
├── Constitutive law
├── Boundary conditions
└── Initial conditions
     │
     ▼
WEAK FORM
     │
     ▼
SPATIAL FE DISCRETIZATION
     │
     ▼
SEMI-DISCRETE SYSTEM
│
└── M a + C v + f_int(d, state) = f_ext(t)
     │
     ▼
LOAD/TIME INCREMENT
│
├── Explicit method
│   │
│   ├── Evaluate material response locally
│   ├── Assemble internal force
│   ├── Compute acceleration directly
│   ├── Update velocity and displacement
│   └── Move to next small stable time step
│
└── Implicit method
    │
    ├── Start time/load increment
    ├── Guess global unknowns
    ├── Local material update at Gauss points
    ├── Assemble global residual
    ├── Check global convergence
    │
    └── If not converged:
        │
        ├── Linearize residual
        ├── Assemble tangent/Jacobian
        ├── Solve K_T Δd = -R
        ├── Update global unknowns
        └── Repeat Newton iteration
```

---

## 11. The three iteration levels

```text
LEVEL 1: LOAD OR TIME STEPS
│
├── n = 0, 1, 2, ...
└── Advance from t_n to t_(n+1)
     │
     ▼
LEVEL 2: GLOBAL NEWTON ITERATIONS
│
├── i = 0, 1, 2, ...
├── Used in nonlinear implicit FE
├── Enforces global equilibrium
└── Repeats until residual converges
     │
     ▼
LEVEL 3: LOCAL MATERIAL ITERATIONS
│
├── At each Gauss point
├── Used for nonlinear constitutive updates
├── Example: return mapping in plasticity
└── Produces stress, state variables, and algorithmic tangent
```

---

## 12. One-sentence summary

```text
Explicit FE:
small time step → local material update → internal force → direct acceleration update → next step

Implicit nonlinear FE:
time/load step → global Newton iteration → local material updates → tangent assembly → linear solve → repeat until equilibrium
```
```

## The distinction to memorize

The following table is the key to keeping the concepts separate:

| Concept | Question it answers | Typical occurrence |
|---|---|---|
| Weak form | What equation is the FE method enforcing? | Before discretization |
| Spatial discretization | How is the field represented with nodal DOFs? | Once per model formulation |
| Time/load increment | How do we advance the physical problem? | Outer loop |
| Local material iteration | What stress/state follows from a strain increment? | At each Gauss point |
| Global Newton iteration | How do we satisfy global equilibrium? | Inside an implicit nonlinear increment |
| Linearization/tangent | What linear approximation is used for Newton? | Every Newton iteration |
| Linear solver iteration | How is \( \mathbf K_T \Delta\mathbf d=-\mathbf R \) solved? | Inside each Newton iteration |
| Matrix inverse | Conceptual only; normally not formed explicitly | Linear algebra stage |

## For your current foam-wave solver

Your current FEniCS/VUMAT solver is most naturally summarized as:

```text
EXPLICIT DYNAMIC FE WITH A LOCAL VUMAT UPDATE

time step n
│
├── Known: u_n, v_(n-1/2), stress_n, state_n
├── Compute external force f_ext,n
├── Compute internal force f_int,n from stress_n
├── Compute acceleration:
│       a_n = M_lumped^(-1) (f_ext,n - f_int,n)
├── Update half-step velocity:
│       v_(n+1/2) = v_(n-1/2) + Δt a_n
├── Update displacement:
│       u_(n+1) = u_n + Δt v_(n+1/2)
├── Compute strain increment from u_(n+1) - u_n
├── Call VUMAT locally:
│       Δε → σ_(n+1), state_(n+1)
└── Proceed to the next time step
```

There is **no global Newton–Raphson loop**, no global tangent stiffness matrix, and no global stiffness-matrix inverse in this explicit formulation. Your VUMAT can still contain a local Newton iteration for its viscoplastic return mapping, but that iteration happens separately at each material point.