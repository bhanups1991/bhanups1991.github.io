Let us revisit some key definitions and recall the symbols used. This page should be visited often and treated as a sacred space. This provides the language on which the equations in the main part are written.

---

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

---

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

### Cheat Sheet: Taxonomy of Mathematical Symbols (Work in Progress)

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