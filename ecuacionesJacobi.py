import numpy as np
def jacobi( matriz, a,):
    max_iter=1000
    A=np.array(matriz, dtype=float)
    b=np.array(a, dtype=float)
    n = len(b)
    x = np.zeros(n)
    omega = 1.2
    tol=0.001
    for _ in range(max_iter):
        x_old = np.copy(x)
        
        for i in range(n):
            sigma = np.dot(A[i, :i], x[:i]) + np.dot(A[i, i+1:], x_old[i+1:])
            x[i] = (1 - omega) * x_old[i] + omega * (b[i] - sigma) / A[i, i]
        
        if (np.linalg.norm(x - x_old, ord=np.inf)/np.linalg.norm(x, ord=np.inf)) < tol:
            break
    
    return x









