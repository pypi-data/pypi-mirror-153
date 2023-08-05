"""
Root-finding solver based on Brent's method

See `<https://en.wikipedia.org/wiki/Brent%27s_method>`_
"""
# pylint: disable=C0103

from dataclasses import dataclass
from typing import Callable, Optional, Tuple

from rich.console import Console
from rich.table import Table

__version__ = "0.0.1"
__all__ = ["Settings", "brent"]


@dataclass
class Settings:
    """
    Describes the settings used in Brent's algorithm
    """

    #: X relative tolerance
    x_rel_tol: float

    #: X absolute tolerance
    x_abs_tol: float

    #: Y absolute tolerance
    y_tol: float

    #: Whether to display progress
    verbose: bool


def test_convergence(a: float, b: float, fb: float, s: Settings) -> Tuple[bool, Optional[str]]:
    """
    Checks convergence of a root finding method

    Args:
        a: Contrapoint
        b: Best guess
        fb: f(b)

    Returns:
        Whether the root finding converges to the specified tolerance and why
    """
    if fb == 0:
        return (True, "Exact root found")
    x_delta = abs(a - b)
    if x_delta <= s.x_abs_tol:
        return (True, "Met x_abs_tol criterion")
    if x_delta / max(a, b) <= s.x_rel_tol:
        return (True, "Met x_rel_tol criterion")
    y_delta = abs(fb)
    if y_delta <= s.y_tol:
        return (True, "Met y_tol criterion")
    return (False, None)


def inverse_quadratic_interpolation_step(
    a: float, b: float, c: float, fa: float, fb: float, fc: float
) -> float:
    """
    Computes an approximation for a zero of a 1D function from three function values

    Note:
        The values ``fa``, ``fb``, ``fc`` need all to be distinct.

    See `<https://en.wikipedia.org/wiki/Inverse_quadratic_interpolation>`_

    Args:
        a: First x coordinate
        b: Second x coordinate
        c: Third x coordinate
        fa: f(a)
        fb: f(b)
        fc: f(c)

    Returns:
        An approximation of the zero
    """
    L0 = (a * fb * fc) / ((fa - fb) * (fa - fc))
    L1 = (b * fa * fc) / ((fb - fa) * (fb - fc))
    L2 = (c * fb * fa) / ((fc - fa) * (fc - fb))
    return L0 + L1 + L2


def secant_step(a: float, b: float, fa: float, fb: float) -> float:
    """
    Computes an approximation for a zero of a 1D function from two function values

    Note:
        The values ``fa`` and ``fb`` need to have a different sign.

    Args:
        a: First x coordinate
        b: Second x coordinate
        fa: f(a)
        fb: f(b)

    Returns:
        An approximation of the zero
    """
    return b - fb * (b - a) / (fb - fa)


def bisection_step(a: float, b: float) -> float:
    """
    Computes an approximation for a zero of a 1D function from two function values

    Note:
        The values ``f(a)`` and ``f(b)`` (not needed in the code) need to have a different sign.

    Args:
        a: First x coordinate
        b: Second x coordinate

    Returns:
        An approximation of the zero
    """
    return min(a, b) + abs(b - a) / 2


def brent(f: Callable[[float], float], a: float, b: float, settings: Settings) -> float:
    """
    Finds the root of a function using Brent's method, starting from an interval enclosing the zero

    Example:
        >>> import math
        >>> s = Settings(1e-12, 1e-12, 1e-12, False)
        >>> brent(math.cos, 0.0, 3.0, s)
            1.5708

    Args:
        f: Function to find the root of
        a: First x coordinate enclosing the root
        b: Second x coordinate enclosing the root

    Returns:
        The approximate root
    """

    if settings.verbose:

        table_settings = Table()
        table_settings.add_column("Parameter", justify="right")
        table_settings.add_column("Value", justify="left")

        table_settings.add_row("X absolute tolerance", f"{settings.x_abs_tol:.2e}")
        table_settings.add_row("X relative tolerance", f"{settings.x_rel_tol:.2e}")
        table_settings.add_row("Y tolerance", f"{settings.y_tol:.2f}")
        console = Console()
        console.print(table_settings)

    fa = f(a)  #: f(a)
    fb = f(b)  #: f(b)

    assert fa * fb <= 0, "Root not bracketed"

    if abs(fa) < abs(fb):
        # force abs(fa) >= abs(fb), make sure that b is the best root approximation known so far
        # and a is the contrapoint
        b, a = a, b
        fb, fa = fa, fb

    c = a  #: Previous iterate
    fc = fa  #: f(c)
    d = a  #: Iterate before the previous iterate
    last_step: Optional[str] = None
    step: Optional[str] = None
    n_iters = 1  #: Current iteration number (1-based)
    converged = None
    reason = None

    table_results: Table = Table()

    def add_row():
        """
        Prints information about an iteration
        """
        dx = abs(a - b)
        dy = abs(fa - fb)
        table_results.add_row(
            f"{n_iters}", f"{b:.6e}", f"{fb:.1e}", f"{dx:.1e}", f"{dy:.1e}", f"{last_step}"
        )

    if settings.verbose:
        table_results.add_column("Iter")
        table_results.add_column("x", justify="right")
        table_results.add_column("f(x)", justify="right")
        table_results.add_column("delta(x)", justify="right")
        table_results.add_column("delta(f(x))", justify="right")
        table_results.add_column("step", justify="right")
        add_row()

    while not converged:
        n_iters = n_iters + 1
        last_step = step
        if fa != fc and fb != fc:
            s = inverse_quadratic_interpolation_step(a, b, c, fa, fb, fc)
            step = "quadratic"
        else:
            s = secant_step(a, b, fa, fb)
            step = "secant"
        perform_bisection = False
        if a <= b and not ((3 * a + b) / 4 <= s <= b):  # pylint: disable=C0325
            perform_bisection = True
        elif b <= a and not (b <= s <= (3 * a + b) / 4):  # pylint: disable=C0325
            perform_bisection = True
        elif last_step == "bisection" and abs(s - b) >= abs(b - c) / 2:
            perform_bisection = True
        elif last_step != "bisection" and abs(a - b) >= abs(c - d) / 2:
            perform_bisection = True
        elif last_step == "bisection" and abs(b - c) < settings.x_abs_tol:
            perform_bisection = True
        elif last_step != "bisection" and abs(c - d) < settings.x_abs_tol:
            perform_bisection = True
        if perform_bisection:
            s = bisection_step(a, b)
            step = "bisection"
        fs = f(s)
        d = c
        c = b
        fc = fb
        # check which point to replace to maintain (a,b) have different signs
        if f(a) * f(s) < 0:
            b = s
            fb = fs
        else:
            a = s
            fa = fs
        # keep b as the best guess
        if abs(fa) < abs(fb):
            b, a = a, b
            fb, fa = fa, fb
        converged, reason = test_convergence(a, b, fb, settings)
        if settings.verbose:
            add_row()

    if settings.verbose:
        console = Console()
        console.print(table_results)
        assert reason is not None
        print(reason)

    return b
