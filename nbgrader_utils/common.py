def eq_tol(v : float, e : float, tol : float = 1e-3):
    return abs(v - e) <= tol
