# Linearization of the Principle of Virtual Work

We consider a geometrically nonlinear problem in a **Total Lagrangian formulation**. All volume integrals are therefore evaluated over the fixed reference configuration $\Omega_0$, and the relevant stress and strain measures are the second Piola--Kirchhoff stress $\mathbf{S}$ and Green--Lagrange strain $\mathbf{E}$.

## 1. Principle of Virtual Work

The principle of virtual work is

$$\delta W_{\mathrm{int}}=\delta W_{\mathrm{ext}}.$$

For a Total Lagrangian formulation,

$$\delta W_{\mathrm{int}}=\int_{\Omega_0}\mathbf{S}:\delta\mathbf{E}\,dV.$$

For dead body forces and prescribed tractions,

$$\delta W_{\mathrm{ext}}=\int_{\Omega_0}\mathbf{f}\cdot\delta\mathbf{u}\,dV+\int_{\Gamma_{0t}}\mathbf{T}\cdot\delta\mathbf{u}\,dA.$$

Hence, the nonlinear weak form can be written as

$$G(\mathbf{u};\delta\mathbf{u})=\int_{\Omega_0}\mathbf{S}:\delta\mathbf{E}\,dV-\int_{\Omega_0}\mathbf{f}\cdot\delta\mathbf{u}\,dV-\int_{\Gamma_{0t}}\mathbf{T}\cdot\delta\mathbf{u}\,dA=0.$$

The nonlinear FE problem is therefore

$$G(\mathbf{u};\delta\mathbf{u})=0.$$

The purpose of Newton--Raphson is to linearize this nonlinear weak form about the current state.

---

## 2. Finite-Deformation Kinematics

The motion is

$$\mathbf{x}_t=\mathbf{X}+\mathbf{u}_t.$$

Therefore, the deformation gradient at time $t$ is

$$\mathbf{F}_t=\frac{\partial\mathbf{x}_t}{\partial\mathbf{X}}=\mathbf{I}+\operatorname{Grad}\mathbf{u}_t.$$

The right Cauchy--Green deformation tensor is

$$\mathbf{C}_t=\mathbf{F}_t^T\cdot\mathbf{F}_t.$$

The Green--Lagrange strain is

$$\mathbf{E}_t=\frac{1}{2}\left(\mathbf{C}_t-\mathbf{I}\right)=\frac{1}{2}\left(\mathbf{F}_t^T\cdot\mathbf{F}_t-\mathbf{I}\right).$$

---

## 3. Variation of the Green--Lagrange Strain

Since

$$\delta\mathbf{F}=\operatorname{Grad}\delta\mathbf{u},$$

the variation of the Green--Lagrange strain is

$$\delta\mathbf{E}=\frac{1}{2}\left[(\operatorname{Grad}\delta\mathbf{u})^T\cdot\mathbf{F}+\mathbf{F}^T\cdot\operatorname{Grad}\delta\mathbf{u}\right].$$

Equivalently,

$$\delta\mathbf{E}=\operatorname{sym}\left(\mathbf{F}^T\cdot\operatorname{Grad}\delta\mathbf{u}\right).$$

Notice that $\delta\mathbf{E}$ depends on the current deformation gradient $\mathbf{F}$. Therefore, even if the material is linear elastic, the weak form is nonlinear when finite-deformation kinematics are used.

---

## 4. Introduce the Increment $t\rightarrow t+\Delta t$

Suppose that the state at $t$ is known and that we seek the state at $t+\Delta t$.

Define the displacement increment as

$$\Delta\mathbf{u}=\mathbf{u}_{t+\Delta t}-\mathbf{u}_t.$$

Therefore,

$$\mathbf{u}_{t+\Delta t}=\mathbf{u}_t+\Delta\mathbf{u}.$$

The deformation gradient at the new state is

$$\mathbf{F}_{t+\Delta t}=\mathbf{I}+\operatorname{Grad}\mathbf{u}_{t+\Delta t}.$$

Hence,

$$\mathbf{F}_{t+\Delta t}=\mathbf{F}_t+\operatorname{Grad}\Delta\mathbf{u}.$$

Define

$$\Delta\mathbf{F}=\operatorname{Grad}\Delta\mathbf{u}.$$

Therefore,

$$\mathbf{F}_{t+\Delta t}=\mathbf{F}_t+\Delta\mathbf{F}.$$

---

## 5. Increment of Green--Lagrange Strain

At the new state,

$$\mathbf{E}_{t+\Delta t}=\frac{1}{2}\left(\mathbf{F}_{t+\Delta t}^T\cdot\mathbf{F}_{t+\Delta t}-\mathbf{I}\right).$$

Substituting $\mathbf{F}_{t+\Delta t}=\mathbf{F}_t+\Delta\mathbf{F}$ gives

$$\mathbf{E}_{t+\Delta t}=\frac{1}{2}\left[(\mathbf{F}_t+\Delta\mathbf{F})^T\cdot(\mathbf{F}_t+\Delta\mathbf{F})-\mathbf{I}\right].$$

Expanding,

$$\mathbf{E}_{t+\Delta t}=\frac{1}{2}\left[\mathbf{F}_t^T\cdot\mathbf{F}_t+\mathbf{F}_t^T\cdot\Delta\mathbf{F}+\Delta\mathbf{F}^T\cdot\mathbf{F}_t+\Delta\mathbf{F}^T\cdot\Delta\mathbf{F}-\mathbf{I}\right].$$

Since

$$\mathbf{E}_t=\frac{1}{2}\left(\mathbf{F}_t^T\cdot\mathbf{F}_t-\mathbf{I}\right),$$

the strain increment is

$$\Delta\mathbf{E}=\frac{1}{2}\left[\mathbf{F}_t^T\cdot\Delta\mathbf{F}+\Delta\mathbf{F}^T\cdot\mathbf{F}_t+\Delta\mathbf{F}^T\cdot\Delta\mathbf{F}\right].$$

Using $\Delta\mathbf{F}=\operatorname{Grad}\Delta\mathbf{u}$,

$$\Delta\mathbf{E}=\frac{1}{2}\left[\mathbf{F}_t^T\cdot\operatorname{Grad}\Delta\mathbf{u}+(\operatorname{Grad}\Delta\mathbf{u})^T\cdot\mathbf{F}_t+(\operatorname{Grad}\Delta\mathbf{u})^T\cdot\operatorname{Grad}\Delta\mathbf{u}\right].$$

The last term is quadratic in $\Delta\mathbf{u}$. Newton--Raphson requires a first-order linearization, so this term is neglected:

$$\boxed{\Delta\mathbf{E}\approx\frac{1}{2}\left[\mathbf{F}_t^T\cdot\operatorname{Grad}\Delta\mathbf{u}+(\operatorname{Grad}\Delta\mathbf{u})^T\cdot\mathbf{F}_t\right].}$$

Equivalently,

$$\boxed{\Delta\mathbf{E}=\operatorname{sym}\left(\mathbf{F}_t^T\cdot\operatorname{Grad}\Delta\mathbf{u}\right)+O(\|\Delta\mathbf{u}\|^2).}$$

---

## 6. Linearization of the Virtual Strain

At $t+\Delta t$,

$$\delta\mathbf{E}_{t+\Delta t}=\frac{1}{2}\left[(\operatorname{Grad}\delta\mathbf{u})^T\cdot\mathbf{F}_{t+\Delta t}+\mathbf{F}_{t+\Delta t}^T\cdot\operatorname{Grad}\delta\mathbf{u}\right].$$

Substituting $\mathbf{F}_{t+\Delta t}=\mathbf{F}_t+\Delta\mathbf{F}$,

$$\delta\mathbf{E}_{t+\Delta t}=\frac{1}{2}\left[(\operatorname{Grad}\delta\mathbf{u})^T\cdot\mathbf{F}_t+\mathbf{F}_t^T\cdot\operatorname{Grad}\delta\mathbf{u}+(\operatorname{Grad}\delta\mathbf{u})^T\cdot\Delta\mathbf{F}+\Delta\mathbf{F}^T\cdot\operatorname{Grad}\delta\mathbf{u}\right].$$

The first two terms constitute $\delta\mathbf{E}_t$. Therefore,

$$\Delta(\delta\mathbf{E})=\frac{1}{2}\left[(\operatorname{Grad}\delta\mathbf{u})^T\cdot\Delta\mathbf{F}+\Delta\mathbf{F}^T\cdot\operatorname{Grad}\delta\mathbf{u}\right].$$

Using $\Delta\mathbf{F}=\operatorname{Grad}\Delta\mathbf{u}$,

$$\boxed{\Delta(\delta\mathbf{E})=\frac{1}{2}\left[(\operatorname{Grad}\delta\mathbf{u})^T\cdot\operatorname{Grad}\Delta\mathbf{u}+(\operatorname{Grad}\Delta\mathbf{u})^T\cdot\operatorname{Grad}\delta\mathbf{u}\right].}$$

Equivalently,

$$\boxed{\Delta(\delta\mathbf{E})=\operatorname{sym}\left[(\operatorname{Grad}\delta\mathbf{u})^T\cdot\operatorname{Grad}\Delta\mathbf{u}\right].}$$

This term will generate the geometric stiffness.

---

## 7. Linearization of the Constitutive Relation

The second Piola--Kirchhoff stress is generally a function of strain and internal variables,

$$\mathbf{S}=\mathbf{S}(\mathbf{E},\boldsymbol{\alpha}).$$

Its first-order increment is

$$\Delta\mathbf{S}=\mathbb{C}_t:\Delta\mathbf{E},$$

where

$$\boxed{\mathbb{C}_t=\frac{\partial\mathbf{S}}{\partial\mathbf{E}}}$$

is the consistent constitutive tangent.

Therefore,

$$\boxed{\Delta\mathbf{S}=\mathbb{C}_t:\operatorname{sym}\left(\mathbf{F}_t^T\cdot\operatorname{Grad}\Delta\mathbf{u}\right).}$$

For a nonlinear constitutive model, $\mathbb{C}_t$ must be consistent with the constitutive integration algorithm if quadratic Newton convergence is to be retained.

---

## 8. Linearization of the Internal Virtual Work

At $t+\Delta t$,

$$\delta W_{\mathrm{int}}^{t+\Delta t}=\int_{\Omega_0}\mathbf{S}_{t+\Delta t}:\delta\mathbf{E}_{t+\Delta t}\,dV.$$

Write

$$\mathbf{S}_{t+\Delta t}=\mathbf{S}_t+\Delta\mathbf{S}$$

and

$$\delta\mathbf{E}_{t+\Delta t}=\delta\mathbf{E}_t+\Delta(\delta\mathbf{E}).$$

Therefore,

$$\delta W_{\mathrm{int}}^{t+\Delta t}=\int_{\Omega_0}\left(\mathbf{S}_t+\Delta\mathbf{S}\right):\left[\delta\mathbf{E}_t+\Delta(\delta\mathbf{E})\right]\,dV.$$

Expanding,

$$\delta W_{\mathrm{int}}^{t+\Delta t}=\int_{\Omega_0}\left[\mathbf{S}_t:\delta\mathbf{E}_t+\mathbf{S}_t:\Delta(\delta\mathbf{E})+\Delta\mathbf{S}:\delta\mathbf{E}_t+\Delta\mathbf{S}:\Delta(\delta\mathbf{E})\right]\,dV.$$

The last term is second order in the increment and is discarded in the Newton linearization. Hence,

$$\boxed{\Delta(\delta W_{\mathrm{int}})=\int_{\Omega_0}\left[\Delta\mathbf{S}:\delta\mathbf{E}_t+\mathbf{S}_t:\Delta(\delta\mathbf{E})\right]\,dV.}$$

This is the key linearization of the internal virtual work.

---

## 9. Substitute the Constitutive Tangent

Using

$$\Delta\mathbf{S}=\mathbb{C}_t:\Delta\mathbf{E},$$

we obtain

$$\boxed{\Delta(\delta W_{\mathrm{int}})=\int_{\Omega_0}\left[(\mathbb{C}_t:\Delta\mathbf{E}):\delta\mathbf{E}_t+\mathbf{S}_t:\Delta(\delta\mathbf{E})\right]\,dV.}$$

Now substitute the expressions for $\Delta\mathbf{E}$ and $\Delta(\delta\mathbf{E})$:

$$\boxed{\Delta(\delta W_{\mathrm{int}})=\int_{\Omega_0}\left[(\mathbb{C}_t:\operatorname{sym}(\mathbf{F}_t^T\cdot\operatorname{Grad}\Delta\mathbf{u})):\delta\mathbf{E}_t+\mathbf{S}_t:\operatorname{sym}((\operatorname{Grad}\delta\mathbf{u})^T\cdot\operatorname{Grad}\Delta\mathbf{u})\right]\,dV.}$$

This is the linearized weak form in tensor notation.

---

## 10. Identification of Material and Geometric Contributions

The first term is

$$\boxed{\Delta(\delta W_{\mathrm{int}})_M=\int_{\Omega_0}(\mathbb{C}_t:\Delta\mathbf{E}):\delta\mathbf{E}_t\,dV.}$$

This term arises because the stress changes when the strain changes:

$$\Delta\mathbf{S}=\mathbb{C}_t:\Delta\mathbf{E}.$$

It therefore produces the **material stiffness**.

The second term is

$$\boxed{\Delta(\delta W_{\mathrm{int}})_G=\int_{\Omega_0}\mathbf{S}_t:\Delta(\delta\mathbf{E})\,dV.}$$

This term arises because the strain variation itself depends on the deformation gradient $\mathbf{F}$. It therefore produces the **geometric stiffness**.

Hence,

$$\boxed{\mathbf{K}_T=\mathbf{K}_M+\mathbf{K}_G.}$$

---

## 11. Material Stiffness

Introduce the FE displacement vector $\mathbf{d}$ through

$$\mathbf{u}=\mathbf{N}\mathbf{d}.$$

Similarly,

$$\delta\mathbf{u}=\mathbf{N}\delta\mathbf{d}.$$

and

$$\Delta\mathbf{u}=\mathbf{N}\Delta\mathbf{d}.$$

The corresponding linearized strain relations can be written as

$$\delta\mathbf{E}_t=\mathbf{B}_t\delta\mathbf{d}.$$

and

$$\Delta\mathbf{E}=\mathbf{B}_t\Delta\mathbf{d}.$$

Therefore,

$$\Delta(\delta W_{\mathrm{int}})_M=\delta\mathbf{d}^T\left[\int_{\Omega_0}\mathbf{B}_t^T\mathbb{C}_t\mathbf{B}_t\,dV\right]\Delta\mathbf{d}.$$

Hence,

$$\boxed{\mathbf{K}_M=\int_{\Omega_0}\mathbf{B}_t^T\mathbb{C}_t\mathbf{B}_t\,dV.}$$

---

## 12. Geometric Stiffness

The geometric contribution is

$$\Delta(\delta W_{\mathrm{int}})_G=\int_{\Omega_0}\mathbf{S}_t:\left[(\operatorname{Grad}\delta\mathbf{u})^T\cdot\operatorname{Grad}\Delta\mathbf{u}\right]\,dV.$$

After substituting the FE interpolation,

$$\Delta(\delta W_{\mathrm{int}})_G=\delta\mathbf{d}^T\mathbf{K}_G\Delta\mathbf{d}.$$

Thus,

$$\boxed{\mathbf{K}_G=\int_{\Omega_0}\mathbf{G}_t^T\mathbf{S}_t\mathbf{G}_t\,dV}$$

where $\mathbf{G}_t$ represents the appropriate displacement-gradient operator.

The exact matrix representation of $\mathbf{G}_t$ depends on the chosen vectorization or Voigt notation, but the underlying tensor expression is

$$\boxed{\mathbf{S}_t:\left[(\operatorname{Grad}\delta\mathbf{u})^T\cdot\operatorname{Grad}\Delta\mathbf{u}\right].}$$

---

## 13. Linearized Equilibrium Equation

The residual at time $t$ is

$$\mathbf{R}_t=\mathbf{F}_{\mathrm{ext},t}-\mathbf{F}_{\mathrm{int},t}.$$

The Newton correction is obtained by requiring the linearized residual to vanish:

$$D G(\mathbf{u}_t;\delta\mathbf{u})[\Delta\mathbf{u}]=-G(\mathbf{u}_t;\delta\mathbf{u}).$$

After FE discretization,

$$\boxed{\mathbf{K}_{T,t}\Delta\mathbf{d}=\mathbf{R}_t.}$$

Since

$$\mathbf{K}_{T,t}=\mathbf{K}_{M,t}+\mathbf{K}_{G,t},$$

we have

$$\boxed{(\mathbf{K}_{M,t}+\mathbf{K}_{G,t})\Delta\mathbf{d}=\mathbf{F}_{\mathrm{ext},t}-\mathbf{F}_{\mathrm{int},t}.}$$

The displacement is then updated as

$$\boxed{\mathbf{d}_{t+\Delta t}=\mathbf{d}_t+\Delta\mathbf{d}.}$$

The process is repeated until the residual and/or displacement correction satisfies the prescribed convergence criteria.

---

## 14. The Complete Derivation in One Chain

The entire derivation can now be viewed as

$$\boxed{\delta W_{\mathrm{int}}=\int_{\Omega_0}\mathbf{S}:\delta\mathbf{E}\,dV}$$

$$\boxed{\mathbf{E}=\frac{1}{2}\left(\mathbf{F}^T\cdot\mathbf{F}-\mathbf{I}\right)}$$

$$\boxed{\delta\mathbf{E}=\frac{1}{2}\left[(\operatorname{Grad}\delta\mathbf{u})^T\cdot\mathbf{F}+\mathbf{F}^T\cdot\operatorname{Grad}\delta\mathbf{u}\right]}$$

$$\boxed{\mathbf{F}_{t+\Delta t}=\mathbf{F}_t+\operatorname{Grad}\Delta\mathbf{u}}$$

$$\boxed{\Delta\mathbf{E}=\operatorname{sym}\left(\mathbf{F}_t^T\cdot\operatorname{Grad}\Delta\mathbf{u}\right)}$$

$$\boxed{\Delta(\delta\mathbf{E})=\operatorname{sym}\left[(\operatorname{Grad}\delta\mathbf{u})^T\cdot\operatorname{Grad}\Delta\mathbf{u}\right]}$$

$$\boxed{\Delta\mathbf{S}=\mathbb{C}_t:\Delta\mathbf{E}}$$

$$\boxed{\Delta(\delta W_{\mathrm{int}})=\int_{\Omega_0}\left[\Delta\mathbf{S}:\delta\mathbf{E}_t+\mathbf{S}_t:\Delta(\delta\mathbf{E})\right]\,dV}$$

$$\boxed{\Delta(\delta W_{\mathrm{int}})=\delta\mathbf{d}^T(\mathbf{K}_M+\mathbf{K}_G)\Delta\mathbf{d}}$$

$$\boxed{\mathbf{K}_T\Delta\mathbf{d}=\mathbf{R}_t}$$

with

$$\boxed{\mathbf{K}_T=\mathbf{K}_M+\mathbf{K}_G.}$$

Thus, the Newton--Raphson method is simply the process of **linearizing the nonlinear principle of virtual work about the current state, solving the resulting linearized problem for $\Delta\mathbf{d}$, updating the state, and repeating until equilibrium is reached.**