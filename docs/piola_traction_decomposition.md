### Reference and Current Normals in the Piola Traction Decomposition

The following section discusses a small clarification of the use of normal vectors while decomposing the traction into a normal and tangential component.
This centers around the [first equation under section 1.3 of this paper](https://www.sciencedirect.com/science/article/pii/S0045782516318448) by Mlika et. al..
In finite-deformation contact mechanics, we need to distinguish carefully between the reference configuration and the current configuration.

Let

- $\boldsymbol{N}$ be the unit normal to the material surface in the **reference configuration**,
- $\boldsymbol{n}_x$ be the unit normal to the corresponding surface in the **current configuration**.

The first Piola–Kirchhoff stress is a two-point tensor. It maps a reference vector to a current vector:

$$\underline{\underline{\boldsymbol{\hat{\sigma}}}}:\text{reference vector}\longrightarrow\text{current vector}.$$

Therefore,

$$\boxed{\boldsymbol{q}=\underline{\underline{\boldsymbol{\hat{\sigma}}}}\cdot\boldsymbol{N}}$$

is a **current/spatial vector**, even though it is obtained by operating on the reference normal $\boldsymbol{N}$. This $\boldsymbol{q}$ is what we call as the Piola traction vector.

---

### The decomposition of the Piola traction

Let us see how it is decomposed in the normal and tangent components. Following is the equation cited above that we will focus on:

$$\underline{\underline{\boldsymbol{\hat{\sigma}}}}\cdot\boldsymbol{N}=\hat{\sigma}_n\boldsymbol{n}_x+\boldsymbol{T}_{\boldsymbol{n}_x}\cdot\left(\underline{\underline{\boldsymbol{\hat{\sigma}}}}\cdot\boldsymbol{N}\right)$$

At first sight, $\boldsymbol{N}$ and $\boldsymbol{n}_x$ appear to be mixed. The key insight is that they perform **different operations**. The reference normal vector, $\boldsymbol{N}$, is used to obtain the Piola traction as shown above. To repeat, a two point tensor that is $\underline{\underline{\boldsymbol{\hat{\sigma}}}}$ operates on a vector in the reference configuration that is $\mathbf{N}$ to yield a vector in the current configuration that is $\boldsymbol{q}$, the Piola traction vector. Since $\boldsymbol{q}$ is a current configuration/spatial vector, we can therefore decompose it using the current normal $\boldsymbol{n}_x$. Before we do that, let us revisit the tangent projection operator.


!!! tip "The tangent projection operator ($\boldsymbol{T}_\boldsymbol{n}$)"

    The operator $\boldsymbol{T}_\boldsymbol{n}$ refers to the projection of a vector on a tangent plane whose normal vector is $\boldsymbol{n}$. It is defined as:

    $$\boldsymbol{T}_{\boldsymbol{n}_x}=\underline{\underline{\boldsymbol{I}}}-\boldsymbol{n}_x\otimes\boldsymbol{n}_x$$

    Notice that the corresponding decomposition of the identity can be written using the above equation as:

    $$\underline{\underline{\boldsymbol{I}}}=\boldsymbol{n}_x\otimes\boldsymbol{n}_x+\boldsymbol{T}_{\boldsymbol{n}_x}.$$


Using the above operator and the decomposition of the identity, we manipulate the Piola traction vector as follows:

$$
\begin{align*}
\boldsymbol{q}
&= \underline{\underline{\boldsymbol{I}}}\cdot\boldsymbol{q} \\
&= \left(\boldsymbol{n}_x\otimes\boldsymbol{n}_x\right)\cdot\boldsymbol{q}+\boldsymbol{T}_{\boldsymbol{n}_x}\cdot\boldsymbol{q} \\
&= \boldsymbol{n}_x\left(\boldsymbol{n}_x\cdot\boldsymbol{q}\right)+\boldsymbol{T}_{\boldsymbol{n}_x}\cdot\boldsymbol{q}\\
&= \left(\boldsymbol{q}\cdot\boldsymbol{n}_x\right)\boldsymbol{n}_x+\boldsymbol{T}_{\boldsymbol{n}_x}\cdot\boldsymbol{q}
\end{align*}
$$

or,

$$\underline{\underline{\boldsymbol{\hat{\sigma}}}}\cdot\boldsymbol{N} = \hat{\sigma}_n\boldsymbol{n}_x+\boldsymbol{T}_{\boldsymbol{n}_x}\cdot\left(\underline{\underline{\boldsymbol{\hat{\sigma}}}}\cdot\boldsymbol{N}\right)$$

which is the same as the equation we saw initially. The first term is the component normal to the **current** surface, while the second term is tangent to the **current** surface. Notice that we have defined the **scalar** normal component as:

$$\hat{\sigma}_n=\left(\boldsymbol{q}\cdot\boldsymbol{n}_x\right)=\left(\underline{\underline{\boldsymbol{\hat{\sigma}}}}\cdot\boldsymbol{N}\right)\cdot\boldsymbol{n}_x$$

!!! tip "The whole operation can be viewed as"

    $$\boxed{\boldsymbol{N}\xrightarrow{\;\underline{\underline{\boldsymbol{\hat{\sigma}}}}\;}\underbrace{\underline{\underline{\boldsymbol{\hat{\sigma}}}}\cdot\boldsymbol{N}}_{\text{spatial Piola traction}}\xrightarrow{\;\boldsymbol{n}_x\;}\underbrace{\hat{\sigma}_n\boldsymbol{n}_x}_{\text{normal}}+\underbrace{\boldsymbol{T}_{\boldsymbol{n}_x}\cdot\left(\underline{\underline{\boldsymbol{\hat{\sigma}}}}\cdot\boldsymbol{N}\right)}_{\text{tangential}}.}$$