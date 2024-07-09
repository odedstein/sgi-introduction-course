# PyTorch Basics

In this module, we will learn how to use basic PyTorch commands to perform an optimization. There are no exercises to complete for this module, but it is suggested that you follow along in the command line and in the file pytorch_demo.py

## PyTorch Overview
PyTorch is a python library for built for optimization. PyTorch is very similar to NumPy. In fact, most PyTorch functions have the same name as their NumPy counterparts. The main difference is that PyTorch supports [automatic differentiation](https://pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html). PyTorch builds a computation graph to keep track of all operations that you run. Then, if you want to compute the gradient of some value with respect to your parameters, you can call the `backwards()` method on that value and PyTorch will automatically differentiate through the graph of operations to give you the desired gradient. This allows us to easily perform gradient descent to optimize parameters. It is especially helpful when we have complex parametric representations which would otherwise require tedious manual calcutions of derivatives.


## Installing Pytorch
To install pytorch, first confirm we have our geometry processing environment activated. If not, run the following command to activate it.
```
source gp/bin/activate
```
Now we want to install the PyTorch library. Follow the instructions for your specific operating system below.

```
# Mac
pip install torch==2.1.1 torchvision==0.16.1 torchaudio==2.1.1

# Linux and Windows
pip install torch==2.1.1 torchvision==0.16.1 torchaudio==2.1.1 --index-url https://download.pytorch.org/whl/cpu
```
Now that PyTorch is installed, let's try to import the library. Boot up Python (by running `python` in the terminal) and try to import PyTorch.
```
>>> import torch
```
Now confirm that the import worked by checking PyTorch's version.
```
>>> torch.__version__
'2.1.1'
```

## Notation Differences from NumPy
Before we start coding in PyTorch, let's go over a few of the minor differences between NumPy and PyTorch notation.
- PyTorch works with "Tensors" instead of "Arrays" but conceptually these two structures are the same. So anywhere you would write `np.array()` switch it to `torch.tensor()` when using PyTorch.
- Instead of using `axis` like NumPy does to specify which dimension to perform the operation on, PyTorch uses the `dim` keyword, however, the functionality is essentially the same. One slight difference is that certain pytorch functions (for example `torch.cross`) have different default values for the `dim` argument than NumPy equivalents have for the `axis` argument so it is helpful to explicitly specify the `dim` argument if you are ever unsure.
- If you are ever unsure, a quick google search for "PyTorch equivalent of <some_numpy_function>" can be quite helpful.

## PyTorch Demo
We will now go through a short demo to see how we can use PyTorch to optimize a parameter. You can follow along by running these commands in your own python file. All code for this demo is also contained in [pytorch_demo.py](pytorch_demo.py).

### Quick High Level Review of Gradient Descent
Given some `parameters`, a parametric function `f(parameters)`, and some `target_value`, we want to figure out how to update the `parameters` so that when we evaluate our function `f` on those `parameters`, we get a value close to our `target_value`. This can be accomplished with the folowing steps:

1) Determine the direction in which to change our `parameters` so that the parameterized function value moves closer to our `target_value`
    - Compute some loss or measure of “closeness” between our current function evaluation and our `target_value`
    - Compute the gradient of this loss w.r.t. our `parameters`
2) Take a small step in that direction
3) Repeat this process over and over until we get “close enough” to our `target_value`

### Setup Our Optimization
Let's start our demo by importing pytorch. Add the following line to the top of your file.
```
import torch
```

Now let's continue by initializing some parameter that we want to optimize.
```
param = torch.Tensor([0])
param = torch.nn.Parameter(param)
```
In the above code, we first initilize our parameter to 0. Then in the second line, we wrap it with the `nn.Parameter` function to tell PyTorch that we want this variable to be a parameter that can be optimized.

Now that we have our parameter, we can initialize an optimizer that will be responsible for updating the value of that parameter based on the gradient update directions we compute. To do so, add the following code:
```
optim = torch.optim.Adam([param], lr=1e-2)
```
Here we set tell the optimizer to use our `param` variable as the parameter and to use a learning rate of `0.01` (how big we want our optimization steps to be / what to scale our update direction by).

In this simple example, we will use the function `f(x) = 2x - 3` as our parametric function:
```
def f(x):
    return 2*x - 3
```

### Computing our loss
So far our file should look like something this:
```
import torch

param = torch.Tensor([0])
param = torch.nn.Parameter(param)

optim = torch.optim.Adam([param], lr=1e-2)

def f(x):
    return 2*x - 3
```

Now we want to add our loss calculation. Let's say we want our target function value to be `7`. Because this function is so simple, we can directly solve for x to get that `x=5`. However, in most cases, our function is not this simple and might not have a closed form solution and we need to use optimzation.

To calculate our loss (the measure of "closeness" between our target value and and current function evaluation) we will use the square of the difference between `7` (our target value) and `f(param)` (the value we get when evaluating our function on our parameter).
```
target = 7
loss = (target - f(param))**2
```

### Performing our optimization
In order to actually optimize our parameter we need to set up an optimization loop.
```
total_iterations = 2000
target = 7

for iteration in range(total_iterations):
    optim.zero_grad()
    loss = (target - f(param))**2
    loss.backward()
    optim.step()
```
The above for first defines the total number of iterations the optimization will run for and the target value. Then it enters a for loop that for each iteration:
1) resets the gradients
2) computes the loss
3) backpropagate gradients to our parameter
4) takes a step in the direction indicated by our gradients

After this for loop finishes, we can check the value of our parameter. If all has gone to plan, it should be very close to `5`!
```
print(param.item())
```

At this point our file should look something like this:
```
import torch

param = torch.Tensor([0])
param = torch.nn.Parameter(param)

optim = torch.optim.Adam([param], lr=1e-2)

def f(x):
    return 2*x - 3

total_iterations = 2000
target = 7

for iteration in range(total_iterations):
    optim.zero_grad()
    loss = (target - f(param))**2
    loss.backward()
    optim.step()

print(param.item())
```

If you haven't already try running the above code in a python file or in python in the terminal. You may also run the file `pytorch_demo.py` which has all of the same components.