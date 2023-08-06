import matplotlib.pyplot as plt
import numpy as np

from .estimate_pi import *

def plot_darts(ndarts, circle=True):
    """
    Function that displays a throw of darts and highlights darts in the unit circle with a different colour

    Parameters
    ----------
    ndarts : int
        number of dart throws
    circle : bool, optional
        if True, draw the boundary

    Returns
    -------
    None
    """
    darts = throw(ndarts)
    incircle = is_in_unit_circle(darts)

    plt.figure(figsize=(5,5))
    plt.plot(darts[0, ~incircle], darts[1, ~incircle], '.', label = 'not in unit circle')
    plt.plot(darts[0,incircle], darts[1,incircle], '.', label = 'in unit circle')
    plt.gca().set_aspect('equal')
    plt.legend()

    if circle: draw_circle(r=1)
    return

def draw_circle(r=1,x0=0,y0=0):
    """ Simple function to draw a circle with radius r centered at x0, y0 on the current axis

    Parameters
    ----------
    r : float
        radius of the circle
    x0, y0 : float
        center of the circle
    """
    theta = np.linspace(0,2*np.pi)
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    plt.plot(x,y,'k:')
