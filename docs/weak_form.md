### The key pre-requisite

$$\nabla\cdot(\boldsymbol{\sigma}\cdot\boldsymbol{v}) = (\nabla\cdot\boldsymbol{\sigma})\cdot\boldsymbol{v} + \boldsymbol{\sigma}\colon(\nabla\boldsymbol{v})$$

$$(\nabla\cdot\boldsymbol{\sigma})\cdot\boldsymbol{v} = \nabla\cdot(\boldsymbol{\sigma}\cdot\boldsymbol{v}) - \boldsymbol{\sigma}\colon(\nabla\boldsymbol{v})$$

### Strong form of the momentum balance equation

For this example, let us first consider the simplest version of the momentum balance equation where an elastic body ($\Omega$) is under a body force $\boldsymbol{f}$. The momentum balance in 3D is written as:

\begin{equation}\label{strong_form}
-\nabla\boldsymbol{\sigma}(\mathbf{u}) = \boldsymbol{f}
\end{equation}

But why is it called as the strong form? That's because there is a strong requirement that $\mathbf{u}$ must be at least of degree 2. Let us focus on the LHS of this equation and see why is that.

\begin{equation}\label{sigma}
\boldsymbol{\sigma}(\mathbf{u}) = \lambda \operatorname{tr}(\boldsymbol{\epsilon}(\mathbf{u})) \boldsymbol{I} + 2 \mu \boldsymbol{\epsilon}(\mathbf{u}) 
\end{equation}

\begin{equation}\label{epsilon}
\boldsymbol{\epsilon}(\mathbf{u}) = \frac{1}{2} \Big[(\nabla \mathbf{u}) + (\nabla \mathbf{u})^T\Big]
\end{equation}

\begin{equation}\label{nabla}
\nabla = \frac{\partial}{\partial x_1} \boldsymbol{e}_1  + \frac{\partial}{\partial x_2} \boldsymbol{e}_2 + \frac{\partial}{\partial x_3} \boldsymbol{e}_3
\end{equation}

If we follow backwards from Eq. $\eqref{nabla}$ to $\eqref{strong_form}$, it becomes evident that the LHS contains terms where the operator $\nabla^2$ or $\frac{\partial^2}{\partial x_i^2}$ acts on $\boldsymbol{u}$. Thus, for the strong form to hold, the displacement field $\boldsymbol{u}$ must possess at least second-order spatial derivatives. In the next section, we will relax this strong requirement by reformulating the strong form of the momentum balance equation in its weak (aka variational) form. The goal is to arrive at an equation where $\boldsymbol{u}$ needs to be just once differentiable instead of twice. In other words, the displacement field is then required to belong only to a first order Sobolov space, typically written as $\boldsymbol{u}\in [H^1(\Omega)]^d$. This reduced requirement allows us to use piecewise linear Lagrange elements ($\mathbb{P}_1$), which have first order derivatives within each element.

!!! NOTE "NOTE:"
    More discussion on the use of different spaces and shape functions to be added in a separate note.


### Weak form of the momentum balance equation / Principle of Virtual Work
To derive the weak form, we multiply the strong form by a test function $\boldsymbol{v}$ and use integration by parts. But why mutliply? What is $\boldsymbol{v}$?. We do this to transform the equation from a force balance to a balance of virtual work. The test function is actually a infinitisimal, and kinematically admissible virtual displacement field. We read the new equation as work done by the external forces is equal to the work done by the internal forces (this expression will gradually take the shape of strain energy). Two key things that we should focus on during this derivation are the following:

- how to perform integration by parts (I say this because it is a but different from the conventional integration by parts understanding we carry over from $1D$ calculus), and
- how do different vector and tensor quantities operate on one another (is there a vector product, dot product, double dot product, or just a scalar multiplication between any two quantities).

Multiplying with $\boldsymbol{v}$ and integrating over the domain of the body ($\Omega)$:

$$-\int_\Omega\nabla\boldsymbol{\sigma}(\mathbf{u})\boldsymbol{v} \, \mathrm{d}\boldsymbol{x} = \int_\Omega\boldsymbol{f}\boldsymbol{v} \, \mathrm{d}\boldsymbol{x} $$

Let us re-write the same equation without the arguments and with proper operations between different quantities, so that we know what operates on what and in what sequence:

$$-\int_\Omega(\nabla\cdot\boldsymbol{\sigma})\cdot \boldsymbol{v} \, \mathrm{d}\boldsymbol{x} = \int_\Omega\boldsymbol{f}\cdot\boldsymbol{v} \, \mathrm{d}\boldsymbol{x} $$

Now, we recall the key pre-requisite at the top of this page. Using that is what actually implements the integration by parts here. Replacing the LHS above using the pre-requisite we saw earlier, the equation becomes:

$$-\int_\Omega \Big[\nabla\cdot(\boldsymbol{\sigma}\cdot\boldsymbol{v}) - \boldsymbol{\sigma}\colon(\nabla\boldsymbol{v})\Big] \, \mathrm{d}\boldsymbol{x} = \int_\Omega\boldsymbol{f}\cdot\boldsymbol{v} \, \mathrm{d}\boldsymbol{x} $$

$$-\int_\Omega \nabla\cdot(\boldsymbol{\sigma}\cdot\boldsymbol{v}) \, \mathrm{d}\boldsymbol{x} + \int_\Omega \boldsymbol{\sigma}\colon(\nabla\boldsymbol{v}) \, \mathrm{d}\boldsymbol{x} = \int_\Omega\boldsymbol{f}\cdot\boldsymbol{v} \, \mathrm{d}\boldsymbol{x} $$

At this point, we revisit the Gauss divergence theorem in 3D.

!!! info "Gauss' Divergence Theorem (3D)"
    Let $\Omega \subset \mathbb{R}^3$ be a sufficiently smooth volume with boundary $\partial\Omega$ and outward unit normal $\boldsymbol{n}$. For a sufficiently smooth vector field $\mathbf{F}: \bar{\Omega} \to \mathbb{R}^3$, where $\boldsymbol{F} = (F_1,F_2,F_3)$, and $\bar{\Omega} = \Omega\cup\partial\Omega$ (up to and including the boundary), Gauss' divergence theorem states that:

    $$\int_{\Omega} \nabla \cdot \boldsymbol{F}\,d\Omega = \int_{\partial\Omega} \boldsymbol{F}\cdot\boldsymbol{n}\,d\Gamma $$

    where the divergence of $\boldsymbol{F}$ is

    $$\nabla\cdot\boldsymbol{F}=\frac{\partial F_1}{\partial x_1}+\frac{\partial F_2}{\partial x_2}+\frac{\partial F_3}{\partial x_3}.$$

    In component form,

    $$\int_{\Omega}\left(\frac{\partial F_1}{\partial x_1}+\frac{\partial F_2}{\partial x_2}+\frac{\partial F_3}{\partial x_3}\right)d\Omega=\int_{\partial\Omega}\left(F_1 n_1 + F_2 n_2 + F_3 n_3\right)d\Gamma.$$

    **Interpretation**: The volume integral of the divergence of a vector field is equal to the net flux of that field through the boundary of the volume.

Using the Gauss divergence theorem in the first term on the LHS, we get the following:

$$-\int_{\partial\Omega} (\boldsymbol{\sigma}\cdot\boldsymbol{v}) \cdot \boldsymbol{n} \, \mathrm{d}\boldsymbol{x} + \int_\Omega \boldsymbol{\sigma}\colon(\nabla\boldsymbol{v}) \, \mathrm{d}\boldsymbol{x} = \int_\Omega\boldsymbol{f}\cdot\boldsymbol{v} \, \mathrm{d}\boldsymbol{x} $$

$$\color{red}{ \int_\Omega \boldsymbol{\sigma}\colon(\nabla\boldsymbol{v}) \, \mathrm{d}\boldsymbol{x} } = \color{green}{ \int_\Omega\boldsymbol{f}\cdot\boldsymbol{v} \, \mathrm{d}\boldsymbol{x} } + \color{blue}{ \int_{\partial\Omega} (\boldsymbol{\sigma}\cdot\boldsymbol{v}) \cdot \boldsymbol{n} \, \mathrm{d}\boldsymbol{x} } $$

Notice that the initial force balance equation has now taken the form of an energy or work balance equation, where we have \(\color{red}{\text{internal virtual work}}\) on the LHS and the \(\color{green}{\text{work of body forces}}\) and \(\color{blue}{\text{boundary/traction forces}}\) on the right. We only need to update the integrand of the second term on the RHS. Let us take a look at the following equivalence.

!!! info "Equivalence of the Boundary Work Terms"
    The boundary term can be written in either of the following forms:

    $$ (\boldsymbol{\sigma}\cdot\boldsymbol{v})\cdot\boldsymbol{n} \qquad \text{or} \qquad (\boldsymbol{\sigma}\cdot\boldsymbol{n})\cdot\boldsymbol{v}. $$

    Using the index notation $\boldsymbol{\sigma}=\sigma_{ij}\boldsymbol{e}_i\otimes\boldsymbol{e}_j$, $\boldsymbol{v}=v_k\boldsymbol{e}_k$, and $\boldsymbol{n}=n_l\boldsymbol{e}_l$, the first expression becomes

    $$
    \begin{aligned}
    (\boldsymbol{\sigma}\cdot\boldsymbol{v})\cdot\boldsymbol{n}
    &= \left(\sigma_{ij}\,\boldsymbol{e}_i\otimes\boldsymbol{e}_j
    \cdot v_k\boldsymbol{e}_k\right)\cdot n_l\boldsymbol{e}_l \\[2mm]
    &= \left(\sigma_{ij}v_k\boldsymbol{e}_i\,\delta_{jk}\right)
    \cdot n_l\boldsymbol{e}_l \\[2mm]
    &= \sigma_{ij}v_j\boldsymbol{e}_i\cdot n_l\boldsymbol{e}_l \\[2mm]
    &= \sigma_{ij}v_j n_l\delta_{il} \\[2mm]
    &= \boxed{\sigma_{ij}v_j n_i}.
    \end{aligned}
    $$

    Similarly, the second expression becomes

    $$
    \begin{aligned}
    (\boldsymbol{\sigma}\cdot\boldsymbol{n})\cdot\boldsymbol{v}
    &= \left(\sigma_{ij}\,\boldsymbol{e}_i\otimes\boldsymbol{e}_j
    \cdot n_k\boldsymbol{e}_k\right)\cdot v_l\boldsymbol{e}_l \\[2mm]
    &= \left(\sigma_{ij}n_k\boldsymbol{e}_i\,\delta_{jk}\right)
    \cdot v_l\boldsymbol{e}_l \\[2mm]
    &= \sigma_{ij}n_j\boldsymbol{e}_i\cdot v_l\boldsymbol{e}_l \\[2mm]
    &= \sigma_{ij}n_jv_l\delta_{il} \\[2mm]
    &= \boxed{\sigma_{ij}n_jv_i}.
    \end{aligned}
    $$

    For a symmetric Cauchy stress tensor, $\sigma_{ij}=\sigma_{ji}$. Therefore,

    $$
    (\boldsymbol{\sigma}\cdot\boldsymbol{n})\cdot\boldsymbol{v}
    =\sigma_{ij}n_jv_i
    =\sigma_{ji}n_jv_i
    =\sigma_{ij}n_iv_j
    =\sigma_{ij}v_jn_i
    =(\boldsymbol{\sigma}\cdot\boldsymbol{v})\cdot\boldsymbol{n}.
    $$

    Hence, when $\boldsymbol{\sigma}$ is **symmetric**:

    $$\boxed{ (\boldsymbol{\sigma}\cdot\boldsymbol{v})\cdot\boldsymbol{n} = (\boldsymbol{\sigma}\cdot\boldsymbol{n})\cdot\boldsymbol{v} }. $$

    **Important:** The two expressions are **not equivalent** for a **nonsymmetric** stress tensor. In classical continuum mechanics, the Cauchy stress tensor is symmetric.

Therefore, we can re-write the weak form as:

$$\int_\Omega \boldsymbol{\sigma}\colon(\nabla\boldsymbol{v}) \, \mathrm{d}\boldsymbol{x} = \int_\Omega\boldsymbol{f}\cdot\boldsymbol{v} \, \mathrm{d}\boldsymbol{x} + \int_{\partial\Omega} (\boldsymbol{\sigma}\cdot\boldsymbol{n}) \cdot \boldsymbol{v} \, \mathrm{d}\boldsymbol{x}$$

\begin{equation}
\boxed{
\int_\Omega \boldsymbol{\sigma}\colon(\nabla\boldsymbol{v}) \, \mathrm{d}\boldsymbol{x} = \int_\Omega\boldsymbol{f}\cdot\boldsymbol{v} \, \mathrm{d}\boldsymbol{x} + \int_{\partial\Omega_T} \boldsymbol{t} \cdot \boldsymbol{v} \, \mathrm{d}\boldsymbol{x}
}
\end{equation}

Notice that there is one subtle but very important update in the last term, the integration domain. Recall that $\partial\Omega = \partial\Omega_T \cup \partial\Omega_D$. Since the virtual displacement field ($\boldsymbol{v}$) is exactly zero on the Dirichilet boundary ($\partial\Omega_D$), only the $\partial\Omega_T$ part of the integral survives in the final weak (variational) form.
