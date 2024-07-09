import torch

torch.manual_seed(42)

def optimize(param, num_iterations, func, loss_fn, target, lr=1e-2):
    """
    A function the optimizes a parameter according to a loss function.

    Args:
        param (torch.Tensor): The parameter to optimize
        num_iterations (int): The number of iterations to optimize the parameter
        func (callable): The function to evaluate the parameter on
        loss_fn (callable): The function to compute the loss between the function evaluation and the target
        target (float): The target value to optimize the parameter towards
        lr (float): The learning rate for the optimizer
    
    Returns:
        torch.Tensor: The optimized parameter
    """
    # Tell PyTorch that this parameter should be an optimizable value
    param = torch.nn.Parameter(param)
    # Register our parameter with the optimizer and set the learning rate
    optim = torch.optim.Adam([param], lr=lr)


    for i in range(num_iterations):
        optim.zero_grad() # reset our gradients
        y = func(param) # evaluate our function
        loss = loss_fn(y, target) # compute our loss
        loss.backward() # backpropagate gradients to our parameter
        optim.step() # take a step in the direction indicated by our gradients

        if i % (num_iterations // 3) == 0:
            print(f"Iteration: {i}, Loss: {loss.item()}, Param: {param.item()}")
    
    return param

def f(x):
    """
    The function we are evaluating our parameter on.
    Here we use: f(x) = 2x - 3

    Args:
        x (torch.Tensor): The parameter to evaluate the function on
    
    Returns:
        torch.Tensor: The result of the function evaluation
    """
    return 2*x - 3

def loss_fn(target, y):
    """
    Computes a loss between our target value (target) and the function evaluation (y)
    The result of this function will be minimized by the optimizer.

    Args:
        target (float): The target value to optimize the parameter towards
        y (torch.Tensor): The result of the function evaluation
    
    Returns:
        torch.Tensor: The loss between the target and the function evaluation
    """
    return (target - y)**2


# Setup our variables
param = torch.rand(1)
target = 7
num_iterations = 2000
learning_rate = 1e-2

# Optimize our parameter
param = optimize(
    param=param,
    num_iterations=num_iterations,
    func=f,
    loss_fn=loss_fn,
    target=target,
    lr=learning_rate
)
print('Optimized value:', param.item())
