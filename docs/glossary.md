Let us revisit some key definitions and recall the symbols used. This page should be visited often and treated as a sacred space. This provides the language on which the equations in the main part are written.

---

### Definiteness of a Matrix

For a **symmetric** matrix (or second-order tensor), definiteness can be classified based on the signs of its eigenvalues $\lambda_i$:

- **Positive Definite:** All eigenvalues are strictly positive,
  $\lambda_i > 0$ for all $i$.

- **Positive Semi-Definite:** All eigenvalues are non-negative,
  $\lambda_i \geq 0$ for all $i$.

- **Negative Definite:** All eigenvalues are strictly negative,
  $\lambda_i < 0$ for all $i$.

- **Negative Semi-Definite:** All eigenvalues are non-positive,
  $\lambda_i \leq 0$ for all $i$.

!!! info "Note"
    If $\boldsymbol{A}$ has both positive and negative eigenvalues, it is **indefinite**.


Let us see why this classification is central to the equations we see in continuum mechanics and FEM. For a symmetric matrix $\boldsymbol{A}$, definiteness is characterized through the **quadratic form** defined as $\boldsymbol{x}^{T}\boldsymbol{A}\boldsymbol{x}$, where $\boldsymbol{x}$ is any nonzero vector in the space on which $\boldsymbol{A}$ acts. Notice that this matrix product yields a scalar quantity. The value and, in particular, the sign of this scalar **for all possible nonzero choices of $\boldsymbol{x}$** determine the definiteness of $\boldsymbol{A}$.

$$
\begin{aligned}
\boldsymbol{x}^{T}\boldsymbol{A}\boldsymbol{x} &> 0
&&\quad \forall\,\boldsymbol{x}\neq\boldsymbol{0}
&&\Rightarrow&& \boldsymbol{A}\text{ is positive definite},\\
\boldsymbol{x}^{T}\boldsymbol{A}\boldsymbol{x} &\geq 0
&&\quad \forall\,\boldsymbol{x}\neq\boldsymbol{0}
&&\Rightarrow&& \boldsymbol{A}\text{ is positive semi-definite},\\
\boldsymbol{x}^{T}\boldsymbol{A}\boldsymbol{x} &< 0
&&\quad \forall\,\boldsymbol{x}\neq\boldsymbol{0}
&&\Rightarrow&& \boldsymbol{A}\text{ is negative definite},\\
\boldsymbol{x}^{T}\boldsymbol{A}\boldsymbol{x} &\leq 0
&&\quad \forall\,\boldsymbol{x}\neq\boldsymbol{0}
&&\Rightarrow&& \boldsymbol{A}\text{ is negative semi-definite}.
\end{aligned}
$$

Just by looking at the definition of the quadratic form, it becomes clear that it is closely related to energy calculations. Recall that the strain energy and kinetic energy of a discretized mechanical system can be written as:

$$
\frac{1}{2}\left(\mathbf{u}^{T}\mathbf{K}\mathbf{u}\right), \quad \text{and} \quad 
\frac{1}{2}\left(\dot{\mathbf{u}}^{T}\mathbf{M}\dot{\mathbf{u}}\right), \quad \text{respectively.}
$$

Naturally, we require the strain energy to be non-negative for any admissible nonzero displacement $\mathbf{u}$. Similarly, we require the kinetic energy to be non-negative for any admissible nonzero velocity $\dot{\mathbf{u}}$. In other words, we need the stiffness matrix $\mathbf{K}$ and mass matrix $\mathbf{M}$ to be positive definite.

In particular, the mass matrix is positive definite, while the stiffness matrix can be positive semi-definite also. Alternatively, the scalar value of the quadratic form or our strain energy can be zero also for a non zero displacement field. This is generally the case when Dirichlet boundary conditions are not imposed. 

In the absence of sufficient constraints, the system can have rigid-body modes, for which the strain energy is zero and, consequently, $\mathbf{u}^{T}\mathbf{K}\mathbf{u}=0.$ The stiffness matrix becomes positive definite when the imposed Dirichlet boundary conditions eliminate all rigid-body modes. For most practical problems, sufficient Dirichlet boundary conditions are imposed to eliminate these rigid-body modes, so we rarely need to worry about this subtle detail. However, it is worth keeping in mind when discussing the definiteness of the stiffness matrix.

!!! warning "Work in Progress:"

    More explanation on the positive definiteness of the stretch tensor and other quantities to be added.

### Function Spaces in FEM: A Plain-English Hierarchy

Before jumping onto the notations, let us see how the broader families of mathematical spaces nest inside one another. Here are some top-level, good-to-know, working definitions. Best to remember all three, but the third one is the key space associated with FEM most of the time.

* **Banach Spaces:** A *Banach space* is any complete vector space equipped with a norm — a way to measure the "size" of a function or vector. Think of a norm as a ruler: it tells us how big something is. "Complete" simply means the space has no holes in it; if a sequence of functions keeps getting closer and closer to each other, the thing they are converging to is also inside the space. No missing limits, no surprises. Usually represented by the letterS $X, Y, B$.

* **Hilbert Spaces:** A *Hilbert space* is a Banach space with one extra gift: an **inner product** — a generalisation of the familiar dot product from vector calculus. Because we now have an inner product, we can talk about *angles* between functions, what it means for two functions to be *orthogonal*, and how to *project* one function onto another. This geometric intuition is exactly what makes weak forms and variational problems so natural to work with. Most linear PDE theory lives here.

    - Generic Hilbert space: $H$, $V$
    - Inner product: $(\cdot,\cdot)$ or $\langle \cdot, \cdot \rangle$
    - The induced norm: $\|u\| = \sqrt{(u,u)}$

* **Sobolev Spaces:** A *Sobolev space* is a particular type of Hilbert space made for functions whose derivatives (up to some chosen order) are also square-integrable. In structural mechanics, displacement fields live in Sobolev spaces like $H^1(\Omega)$ because we need the solution to carry finite energy. Usually represented by the letters $L, H$. Most of the times, H has a superscript denoting the order upto and including which the derivates are also square integrable. 

    - What exactly is square-integrability? It means that if we take a function $f$, square it to get $f^2$, and integrate over the domain, the result must be finite — not blow up, not be infinite. Recall the energy stored in a uniaxial bar: $\frac{1}{2} E \varepsilon^2$. In 3D, the same idea holds — the integral of the squared strain field over the body gives us the total stored elastic energy. A real, finite body made of a real material can only store a finite amount of energy. So square-integrability is not an abstract mathematical demand; it is simply the mathematical way of saying that our strain field must be physically reasonable. If the strains (derivatives of displacements) blow up somewhere in a non-integrable way, we are describing an object with infinite stored energy — which is not physical.

    - This is why we need derivatives to also be square-integrable, not just the displacements themselves. Displacements tell us where points moved; strains tell us how the material deformed; energy depends on the strains. All three must be well-behaved and finite.

    - Here are some sample definitions:
        - $L^2(\Omega)$ — Square-integrable functions on $\Omega$ (the base case, zero derivatives needed)
        - $H^1(\Omega)$ — Functions in $L^2$ whose first derivatives are also in $L^2$
        - $H^k(\Omega)$ — Functions whose derivatives up to order $k$ are in $L^2$
        - $H^1_0(\Omega)$ — Subspace of $H^1$ with zero trace on $\partial\Omega$ (strong Dirichlet BC built-in)
    
    - What does zero trace or strong Dirichlet BC built-in mean? This means that the space definition itself says that the functions vanish on the boundary. In other words it is a collection of all $H^1$ functions whose boundary footprint is exactly zero. When we pick the test functions from $H^1_0$, it comes pre-loaded with the condition $v|_{\partial\Omega}=0$. No extra condition needs to be imposed. An example of saying so much by using just a 0 in the subscript.
        

* **Finite-Dimensional Subspaces ($V_h$):** Sobolev spaces contain infinitely many functions — a computer cannot work with that directly. So we shrink the problem down to a *finite-dimensional subspace* $V_h \subset H^1(\Omega)$: a carefully chosen collection of simple, piecewise polynomial functions defined on a mesh of element size $h$. Instead of searching over all possible displacement fields in $H^1(\Omega)$, we search only within $V_h$. This is the step that turns a continuous variational problem into a finite matrix equation that a computer can actually solve. The mesh size $h$ controls how fine this approximation is — as $h \to 0$, $V_h$ grows and the FEM solution converges back toward the true Sobolev-space solution. Here are some sample definitions:
    - $V_h \subset H^1(\Omega)$ — the FEM trial/test space
    - $V_h^0 \subset H^1_0(\Omega)$ — same but with zero boundary trace enforced as explained above
    - The subscript $h$ always signals discretisation at mesh scale $h$
    - Elements of $V_h$ are often written $u_h$, $v_h$ to distinguish them from the true solution $u \in H^1$

!!! info "NOTE: The Central Approximation of FEM"
    The jump from $u \in H^1(\Omega)$ to $u_h \in V_h$ is the central approximation of FEM — and the whole error analysis of FEM is essentially asking: how large is $\|u - u_h\|_{H^1}$, and how fast does it shrink as $h \to 0$?

---

### Dissecting an example Notation

Let us say, we have this definition of $V_h$. This is taken from section 1.5 of [this](https://link.springer.com/article/10.1007/s00211-018-0950-x) paper by Chouly et. al..

$$\mathbf{V}_h = (\mathbf{V}_h^1 \times \mathbf{V}_h^2), \quad \text{with } \mathbf{V}_h^i = \left\{ \mathbf{v}_h^i \in \mathscr{C}^0(\overline{\Omega^i}) : \mathbf{v}_h^i\vert{}_T \in (\mathbb{P}_k(T))^d, \forall T \in \mathcal{T}_h^i, \mathbf{v}_h^i = 0 \text{ on } \Gamma_D^i \right\}$$

Let's break down every single component piece-by-piece:

* $\mathcal{T}_h^i$: The finite element mesh (triangulation) of domain $\Omega^i$ with mesh size parameter $h$.
* $\mathbf{V}_h$: The total global trial/test space for *both* bodies combined (the Cartesian product of the spaces for Body 1 and Body 2).
* $\mathbf{V}_h^i$: The finite-dimensional vector space of discrete functions belonging to body $i$ ($i \in \{1, 2\}$).
* $\mathscr{C}^0(\overline{\Omega^i})$: The space of **continuous functions** over the closed domain $\overline{\Omega^i}$ (meaning no gaps or tears between elements; standard $C^0$ continuity used in Lagrangian finite elements).
* $\mathbf{v}_h^i\vert{}_T$: The restriction of the vector field $\mathbf{v}_h^i$ to a single element $T$ (e.g., a specific triangle in the mesh).
* $(\mathbb{P}_k(T))^d$: Polynomials of degree up to $k$ defined on element $T$, raised to the power $d$ (where $d$ is the spatial dimension, e.g., $d=2$ for 2D vectors $(u_x, u_y)$).
* $\forall T \in \mathcal{T}_h^i$: **"For all"** elements $T$ inside the mesh $\mathcal{T}_h^i$. This means the function is a piecewise polynomial element-by-element.
* $\mathbf{v}_h^i = 0 \text{ on } \Gamma_D^i$: The essential boundary condition. The trial/test functions must **vanish (equal zero)** on the Dirichlet boundary $\Gamma_D^i$ where displacements are locked.

---

### Cheat Sheet: Taxonomy of Mathematical Symbols

| Symbol / Notation | Meaning in Plain English | Example |
| --- | --- | --- |
| $\Omega$ | A spatial domain (the geometry of the body). | $\Omega \subset \mathbb{R}^2$ |
| $\partial\Omega$ or $\Gamma$ | The boundary of the domain. | $\Gamma_C$ (contact boundary), $\Gamma_D$ (Dirichlet boundary) |
| $\mathcal{T}_h$ | A triangulation or mesh of the domain parameterized by mesh size $h$. | $T \in \mathcal{T}_h$ (a single element) |
| $\mathscr{C}^k(\Omega)$ | Space of $k$-times continuously differentiable functions. | $\mathscr{C}^0$ is continuous; $\mathscr{C}^1$ has continuous first derivatives. |
| $\mathbb{P}_k(T)$ | Polynomial space of degree $k$ defined on element $T$. | $\mathbb{P}_1$ is linear; $\mathbb{P}_2$ is quadratic. |
| $(\cdot)^d$ | Cartesian product power $d$, indicating a vector-valued function of dimension $d$. | $(\mathbb{P}_k)^2$ means a 2D vector where each component is a degree-$k$ polynomial. |
| $\in$ | "Belongs to" or "is an element of". | $x \in \Omega$ |
| $\subset$ | "Is a subset of" (contained within). | $\mathbf{V}_h \subset H^1(\Omega)$ |
| $\forall$ | **"For all"** (universal quantifier). | $\forall T \in \mathcal{T}_h$ |
| $\times$ | Cartesian product (combining sets or spaces). | $\mathbf{V}_h^1 \times \mathbf{V}_h^2$ combines the spaces of both bodies into a joint system. |
| $\mid_T$ | **Restriction** of a function to a specific subdomain or element $T$. | $v\vert{}_T$ is the function evaluated strictly inside element $T$. |

!!! warning "Work in Progress"
    More symbols to be added as needed.
