# Nonlinear Solvers & Linear Algebra — FAQ

Consolidated from prior technical discussions on Newton-type nonlinear solution procedures, time integration, and the underlying linear-algebra machinery (direct/iterative solvers, Krylov methods, PETSc SNES/KSP). FE discretization and contact-specific kinematics/enforcement are covered in their own companion FAQs; this file focuses on how the resulting nonlinear residual equation is actually driven to zero.

---

## 1. The Nonlinear Solution Procedure

**Q: What's the cleanest mental model for the nonlinear FE solution process?**
Three nested loops:

```
FOR each load/time increment  n → n+1          ← OUTER LOOP (physical steps)
  FOR each Newton–Raphson iteration  k          ← MIDDLE LOOP (nonlinear convergence)
    Solve  K_T · Δd = R                         ← INNER LOOP (linear algebra)
```

An "increment" is bookkeeping — how far you've marched in load/time; a "Newton iteration" is how many times you re-linearize and correct the solution within one increment; a "linear-solve iteration" (Krylov methods only) is how many times the *linear* solver refines its guess of $\Delta d$ within one Newton step. All three loops are logically distinct, and confusing them (e.g. calling a Krylov iteration a "Newton iteration") is a common source of miscommunication.

**Q: How is the Newton–Raphson equation derived from the nonlinear residual, and why does it converge quadratically?**
The discretized equilibrium is $\mathbf R(\mathbf d) = \mathbf f_{ext} - \mathbf f_{int}(\mathbf d) - \mathbf f_c(\mathbf d) = \mathbf 0$. Taylor-expanding about the current iterate:

$$\mathbf R(\mathbf d+\Delta\mathbf d) \approx \mathbf R(\mathbf d) + \frac{\partial\mathbf R}{\partial\mathbf d}\Delta\mathbf d$$

Setting the next residual to zero and defining $\mathbf K_T = -\partial\mathbf R/\partial\mathbf d$ gives

$$\boxed{\mathbf K_T\,\Delta\mathbf d = \mathbf R}, \qquad \mathbf d_{k+1} = \mathbf d_k + \Delta\mathbf d_k$$

If $\mathbf R$ is sufficiently smooth and its Jacobian nonsingular near the solution, $\mathbf R(\mathbf d_k) = J^*e_k + O(\|e_k\|^2)$, and Newton cancels the first-order error term exactly, leaving

$$\boxed{\|e_{k+1}\| \le C\|e_k\|^2}$$

— **quadratic** convergence, but only **locally**: far from the solution the Taylor-expansion/nonsingularity assumptions can fail, motivating line search, arc-length continuation, or adaptive stepping (below). Newton linearization does *not* replace the original nonlinear physical problem with a globally linear model — the original geometric, material, and contact nonlinearities remain fully present in $\mathbf R$ and $\mathbf K_T$ as evaluated at the current state; repeated *local* linear corrections are what solves the *original* nonlinear problem.

**Q: What's the difference between full Newton, modified Newton, generalized Newton, and quasi-Newton?**
- **Full Newton**: recompute (and refactorize) $\mathbf K_T$ every iteration → quadratic convergence, but expensive per step.
- **Modified Newton**: reuse an earlier $\mathbf K_T$ for several iterations → cheaper per step, only linear convergence, more iterations needed overall.
- **Quasi-Newton** (e.g. BFGS): update an approximation to $\mathbf K_T$ or $\mathbf K_T^{-1}$ from secant information gathered across iterations, avoiding repeated reassembly/refactorization while still improving on modified-Newton's convergence rate.
- **Generalized Newton**: variants suited to specialized or non-smooth operators (e.g. semismooth Newton for friction's non-smooth stick–slip operator).

The trade-off throughout is tangent-construction/factorization cost per iteration vs. the number of iterations needed.

**Q: What happens when Newton doesn't converge?**
- **Adaptive stepping**: shrink the load/time increment $\Delta\lambda$ or $\Delta t$ and retry.
- **Line search**: scale the Newton correction, $\mathbf d^{k+1} = \mathbf d^k + \alpha\,\Delta\mathbf d_N$, $0<\alpha\le1$, choosing $\alpha$ via a merit function such as $\Phi(\mathbf d) = \tfrac12\|\mathbf R(\mathbf d)\|^2$ rather than automatically taking the full step. The *direction* remains Newton's; only its magnitude is reduced when the full step would overshoot.
- **Arc-length/continuation**: needed past limit points (snap-through/snap-back), where ordinary load control fails because the load parameter stops being a monotonic continuation variable.
- **Stabilization/regularization**: numerical damping, viscous regularization, contact stabilization — distinct from *physical* damping, used purely to help the iteration converge.

**Q: How does load stepping parameterize a nonlinear equilibrium path?**
Write $\mathbf f_{ext} = \lambda\mathbf f_0$ for a fixed reference load $\mathbf f_0$ and scalar load factor $\lambda$, so equilibrium reads

$$\boxed{\mathbf R(\mathbf d,\lambda) = \lambda\mathbf f_0 - \mathbf f_{int}(\mathbf d) - \mathbf f_c(\mathbf d) = \mathbf 0}$$

Increasing $\lambda$ gradually turns one hard nonlinear problem into a sequence of nearby equilibrium problems, each easier for Newton to solve starting from the previous converged state. Adaptive step reduction (shrinking $\Delta\lambda$) is standard when convergence deteriorates.

**Q: Why can load control fail at a limit point, and how does arc-length continuation help?**
At a turning point (snap-through), the load–displacement curve becomes locally vertical or reverses — $\lambda$ ceases to be a valid monotonic continuation parameter, so no increase in $\lambda$ corresponds to the next equilibrium state (there may be zero or two solutions at nearby $\lambda$). Arc-length methods introduce an additional constraint coupling displacement and load increments, e.g.

$$\boxed{\|\Delta\mathbf d\|^2 + \alpha^2(\Delta\lambda)^2 = \Delta s^2}$$

so displacement and load are solved for **simultaneously**, letting the numerical path follow the true equilibrium path through — and past — turning points that ordinary load-controlled Newton cannot traverse.

**Q: How should convergence of a nonlinear FE solve actually be assessed?**
Multiple criteria should be checked together — a residual (force-equilibrium) criterion, a solution-increment (displacement) criterion, and sometimes an energy/work criterion — since relying on just one can give a false positive. Representative forms:

$$\frac{\|\mathbf R_k\|}{\max(\|\mathbf R_0\|, R_{\text{ref}})} < \varepsilon_R, \qquad \frac{\|\Delta\mathbf d_k\|}{\max(\|\mathbf d_k\|, d_{\text{ref}})} < \varepsilon_d$$

Using several independent measures reduces the risk of declaring convergence from one misleading numerical indicator (e.g. a small residual that's small only because the increment happens to be small too, or vice versa).

**Q: Why is adaptive load/time stepping useful beyond just "convergence failed → shrink the step"?**
It matches increment size to local problem difficulty: small increments where the response is stiffness-changing rapidly (contact activation, yielding, near an instability), larger increments where the response is smooth — improving robustness without paying the cost of small steps everywhere.

---

## 2. Implicit vs. Explicit Time Integration

**Q: What's the core difference between implicit and explicit dynamics?**
Both solve $\mathbf M\ddot{\mathbf d} + \mathbf C\dot{\mathbf d} + \mathbf f_{int}(\mathbf d) = \mathbf f_{ext}(t)$. **Explicit** computes $\mathbf d_{n+1}$ directly from known quantities at $t_n$ (central difference), needing only a diagonal/lumped-mass solve and no $\mathbf K_T$ or global Newton loop:

$$\boxed{\mathbf d_{n+1} = 2\mathbf d_n - \mathbf d_{n-1} + \Delta t^2\mathbf M^{-1}(\mathbf f_{ext,n} - \mathbf f_{int,n})}$$

**Implicit** enforces equilibrium at the unknown $t_{n+1}$, requiring a full Newton loop and linear solves per step (Newmark, HHT-$\alpha$, generalized-$\alpha$). There is therefore no *global* nonlinear equilibrium solve at each explicit step, though local constitutive integration (e.g. return mapping in plasticity) may itself be iterative.

**Q: Why is explicit's $\Delta t$ so restrictive?**
The CFL/stability condition

$$\boxed{\Delta t_{\text{crit}} \approx \frac{2}{\omega_{\max}} \sim \frac{L_{\min}}{c}}$$

(wave speed $c$ divided by smallest element dimension $L_{\min}$, equivalently the highest natural frequency $\omega_{\max}$ of the discrete system) is governed by the stiffest, smallest element in the *entire* mesh, regardless of the physics of interest elsewhere. Violating it makes the numerical amplification factor exceed 1, and any small numerical error blows up exponentially step-to-step. Mesh refinement reduces $L_{\min}$, raises $\omega_{\max}$, and therefore *reduces* the stable explicit time step — a direct coupling between spatial and temporal resolution that implicit schemes don't have.

**Q: Why can implicit integration use a large $\Delta t$?**
Because the update solves for the state *at* $t_{n+1}$ self-consistently (equilibrium enforced there, not extrapolated from the past), schemes like Newmark average-acceleration ($\gamma=1/2$, $\beta=1/4$) have amplification factor $|A|\le1$ for **every** frequency and **every** $\Delta t$ — unconditional stability. This comes from built-in algorithmic/numerical damping of high-frequency content, not from resolving it accurately. Caveat: unconditional stability $\neq$ accuracy — an overly large $\Delta t$ still gives a stable but inaccurate or oscillatory answer, and can itself degrade Newton convergence within the step.

**Q: What is the effective tangent used in implicit dynamics?**
Starting from $\mathbf M\ddot{\mathbf d} + \mathbf C\dot{\mathbf d} + \mathbf f_{int}(\mathbf d) = \mathbf f_{ext}$, time discretization relates acceleration and velocity increments linearly to the displacement increment, $\Delta\ddot{\mathbf d} = a_0\Delta\mathbf d$, $\Delta\dot{\mathbf d} = a_1\Delta\mathbf d$ (coefficients $a_0,a_1$ set by the chosen integration scheme), giving

$$\boxed{\mathbf K_{\text{eff}} = \mathbf K_T + a_1\mathbf C + a_0\mathbf M}$$

Newton is then applied to this effective tangent instead of $\mathbf K_T$ alone.

**Q: When should you use explicit vs. implicit integration?**
- **Explicit**: short-duration, highly nonlinear, high-rate events (impact, crash, blast, forming) — no risk of Newton non-convergence, and naturally handles severe contact/plasticity without needing a converged global tangent.
- **Implicit**: quasi-static problems, low-to-moderate-rate dynamics, and long-duration/low-frequency response (statics, modal analysis, slow forming) — where the $\Delta t$ savings from unconditional stability outweigh the per-step cost of Newton iteration and factorization.

---

## 3. Direct and Iterative Linear Solvers

**Q: Why does nonlinear FE reduce to a sequence of linear algebra problems, and why solve $\mathbf K\Delta\mathbf d=\mathbf R$ rather than explicitly form $\mathbf K^{-1}$?**
Newton linearization turns $\mathbf R(\mathbf d)=0$ into a sequence of linear systems $\mathbf K_T\Delta\mathbf d = \mathbf R$ (one per Newton iteration); the nonlinear algorithm updates state and tangent, the linear solver computes the correction. Explicitly forming $\mathbf K^{-1}$ is unnecessary, more expensive, less numerically stable, and destroys the matrix's sparse structure (the inverse of a sparse matrix is generally dense). Direct factorization or an iterative method computes the required correction vector directly, without ever constructing the inverse — production FE codes implement linear *solves*, never explicit matrix inversion.

**Q: How do direct and iterative linear solvers differ, and when is each more efficient?**
**Direct** methods factorize the sparse matrix — $\mathbf K = \mathbf{LU}$ (unsymmetric) or $\mathbf{LDL}^T$/Cholesky (symmetric/SPD) — then solve via forward/back substitution. Cost scales roughly $O(N^{1.5\text{–}2})$ in 3D due to fill-in, and memory grows faster than linear; but direct methods always converge to the (numerically) exact answer and are robust for ill-conditioned systems (contact, near-incompressibility, mixed shell/solid models). **Iterative** (Krylov) methods generate successive approximations via matrix-vector products, with cost per iteration that's much lower and scales better for very large sparse systems — but can stagnate on ill-conditioned systems without an effective preconditioner. This is why direct solvers remain the default for nonlinear/contact analysis in most production codes even though they scale worse asymptotically: robustness under changing, sometimes-indefinite tangents matters more than raw per-solve cost for most practical problem sizes.

**Q: What is the Krylov-subspace formulation behind GMRES, and how does it differ from CG?**
For $A\mathbf x = \mathbf b$ with initial residual $\mathbf r_0$, the Krylov subspace is

$$\boxed{\mathcal K_m = \operatorname{span}\{\mathbf r_0, A\mathbf r_0, \ldots, A^{m-1}\mathbf r_0\}}$$

**GMRES** chooses $\mathbf x_m \in \mathbf x_0 + \mathcal K_m$ to minimize $\|\mathbf b - A\mathbf x_m\|_2$ over that subspace, and — unlike CG — requires neither symmetry nor positive-definiteness of $A$, making it the standard choice for general (e.g. unsymmetric, or symmetric-indefinite from contact/mixed formulations) FE tangent systems. **CG (Conjugate Gradient)** is restricted to symmetric positive-definite $A$, where it minimizes the $A$-norm of the error over the same style of Krylov subspace at lower memory/compute cost per iteration than GMRES (GMRES's cost per iteration grows with $m$ unless restarted, since it must store/orthogonalize against the whole growing basis; CG uses short recurrences and constant per-iteration cost).

**Q: Why is preconditioning central to iterative FE solvers?**
A preconditioner $M^{-1}$ transforms the system to $M^{-1}A\mathbf x = M^{-1}\mathbf b$ (or a symmetric variant), with the objective of giving the transformed system a more favorable spectrum or field of values for the Krylov method — clustering eigenvalues, reducing the condition number. Critically, $M^{-1}$ need **not** approximate $A^{-1}$ accurately; it only needs to make the transformed system easier to solve. For large sparse FE systems, the choice and quality of preconditioner is often the single largest factor determining whether an iterative solver is practical at all.

**Q: How do the Abaqus and MSC Nastran solvers compare architecturally?**
Abaqus was designed nonlinear-first, with Standard (implicit) / Explicit as its core split from inception. Nastran was designed linear-first (aerospace certification analysis: linear statics, modal, frequency response), with nonlinear capability (SOL 400) added later as an extension. Both default to **sparse multifrontal direct solvers** (LU for unsymmetric, LDL$^T$/Cholesky for symmetric/SPD). Nastran's implementation is tuned for low-memory, out-of-core operation — a legacy of memory-constrained hardware, and still strong for huge linear/modal models. Abaqus's is tuned for nonlinear/contact robustness — reliable refactorization every Newton iteration even as $\mathbf K_T$'s definiteness changes (e.g. through buckling or contact status changes). For iterative solvers, both are Krylov-based with preconditioning but differ in choice: Abaqus commonly uses incomplete-LU (ILU) preconditioning (for symmetric systems, single load case, statics/quasi-static only, with no guaranteed convergence), while Nastran uses Block Incomplete Cholesky (BIC) preconditioning with PCG.

---

## 4. PETSc: SNES, KSP, and the Solver Hierarchy

**Q: What is the relationship between PETSc's SNES and KSP?**
**SNES** (Scalable Nonlinear Equations Solver) solves the nonlinear problem $\mathbf R(\mathbf d) = 0$. Its Newton-type methods produce a linearized system $\mathbf J_R\,\Delta\mathbf d = -\mathbf R$ at each nonlinear iteration; **KSP** (Krylov Subspace solver) then solves that linear system. The hierarchy is

$$\boxed{\text{SNES} \to \text{nonlinear iteration} \to \text{Jacobian} \to \text{KSP} \to \text{linear solve}}$$

SNES and a Krylov method like GMRES therefore operate at strictly different levels: SNES controls the *outer* nonlinear iteration (convergence criteria, globalization, line search), KSP (with a chosen method — GMRES, CG, etc. — and preconditioner) solves each resulting *linear* system. This mirrors the "three nested loops" picture at the top of this file: SNES = middle loop, KSP = inner loop.
