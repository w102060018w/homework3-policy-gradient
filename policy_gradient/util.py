from gym.spaces import Box, Discrete
import numpy as np
from scipy.signal import lfilter
import math, scipy
import matplotlib.pyplot as plt
plt.style.use('ggplot')

def flatten_space(space):
    if isinstance(space, Box):
        return np.prod(space.shape)
    elif isinstance(space, Discrete):
        return space.n
    else:
        raise ValueError("Env must be either Box or Discrete.")

def discount_cumsum(x, discount_rate):
    # x is the immediate reward, length(num_r) is the time-step t to the end of the episode
    discounted_r = np.zeros(len(x))
    num_r = len(x)
    for i in range(num_r):
        discounted_r[i] = x[i]*math.pow(discount_rate,i)
    discounted_r = np.cumsum(discounted_r[::-1])
    return discounted_r[::-1]

def discount_bootstrap(x, discount_rate, b):
    """
    Args:
        x: the immediate reward for each timestep. e.g. [1, 1, 0]
        discount_factor: the \gamma in standard reinforcement learning
        b: the prediction of the baseline. e.g. [1.3, 0.4, 0.2]
    Returns: a numpy array y = r(s_t,a,s_{t+1}) + \gamma*V_t 
             (the shape of it should be the same as the `x` and `b`)
    Sample code should be about 3 lines
    """
    #V_t is the baseline
    #r is the immediate reward
    #Formula: A_t = r_t + gamma*V_t+1 - V_t
    #Formula: A_t = discounted_bootstrap - V_t
    L = len(x)
    b_shift = np.roll(b, L-1)
    b_shift[-1] = 0.0
    return x + discount_rate*b_shift
    
def plot_curve(data, key, filename=None):
    # plot the surrogate loss curve
    x = np.arange(len(data))
    plt.plot(x, data)
    plt.xlabel("iterations")
    plt.ylabel(key)
    if filename is not None:
        plt.savefig(filename)
    plt.show()
    plt.close()

def discount(x, discount_factor):
    return scipy.signal.lfilter([1.0], [1.0, -discount_factor], x[::-1])[::-1]

