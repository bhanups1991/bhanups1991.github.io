# Matrix Diagnostics for \(Ax=B\)

This note defines the three diagnostics used in the contact solver: relative asymmetry, minimum singular value, and residual history. The definitions apply to a general matrix \(A\), while the Jacobian \(J\) in the nonlinear contact problem is a particular application.

## 1. Relative asymmetry

For a square matrix \(A\), define

\[
\eta_A =
\frac{\|A-A^T\|_F}{2\|A\|_F},
\]

where

\[
\|A\|_F =
\sqrt{\sum_{i,j}a_{ij}^2}
\]

is the Frobenius norm.

The diagnostic code uses exactly this quantity for the assembled Jacobian:

\[
\eta_J =
\frac{\|J-J^T\|_F}{2\|J\|_F}.
\]

The factor \(2\) normalizes the measure because, for a perfectly skew-symmetric matrix, \(A^T=-A\), giving

\[
\|A-A^T\|_F=2\|A\|_F.
\]

Therefore:

- \(\eta_A=0\): perfectly symmetric.
- \(0<\eta_A<1\): partially asymmetric.
- \(\eta_A=1\): perfectly skew-symmetric.

Thus, this diagnostic measures departure from symmetry. It does **not** determine positive definiteness, invertibility, or conditioning.

For a tangent matrix \(J=DF(u)\), symmetry is particularly relevant because a symmetric tangent is associated with conservative/variational formulations, whereas frictional contact generally introduces nonsymmetry.

## 2. Minimum singular value

The singular values of \(A\) are the square roots of the eigenvalues of

\[
A^T A.
\]

They are ordered as

\[
\sigma_1(A)\geq \sigma_2(A)\geq\cdots\geq\sigma_n(A)\geq0.
\]

The minimum singular value is therefore

\[
\sigma_{\min}(A)
=
\min_{\|x\|_2=1}\|Ax\|_2.
\]

It measures how strongly the matrix acts in its weakest direction.

If

\[
\sigma_{\min}(A)>0,
\]

then \(A\) is nonsingular. If

\[
\sigma_{\min}(A)\rightarrow0,
\]

the matrix is approaching singularity.

This has a direct interpretation for

\[
Ax=B.
\]

For a nonsingular square matrix,

\[
x=A^{-1}B.
\]

A small \(\sigma_{\min}(A)\) means that some directions in \(x\) produce only a very small change in \(Ax\). Consequently, perturbations in \(B\), numerical errors, or modelling errors can produce relatively large changes in \(x\).

The condition number in the 2-norm is

\[
\kappa_2(A)
=
\frac{\sigma_{\max}(A)}{\sigma_{\min}(A)}.
\]

Hence, \(\sigma_{\min}\) alone indicates proximity to singularity, while \(\sigma_{\min}\) together with \(\sigma_{\max}\) quantifies conditioning.

### Important distinction

A positive minimum singular value does **not** imply positive definiteness.

For example, a nonsymmetric or even skew-symmetric matrix can have all singular values positive. Positive definiteness is instead a property normally defined for a symmetric matrix through

\[
x^T A x>0
\qquad
\forall x\neq0.
\]

Therefore, \(\sigma_{\min}(J)>0\) should be interpreted as evidence of nonsingularity, not coercivity.

## 3. Residual history

For a nonlinear equilibrium problem

\[
F(u)=0,
\]

the residual at iteration \(k\) is

\[
r_k=F(u_k).
\]

A scalar residual measure is commonly

\[
\|r_k\|_2=\|F(u_k)\|_2.
\]

The solver's residual history is therefore the sequence

\[
\|F(u_0)\|,\;
\|F(u_1)\|,\;
\ldots,\;
\|F(u_k)\|.
\]

The diagnostic code records the SNES residual norm and plots it on a logarithmic vertical axis.

A decreasing residual indicates that the iterative method is approaching equilibrium. The shape of the curve gives information about convergence:

- rapid, approximately linear decrease: robust convergence;
- initially rapid then slower decrease: convergence is degrading;
- stagnation: the nonlinear iteration is no longer making significant progress;
- increasing residual: the iteration is moving away from equilibrium;
- convergence to a small residual: a numerical equilibrium has been reached.

For a linear problem

\[
Ax=B,
\]

the analogous residual is

\[
r_k=B-Ax_k.
\]

At the exact solution,

\[
r=0.
\]

For a nonlinear problem, however, residual convergence and Jacobian properties describe different aspects of the problem. A small residual indicates equilibrium satisfaction; it does not by itself establish uniqueness, coercivity, or good conditioning.

## 4. Interpretation for the contact Jacobian

In the present formulation,

\[
F(u)=0,
\]

and

\[
J(u)=DF(u).
\]

The three diagnostics therefore probe different properties:

| Diagnostic | Mathematical quantity | Main information |
|---|---|---|
| Relative asymmetry | \(\|J-J^T\|_F/(2\|J\|_F)\) | Departure from symmetry |
| Minimum singular value | \(\sigma_{\min}(J)\) | Distance from singularity |
| Residual history | \(\|F(u_k)\|\) | Nonlinear equilibrium convergence |

Together they provide a computational picture of the tangent operator during the nonlinear solution process, but they should not be interpreted as interchangeable tests of well-posedness, coercivity, or uniqueness.
