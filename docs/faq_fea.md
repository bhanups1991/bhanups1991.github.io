# Review of Common Topics in FEA

!!! info "Under Revision"
    Page under heavy revision.

Let us collect the core ideas of the finite element method in one place: how the weak form arises, how elements are mapped and integrated, why elements lock, how stresses are recovered, how errors shrink, and how the tangent stiffness is built. Each topic below follows the same rhythm: *why it matters*, then the idea in plain words, then the equation, then the one thing to remember. Longer algebra sits in collapsible blocks so that the main line stays readable.

The symbols follow the [Consistent Reminders](../glossary/) page. Where this page needs extra symbols, they are fixed once in the table below.


---

### Notation used on this page

| Symbol | Meaning | Note |
| ------ | ------- | ---- |
| \(T,\ \hat T\) | A physical element and its parent (reference) element | Same \(T\in\mathcal T_h\) as in the glossary |
| \(\boldsymbol\xi\) | Parent-element coordinates | Purely computational |
| \(\mathbf X,\ \mathbf x\) | Undeformed and deformed positions of a material point | Physics |
| \(J_{ij}=\partial x_i/\partial\xi_j\) | Element Jacobian, rows = physical coordinates | Convention matters, see Sec. 3 |
| \(\mathbf F\) | Deformation gradient | Never used for force |
| \(\mathbf f\) | Global force vector | \(\mathbf K\mathbf d=\mathbf f\) |
| \(\mathbf K,\ \mathbf K_e\) | Global and element stiffness matrices | |
| \(\mathbf d\) | Vector of nodal degrees of freedom | |
| \(\mathbf n\) | Outward unit normal | |
| \(n_{en}\) | Number of nodes of an element | Not \(n\) |
| \(k\) | Polynomial degree of the *solution* | The "\(p\)" in "\(p\)-refinement" |
| \(q\) | Polynomial degree of the *geometry map* | \(q=k\) is isoparametric |

---

## 1. Foundations: Weak Form and Boundary Conditions

### From strong form to weak form

The finite element method does not solve the pointwise equilibrium equation directly. It solves an integral statement of it, which only asks for as much smoothness as the energy needs. The weak form is how we get there.

Start from pointwise balance, \(-\nabla\cdot\boldsymbol\sigma=\mathbf b\) in \(\Omega\), with \(\mathbf u=\mathbf u_D\) on \(\Gamma_D\) and \(\boldsymbol\sigma\mathbf n=\mathbf t\) on \(\Gamma_t\). Multiply by an admissible virtual displacement \(\delta\mathbf u\) (one that vanishes on \(\Gamma_D\)), integrate over the body, and integrate by parts:

\[-\int_\Omega(\nabla\cdot\boldsymbol\sigma)\cdot\delta\mathbf u\,dV=\int_\Omega\boldsymbol\sigma:\nabla\delta\mathbf u\,dV-\int_{\partial\Omega}(\boldsymbol\sigma\mathbf n)\cdot\delta\mathbf u\,dS\]

Three small facts finish the job. The boundary splits into \(\Gamma_D\cup\Gamma_t\). On \(\Gamma_D\) we have \(\delta\mathbf u=\mathbf 0\), so that part drops out. On \(\Gamma_t\) we replace \(\boldsymbol\sigma\mathbf n\) by the prescribed traction \(\mathbf t\). Because \(\boldsymbol\sigma\) is symmetric, \(\boldsymbol\sigma:\nabla\delta\mathbf u=\boldsymbol\sigma:\boldsymbol\varepsilon(\delta\mathbf u)\). The result is

\[\int_\Omega\boldsymbol\sigma:\boldsymbol\varepsilon(\delta\mathbf u)\,dV=\int_\Omega\mathbf b\cdot\delta\mathbf u\,dV+\int_{\Gamma_t}\mathbf t\cdot\delta\mathbf u\,dS\]

The scalar Poisson problem \(-\nabla^2u=f\) follows the same path:

\[\int_\Omega\nabla u\cdot\nabla v\,dx-\int_{\partial\Omega}(\nabla u\cdot\mathbf n)\,v\,ds=\int_\Omega fv\,dx\]

!!! tip "In short"
    Integration by parts *always* produces a boundary term. Everything that follows (essential vs natural conditions, Nitsche's method) is about what we do with that term.

### Essential vs natural boundary conditions

The two kinds of boundary condition differ in what they do with the boundary term.

**Essential (Dirichlet) conditions** prescribe the primary unknown, here the displacement. They are not part of the equation; they are part of the *space* we search in. Every admissible trial function must already satisfy them, which is why test functions are taken from \(H^1_0\) and the boundary term vanishes on that part of the boundary (see [Function Spaces](../glossary/#function-spaces-in-fem-a-plain-english-hierarchy)).

**Natural (Neumann) conditions** prescribe a derived quantity, here the traction \(\mathbf t=\boldsymbol\sigma\mathbf n\). Nothing is imposed explicitly. The boundary term produced by integration by parts is exactly \(\int_{\Gamma_t}\mathbf t\cdot\delta\mathbf u\,dS\), so supplying the traction simply fills in that term.

!!! tip "In short"
    Essential conditions restrict the space; natural conditions appear in the equation. A traction-free edge needs no code: set \(\mathbf t=\mathbf 0\) and the term vanishes.

!!! warning "Common pitfall"
    "Free" does not mean "unconstrained". A model with only natural conditions still has rigid-body modes, so \(\mathbf K\) is only positive semi-definite and the solve is singular.

### Why the boundary integral vanishes under strong Dirichlet enforcement

Consider the Poisson problem with Dirichlet data on the *whole* boundary. The test functions come from \(H^1_0(\Omega)\), the \(H^1\) functions with zero trace. Since \(v=0\) on \(\partial\Omega\),

\[\int_{\partial\Omega}(\nabla u\cdot\mathbf n)\,v\,ds\equiv0\]

Nothing is dropped or approximated here. The definition of the space does the work. The trial function lives in the affine space \(u\in u_D+H^1_0(\Omega)\): a fixed boundary lift \(u_D\) plus any \(H^1_0\) correction. Numerically this is exactly what applying a Dirichlet boundary condition does: pin the boundary degrees of freedom and solve for the rest. If part of the boundary carries Neumann data instead, the boundary integral over that part is replaced by the prescribed flux, just as the traction term appears above.

---

## 2. Weak Enforcement: Nitsche's Method

### Why it exists

Strong enforcement puts the constraint into the function space. That is easy when the Dirichlet boundary coincides with mesh edges and awkward when it does not: unfitted meshes, embedded interfaces, non-matching meshes in contact. Nitsche's method enforces the condition **weakly**, through extra terms in the variational form. Both \(u_h\) and \(v_h\) then live in the full space \(V_h\subset H^1(\Omega)\) with no boundary constraint, so the boundary integral no longer vanishes and we must handle it deliberately.

### The two extra terms

Start from the integrated-by-parts form, which already contains the flux (consistency) term \(-\int_{\partial\Omega}(\nabla u\cdot\mathbf n)v\,ds\). Nitsche adds two more:

\[-\int_{\partial\Omega}(\nabla v\cdot\mathbf n)(u-u_D)\,ds\;+\;\frac{\alpha}{h}\int_{\partial\Omega}(u-u_D)\,v\,ds\]

- **Symmetry term** \(-\int_{\partial\Omega}(\nabla v\cdot\mathbf n)(u-u_D)\,ds\). It is the transpose of the flux term, so the bilinear form becomes symmetric, \(a(u,v)=a(v,u)\). It vanishes for the exact solution, so consistency is untouched.
- **Penalty term** \(\frac{\alpha}{h}\int_{\partial\Omega}(u-u_D)\,v\,ds\). It pushes \(u\) towards \(u_D\) and restores coercivity. The factor \(1/h\) makes the penalty scale correctly under mesh refinement, and \(\alpha\) must exceed a threshold set by the inverse trace inequality (it depends on polynomial degree and element shape, not on \(h\)).

### Why both terms are needed

The flux term is always there, so the real question is what happens if we drop one of the two additions.

| Terms kept | Consistent | Symmetric | Coercive | Consequence |
| ---------- | :--------: | :-------: | :------: | ----------- |
| Flux + penalty | yes | no | yes (large \(\alpha\)) | Optimal in \(H^1\), suboptimal in \(L^2\) (adjoint-inconsistent) |
| Flux + symmetry | yes | yes | **no** | System can be singular or unstable |
| Flux + symmetry + penalty (Nitsche) | yes | yes | yes | Optimal, symmetric, solvable with standard symmetric solvers |

A non-symmetric matrix does not "break" solvers; it rules out CG and loses the duality argument used for \(L^2\) estimates. Symmetry is what buys the optimal \(L^2\) rate and the symmetric matrix, not the \(H^1\) rate.

!!! tip "In short"
    Consistency keeps the exact solution admissible, the penalty gives coercivity, and the symmetry term gives a symmetric, adjoint-consistent form.

### The final form

All terms containing \(u\) go into the bilinear form, and all known data \(u_D\) goes to the right-hand side, giving the standard \(\mathbf A\mathbf u=\mathbf b\):

\[a(u,v)=\int_\Omega\nabla u\cdot\nabla v\,dx+\int_{\partial\Omega}\Big[-(\mathbf n\cdot\nabla u)\,v-(\mathbf n\cdot\nabla v)\,u+\tfrac{\alpha}{h}\,uv\Big]ds\]

\[L(v)=\int_\Omega fv\,dx+\int_{\partial\Omega}\Big[-(\mathbf n\cdot\nabla v)\,u_D+\tfrac{\alpha}{h}\,u_D\,v\Big]ds\]

!!! note "A regularity subtlety"
    For a general \(H^1\) function, \(\nabla u\cdot\mathbf n\) has no trace. The consistency argument needs a sufficiently regular exact solution, and coercivity is proved on the discrete space \(V_h\) using the inverse trace inequality \(\|\nabla v_h\cdot\mathbf n\|_{L^2(\partial\Omega)}\le C_{inv}\,h^{-1/2}\|\nabla v_h\|_{L^2(\Omega)}\).

The same skeleton, with a one-sided inequality in place of the equality constraint, underlies Nitsche-based contact enforcement. See [Signorini Conditions](../signorini_conditions/).

---

## 3. Geometry and Mapping: Isoparametric Elements

### The idea

An isoparametric element uses the **same shape functions** for the geometry map (parent element to physical element) and for interpolating the solution. "Iso" means same; "parametric" refers to the coordinate parametrization. One set of shape functions does both jobs. See also the dedicated page on [Isoparametric Elements](../isoparametric_elements/).

### What problem it solves

Two problems at once. First, straight-edged elements on a curved domain leave a geometry error that does not shrink when the element degree is raised; curved isoparametric elements follow the true boundary. Second, Gauss quadrature and shape-function differentiation are clean only on a standard shape (the bi-unit square, the unit triangle). Isoparametric elements let all the calculus happen once on the parent element \(\hat T\) and then map the results back.

### The map and the interpolation

For an element \(T\) with \(n_{en}\) nodes at \(\{\mathbf x_i\}\):

\[\mathbf x(\boldsymbol\xi)=\sum_{i=1}^{n_{en}}N_i(\boldsymbol\xi)\,\mathbf x_i,\qquad u_h(\boldsymbol\xi)=\sum_{i=1}^{n_{en}}N_i(\boldsymbol\xi)\,u_i\]

Same \(N_i\), same \(\boldsymbol\xi\): physical coordinates are interpolated from nodal coordinates, and the solution from nodal values.

### The Jacobian and its two jobs

With the convention \(J_{ij}=\partial x_i/\partial\xi_j\) (rows are physical coordinates),

\[\mathbf J=\frac{\partial(x,y)}{\partial(\xi,\eta)},\qquad \frac{\partial x}{\partial\xi}=\sum_i\frac{\partial N_i}{\partial\xi}\,x_i\]

1. **Physical gradients.** The chain rule gives \(\nabla_\xi N_i=\mathbf J^{T}\nabla_x N_i\), hence
   \[\nabla_x N_i=\mathbf J^{-T}\nabla_\xi N_i\]
   (With the opposite layout, rows \(=\xi,\eta\), this reads \(\mathbf J^{-1}\). Always state which one you use.)
2. **Change of variables in integrals:**
   \[\int_T f\,dx\,dy=\int_{\hat T}f\,|\det\mathbf J|\,d\xi\,d\eta\]

\(|\det\mathbf J|\) is the local area (volume) scaling. If \(\det\mathbf J=0\) inside an element, the map is degenerate and the stiffness matrix is meaningless. A negative \(\det\mathbf J\) signals an inverted element.

### Parent element vs reference configuration

Same vocabulary, different objects, and this trips up almost everyone.

|  | Continuum mechanics | Isoparametric FEM |
| -------- | ------------------- | ----------------- |
| Domain 1 | Undeformed body \(\mathcal B_0\), coordinates \(\mathbf X\) | Parent element \(\hat T\), coordinates \(\boldsymbol\xi\) |
| Domain 2 | Deformed body \(\mathcal B_t\), coordinates \(\mathbf x\) | Physical element \(T\), coordinates \(\mathbf x\) |
| Map | Deformation \(\boldsymbol\varphi(\mathbf X)\), **physics** | Element map \(F_T(\boldsymbol\xi)\), **bookkeeping** |
| Gradient of the map | \(\mathbf F=\nabla_X\boldsymbol\varphi\), carries the deformation (strain follows from it; stress enters through the constitutive law) | \(\mathbf J=\partial\mathbf x/\partial\boldsymbol\xi\), carries integration weights and shape-function gradients |
| Meaning | Material is actually moving | Nothing moves; pure change of variables |

This is also why a mesh Jacobian is needed even in an Eulerian formulation whose mesh does not follow material particles: the discretization still needs a parent-to-physical map, entirely separate from the material deformation gradient.

### Two Jacobians in geometrically nonlinear problems

Three configurations coexist:

\[\hat T\xrightarrow{\ \mathbf J_0\ }T_0\xrightarrow{\ \mathbf F\ }T_t,\qquad \mathbf J_t=\mathbf F\,\mathbf J_0\]

Here \(\mathbf J_0=\partial\mathbf X/\partial\boldsymbol\xi\) maps the parent element to the fixed undeformed mesh, and \(\mathbf F=\partial\mathbf x/\partial\mathbf X\) is the physical deformation. In a **Total Lagrangian** formulation, integration stays over the reference configuration with \(\mathbf J_0\); the mesh coordinates never change, and all the physics of deformation is carried by \(\mathbf F\). See [Geometric Nonlinearity](../geometric_nonlinearity/) for the full treatment.

### Sub-, iso-, and superparametric elements

| Variant | Geometry order | Solution order | Comment |
| ------- | -------------- | -------------- | ------- |
| Subparametric | \(q<k\) | higher | Common in practice: straight-edged P2 meshes, many \(p\)-version codes. Geometry error limits accuracy on curved boundaries |
| Isoparametric | \(q=k\) | same | The standard workhorse |
| Superparametric | \(q>k\) | lower | Better geometry representation than solution; specialised |

### When is the map valid?

The isoparametric map \(F_T:\hat T\to T\) is defined for any node count, with one condition: it must be a **bijection**, one-to-one and onto, with \(\det\mathbf J\neq0\) throughout the element interior. Whether this holds depends on node placement, not on the element type alone. The classic danger is a badly placed midside node. In a quadratic element, moving a midside node towards a corner makes \(\det\mathbf J\) reach zero at that corner exactly when the node sits at the **quarter point**, and go negative beyond it.

!!! note "A deliberate exception"
    Quarter-point elements place the midside node on purpose at that position, so \(\det\mathbf J=0\) at the crack tip and the strain acquires the \(r^{-1/2}\) singularity of linear elastic fracture mechanics. Mesh-quality checks flag it everywhere else.

### Gauss quadrature on mapped elements

Gauss quadrature is exact for polynomials up to a given degree. What it integrates here is not always a polynomial.

- On an **affine** element (parallelogram, parallelepiped, straight-sided triangle or tetrahedron), \(\mathbf J\) is constant and the stiffness integrand is polynomial, so a suitable rule is exact.
- On a **non-affine** element, \(\mathbf J^{-T}\) and \(1/\det\mathbf J\) enter the stiffness integrand, which becomes *rational*. Finite-point quadrature is then an approximation whose accuracy depends on element order, distortion and the chosen rule.
- The **mass** matrix is friendlier. Whenever the geometry map is polynomial, \(\det\mathbf J\) is polynomial too, so \(N_iN_j\det\mathbf J\) is polynomial and can be integrated exactly with a sufficient rule.

### Why match geometry order to solution order

Two error sources are present at once: approximating the boundary \(\partial\Omega\) with a degree-\(q\) map, and approximating \(u\) with degree-\(k\) functions. For a smooth solution, isoparametric elements (\(q=k\)) give an \(H^1\) error of \(O(h^k)\), so going up an order changes the **rate**, not just a constant. With \(q<k\) on a curved boundary the geometry error caps the rate however large \(k\) is. For a Dirichlet problem on a straight-edged approximation, the classical result is a rate limited to roughly \(h^{3/2}\) (Ciarlet and Raviart; Strang and Fix). Choosing \(q=k\) keeps neither error source from polluting the other.

!!! warning "In DOLFINx, the function space does not set the geometry"
    A `("Lagrange", 2)` element defines the *function space* only. The mesh has its own coordinate element, which is degree 1 by default, so P2 on a default mesh is **subparametric**. For isoparametric P2, generate a second-order mesh (for example with `gmsh.model.mesh.setOrder(2)`) and read it in with DOLFINx's Gmsh reader, so the mesh carries a degree-2 coordinate element.

### What if isoparametric elements are not used?

There are two options, and neither is attractive.

- **Subparametric geometry**: a straight-edged mesh with a high-order solution. The geometry error persists regardless of the solution degree: a curved boundary stays a polygon, and only \(h\)-refinement reduces the error.
- **Shape functions defined directly in physical space**: possible in principle, but every element then has a different shape, so Gauss points and shape-function tables cannot be reused, and building well-behaved polynomials on distorted or curved physical elements is hard. The efficiency of assembly collapses.

Isoparametric elements are not mathematically mandatory. They dominate because they make the implementation uniform, efficient and clean across all element shapes.

### Higher-order elements under geometric nonlinearity

In a geometrically nonlinear problem the fixed mesh map is only part of the story. The deformation gradient \(\mathbf F=\mathbf I+\nabla\mathbf u_h\) comes from the displacement field, and \(\nabla\mathbf u_h\) has polynomial degree one lower than \(\mathbf u_h\) (on affine elements). So the picture is richer than in linear elasticity:

- For P2 displacements on affine elements, \(\mathbf F\) is linear within the element.
- Green–Lagrange strain contains \(\nabla\mathbf u_h^T\nabla\mathbf u_h\), so \(\mathbf E\) is already **quadratic**.
- For a hyperelastic or plastic material, \(\mathbf S(\mathbf E)\) is not polynomial at all.
- On non-affine elements, \(\mathbf J^{-T}\) adds a rational factor on top.

No quadrature rule therefore integrates the internal force exactly. The rule is chosen for accuracy and stability, and reduced rules bring the hourglass issues of the next section.

---

## 4. Locking, Integration, and Cures

### What locking is

Locking is **artificial stiffening**. The discrete displacement space cannot represent a deformation that the physics allows without picking up spurious strain energy. In both cases below, a constraint that should be satisfied *only in a limit* gets enforced everywhere.

|  | Shear locking | Volumetric locking |
| -- | ------------- | ------------------ |
| Trigger | Bending of low-order elements | Near-incompressibility (any order, worst for linear) |
| Constraint over-enforced | Transverse shear strain \(\approx0\) (Kirchhoff limit) | \(\operatorname{div}\mathbf u=0\) pointwise |
| Material-dependent? | No, a geometry/interpolation issue | Yes, tied to Poisson's ratio and the material law |
| Typical cures | Reduced or selective integration, higher-order elements, incompatible modes | Mixed \(u\)–\(p\) formulation, B-bar, selective reduced integration |

!!! tip "In short"
    Zero shear in pure bending, zero volume change at incompressibility: the exact solution needs it, the discrete space cannot deliver it, and the shortfall is paid for in energy.

### Shear locking, concretely

Take a 2-node Timoshenko beam. The shear strain is \(\gamma(x)=dw/dx-\theta(x)\). Linear shape functions make \(dw/dx\) constant but \(\theta(x)\) linear, so

\[\gamma(x)=\frac{w_2-w_1}{L}-\theta_1-\frac{(\theta_2-\theta_1)\,x}{L}\]

Whenever there is curvature (\(\theta_1\neq\theta_2\)), \(\gamma\) cannot vanish everywhere, so real bending drags along spurious shear. Per unit width, the shear stiffness scales as \(GA_s\sim Et\) while the bending stiffness scales as \(EI\sim Et^3\), so their ratio grows like \(1/t^2\). As the beam gets slender, the spurious shear term dominates the energy and the element stiffens artificially.

??? note "The same picture in 2D: a Q4 element in pure bending"
    The exact bending field is \(u_x=-\kappa xy\), \(u_y=\tfrac12\kappa x^2\), with \(\gamma_{xy}=\partial_y u_x+\partial_x u_y=0\). On a rectangle with nodes at \(x=\pm a\), \(y=\pm b\), bilinear interpolation gives
    \(u_x^h=-\kappa xy\) (this field lies in the bilinear space) and \(u_y^h=\tfrac12\kappa a^2\) (the nodal values at \(x=\pm a\) are equal, so there is no variation in \(x\)). Therefore \(\partial_x u_y^h=0\) while \(\partial_y u_x^h=-\kappa x\), and \(\gamma^h_{xy}=-\kappa x\neq0\).

### Hourglassing is a side effect of the cure

Hourglassing is **not** a consequence of shear or volumetric locking. It is a side effect of the usual cure, *reduced integration*. Integration order is a single lever with two failure modes: too much integration locks, too little produces hourglass modes.

### Undersampling in the rank picture

The element stiffness is \(\mathbf K_e=\sum_{gp}w_{gp}\,\mathbf B^T\mathbf D\,\mathbf B\,|\det\mathbf J|\). Each Gauss point contributes rank at most the number of strain components, so \(\operatorname{rank}(\mathbf K_e)\le n_{gp}\times(\text{strain components})\). By rank–nullity, the dimension of the null space is the number of DOFs minus the rank.

For a 4-node plane element with 1-point integration, \(\operatorname{rank}(\mathbf K_e)\le3\) and there are 8 DOFs, so the null space has dimension at least 5. Only 3 of those are legitimate rigid-body modes (two translations, one rotation). The remaining \(\ge2\) are **hourglass modes**: displacement patterns whose strain vanishes at the single sample point while storing real energy elsewhere in the element. They are like a sine wave sampled only at its zero crossings. In Abaqus, reduced-integration elements such as `CPS4R` and `C3D8R` therefore carry artificial hourglass stiffness.

### Selective reduced integration (SRI)

Integrate the *problematic* strain part (shear for shear locking, volumetric for volumetric locking) at reduced order, and the well-behaved part (bending, deviatoric) at full order. This removes the over-constraint that causes locking, while the fully integrated part keeps the element from hourglassing. It is a middle path between full integration (locks) and uniform reduced integration (hourglasses).

### The B-bar method

Split the strain into deviatoric and volumetric parts. Keep \(\mathbf B_{dev}\) from the full shape-function derivatives and replace \(\mathbf B_{vol}\) by an averaged, lower-order \(\bar{\mathbf B}_{vol}\), still evaluated at the **full** set of Gauss points. The cure comes from making the volumetric operator *poorer*, so that it cannot over-charge energy in the incompressible mode, rather than from sampling fewer points. Hourglassing does not appear because the deviatoric part is fully integrated and keeps \(\mathbf K_e\) at full rank.

For isotropic linear elasticity, B-bar and SRI can be shown to give the same \(\mathbf K_e\) (Hughes, 1980): same cure, different mechanism (under-representing vs. undersampling).

### Incompatible modes

Enrich the interpolation with extra internal "bubble" modes, statically condensed out, so the element can bend with a richer internal curvature field. This fixes shear locking without forcing spurious shear strain: the same goal as SRI and B-bar, reached by adding kinematic freedom rather than weakening the sampling. The quadrature stays fully integrated, so no hourglass modes arise in the small-strain setting.

"Incompatible" points to a separate issue. These modes can break displacement continuity between elements, which is why Taylor's correction is needed for the element to pass the patch test. Under large compressive strains, enhanced elements can show hourglass-like instabilities (Wriggers and Reese).

---

## 5. Verifying Elements: The Patch Test

The patch test asks whether an assembly of elements, with arbitrary geometry, reproduces an exact constant-strain field when the boundary conditions are set up to produce it. Passing means the element is *consistent*: it can represent the simplest non-trivial state correctly. Passing, together with stability, is what is needed for convergence as \(h\to0\).

!!! warning "What the patch test does not tell you"
    It does not guarantee good bending behaviour, resistance to locking, robustness under severe distortion, accurate contact pressure, or good dynamic performance. It is a minimum requirement, not a certificate of quality.

---

## 6. Strain and Stress Output

### Where strains and stresses are computed

At the **Gauss (integration) points**, not at the nodes. The solve of \(\mathbf K\mathbf d=\mathbf f\) produces only nodal displacements. Strain and stress are derived quantities: \(\boldsymbol\varepsilon(\boldsymbol\xi)=\mathbf B(\boldsymbol\xi)\,\mathbf d_e\), and for linear elasticity \(\boldsymbol\sigma=\mathbf D\boldsymbol\varepsilon\). In a nonlinear analysis the stress comes instead from the constitutive update at each Gauss point. Gauss points are the natural place for three reasons:

1. \(\mathbf B\) is already evaluated there during stiffness assembly.
2. Nonlinear state variables (plastic strain, contact status) are stored and updated there.
3. Certain Gauss points are **superconvergent** for stresses: on regular meshes and for smooth solutions, the stress is more accurate there than elsewhere, including at the nodes. These are the Barlow points, the Gauss points of the *reduced* rule (the centroid for Q4, the \(2\times2\) points for Q8/Q9), which need not coincide with the full-integration points.

### From Gauss points to nodal plots

Nodal stress values in a contour plot are a post-processing product. The solver extrapolates each element's Gauss-point values to its own nodes (with the same or a specially fitted shape function evaluated outside the Gauss-point range), then averages across the elements that share a node. This is why post-processors offer "averaged" and "unaveraged" nodal stress. Unaveraged plots look discontinuous across element boundaries; averaged plots look smooth.

!!! tip "In short"
    The jumps in an unaveraged plot are not an eyesore to be hidden. They are a free indicator of discretization error, and averaging smooths them away.

---

## 7. Mesh Refinement and Convergence Rates

### Error norms and rates

For polynomial degree \(k\) and a sufficiently smooth solution, the energy (\(H^1\)) error behaves like \(O(h^k)\), while the \(L^2\) error behaves like \(O(h^{k+1})\), one order higher (the Aubin–Nitsche duality argument, which needs adequate elliptic regularity of the problem). For linear elements (\(k=1\)): the energy error is \(O(h)\), so halving \(h\) halves it, but the \(L^2\) error is \(O(h^2)\), so halving \(h\) quarters it.

### \(h\)-, \(p\)-, and \(hp\)-refinement

| Strategy | What changes | Convergence |
| -------- | ------------ | ----------- |
| \(h\)-refinement | Smaller elements, fixed \(k\) | Algebraic, \(O(h^k)\) for smooth \(u\); limited by the regularity of \(u\) otherwise |
| \(p\)-refinement | Higher \(k\), fixed mesh | **Exponential** for smooth (analytic) solutions; algebraic with a singularity, at roughly twice the \(h\)-rate (Babuška–Suri) |
| \(hp\)-refinement | Graded mesh at singularities, high \(k\) elsewhere | Exponential, even with singularities |

### Where \(h\)-refinement earns its keep

Wherever regularity is lost: crack-tip singularities in fracture mechanics, the contact edge in contact mechanics (sharp gradients, a moving active set), shock and compaction fronts in dynamics, re-entrant corners and notches, thin boundary and shear layers. Here no polynomial degree removes the problem locally, and shrinking the region a polynomial has to approximate is the right response.

### Where \(p\)-refinement earns its keep

Wherever the solution is smooth: linear-elastic stress analysis away from singularities, modal and vibration analysis, heat conduction in smooth homogeneous domains, low-to-moderate-frequency wave propagation and acoustics, smooth-geometry Dirichlet problems without contact.

!!! tip "In short"
    \(h\)-refinement compensates for *lost regularity*. \(p\)-refinement exploits *smoothness that is already there*. \(hp\)-adaptive methods spend \(h\) where regularity is bad and \(p\) where it is good.

---

## 8. Nonlinearity and the Tangent Stiffness

### Where nonlinearity comes from

Three independent sources, combinable at will.

- **Material.** The constitutive law \(\boldsymbol\sigma(\boldsymbol\varepsilon)\) is nonlinear (plasticity, hyperelasticity). This alone makes the residual nonlinear even under small-strain kinematics: the strain–displacement relation stays linear, but stress against strain does not.
- **Geometric.** The strain measure is nonlinear in displacement (e.g. the quadratic term in Green–Lagrange strain), and equilibrium refers to the current, unknown configuration.
- **Contact and boundary.** The active set, gap, normals, friction or topology change with the solution. This is often non-smooth, not just nonlinear, and it can make the residual nonlinear even when material and kinematics are both linear. Follower loads and nonlinear boundary conditions belong here too.

### What is linearized to build the tangent

Newton's method needs the derivative of the residual \(R\) with respect to the displacement \(u\) in a direction \(\Delta u\): the Gateaux derivative. It gives a tangent bilinear form, which after discretization becomes \(\mathbf K_T=\partial\mathbf R/\partial\mathbf d\). For standard Galerkin FEM, linearize-then-discretize and discretize-then-linearize give the same matrix. In FEniCS/UFL, `derivative` differentiates the *weak form* symbolically, and the discretization happens when the form is assembled. For contact discretizations (mortar, segment-to-segment) the two orders of operation need not agree, which is one reason contact tangents need care.

### Material and geometric stiffness

Start from the internal virtual work in the reference configuration,

\[\delta W_{int}=\int_{\Omega_0}\mathbf S:\delta\mathbf E\,dV_0\]

with the second Piola–Kirchhoff stress \(\mathbf S\) and the Green–Lagrange strain \(\mathbf E\). Linearizing about the current state gives two terms:

\[\Delta(\delta W_{int})=\int_{\Omega_0}\Delta\mathbf S:\delta\mathbf E\,dV_0+\int_{\Omega_0}\mathbf S:\Delta(\delta\mathbf E)\,dV_0\]

- With \(\Delta\mathbf S=\mathbb C_{tan}:\Delta\mathbf E\), the first term is the **material stiffness** \(\mathbf K_M\). It carries the constitutive tangent.
- The second term is the **geometric (initial-stress) stiffness** \(\mathbf K_G\). The *existing* stress \(\mathbf S\) acts on the change of the strain *variation*, \(\Delta(\delta\mathbf E)\), which is nonzero because \(\mathbf E\) is nonlinear in \(\mathbf u\).

Together, \(\mathbf K_T=\mathbf K_M+\mathbf K_G\), plus a contact part \(\mathbf K_{c}\) when contact is present.

!!! note "A naming caution"
    \(\mathbf K_M\) is "material" because it contains \(\mathbb C_{tan}\), but it also contains the displacement-dependent part of \(\mathbf B\) (the large-displacement effect). It is not simply the small-strain stiffness.

### What linearization drops

The Newton step is first-order in \(\Delta u\), so everything of higher order is thrown away. On the stress side, \(\mathbf S(\mathbf E+\Delta\mathbf E)\approx\mathbf S+\mathbb C_{tan}:\Delta\mathbf E\), with constitutive nonlinearity in the remainder. On the strain side, \(\mathbf E(\mathbf u+\Delta\mathbf u)\) contains a quadratic piece \(\tfrac12\nabla\Delta\mathbf u^T\nabla\Delta\mathbf u\), which is dropped. This is *not* where \(\mathbf K_G\) comes from; \(\mathbf K_G\) is first-order in \(\Delta\mathbf u\) and arises from the variation \(\delta\mathbf E\), as shown above. Contact adds its own contribution from linearizing the gap and traction terms, often non-smooth rather than polynomial.

### The consistent (algorithmic) tangent

In path-dependent problems like plasticity, the stress at a Gauss point is produced by a time-stepping algorithm (for example a return mapping). The **consistent tangent** is the exact derivative of *that algorithm's* output with respect to the strain increment (Simo and Taylor), not the continuum tangent \(\mathbb C_{tan}\). Using it is what restores the quadratic convergence of Newton's method. With the continuum tangent the iteration still converges, but only linearly.

!!! tip "In short"
    \(\mathbf K_T=\mathbf K_M+\mathbf K_G\,(+\,\mathbf K_c)\). The material part comes from linearizing the stress, the geometric part from the change of the strain variation, and "consistent" means consistent with the discrete update, not with the continuum law.

---

*More topics to be added as needed.*