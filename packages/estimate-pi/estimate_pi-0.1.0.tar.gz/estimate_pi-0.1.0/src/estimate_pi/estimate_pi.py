import numpy as np


def throw(ndarts):
    """Function that *throws n darts*

    This functions generates n sets of coordinates that are each drawn from a uniform distribution between -1 and 1

    Parameters
    ----------
    ndarts : int
        Number of coordinates to draw (darts to throw).

    Returns
    -------
    darts : array
        array of size (2xn) with the coordinates of darts thrown.
    """
    return (np.random.rand(2, ndarts) - 0.5) * 2


def is_in_unit_circle(dart):
    """Checks if a dart is in the unit circle

    function that checks whether a coordinate `dart` is inside the unit circle

    Parameters
    ----------
    dart : array
        Array of coordinates (dart positions) with size (2xn)

    Returns
    -------
    isincircle : array (boolean)
        Array of size n set to `True` where `dart` is in the unit circle, false otherwise.
    """

    # Distance to origin for each dart
    distance = np.sqrt(np.sum(dart**2, axis=0))

    isincircle = distance < 1

    return isincircle


def estimate_pi(ndarts):
    """Function that estimates pi using the 'throw of darts' method

    Parameters
    ----------
    ndarts : int
        number of darts to throw

    Returns
    -------
    pi : float
        An estimate for pi
    """
    darts = throw(ndarts)
    incircle = is_in_unit_circle(darts)
    return 4.0 * np.sum(incircle) / ndarts


def make_realisation(nrea, ndarts):
    """function that makes `nrea` realisations of `ndarts` dart throws and records the result

    Parameters
    ----------
    nrea : int
        number of realisation
    ndarts : int
        number of darts thrown at each realisation

    Returns
    -------
    pies : array
        array of the estimates of pi at each iteration
    """
    pies = []

    [pies.append(estimate_pi(ndarts)) for i in range(nrea)]
    return np.array(pies)


def get_pi_accuracy(nrea, nthrows):
    """
    Function that plots the mean and standard deviation of the results of `nrea` realisations
    of dart `nthrows` dart throws

    Parameters
    ----------
    nrea : int
        number of realisations of throws for each number of throws
    nthrows : array
        array containing numbers of throws for which we want `nrea` realisations

    Returns
    -------
    mean : array
        mean estimates
    std : array
        errors
    None
    """
    mean = []
    std = []
    for throw in nthrows:
        realisations = make_realisation(nrea, throw)
        mean.append(realisations.mean())
        std.append(realisations.std())
    return np.array(mean), np.array(std)
