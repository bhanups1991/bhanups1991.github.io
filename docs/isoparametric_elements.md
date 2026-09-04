This section takes a look at the formulation and the key benefits of using isoparametric formulation in the finite element method.

### Preamble

Let us dissect the name itself. An isoparametric element means there is some parameterization happening (**parametric**) and, in addition to that, there is something which remains the same (**iso**). Naturally, this parameterization is of a finite element. Just keeping these three things in mind clears some air.

Additionally, we can keep the following things in mind. There is no harm if we forget or do not recall these; it is, however, better to have a bird's-eye view before moving to the detailed explanation. The isoparametric formulation allows us to efficiently compute derivatives of displacement and integral quantities appearing in the equilibrium equation. In other words, we map the position and displacement fields of an element to a parametric domain, referred to as the parent domain. This mapping allows us to compute physical derivatives using the Jacobian evaluated at the Gauss quadrature points. Moreover, it allows us to transform the limits of integration from the physical domain to the parametric domain, where the integration is performed using the Gauss quadrature rule.

!!! tip "Point of Confusion"

    The parent domain is **NOT** the reference configuration. The physical configurations are entirely different from the parametric or parent domain. Though it is not exactly true, nonetheless, the easiest way to clear this confusion is to think of the isoparametric formulation as more of a computational concept and less of a continuum mechanics concept.

    The isoparametric element lives in a separate standard mathematical domain. The physical element, however, lives in the actual physical domain of the problem. Whichever configuration (reference or current) we use for our equilibrium equations, our physical element lives there. It has no effect on the parametric element's formulation. We simply build a connection between the parent domain and the physical domain of our choice.

### What is done and how it is done? 

We will take the example of a two-dimensional quadrilateral element, for which the parent element is chosen as a perfect square defined on the $\xi, \eta$ coordinates with limits:

$$-1\leq \xi\leq 1,\qquad-1\leq \eta\leq 1.$$

The coordinates \((\xi,\eta)\) are called **natural**, **local**, or **parent-element coordinates**.

For all two-dimensional quadrilateral elements in our analysis, the parent element will always be the same square confined to the space $\hat{\Omega}$:

$$\hat{\Omega}=[-1,1]\times[-1,1].$$

It is important to remind ourselves that the parent element is **not necessarily the reference configuration of the body**. It is simply a convenient mathematical coordinate domain. Recall that for a four-node bilinear quadrilateral, the shape functions are:

$$N_1=\frac{1}{4}(1-\xi)(1-\eta),$$

$$N_2=\frac{1}{4}(1+\xi)(1-\eta),$$

$$N_3=\frac{1}{4}(1+\xi)(1+\eta),$$

$$N_4=\frac{1}{4}(1-\xi)(1+\eta).$$


We will first see how the parametrization is done. On the way, we will also see the **iso** part of the definition. The parameterization is simply a mapping from the physical domain to the parent domain. Let us consider a four-node quadrilateral element living in the physical domain. Let the nodal coordinates in the physical domain be

$$\mathbf{x}_a=\begin{bmatrix}x_a\\y_a\end{bmatrix},\qquad a=1,\ldots,4.$$

We describe the position of any point inside the physical element using the shape functions defined above:

$$\mathbf{x}(\xi,\eta)=\sum_{a=1}^{4}N_a(\xi,\eta)\mathbf{x}_a$$

<!-- Therefore, -->

<!-- $$\mathbf{x}(\xi,\eta)=\begin{bmatrix}x(\xi,\eta)\\y(\xi,\eta)\end{bmatrix}=\sum_{a=1}^{4}N_a(\xi,\eta)\begin{bmatrix}x_a\\y_a\end{bmatrix}.$$

$$\mathbf{x}(\xi,\eta)=\begin{bmatrix}x(\xi,\eta)\\y(\xi,\eta)\end{bmatrix}=N_1\begin{bmatrix}x_1\\y_1\end{bmatrix}+N_2\begin{bmatrix}x_2\\y_2\end{bmatrix}+N_3\begin{bmatrix}x_3\\y_3\end{bmatrix}+N_4\begin{bmatrix}x_4\\y_4\end{bmatrix}.$$ -->

This provides a mapping

$$\boxed{(\xi,\eta)\longrightarrow(x,y)}$$

from the standard parent square to the actual physical element.

Now let us see the **iso** in the isoparametric element. In most structural analysis, the primary unknown field is the displacment, so lets take that. Suppose the unknown field is the displacement \(\mathbf{u}\). We interpolate the displacement using **the same shape functions**:

$$\mathbf{u}(\xi,\eta)=\sum_{a=1}^{4}N_a(\xi,\eta)\mathbf{u}_a$$

<!-- $$\mathbf{u}(\xi,\eta)=\begin{bmatrix}u(\xi,\eta)\\v(\xi,\eta)\end{bmatrix}=\begin{bmatrix}N_1 & N_2 & N_3 & N_4\end{bmatrix}\begin{bmatrix}u_1 & v_1\\u_2 & v_2\\u_3 & v_3\\u_4 & v_4\end{bmatrix}.$$

$$\mathbf{u}(\xi,\eta)=\begin{bmatrix}u(\xi,\eta)\\v(\xi,\eta)\end{bmatrix}=N_1\begin{bmatrix}u_1\\v_1\end{bmatrix}+N_2\begin{bmatrix}u_2\\v_2\end{bmatrix}+N_3\begin{bmatrix}u_3\\v_3\end{bmatrix}+N_4\begin{bmatrix}u_4\\v_4\end{bmatrix}.$$ -->

This is the essential meaning of **isoparametric**. The word *iso-parametric* means that the **same parameterization** is used for both the **geometry** and the **field variable**. That is,

$$\mathbf{x}(\xi,\eta)=\sum_a{\color{red}{N_a}}\mathbf{x}_a,\qquad\mathbf{u}(\xi,\eta)=\sum_a{\color{red}{N_a}}\mathbf{u}_a.$$

!!! info "Note"
    Notice that strain and stress are not independently required to use the same shape functions. Strain is obtained by differentiating the displacement field, while stress is subsequently obtained from the constitutive relation.

!!! warning "Work in Progress"
    Expanded and matrix forms of all summation terms to be added later.
    Refined till here, rest to be worked.



### The Jacobian

The physical coordinates depend on \(\xi\) and \(\eta\). Therefore,

$$
\frac{\partial x}{\partial \xi},
\quad
\frac{\partial x}{\partial \eta},
\quad
\frac{\partial y}{\partial \xi},
\quad
\frac{\partial y}{\partial \eta}
$$

describe how the parent element is stretched and distorted when mapped to the physical element.

We collect these quantities into the Jacobian matrix:

$$
\boxed{
\mathbf{J}
=
\frac{\partial(x,y)}{\partial(\xi,\eta)}
=
\begin{bmatrix}
\dfrac{\partial x}{\partial \xi}
&
\dfrac{\partial x}{\partial \eta}
\\[3mm]
\dfrac{\partial y}{\partial \xi}
&
\dfrac{\partial y}{\partial \eta}
\end{bmatrix}
}
$$

Since

$$
x=\sum_aN_a x_a,
\qquad
y=\sum_aN_a y_a,
$$

the Jacobian can be written as

$$
\mathbf{J}
=
\begin{bmatrix}
\displaystyle\sum_a\frac{\partial N_a}{\partial\xi}x_a
&
\displaystyle\sum_a\frac{\partial N_a}{\partial\eta}x_a
\\[3mm]
\displaystyle\sum_a\frac{\partial N_a}{\partial\xi}y_a
&
\displaystyle\sum_a\frac{\partial N_a}{\partial\eta}y_a
\end{bmatrix}.
$$

### Transforming derivatives

The displacement is known as a function of \((\xi,\eta)\), but the weak form generally requires derivatives with respect to the physical coordinates \((x,y)\).

Using the chain rule,

$$
\begin{bmatrix}
\dfrac{\partial}{\partial\xi}\\[2mm]
\dfrac{\partial}{\partial\eta}
\end{bmatrix}
=
\mathbf{J}^T
\begin{bmatrix}
\dfrac{\partial}{\partial x}\\[2mm]
\dfrac{\partial}{\partial y}
\end{bmatrix}.
$$

Therefore,

$$
\boxed{
\begin{bmatrix}
\dfrac{\partial}{\partial x}\\[2mm]
\dfrac{\partial}{\partial y}
\end{bmatrix}
=
\mathbf{J}^{-T}
\begin{bmatrix}
\dfrac{\partial}{\partial\xi}\\[2mm]
\dfrac{\partial}{\partial\eta}
\end{bmatrix}
}
$$

and consequently,

$$
\boxed{
\nabla\mathbf{u}
=
\nabla_{\xi,\eta}\mathbf{u}\,\mathbf{J}^{-1}
}
$$

depending on the adopted tensor convention.

Thus, derivatives of the shape functions with respect to the physical coordinates can be obtained from their derivatives with respect to the parent coordinates through the Jacobian.

This is one of the major computational advantages of the formulation.

### Transforming the integral

The second important consequence of the mapping is the transformation of the integration domain.

Suppose we have an integral over the physical element:

$$
\int_{\Omega_e}f(x,y)\,d\Omega.
$$

Using the mapping

$$
(\xi,\eta)\rightarrow(x,y),
$$

we obtain

$$
\boxed{
\int_{\Omega_e}f(x,y)\,d\Omega
=
\int_{-1}^{1}\int_{-1}^{1}
f(x(\xi,\eta),y(\xi,\eta))
\det(\mathbf J)
\,d\xi\,d\eta
}
$$

The physical element has therefore been replaced by the same standard square for every element.

This is the key reason why standard Gaussian quadrature can be used.

### Gaussian quadrature

For example, using a two-dimensional tensor-product Gauss rule,

$$
\int_{-1}^{1}\int_{-1}^{1}g(\xi,\eta)
\,d\xi\,d\eta
\approx
\sum_{i=1}^{n}\sum_{j=1}^{n}
w_iw_jg(\xi_i,\eta_j).
$$

Therefore,

$$
\boxed{
\int_{\Omega_e}f\,d\Omega
\approx
\sum_{i=1}^{n}\sum_{j=1}^{n}
w_iw_j
f(\xi_i,\eta_j)
\det\mathbf{J}(\xi_i,\eta_j)
}
$$

We should be precise here: Gaussian quadrature is **exact for polynomials up to degree \(2n-1\) in one dimension**, when \(n\) Gauss points are used.

However, an isoparametric mapping does not necessarily produce a polynomial integrand after transformation because terms such as \(\mathbf{J}^{-1}\) contain \(1/\det\mathbf{J}\). Therefore, the finite-element integral is generally evaluated approximately.

### But why not integrate directly over the physical element?

We could, in principle, formulate an integration scheme directly over every physical element.

The problem is that every element could have a different geometry, orientation, size, and distortion.

The isoparametric formulation instead maps every element to the same parent domain:

$$
\boxed{
\text{physical element}
\quad\longrightarrow\quad
\text{standard parent element}
}
$$

We can therefore use the same:

* shape functions,
* Gauss points,
* Gauss weights,
* integration procedure,
* derivative-transformation procedure,

for every element.

This provides a major computational and implementation advantage.

### Parent configuration versus reference configuration

There is one final distinction that is particularly important in finite-strain mechanics.

The parent coordinates

$$
(\xi,\eta)
$$

are **not** the same thing as the material reference coordinates

$$
\mathbf{X}.
$$

For example, in a total Lagrangian formulation, we may write

$$
\mathbf{X}(\xi,\eta)
=
\sum_aN_a(\xi,\eta)\mathbf{X}_a.
$$

Here the parent element is mapped to the **reference configuration**:

$$
\boxed{
(\xi,\eta)\longrightarrow\mathbf{X}
}
$$

The corresponding Jacobian is

$$
\mathbf{J}_0
=
\frac{\partial\mathbf{X}}
{\partial(\xi,\eta)}.
$$

On the other hand, the current configuration is

$$
\mathbf{x}(\xi,\eta)
=
\sum_aN_a(\xi,\eta)\mathbf{x}_a,
$$

giving

$$
\mathbf{J}_t
=
\frac{\partial\mathbf{x}}
{\partial(\xi,\eta)}.
$$

The deformation gradient is a different mapping:

$$
\boxed{
\mathbf{F}
=
\frac{\partial\mathbf{x}}{\partial\mathbf{X}}
}
$$

and the three mappings are related through

$$
\boxed{
\mathbf{J}_t=\mathbf{F}\mathbf{J}_0
}
$$

or equivalently,

$$
\boxed{
\mathbf{F}
=
\mathbf{J}_t\mathbf{J}_0^{-1}.
}
$$

Therefore, the parent element is simply a **computational parameter domain**. Depending on the formulation, it can be mapped to the reference configuration, current configuration, or another configuration.

### The main idea

The entire isoparametric formulation can therefore be summarized as:

$$
\boxed{
\text{Parent element}
\overset{\text{shape functions}}{\longrightarrow}
\text{physical element}
}
$$

while using the same shape functions to represent the primary field:

$$
\boxed{
\mathbf{x}=\sum_aN_a\mathbf{x}_a,
\qquad
\mathbf{u}=\sum_aN_a\mathbf{u}_a.
}
$$

This gives us a systematic way to:

1. represent arbitrary element geometries,
2. transform derivatives using the Jacobian,
3. transform physical integrals to a standard domain, and
4. evaluate those integrals using the same Gaussian quadrature procedure for every element.

The important conceptual point is that **isoparametric does not mean "reference configuration."** It means that the geometry and the primary field are represented using the same shape functions in terms of the same parent coordinates.
