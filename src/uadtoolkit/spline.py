
import numpy as np

class NaturalCubicSpline:
    """C^2 natural cubic spline with evaluate()."""
    def __init__(self, x, y):
        x = np.asarray(x, float); y = np.asarray(y, float)
        order = np.argsort(x); x = x[order]; y = y[order]
        keep = np.concatenate(([True], np.diff(x) > 0))
        self.x = x[keep]; self.y = y[keep]
        n = self.x.size
        if n < 2: raise ValueError("Need at least two points")
        h = np.diff(self.x)
        alpha = np.zeros(n)
        for i in range(1, n-1):
            alpha[i] = 3*((y[i+1]-y[i])/h[i] - (y[i]-y[i-1])/h[i-1])
        l = np.ones(n); mu = np.zeros(n); z = np.zeros(n)
        for i in range(1, n-1):
            l[i] = 2*(self.x[i+1]-self.x[i-1]) - h[i-1]*mu[i-1]
            mu[i] = h[i]/l[i]; z[i] = (alpha[i] - h[i-1]*z[i-1]) / l[i]
        c = np.zeros(n); b = np.zeros(n-1); d = np.zeros(n-1)
        for j in range(n-2, -1, -1):
            c[j] = z[j] - mu[j]*c[j+1]
            b[j] = (y[j+1]-y[j])/h[j] - h[j]*(c[j+1]+2*c[j])/3.0
            d[j] = (c[j+1]-c[j])/(3.0*h[j])
        self.a = y[:-1]; self.b = b; self.c = c[:-1]; self.d = d

    def _seg(self, xq):
        j = np.searchsorted(self.x, xq) - 1
        return int(np.clip(j, 0, self.x.size-2))

    def evaluate(self, xq):
        xq = np.asarray(xq, float)
        out = np.empty_like(xq, dtype=float)
        for idx, xv in np.ndenumerate(xq):
            xv = np.clip(xv, self.x[0], self.x[-1])
            j = self._seg(xv); dx = xv - self.x[j]
            out[idx] = self.a[j] + self.b[j]*dx + self.c[j]*dx**2 + self.d[j]*dx**3
        return out
