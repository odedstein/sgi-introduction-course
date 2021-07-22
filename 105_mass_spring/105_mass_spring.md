# Mass-Spring Systems
It's happening! We're finally making compelling animations with the help of physics. In the real world, physics is deterministic: if we know the current state, we can be sure of what the next state will be (at least at the scales we're considering). This is also true for our physical simulation: given initial conditions e.g. each material point's starting position and velocity, we'll be able to create an animation of rigid and deformable objects following the laws of physics forward in time, and reproduce a wide variety of real-world phenomena.

Physics-based animation leverages techniques from classical mechanics, numerical solutions of ordinary and partial differential equations (and many more!!). In this exercise, to make our life easier, we consider a 2-dimensional mass-spring system to model the shape's physical behavior. Thus, we can think of our shape as a curve living in 2d where each vertex is a point mass, and each edge is a spring.

<p align="center">
    <img src="./assets/mass-spring.png" width="50%">
</p>

To consider a shape's dynamical behavior, we always start from Newton's second law i.e. <img src="./svgs/adb1848d6bcc268741b2159e2b1cd095.svg?invert_in_darkmode" align=middle width=53.10859125pt height=22.8310566pt/> where <img src="./svgs/3dd792263ccad28e59bb12f8251ca878.svg?invert_in_darkmode" align=middle width=50.6391039pt height=26.7617526pt/> is the force acting on a body, <img src="./svgs/37dc7590055031b155222eec1b1ee672.svg?invert_in_darkmode" align=middle width=48.7022448pt height=22.5570873pt/> is the shape's mass and <img src="./svgs/778bc9827ead68d23ad072dee8c9a151.svg?invert_in_darkmode" align=middle width=49.51084545pt height=26.7617526pt/> is the acceleration. A single spring is defined by its stiffness <img src="./svgs/f9bbd08bf846520586581437c960abac.svg?invert_in_darkmode" align=middle width=39.21220215pt height=22.8310566pt/>, rest length <img src="./svgs/a8ebec72f0419145acebff41d5f6c225.svg?invert_in_darkmode" align=middle width=53.26274745pt height=22.5570873pt/> and the current mass positions <img src="./svgs/e3bd31ed3ead9eee1fbf36a01ec5856c.svg?invert_in_darkmode" align=middle width=77.06790795pt height=26.7617526pt/>. Its potential energy measures the squared difference of the current length and the rest length times the stiffness (Well the mighty Hooke's Law from high shcool physics):

<p align="center"><img src="./svgs/dd508e5d1a0309c50b4effea67a5dd5f.svg?invert_in_darkmode" align=middle width=245.46504675pt height=32.990166pt/></p>

The force exerted by the spring on each mass is the partial derivative of the elastic potential energy <img src="./svgs/a9a3a4a202d80326bda413b5562d5cd1.svg?invert_in_darkmode" align=middle width=13.24203705pt height=22.4657235pt/> with respect to the corresponding mass position. For example, for <img src="./svgs/f13e5bc0860402c82f869bcf883eb8b0.svg?invert_in_darkmode" align=middle width=15.15312645pt height=14.6118786pt/> we have

<p align="center"><img src="./svgs/5a34945ecb0a35264230b60fbafbcfb4.svg?invert_in_darkmode" align=middle width=127.8270213pt height=37.0084374pt/></p>

We'll assume we know the current positions for each mass <img src="./svgs/4e6aac200b5f6f92fab0cb5357f3641a.svg?invert_in_darkmode" align=middle width=57.11160675pt height=26.7617526pt/> at the current time (<img src="./svgs/4f4f4e395762a3af4575de74c019ebb5.svg?invert_in_darkmode" align=middle width=5.93609775pt height=20.2218027pt/>) and the current velocities <img src="./svgs/b2cb7e2cbb1018aace98f006fc8ea7aa.svg?invert_in_darkmode" align=middle width=147.16191105pt height=26.7617526pt/>. When <img src="./svgs/1c899e1c767eb4eac89facb5d1f2cb0d.svg?invert_in_darkmode" align=middle width=36.0729369pt height=21.1872144pt/> then we call these the initial conditions of the entire simulation. For <img src="./svgs/41163b95295e685e3f25bc73af21a8fb.svg?invert_in_darkmode" align=middle width=36.0729369pt height=21.1872144pt/>, we can still think of these values as the initial conditions for the remaining time.

In the real world, the trajectory of an object follows a continuous curve as a function of time. In our simulation, we only need to know the position of each pass at discrete moments in time. We use this to build discrete approximation of the time derivatives (velocities and accelerations) that we encounter. Immediately, we can replace the current velocties <img src="./svgs/0b39cd3b1c07dcc4dcbea210f38358ec.svg?invert_in_darkmode" align=middle width=15.46801905pt height=26.0859621pt/> with a backward finite difference of the positions over the small time step:

<p align="center"><img src="./svgs/5a2c6cddab32462002913617658dbf8f.svg?invert_in_darkmode" align=middle width=118.8900603pt height=37.29153615pt/></p>

where <img src="./svgs/eb1dcd0788eedbaa067d86a516cb9d5d.svg?invert_in_darkmode" align=middle width=83.1505092pt height=29.7899547pt/> is the vertex position at the previous time step.

Similarly, we can also use a central finite difference to define the acceleration at time <img src="./svgs/4f4f4e395762a3af4575de74c019ebb5.svg?invert_in_darkmode" align=middle width=5.93609775pt height=20.2218027pt/>:

<p align="center"><img src="./svgs/e86de69b55074d2bba995d8d6f1b899d.svg?invert_in_darkmode" align=middle width=621.88096245pt height=37.29153615pt/></p>

This expression mentions our unknown variables <img src="./svgs/60cd486c9b59db93b3a4fad0605ccebb.svg?invert_in_darkmode" align=middle width=41.32432425pt height=29.7899547pt/> for the first time. Based on the previous time steps solving unknown variables <img src="./svgs/60cd486c9b59db93b3a4fad0605ccebb.svg?invert_in_darkmode" align=middle width=41.32432425pt height=29.7899547pt/> for the next step becomes our goal and we'll soon show how these can be solved by casting physics simulation into an energy optimization problem.

### Time integration as energy optimization
Solving for the unknown variables <img src="./svgs/60cd486c9b59db93b3a4fad0605ccebb.svg?invert_in_darkmode" align=middle width=41.32432425pt height=29.7899547pt/> of the next time step boils down to solving the equation <img src="./svgs/f428e42f1278299d021e503dfeb2f94f.svg?invert_in_darkmode" align=middle width=53.10859125pt height=22.8310566pt/>. Although the acceleration term <img src="./svgs/41f28962986ecdd9c1dc2af8b83fef84.svg?invert_in_darkmode" align=middle width=9.1894341pt height=14.6118786pt/> depends linearly on the unknowns <img src="./svgs/61cf41460b5d444b8df90703eb5ef637.svg?invert_in_darkmode" align=middle width=41.32432425pt height=27.6567522pt/>, unfortunately even for a simple spring the forces <img src="./svgs/c0b31e02ffb7134d190a55acd456c67b.svg?invert_in_darkmode" align=middle width=109.7259174pt height=27.6567522pt/> depend non-linearly on <img src="./svgs/61cf41460b5d444b8df90703eb5ef637.svg?invert_in_darkmode" align=middle width=41.32432425pt height=27.6567522pt/>. This means we have a non-linear system of equations, which can be tricky to solve directly.

Alternatively, in this exercise we will take a variational perspective i.e. view physics simulation as an optimization problem. We will define an energy that will be minimized by the value of <img src="./svgs/61cf41460b5d444b8df90703eb5ef637.svg?invert_in_darkmode" align=middle width=41.32432425pt height=27.6567522pt/> that satisfies <img src="./svgs/f428e42f1278299d021e503dfeb2f94f.svg?invert_in_darkmode" align=middle width=53.10859125pt height=22.8310566pt/>. You will probably find this familiar if you have taken a variational mechanics class. The minimizer <img src="./svgs/980fcd4213d7b5d2ffcc82ec78c27ead.svg?invert_in_darkmode" align=middle width=10.5022269pt height=14.6118786pt/> of some function <img src="./svgs/29caae963fbe810e18a545ca36f0c169.svg?invert_in_darkmode" align=middle width=36.3698379pt height=24.657534pt/> will satisfy <img src="./svgs/50eff1c869952649a256668f39a1a6be.svg?invert_in_darkmode" align=middle width=82.4540607pt height=24.657534pt/>. So we construct an energy <img src="./svgs/84df98c65d88c6adf15d4645ffa25e47.svg?invert_in_darkmode" align=middle width=13.0821966pt height=22.4657235pt/> such that <img src="./svgs/1659b79562bb1cb2d662028a17b053cf.svg?invert_in_darkmode" align=middle width=155.6538423pt height=24.657534pt/>:

<p align="center"><img src="./svgs/1e170ae0eb32b9f3a8d4af4aa1256323.svg?invert_in_darkmode" align=middle width=733.65237495pt height=59.1786591pt/></p>


where, in our case, <img src="./svgs/6be6c3f773137fe769edcd81b92b4fba.svg?invert_in_darkmode" align=middle width=72.3438771pt height=26.0859621pt/> is the gravity exerted on all the masses ang <img src="./svgs/b55cebd57d98b8b971bcb3376f25d605.svg?invert_in_darkmode" align=middle width=50.53626435pt height=26.7617526pt/> is the gravitational acceleration. Keen observers will identify that the first term is our elastic potential energy <img src="./svgs/a9a3a4a202d80326bda413b5562d5cd1.svg?invert_in_darkmode" align=middle width=13.24203705pt height=22.4657235pt/>, the second term resembles kinetic energy and the last term is the gravitational potential energy.

Alright, now we have our objective function to optimize. But still, it looks somewhat messy and hard to deal with. Before looking for ways to solve it computationally, we leverage the matrix notation to convert the above function into a more compact form. We will stack up all of the <img src="./svgs/55a049b8f161ae7cfeb0197d75aff967.svg?invert_in_darkmode" align=middle width=9.86687625pt height=14.1552444pt/> unknown mass positions <img src="./svgs/e257b7a1307d19169e36e12a3f140bdc.svg?invert_in_darkmode" align=middle width=56.7967158pt height=26.7617526pt/> as a column vector <img src="./svgs/d42c0343814f1bf20a40ce42109d8d4a.svg?invert_in_darkmode" align=middle width=59.4499422pt height=26.7617526pt/> such that

<p align="center"><img src="./svgs/d0c753c4b26c2fc6ac00b03539f58bcc.svg?invert_in_darkmode" align=middle width=79.98652035pt height=216.9884838pt/></p>


 We can do the same for the known previous time steps' positions <img src="./svgs/15aef991cebbf885df94a7b019c5e8c5.svg?invert_in_darkmode" align=middle width=114.8723301pt height=27.6567522pt/>.

 We can then, for example, express the inertial term using matrices:

<p align="center"><img src="./svgs/df30579bf527eb6b4476d2487dc01063.svg?invert_in_darkmode" align=middle width=715.7886252pt height=99.42909735pt/></p>

where <img src="./svgs/c86080e161350406e3815e409ef7f8eb.svg?invert_in_darkmode" align=middle width=91.64002155pt height=26.7617526pt/> is a diagonal matrix with the diagonal entries being the corresponging point mass <img src="./svgs/0e51a2dede42189d77627c4d742822c3.svg?invert_in_darkmode" align=middle width=14.4331011pt height=14.1552444pt/> i.e. <img src="./svgs/c77736a9a18701ee9f8b4a2671151cd4.svg?invert_in_darkmode" align=middle width=67.0728201pt height=22.4657235pt/>. <img src="./svgs/fb97d38bcc19230b0acd442e17db879c.svg?invert_in_darkmode" align=middle width=17.7397374pt height=22.4657235pt/> is often called the mass matrix.

## Task 1: Derivation
In this task, express the gravitational potential energy using matrices, similar to the inertial term. (Notice that the matrix form for the elastic potential energy can be too complicated to write down so we simply leave it as <img src="./svgs/ff7c739f92afe11880a6d085713db7be.svg?invert_in_darkmode" align=middle width=34.29803025pt height=24.657534pt/> for now.)

## Task 2: Newton's method
Now we have our objective function in hand. To solve this energy minimization problem, there are many effective optimization techniques that can be applied. Following what we learned from the lecture, we use Newton's method to compute the local minimum of our objective function by solving a sequence of quadratic functions. At the <img src="./svgs/77a3b857d53fb44e33b53e4c8b68351a.svg?invert_in_darkmode" align=middle width=5.6632257pt height=21.6830097pt/>th Newton iteration, we solve for the newton update <img src="./svgs/ffed04f34013aa39526b0a3d1819253c.svg?invert_in_darkmode" align=middle width=28.85179935pt height=22.4657235pt/> s.t. <img src="./svgs/97a7156a28f084ab44e542c88959bdd6.svg?invert_in_darkmode" align=middle width=119.63720835pt height=22.4657235pt/> by doing Taylor expansion of our objective around <img src="./svgs/6fe8024b4513e51e4f386d07825e1509.svg?invert_in_darkmode" align=middle width=31.97969445pt height=14.6118786pt/> up to the second order:

<p align="center"><img src="./svgs/14a4d09bb4cf1946920750e0df997f7f.svg?invert_in_darkmode" align=middle width=774.6358587pt height=35.2393965pt/></p>

where <img src="./svgs/71e80f2e4a91923dda27257b3fcc7c6f.svg?invert_in_darkmode" align=middle width=60.4499412pt height=24.657534pt/> and <img src="./svgs/a7d57a101ca8e857d850a0dbcbb3966f.svg?invert_in_darkmode" align=middle width=60.40427415pt height=24.657534pt/> are the gradient and hessian of the elastic potential energy <img src="./svgs/a9a3a4a202d80326bda413b5562d5cd1.svg?invert_in_darkmode" align=middle width=13.24203705pt height=22.4657235pt/> evaluated at <img src="./svgs/6fe8024b4513e51e4f386d07825e1509.svg?invert_in_darkmode" align=middle width=31.97969445pt height=14.6118786pt/>.

The solution to this minimization problem is found by solving

<p align="center"><img src="./svgs/dafd9b9fa2f85450359026e65f0dd310.svg?invert_in_darkmode" align=middle width=93.45200865pt height=14.4748956pt/></p>

where <img src="./svgs/930b956ef51654e0669455a2cdd62fb5.svg?invert_in_darkmode" align=middle width=14.7944511pt height=22.5570873pt/> and <img src="./svgs/5f3cc59831e6b4aef298a2dacada3fe7.svg?invert_in_darkmode" align=middle width=9.7145763pt height=14.6118786pt/> are the hessian and gradient of the above quadratic energy respectively.

Hint: Write down <img src="./svgs/930b956ef51654e0669455a2cdd62fb5.svg?invert_in_darkmode" align=middle width=14.7944511pt height=22.5570873pt/> and <img src="./svgs/5f3cc59831e6b4aef298a2dacada3fe7.svg?invert_in_darkmode" align=middle width=9.7145763pt height=14.6118786pt/> first. Also the helper function `mass_spring_hessian_gradient.m` gives you the gradient and hessian of the elastic potential energy evaluated at <img src="./svgs/2ec6e630f199f589a2402fdf3e0289d5.svg?invert_in_darkmode" align=middle width=8.27056725pt height=14.1552444pt/>.

To get interesting dynamics, we also need some certain boundary conditions. For example, fix some of the masses such that the whole system doesn't immediately fall off because of the gravity. Hint: in `102_min_quad_with_fixed` you have learned how to solve a quadratic problem with fixed value constraint. How could it be helpful here?

Once it is sucessfully implemented, you will get a fun mass-spring system!
<p align="center">
    <img src="./assets/mass-spring.gif" width="50%">
</p>

## Fun Challenge
Convert an arbitrary 2D mesh into a graph of point masses and springs and make it wiggle! Furthermore, extend the current framework to 3D and get a waving flag as shown below :D
<p align="center">
    <img src="./assets/flag.gif" width="50%">
</p>
<p align="center">
(image source: Alec Jacobson)
</p>