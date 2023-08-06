import numpy as np

from . import LOG


def compute_q(p_w: float, cos_phi: float, mode: str = "inductive") -> float:
    """Calculates reactive power

    Reactive power is calculated with `p_w * tan(arccos(cos_phi))`.
    If mode equals `capacitive`, the returned value is negative.

    Parameters
    ----------
    p_w : float
        The active power (can also be kW)
    cos_phi : float
        The phase angle to calculate q.
    mode : str, optional
        Can be either 'inductive' or 'capacitive'. Defaults to
        'inductive', which returns the value as it is. If set to
        'capacitive', the sign of the output is flipped.

    Returns
    -------
    float
        Returns *q_var* in the same size of order like p_w (e.g., if
        *p* is in kW, *q* will be in kvar)

    """
    abs_q = p_w * np.tan(np.arccos(cos_phi))
    # inductive load 'consumes' reactive power
    if mode == "inductive":
        return abs_q

    # capacitve load 'provides' reactive power
    elif mode == "capacitve":
        return -1 * abs_q
    else:
        LOG.warning(
            "Illegal mode: %s. Falling back to default (inductive).",
            str(mode),
        )
        return abs_q
