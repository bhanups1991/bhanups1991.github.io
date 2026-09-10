# Equation and Derivation Reference

!!! warning "Under Construction"
    This section is currently being updated.

Color convention: <span style="color:#1565C0">blue</span> = kinematics/geometric quantities; <span style="color:#2E7D32">green</span> = stress/constitutive quantities; <span style="color:#C62828">red</span> = residual/contact quantities; <span style="color:#6A1B9A">purple</span> = FE/solver quantities.

## Section 1 — Continuum Mechanics

**Q1:** Derive the deformation gradient starting from the motion and displacement mappings.

The motion is

$$
\mathbf{x}=\boldsymbol{\chi}(\mathbf{X},t)=\mathbf{X}+\mathbf{u}.
\tag{1}
$$

Therefore,

$$
\boxed{\textcolor{#1565C0}{\mathbf F}=\frac{\partial\mathbf x}{\partial\mathbf X}=\mathbf I+\frac{\partial\mathbf u}{\partial\mathbf X}}
\tag{2}
$$

The deformation gradient is therefore the local reference-to-current configuration map.

**Reference:** Bonet, Gil & Wood, Chapter 4, Sections 4.2–4.4; Holzapfel, Chapter 2, Section 2.4; Bathe, Nonlinear Analysis Lecture 3.

---

**Q2:** Derive the Green–Lagrange strain starting from the deformation gradient.

A material line element transforms as

$$
d\mathbf x=\mathbf F\,d\mathbf X.
$$

Hence,

$$
d\mathbf x\cdot d\mathbf x=d\mathbf X\cdot\mathbf F^T\mathbf F\,d\mathbf X.
$$

Defining

$$
\mathbf C=\mathbf F^T\mathbf F,
$$

the change in squared length gives

$$
\boxed{\textcolor{#1565C0}{\mathbf E=\frac12(\mathbf C-\mathbf I)=\frac12(\mathbf F^T\mathbf F-\mathbf I)}}
\tag{3}
$$

**Reference:** Bonet et al., Chapter 4, Section 4.5; Bathe, Nonlinear Analysis Lecture 3.

---

**Q3:** Expand the Green–Lagrange strain in terms of the displacement gradient.

Using

$$
\mathbf F=\mathbf I+\mathbf H,
\qquad
\mathbf H=\operatorname{Grad}\mathbf u,
$$

in Equation (3),

$$
\boxed{\textcolor{#1565C0}{\mathbf E=\frac12(\mathbf H+\mathbf H^T+\mathbf H^T\mathbf H)}}
\tag{4}
$$

The first two terms are linear; \(\mathbf H^T\mathbf H\) is the geometric nonlinear contribution.

---

**Q4:** Derive infinitesimal strain as the small-deformation limit of Green–Lagrange strain.

From Equation (4),

$$
\mathbf E=\frac12(\mathbf H+\mathbf H^T+\mathbf H^T\mathbf H).
$$

For \(\|\mathbf H\|\ll1\), neglect \(\mathbf H^T\mathbf H\):

$$
\boxed{\boldsymbol\varepsilon
=\frac12(\nabla\mathbf u+\nabla\mathbf u^T)}
\tag{5}
$$

Thus infinitesimal strain is the linearized form of the finite-strain measure.

**Reference:** Bonet et al., Chapter 4, Section 4.10.

---

**Q5:** Derive the polar decomposition of the deformation gradient.

Define

$$
\mathbf C=\mathbf F^T\mathbf F,
\qquad
\mathbf U=\sqrt{\mathbf C}.
$$

Then

$$
\boxed{\textcolor{#1565C0}{\mathbf F=\mathbf R\mathbf U=\mathbf V\mathbf R}}
\tag{6}
$$

where \(\mathbf R\) is a proper orthogonal rotation and \(\mathbf U,\mathbf V\) are the right and left stretch tensors.

**Reference:** Bonet et al., Chapter 4, Section 4.6; Holzapfel, Chapter 2, Section 2.6; Bathe, Nonlinear Analysis Lecture 3.

---

**Q6:** Derive the volume-change relation from the deformation gradient.

The differential volume transforms as

$$
\boxed{dv=J\,dV,\qquad J=\det\mathbf F}
\tag{7}
$$

so

$$
\boxed{\frac{dv}{dV}=\det\mathbf F}.
\tag{8}
$$

Thus \(J\) measures the local volume ratio.

**Reference:** Bonet et al., Chapter 4, Section 4.7.

---

**Q7:** Derive the velocity gradient from the deformation gradient.

Starting from

$$
\mathbf F=\frac{\partial\mathbf x}{\partial\mathbf X},
$$

differentiate with respect to time:

$$
\dot{\mathbf F}
=
\frac{\partial\mathbf v}{\partial\mathbf X}
=
\frac{\partial\mathbf v}{\partial\mathbf x}
\frac{\partial\mathbf x}{\partial\mathbf X}.
$$

Therefore,

$$
\boxed{\textcolor{#1565C0}{\mathbf L=\frac{\partial\mathbf v}{\partial\mathbf x}
=\dot{\mathbf F}\mathbf F^{-1}}}
\tag{9}
$$

**Reference:** Bonet et al., Chapter 4, Sections 4.11–4.12.

---

**Q8:** Derive the rate-of-deformation tensor and spin tensor from the velocity gradient.

Directly decompose

$$
\boxed{\mathbf L=\mathbf D+\mathbf W}
\tag{10}
$$

with

$$
\boxed{\mathbf D=\frac12(\mathbf L+\mathbf L^T)},
\qquad
\boxed{\mathbf W=\frac12(\mathbf L-\mathbf L^T)}.
\tag{11}
$$

Thus \(\mathbf D\) contains deformation rates and \(\mathbf W\) contains local spin.

**Reference:** Bonet et al., Chapter 4, Sections 4.12–4.13; Holzapfel, Chapter 2, Section 2.7.

---

**Q9:** Derive the material derivative in an Eulerian description.

For \(f(\mathbf x,t)\),

$$
\boxed{\frac{Df}{Dt}
=
\frac{\partial f}{\partial t}
+
\mathbf v\cdot\nabla f}
\tag{12}
$$

The first term is local temporal change; the second is the convective contribution due to material transport.

**Reference:** Bonet et al., Chapter 4, Section 4.11.

---

**Q10:** Derive the pure-bending strain field and show why transverse shear vanishes.

Take

$$
u_x=-\kappa xy,
\qquad
u_y=\frac12\kappa x^2.
\tag{13}
$$

Then

$$
\varepsilon_x=\frac{\partial u_x}{\partial x}=-\kappa y,
\qquad
\varepsilon_y=0,
$$

while

$$
\boxed{\gamma_{xy}
=
\frac{\partial u_x}{\partial y}
+
\frac{\partial u_y}{\partial x}
=
-\kappa x+\kappa x=0}.
\tag{14}
$$

This exact cancellation is the condition that a bending element must reproduce.

**Reference:** Bathe, Nonlinear Analysis Lecture 20, discussion of shear and membrane locking.

---

**Q11:** Derive the spurious shear strain produced by a bilinear Q4 element in pure bending.

For \(u_y=\kappa x^2/2\), a Q4 element whose nodes have \(x=\pm a\) has identical nodal \(u_y\) values:

$$
u_y=\frac{\kappa a^2}{2}.
$$

Therefore the bilinear interpolation gives

$$
\frac{\partial u_y^h}{\partial x}=0.
$$

Meanwhile \(u_x=-\kappa xy\) gives

$$
\frac{\partial u_x^h}{\partial y}=-\kappa x.
$$

Hence

$$
\boxed{\gamma_{xy}^h=-\kappa x\neq0}.
\tag{15}
$$

The FE space cannot reproduce the exact zero-shear bending field, creating artificial shear energy and locking.

**Reference:** Bathe, Nonlinear Analysis Lecture 20.

---

## Section 2 — FEM and Nonlinear Linearization

**Q12:** Derive the weak form starting from the strong equilibrium equation.

Starting from

$$
-\nabla\cdot\boldsymbol\sigma=\mathbf b,
$$

multiply by \(\delta\mathbf u\) and integrate by parts:

$$
\int_\Omega\boldsymbol\sigma:\nabla\delta\mathbf u\,dV
=
\int_\Omega\mathbf b\cdot\delta\mathbf u\,dV
+
\int_{\Gamma_t}\mathbf t\cdot\delta\mathbf u\,dS.
$$

Hence,

$$
\boxed{\delta W_{\mathrm{int}}-\delta W_{\mathrm{ext}}=0}.
\tag{16}
$$

**Reference:** Bathe, Linear Analysis Lecture 2; Wriggers, Chapter 4, pp. 31–56.

---

**Q13:** Derive the finite-deformation virtual-work equation using \(\mathbf S\) and \(\mathbf E\).

For a total Lagrangian formulation,

$$
\boxed{
\delta W_{\mathrm{int}}
=
\int_{\Omega_0}\textcolor{#2E7D32}{\mathbf S}:\delta\textcolor{#1565C0}{\mathbf E}\,dV_0
}
\tag{17}
$$

and equilibrium requires

$$
\boxed{\delta W_{\mathrm{int}}-\delta W_{\mathrm{ext}}=0}.
\tag{18}
$$

The important point is that \(\mathbf S\) and \(\mathbf E\) form a work-conjugate pair.

**Reference:** Bathe, Nonlinear Analysis Lecture 3.

---

**Q14:** Derive the isoparametric Jacobian and the parent-to-physical coordinate transformation.

With

$$
\mathbf x(\boldsymbol\xi)=\sum_aN_a(\boldsymbol\xi)\mathbf x_a,
$$

the Jacobian is

$$
\boxed{\textcolor{#6A1B9A}{\mathbf J=\frac{\partial\mathbf x}{\partial\boldsymbol\xi}}}.
\tag{19}
$$

Therefore,

$$
\boxed{dV=\det\mathbf J\,dV_\xi}.
\tag{20}
$$

The physical derivatives follow from

$$
\nabla_xN_a=\mathbf J^{-T}\nabla_\xi N_a.
\tag{21}
$$

**Reference:** Bathe, Linear Analysis Lecture 6, isoparametric formulation and Jacobian transformation.

---

**Q15:** Derive the relation between parent, reference, and current configurations.

Define

$$
\mathbf J_0=\frac{\partial\mathbf X}{\partial\boldsymbol\xi},
\qquad
\mathbf J_t=\frac{\partial\mathbf x}{\partial\boldsymbol\xi}.
$$

Using the chain rule,

$$
\mathbf J_t
=
\frac{\partial\mathbf x}{\partial\mathbf X}
\frac{\partial\mathbf X}{\partial\boldsymbol\xi}
=
\mathbf F\mathbf J_0.
$$

Therefore,

$$
\boxed{\mathbf F=\mathbf J_t\mathbf J_0^{-1}}.
\tag{22}
$$

This separates the computational parent-coordinate mapping from the physical deformation mapping.

---

**Q16:** Derive the FE internal force vector from the virtual-work equation.

Using

$$
\delta\mathbf E=\mathbf B\,\delta\mathbf d,
$$

insert into Equation (17):

$$
\delta W_{\mathrm{int}}
=
\delta\mathbf d^T
\int_{\Omega_0}\mathbf B^T\mathbf S\,dV_0.
$$

Hence,

$$
\boxed{\textcolor{#6A1B9A}{\mathbf f_{\mathrm{int}}
=
\int_{\Omega_0}\mathbf B^T\mathbf S\,dV_0}}.
\tag{23}
$$

For small-strain linear elasticity this reduces to

$$
\boxed{\mathbf K=\int_\Omega\mathbf B^T\mathbf C\mathbf B\,dV}.
\tag{24}
$$

**Reference:** Bathe, Linear Analysis Lecture 3 and Nonlinear Analysis Lecture 6.

---

**Q17:** Derive the nonlinear residual including contact.

Equilibrium requires

$$
\mathbf f_{\mathrm{int}}+\mathbf f_c=\mathbf f_{\mathrm{ext}}.
$$

Therefore,

$$
\boxed{
\textcolor{#C62828}{\mathbf R(\mathbf d)}
=
\mathbf f_{\mathrm{ext}}
-
\mathbf f_{\mathrm{int}}(\mathbf d)
-
\mathbf f_c(\mathbf d)
=
\mathbf0
}.
\tag{25}
$$

Material, geometric, and contact nonlinearities enter through the dependence of these terms on \(\mathbf d\).

---

**Q18:** Derive the Newton–Raphson equation by linearizing the nonlinear residual.

Expand

$$
\mathbf R(\mathbf d+\Delta\mathbf d)
\approx
\mathbf R(\mathbf d)
+
\frac{\partial\mathbf R}{\partial\mathbf d}\Delta\mathbf d.
$$

Setting the new residual to zero,

$$
\frac{\partial\mathbf R}{\partial\mathbf d}\Delta\mathbf d
=
-\mathbf R.
$$

Since

$$
\mathbf K_T
=
-\frac{\partial\mathbf R}{\partial\mathbf d},
$$

we obtain

$$
\boxed{\textcolor{#6A1B9A}{\mathbf K_T\Delta\mathbf d=\mathbf R}}.
\tag{26}
$$

Then

$$
\boxed{\mathbf d_{i+1}=\mathbf d_i+\Delta\mathbf d_i}.
\tag{27}
$$

**Reference:** Bathe, Nonlinear Analysis Lecture 10.

---

**Q19:** Derive the material and geometric tangent stiffness from the nonlinear virtual work.

Starting from

$$
\delta W_{\mathrm{int}}
=
\int_{\Omega_0}\mathbf S:\delta\mathbf E\,dV_0,
$$

linearization gives

$$
\Delta(\delta W_{\mathrm{int}})
=
\int_{\Omega_0}
\Delta\mathbf S:\delta\mathbf E\,dV_0
+
\int_{\Omega_0}
\mathbf S:\Delta(\delta\mathbf E)\,dV_0.
\tag{28}
$$

Using

$$
\Delta\mathbf S=\mathbf C:\Delta\mathbf E,
$$

the first term gives the material tangent and the second gives the geometric tangent:

$$
\boxed{\mathbf K_T=\mathbf K_M+\mathbf K_G}.
\tag{29}
$$

The key distinction is therefore constitutive linearization versus geometric linearization.

**Reference:** Bonet et al., Chapter 8; Bathe, Nonlinear Analysis Lectures 6 and 10.

---

**Q20:** Derive the effective tangent for an implicit dynamic FE step.

The semi-discrete equation is

$$
\mathbf M\ddot{\mathbf d}
+
\mathbf C\dot{\mathbf d}
+
\mathbf f_{\mathrm{int}}(\mathbf d)
=
\mathbf f_{\mathrm{ext}}.
\tag{30}
$$

After time discretization,

$$
\Delta\ddot{\mathbf d}=a_0\Delta\mathbf d,
\qquad
\Delta\dot{\mathbf d}=a_1\Delta\mathbf d.
$$

Therefore,

$$
\boxed{\mathbf K_{\mathrm{eff}}
=
\mathbf K_T+a_1\mathbf C+a_0\mathbf M}.
\tag{31}
$$

The coefficients depend on the selected implicit time-integration scheme.

**Reference:** Bathe, Linear Analysis Lecture 10 and Nonlinear Dynamic Response Lectures 13–14.

---

**Q21:** Derive the explicit central-difference displacement update.

Starting from

$$
\mathbf M\ddot{\mathbf d}_n=\mathbf R_n,
$$

use

$$
\ddot{\mathbf d}_n
\approx
\frac{\mathbf d_{n+1}-2\mathbf d_n+\mathbf d_{n-1}}{\Delta t^2}.
$$

Thus,

$$
\boxed{
\mathbf d_{n+1}
=
2\mathbf d_n-\mathbf d_{n-1}
+
\Delta t^2\mathbf M^{-1}\mathbf R_n
}.
\tag{32}
$$

No global Newton equilibrium iteration is required.

**Reference:** Bathe, Linear Analysis Lecture 10.

---

**Q22:** Derive the explicit critical time-step estimate from the highest natural frequency.

For the undamped system,

$$
\mathbf M\ddot{\mathbf d}+\mathbf K\mathbf d=0,
$$

central-difference stability requires approximately

$$
\boxed{\Delta t_{\mathrm{crit}}\approx\frac{2}{\omega_{\max}}}.
\tag{33}
$$

Using the smallest element length and characteristic wave speed gives the engineering estimate

$$
\boxed{\Delta t_{\mathrm{crit}}\sim\frac{L_{\min}}{c}}.
\tag{34}
$$

**Reference:** Bathe, Linear Analysis Lecture 10.

---

## Section 3 — Contact Mechanics

**Q23:** Derive the normal gap using closest-point projection.

Let \(\mathbf x_m(\boldsymbol\xi)\) be the master surface. The closest point minimizes

$$
d^2(\boldsymbol\xi)
=
\|\mathbf x_s-\mathbf x_m(\boldsymbol\xi)\|^2.
$$

Hence,

$$
(\mathbf x_s-\mathbf x_m)\cdot\mathbf x_{m,\alpha}=0.
\tag{35}
$$

The connecting vector is normal to the surface:

$$
\mathbf x_s-\mathbf x_m=g_n\mathbf n.
$$

Therefore,

$$
\boxed{\textcolor{#C62828}{g_n=(\mathbf x_s-\mathbf x_m)\cdot\mathbf n}}.
\tag{36}
$$

**Reference:** Wriggers, Chapter 5, “Contact Kinematics”, pp. 57–67.

---

**Q24:** Derive the unilateral contact complementarity conditions.

Nonpenetration requires

$$
g_n\ge0.
$$

The compressive normal reaction satisfies

$$
\lambda_n\ge0.
$$

Reaction exists only when contact is active:

$$
g_n\lambda_n=0.
$$

Thus,

$$
\boxed{
g_n\ge0,\qquad
\lambda_n\ge0,\qquad
g_n\lambda_n=0
}.
\tag{37}
$$

**Reference:** Wriggers, Chapter 7, pp. 109–156.

---

**Q25:** Derive the penalty contact law from a penalty potential.

Introduce

$$
\Pi_c=\frac12\epsilon\langle-g_n\rangle_+^2.
$$

Differentiation gives

$$
\boxed{\lambda_n=\epsilon\langle-g_n\rangle_+}.
\tag{38}
$$

For active contact,

$$
\boxed{-g_n=\frac{\lambda_n}{\epsilon}}.
\tag{39}
$$

Thus increasing \(\epsilon\) reduces penetration but increases the contact stiffness scale.

**Reference:** Wriggers, Chapters 7 and 9.

---

**Q26:** Derive the local penalty contact tangent.

For active contact,

$$
\lambda_n=-\epsilon g_n.
$$

Therefore,

$$
\boxed{k_c=\frac{\partial\lambda_n}{\partial g_n}=-\epsilon}.
\tag{40}
$$

The sign depends on the residual/gap convention; the important point is that the tangent magnitude scales with the penalty parameter.

---

**Q27:** Derive the Lagrange-multiplier contact constraint from the weak form.

Introduce \(\lambda_n\) as the multiplier for

$$
g_n=0.
$$

The contact contribution is

$$
\delta W_c
=
\int_{\Gamma_c}\lambda_n\,\delta g_n\,dA.
$$

Variation with respect to \(\lambda_n\) gives

$$
\int_{\Gamma_c}g_n\,\delta\lambda_n\,dA=0.
$$

Since \(\delta\lambda_n\) is arbitrary,

$$
\boxed{g_n=0}.
\tag{41}
$$

Thus the constraint is exact, but \(\lambda_n\) becomes an additional unknown.

**Reference:** Wriggers, Chapter 7; Chapter 9 for FE discretization.

---

**Q28:** Derive the augmented-Lagrangian contact relation.

The augmented formulation combines multiplier and penalty contributions:

$$
\boxed{
\lambda_n^{k+1}
=
\lambda_n^k
+
\epsilon\langle-g_n\rangle_+
}.
\tag{42}
$$

The multiplier carries the contact reaction while the penalty term controls constraint violation during iteration.

**Reference:** Wriggers, Chapters 7 and 11; Pietrzak & Curnier, 1999, for large-deformation frictional contact and augmented-Lagrangian treatment.

---

**Q29:** Derive the local contact operator and its tangent.

At a contact quadrature point,

$$
\boxed{\textcolor{#C62828}{\mathbf t_c=\mathcal C(\mathbf g)}}.
\tag{43}
$$

Linearization gives

$$
\boxed{
\Delta\mathbf t_c
=
\mathbf K_c^{\mathrm{loc}}\Delta\mathbf g,
\qquad
\mathbf K_c^{\mathrm{loc}}
=
\frac{\partial\mathcal C}{\partial\mathbf g}
}.
\tag{44}
$$

This local operator is the fundamental object used to construct a consistent contact tangent.

**Reference:** Alart & Curnier (1991), mixed penalty-duality formulation and conewise-linear contact operator.

---

**Q30:** Derive the local-to-global contact stiffness relation.

Relate the gap increment to nodal displacement:

$$
\Delta\mathbf g=\mathbf G\Delta\mathbf d.
$$

Then

$$
\Delta\mathbf t_c
=
\mathbf K_c^{\mathrm{loc}}\mathbf G\Delta\mathbf d.
$$

The corresponding global contribution has the form

$$
\boxed{
\mathbf K_c
=
\int_{\Gamma_c}
\mathbf G^T
\mathbf K_c^{\mathrm{loc}}
\mathbf G\,d\Gamma
}.
\tag{45}
$$

Thus

$$
\boxed{
\text{contact operator}
\rightarrow
\text{local tangent}
\rightarrow
\text{global contact tangent}
}.
$$

**Reference:** Wriggers, Chapters 7, 10 and 11; Alart & Curnier (1991).

---

**Q31:** Derive the Coulomb friction condition from normal reaction and tangential traction.

The admissible tangential traction satisfies

$$
\boxed{\|\mathbf t_t\|\le\mu\lambda_n}.
\tag{46}
$$

Define

$$
\phi_f=\|\mathbf t_t\|-\mu\lambda_n.
$$

Then

$$
\phi_f<0:\text{ stick},
\qquad
\phi_f=0:\text{ slip}.
\tag{47}
$$

**Reference:** Wriggers, Chapter 6, pp. 69–108; Alart & Curnier (1991).

---

**Q32:** Derive the closest-point projection condition from minimization of the distance.

Starting with

$$
d^2(\boldsymbol\xi)
=
\|\mathbf x_s-\mathbf x_m(\boldsymbol\xi)\|^2,
$$

differentiate:

$$
\frac{\partial d^2}{\partial\xi_\alpha}
=
-2(\mathbf x_s-\mathbf x_m)\cdot\mathbf x_{m,\alpha}.
$$

At the minimum,

$$
\boxed{
(\mathbf x_s-\mathbf x_m)\cdot\mathbf x_{m,\alpha}=0
}.
\tag{48}
$$

For nonlinear surface interpolation this becomes a nonlinear system for \(\boldsymbol\xi\).

**Reference:** Wriggers, Chapter 5; Konyukhov & Schweizerhof, Chapter 4, “Closest Point Projection Procedure”.

---

**Q33:** Derive the distinction between contact mapping and contact enforcement.

Geometric mapping determines the opposing point:

$$
\mathbf x_s\rightarrow\mathbf x_m(\boldsymbol\xi)
\rightarrow g_n.
$$

Constraint enforcement then maps the gap to a reaction:

$$
g_n\rightarrow\lambda_n
$$

through penalty, Lagrange multiplier, augmented Lagrangian, Nitsche, or another formulation.

Hence,

$$
\boxed{
\text{mapping}
\neq
\text{enforcement}
}.
\tag{49}
$$

Closest-point projection and ray tracing belong to the first stage; Nitsche and penalty belong to the second.

**Reference:** Wriggers, Chapters 5–7; Konyukhov & Schweizerhof, Chapters 4–7.

---

**Q34:** Derive the basic structure of a Nitsche boundary term.

For a constraint \(u=g\), the Nitsche formulation adds consistency, symmetry, and stabilization terms schematically as

$$
\boxed{
-\langle\sigma(u)n,v\rangle_\Gamma
-\langle\sigma(v)n,u-g\rangle_\Gamma
+\left\langle\frac{\gamma}{h}(u-g),v\right\rangle_\Gamma
}.
\tag{50}
$$

The first two terms provide consistency/symmetry; the last provides stabilization.

For contact, \(u-g\) is replaced by the appropriate unilateral contact residual.

**Reference:** Chouly, Mlika & Renard (2018), *Numerische Mathematik* 139, 593–631; Wriggers, Chapter 7.

---

## Section 4 — Linear Algebra and Nonlinear Solvers

**Q35:** Derive the global linear system solved at every Newton iteration.

Starting from

$$
\mathbf R(\mathbf d)=\mathbf0,
$$

linearization gives

$$
\mathbf R+\frac{\partial\mathbf R}{\partial\mathbf d}\Delta\mathbf d=0.
$$

Since

$$
\mathbf K_T=-\frac{\partial\mathbf R}{\partial\mathbf d},
$$

we obtain

$$
\boxed{\textcolor{#6A1B9A}{\mathbf K_T\Delta\mathbf d=\mathbf R}}.
\tag{51}
$$

Thus Newton converts the nonlinear FE problem into a sequence of linear algebra problems.

**Reference:** Bathe, Nonlinear Analysis Lecture 10.

---

**Q36:** Derive why the tangent is a Jacobian rather than an explicitly inverted stiffness matrix.

From

$$
\mathbf R=\mathbf f_{\mathrm{ext}}-\mathbf f_{\mathrm{int}},
$$

we obtain

$$
\frac{\partial\mathbf R}{\partial\mathbf d}
=
-\frac{\partial\mathbf f_{\mathrm{int}}}{\partial\mathbf d}.
$$

Therefore,

$$
\boxed{
\mathbf K_T
=
\frac{\partial\mathbf f_{\mathrm{int}}}{\partial\mathbf d}
=
-\frac{\partial\mathbf R}{\partial\mathbf d}
}.
\tag{52}
$$

The solver computes \(\Delta\mathbf d\) from

$$
\mathbf K_T\Delta\mathbf d=\mathbf R,
$$

rather than forming \(\mathbf K_T^{-1}\).

---

**Q37:** Derive the direct linear solve through matrix factorization.

Given

$$
\mathbf K\Delta\mathbf d=\mathbf R,
$$

factorize, for example,

$$
\mathbf K=\mathbf L\mathbf U.
$$

Then solve sequentially:

$$
\mathbf L\mathbf y=\mathbf R,
\qquad
\mathbf U\Delta\mathbf d=\mathbf y.
\tag{53}
$$

The factorization is therefore the computational replacement for explicitly forming \(\mathbf K^{-1}\).

**Reference:** Bathe, Linear Analysis Lecture 9.

---

**Q38:** Derive the Krylov subspace used by GMRES.

For

$$
\mathbf A\mathbf x=\mathbf b,
$$

with initial residual \(\mathbf r_0\), GMRES uses

$$
\boxed{
\mathcal K_m
=
\operatorname{span}
\{\mathbf r_0,\mathbf A\mathbf r_0,\ldots,\mathbf A^{m-1}\mathbf r_0\}
}.
\tag{54}
$$

The approximate solution is selected to minimize the residual norm over this subspace:

$$
\boxed{
\mathbf x_m
=
\arg\min_{\mathbf x\in\mathbf x_0+\mathcal K_m}
\|\mathbf b-\mathbf A\mathbf x\|_2
}.
\tag{55}
$$

Preconditioning transforms the problem to improve the spectral properties relevant to convergence.

---

**Q39:** Derive the relationship between a nonlinear solver such as SNES and a linear solver such as KSP.

The nonlinear problem is

$$
\mathbf R(\mathbf d)=0.
$$

Newton linearization produces

$$
\mathbf J_R\Delta\mathbf d=-\mathbf R,
\qquad
\mathbf J_R=\frac{\partial\mathbf R}{\partial\mathbf d}.
\tag{56}
$$

Thus the hierarchy is

$$
\boxed{
\text{SNES}
\rightarrow
\text{Newton/Jacobian}
\rightarrow
\text{KSP}
\rightarrow
\text{linear solve}
}.
\tag{57}
$$

SNES controls the nonlinear iterations; KSP solves the linearized systems.

---

**Q40:** Derive the line-search modification of the Newton update.

The full Newton step is \(\Delta\mathbf d_N\). Introduce

$$
\boxed{
\mathbf d_{k+1}
=
\mathbf d_k+\alpha\Delta\mathbf d_N,
\qquad
0<\alpha\le1
}.
\tag{58}
$$

A typical merit function is

$$
\Phi(\mathbf d)=\frac12\|\mathbf R(\mathbf d)\|_2^2.
\tag{59}
$$

The line search chooses \(\alpha\) to obtain sufficient reduction in \(\Phi\).

**Reference:** Bathe, Nonlinear Analysis Lecture 10.

---

**Q41:** Derive the load-stepping formulation using a scalar load parameter.

Let

$$
\mathbf f_{\mathrm{ext}}=\lambda\mathbf f_0.
$$

Then

$$
\boxed{
\mathbf R(\mathbf d,\lambda)
=
\lambda\mathbf f_0-\mathbf f_{\mathrm{int}}(\mathbf d)
=
\mathbf0
}.
\tag{60}
$$

A sequence of increasing \(\lambda\) values converts the nonlinear loading path into a sequence of nearby equilibrium problems.

---

**Q42:** Derive the arc-length constraint used to follow equilibrium paths through limit points.

The equilibrium equations are

$$
\mathbf R(\mathbf d,\lambda)=0.
$$

Introduce an additional constraint, for example,

$$
\boxed{
\|\Delta\mathbf d\|^2
+
\alpha^2(\Delta\lambda)^2
=
\Delta s^2
}.
\tag{61}
$$

The unknowns become \(\Delta\mathbf d\) and \(\Delta\lambda\), allowing the algorithm to continue through turning points where ordinary load control may fail.

**Reference:** Bathe, nonlinear solution procedures; Wriggers, Chapter 14, critical points with contact constraints.

---

**Q43:** Derive the local-to-global tangent hierarchy for a nonlinear constitutive FE problem.

At a material point,

$$
\Delta\boldsymbol\sigma
=
\mathbf C_{\mathrm{tan}}\Delta\boldsymbol\varepsilon.
\tag{62}
$$

The element contribution is schematically

$$
\mathbf K_e
=
\int_{\Omega_e}
\mathbf B^T\mathbf C_{\mathrm{tan}}\mathbf B\,dV
+
\mathbf K_{G,e}.
\tag{63}
$$

Assembly gives

$$
\boxed{
\mathbf C_{\mathrm{tan}}
\rightarrow
\mathbf K_e
\rightarrow
\mathbf K_T
}.
\tag{64}
$$

Thus the global tangent inherits its constitutive information from the local material tangent.

---

**Q44:** Derive the complete mathematical chain from continuum mechanics to the linear solver.

The essential sequence is

$$
\boxed{
\text{kinematics}
\rightarrow
\text{constitutive law}
\rightarrow
\text{weak form}
\rightarrow
\text{FE discretization}
\rightarrow
\text{residual}
\rightarrow
\text{linearization}
\rightarrow
\text{global tangent}
\rightarrow
\text{linear solve}
}.
\tag{65}
$$

More explicitly,

$$
\mathbf F
\rightarrow
\mathbf E
\rightarrow
\mathbf S
\rightarrow
\mathbf f_{\mathrm{int}}
\rightarrow
\mathbf R
\rightarrow
\mathbf K_T
\rightarrow
\Delta\mathbf d.
\tag{66}
$$

With contact,

$$
\mathbf R
=
\mathbf f_{\mathrm{ext}}
-
\mathbf f_{\mathrm{int}}
-
\mathbf f_c,
$$

so the contact operator contributes directly to the global Jacobian.

This is the mathematical chain connecting continuum mechanics, FEM, contact mechanics, and nonlinear numerical solution.

**References:** Bathe, Nonlinear Analysis Lectures 2, 3, 6 and 10; Bonet et al., Chapters 4, 5 and 8; Wriggers, Chapters 4, 7 and 11.
