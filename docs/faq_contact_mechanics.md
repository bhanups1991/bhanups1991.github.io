# Contact Mechanics — FAQ

Consolidated from prior technical discussions on contact search, discretization, kinematics, and constraint enforcement. Continuum kinematics/stress and the linear-algebra/nonlinear-solver machinery that contact tangents feed into are covered in their own companion FAQs.

---

## 1. The Computational Hierarchy of FE Contact

**Q: What's the overall computational hierarchy of a nonlinear contact problem?**
A useful decomposition:

$$\boxed{\text{candidate search} \to \text{contact discretization} \to \text{geometric mapping} \to \text{gap/slip} \to \text{constraint enforcement} \to \text{global linearization}}$$

**Search** identifies possibly-interacting entities; **discretization** decides which geometric entities are coupled (nodes, segments, surfaces); **mapping** (projection/ray tracing) determines correspondence between them; **kinematics** produce the gap and slip from that correspondence; **enforcement** turns the gap/slip into a reaction; **linearization** supplies the contact contribution to the global Newton tangent. Keeping these layers conceptually separate prevents methods at different levels — e.g. mortar (a discretization) and Nitsche (an enforcement method) — from being wrongly treated as competing alternatives at the same level.

**Q: What's the difference between contact discretization and contact enforcement?**
**Discretization** specifies *which* geometric entities interact — nodes, segments, facets, surfaces. **Enforcement** specifies *how* the inequality constraint is imposed — penalty, Lagrange multiplier, augmented Lagrangian, Nitsche. These are independent, orthogonal layers and can be combined in different ways (e.g. mortar discretization with penalty enforcement, or node-to-segment with Nitsche enforcement).

---

## 2. Contact Search

**Q: How do broad-phase contact search algorithms differ?**
Brute force tests every pair — $O(n^2)$, simple but expensive. AABB/BVH (axis-aligned bounding box / bounding volume hierarchy) methods reject spatially separated entities through hierarchical bounding volumes. Spatial hashing maps objects into nearby grid cells. Sweep-and-prune sorts projected intervals along an axis and exploits frame-to-frame temporal coherence. Octrees/k-d trees recursively subdivide space. All of these accelerate *candidate* identification; none define the contact constraint itself — that's a separate, subsequent step.

**Q: What's the distinction between broad-phase and narrow-phase search?**
Broad-phase efficiently narrows down which entities *could* interact (bounding boxes, trees, spatial hashing). Narrow-phase then computes the precise geometric relationship between the surviving candidates — closest-point projection, intersection, surface normal, contact gap.

---

## 3. Contact Kinematics: Gap and the Signorini Conditions

**Q: How is the normal gap obtained from closest-point projection?**
For a master surface $\mathbf x_m(\boldsymbol\xi)$, minimize the distance from a slave point $\mathbf x_s$:

$$d^2(\boldsymbol\xi) = \|\mathbf x_s - \mathbf x_m(\boldsymbol\xi)\|^2$$

Stationarity gives $(\mathbf x_s - \mathbf x_m)\cdot\mathbf x_{m,\alpha} = 0$ for each parametric tangent direction $\alpha$ — i.e. the connecting vector is orthogonal to the master surface's tangent plane, hence normal to it. Therefore

$$\boxed{g_n = (\mathbf x_s - \mathbf x_m)\cdot\mathbf n}$$

**Q: How are the unilateral (frictionless) contact conditions expressed mathematically?**
The **Signorini conditions**:

$$\boxed{g_n \ge 0, \qquad \lambda_n \ge 0, \qquad g_n\lambda_n = 0}$$

expressing, respectively: non-penetration; a non-negative (compressive) contact reaction; and complementarity — reaction is nonzero only where the gap is closed ($g_n=0$), and the gap can only be positive where reaction is zero. (Sign conventions for $\lambda_n$ vary by source — some define it as compressive-negative — but the complementarity structure is universal.)

**Q: What's the optimization interpretation of frictionless elastic contact?**
Elastic contact can be formulated as minimizing total potential energy subject to the unilateral non-penetration constraint $g_n\ge0$. The same problem can equivalently be expressed as a **variational inequality**, a **complementarity problem**, or via **Karush–Kuhn–Tucker (KKT)** conditions — the Signorini conditions above are exactly the KKT conditions of that constrained minimization. Every enforcement method below (penalty, multiplier, augmented Lagrangian, Nitsche, barrier) is a different numerical realization of the same underlying constrained-optimization structure.

**Q: Why can a nonlinear contact problem have multiple solutions?**
Geometric nonlinearity, friction, changing contact topology, material nonlinearity, and structural instability can all make the equilibrium problem nonconvex. Multiple admissible equilibrium configurations may then exist, and which one the solver converges to can depend on loading history, initial configuration, active-set evolution during Newton iteration, and the specific nonlinear solution strategy used.

---

## 4. Discretization: Node-to-Node, Node-to-Segment, Segment-to-Segment, Mortar

**Q: How do node-to-node, node-to-segment, segment-to-segment, and mortar contact differ?**

| Method | Mechanism | Trade-off |
|---|---|---|
| **Node-to-node** | Directly couples corresponding nodes on opposing surfaces | Simple, but requires matching meshes and is restrictive under sliding |
| **Node-to-segment** | Projects a discrete slave node onto an opposing master segment/facet | Flexible for non-matching meshes and sliding, but introduces master/slave bias |
| **Segment-to-segment / surface-to-surface** | Couples interacting surface *patches* rather than a point-to-segment pair | Improves pressure transfer, reduces (but doesn't eliminate) bias |
| **Mortar** | Variational interface formulation — surface fields (and usually a multiplier field) coupled through interface integrals | Systematically handles non-matching meshes; compatibility is enforced over the interface, not node-by-node |

Mortar and segment-to-segment are **not synonyms**: mortar describes a *variational* interface formulation, while segment-to-segment describes a *geometric coupling* strategy. Mortar formulations are frequently *implemented* through segment-to-segment integration, but a segment-to-segment scheme need not be variationally mortar.

**Q: What is node-to-segment contact, concretely?**
A slave node is projected onto a master segment/surface; the projection determines a corresponding master point, whose normal defines the gap (as in the closest-point-projection formula above). The master's interpolation distributes the contact contribution to the master's nodes. This accommodates non-matching meshes and sliding, but the formulation is inherently one-sided.

**Q: What is mortar contact, and how is its integration domain built?**
Potential contact surfaces are decomposed into interacting facet pairs; geometric projection or intersection determines local interaction regions for each pair. The global contact integration domain is assembled from these local regions, with the interface integral evaluated by summing quadrature contributions over the interacting pairs. Surface fields — and usually a Lagrange-multiplier field representing contact pressure — are interpolated and coupled through these interface integrals, so compatibility is enforced *variationally over the interface* rather than pointwise at individual slave nodes. (The actual interacting regions are only known once contact search and geometric mapping have run on the current configuration — the potential surfaces are specified in advance, but not the active interacting regions.)

---

## 5. Master/Slave Bias

**Q: Why does node-to-segment contact introduce master/slave bias, and what does it mean concretely?**
The discretization is asymmetric: one surface (the "master") supplies the projection geometry, interpolation, and normal; the other ("slave") supplies the point being projected. Reversing which surface is master therefore changes the projection, the normal, the interpolation, the quadrature, the discrete gap, and its derivative — hence the assembled contact residual and tangent. The continuum contact problem is symmetric with respect to the two bodies; the discrete node-to-segment approximation generally is not.

**Q: Does master/slave bias mean the global tangent stiffness becomes ill-conditioned?**
No — these are separate issues. **Bias** means the discrete *solution* can depend on the (in principle arbitrary) choice of which surface is master. **Ill-conditioning** is a numerical property of the resulting algebraic system (its eigenvalue spread, roughly). A biased formulation can *contribute* to poor conditioning in particular situations, but bias is fundamentally about discretization asymmetry, not conditioning per se.

**Q: What makes irregular or differently-discretized contact surfaces especially sensitive to master/slave choice?**
Reversing the master changes the surface supplying projection, interpolation, normal evaluation, and contact-point representation. When the two surfaces differ substantially in curvature, mesh resolution, or topology, these changes become significant, and the discrete contact forces (and the overall solution) can differ noticeably depending on which side is designated master.

**Q: What does an "unbiased" contact formulation change relative to a standard master/slave formulation?**
It treats the two contacting surfaces symmetrically, so the discrete contact problem no longer depends on an arbitrary master designation — achieved through two-sided contributions, symmetric variational terms, or other unbiased formulations (e.g. unbiased Nitsche contact). The central objective is eliminating master/slave dependence from the discrete approximation, not merely reducing it.

---

## 6. Constraint Enforcement: Penalty, Multiplier, Augmented Lagrangian, Nitsche, Barrier

**Q: How do penalty, Lagrange-multiplier, augmented-Lagrangian, and Nitsche methods differ?**
- **Penalty**: enforces the constraint approximately through a finite stiffness, $\lambda_n = \epsilon\langle -g_n\rangle_+$ (the Macaulay bracket $\langle\cdot\rangle_+$ activates only under penetration). Adds no extra unknowns, but the constraint is only satisfied approximately, with residual penetration $-g_n = \lambda_n/\epsilon$.
- **Lagrange multiplier**: enforces the *active* constraint exactly, but introduces an independent multiplier field as an additional unknown, giving the assembled system a saddle-point (indefinite) structure.
- **Augmented Lagrangian**: combines the two — a multiplier that's iteratively updated, stabilized by a penalty term; approaches exact enforcement without requiring the arbitrarily large penalty a pure-penalty method would need.
- **Nitsche**: enforces the condition weakly through consistent variational terms plus stabilization, *without* an independent multiplier field — retaining a purely displacement-based unknown structure while incorporating the contact condition directly into the weak form.

These differ in constraint enforcement accuracy, number of unknowns, system conditioning, and linearization structure.

**Q: What is the optimization role of the penalty method, and why does increasing $\epsilon$ hurt conditioning?**
Penalty replaces exact constraint enforcement with an energetic penalty for penetration. For active contact, $-g_n = \lambda_n/\epsilon$, so larger $\epsilon$ reduces penetration — but

$$\left\|\frac{\partial\lambda_n}{\partial g_n}\right\| = \epsilon$$

so the local contact stiffness grows unboundedly large relative to the surrounding bulk stiffness scales as $\epsilon\to\infty$. This increases the assembled system's condition number and can degrade iterative-solver performance (and, in the small-$\epsilon$ limit, permits excessive penetration). The method therefore trades constraint accuracy against numerical conditioning — there's no free lunch in $\epsilon$.

**Q: What is the optimization role of Lagrange multipliers in contact?**
Multipliers enforce the constraint directly and carry the physical interpretation of contact reaction/pressure. The resulting discrete system contains both displacement and multiplier unknowns and has a saddle-point structure (indefinite, requiring compatible discretizations — e.g. an inf-sup/LBB-type condition on the multiplier space — and specialized linear solvers). Unlike penalty, exact enforcement doesn't require an arbitrarily large stiffness parameter.

**Q: How does the augmented-Lagrangian update combine penalty and multiplier enforcement?**
A representative update:

$$\boxed{\lambda_n^{k+1} = \lambda_n^k + \epsilon\langle -g_n\rangle_+}$$

The multiplier $\lambda_n$ carries the physical reaction, while the penalty term controls constraint violation *during* the iterative update — allowing convergence to (near-)exact enforcement without needing the extreme penalty stiffness a pure-penalty formulation would.

**Q: How does Nitsche enforcement differ from Lagrange-multiplier enforcement in structure?**
A representative Nitsche-type Dirichlet structure (see the FEA FAQ for the full derivation in the Poisson case) is

$$-\langle\sigma(u)n, v\rangle_\Gamma - \langle\sigma(v)n, u-g\rangle_\Gamma + \left\langle\frac{\gamma}{h}(u-g), v\right\rangle_\Gamma$$

Contact modifies this structure for the unilateral/frictional case (typically via a projection/complementarity function rather than a linear penalty). The method avoids an independent multiplier field while retaining consistency through the added variational terms — so it keeps the system size and sparsity pattern of a plain displacement-based problem, unlike the Lagrange-multiplier approach.

**Q: What are barrier methods in contact mechanics?**
Barrier methods incorporate the non-penetration inequality through a potential that becomes increasingly unfavorable (formally diverges) as the admissible boundary ($g_n=0$) is approached from the feasible side. They therefore aim to keep the solution *strictly* within the feasible region ($g_n>0$) rather than permitting finite penetration and penalizing it after the fact — giving barrier formulations a direct connection to interior-point methods for inequality-constrained optimization.

**Q: What is the third-medium method?**
Introduces an artificial, highly compliant deformable medium filling the gap between two potentially-contacting bodies. Contact interaction is represented through the constitutive response of this third medium rather than through an explicit inequality constraint between the two surfaces. This reformulates contact as a (nonlinear) material/continuum problem, which can be advantageous for complex contact topology changes and self-contact, where explicit surface-pairing logic becomes cumbersome.

---

## 7. Friction

**Q: How is Coulomb friction expressed as a local contact constitutive condition?**
With tangential traction $\mathbf t_t$ and normal reaction $\lambda_n$:

$$\boxed{\|\mathbf t_t\| \le \mu\lambda_n}$$

Defining the slip function $\phi = \|\mathbf t_t\| - \mu\lambda_n$: **stick** corresponds to $\phi<0$ (tangential traction strictly inside the friction cone, no relative sliding), **sliding** to $\phi=0$ (traction on the cone boundary, $\mathbf t_t$ opposing the slip direction). The contact operator is therefore piecewise-defined and **non-smooth** at stick–slip transitions — a genuinely different kind of nonlinearity from ordinary smooth constitutive nonlinearity, and the reason contact/friction problems typically need semismooth-Newton or active-set treatment rather than plain Newton.

---

## 8. Local Contact Operators and the Contact Tangent

**Q: What is a local contact operator, and why does its Jacobian matter?**
At a contact quadrature point, the traction is some function of the gap (and slip, for friction):

$$\boxed{\mathbf t_c = \mathcal C(\mathbf g)}, \qquad \boxed{\Delta\mathbf t_c = \mathbf K_c^{\text{loc}}\Delta\mathbf g, \quad \mathbf K_c^{\text{loc}} = \frac{\partial\mathcal C}{\partial\mathbf g}}$$

The global contact residual is assembled from these local contributions, and $\mathbf K_c^{\text{loc}}$ governs the contact contribution to the global Newton tangent. Its continuity, monotonicity, differentiability (or, where non-smooth, semismoothness), and conditioning are important numerical properties — they influence existence/uniqueness of the discrete problem, the validity of standard Newton linearization, convergence rate, and what solver/globalization strategy is appropriate. A representative such operator is the **Alart–Curnier** mixed penalty-duality formulation, particularly for frictional contact — it produces a local nonlinear operator relating gaps, tractions, and frictional state that is piecewise (hence potentially non-smooth), which is why generalized/semismooth Newton methods are relevant when using it.

**Q: How can the local contact operator's monotonicity and Jacobian be verified numerically?**
**Monotonicity**: evaluate the operator at many pairs of admissible states and check whether the change in output has a nonnegative inner product with the corresponding change in input, covering inactive contact, active contact, stick/slip transitions, and (where relevant) frictional regimes; systematic violations indicate non-monotone behavior. **Jacobian correctness**: a directional finite-difference test compares the observed change in the local residual against $\mathbf K_c^{\text{loc}}$ applied to the same perturbation, repeated over several perturbation magnitudes to distinguish genuine implementation errors from finite-difference truncation/round-off noise. Symmetry and eigenvalue checks on $\mathbf K_c^{\text{loc}}$ additionally reveal whether the local operator has a symmetric variational structure (relevant to solver choice) and whether it has positive, zero, or negative curvature directions (relevant to local stability/conditioning and possible nonconvexity).

**Q: How does the local contact tangent enter the global FE Jacobian?**
If the local gap variation relates to the global displacement increment through $\Delta\mathbf g = \mathbf G\,\Delta\mathbf d$ (with $\mathbf G$ built from the contact discretization's interpolation and projection geometry), then $\Delta\mathbf t_c = \mathbf K_c^{\text{loc}}\mathbf G\,\Delta\mathbf d$, and the assembled contact stiffness is

$$\boxed{\mathbf K_c = \int_{\Gamma_c}\mathbf G^T\mathbf K_c^{\text{loc}}\mathbf G\,d\Gamma}$$

The overall chain is: contact operator $\to$ local tangent $\to$ contact stiffness $\to$ global Jacobian — assembled into $K_T = K_{\text{material}}+K_{\text{geometric}}+K_c$ alongside the bulk material and geometric stiffness from the FEA FAQ, and passed to the same Newton/linear-solver machinery covered in the Linear Algebra & Solvers FAQ.
