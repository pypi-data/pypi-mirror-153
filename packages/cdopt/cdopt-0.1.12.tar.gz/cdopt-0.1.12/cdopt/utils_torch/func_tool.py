import numpy as np
import torch 


def cg_subsolver(linear_transform, b, xinit , tol = 1e-8, max_iter = 1000 ):
    '''
    Solve the linear equation 
    linear_transform(x) = b
    Here linear_transform() should be self-adjoint (symmetric)
    '''
    x = xinit
    grad = linear_transform(x)
    r = b - grad 

    # num_iter = 1

    r_norm = np.sqrt( np.sum( r ** 2 ) )
    if r_norm < tol:
            return x, [1, r_norm]

    y = r 
    Ay = linear_transform(y)
    # z = Ay


    t = np.sum(r ** 2)/ np.sum( Ay * y )


    x = x+ t*y

    for num_iter in range(max_iter):
        r_norm_p = r_norm 
        r = r - t*Ay 
        r_norm = np.sqrt( np.sum( r ** 2 ) )
        if r_norm < tol:
            return x, [num_iter, r_norm]

        delta = (r_norm / r_norm_p ) ** 2
        y = r + delta * y 
        Ay = linear_transform(y)

        t = np.sum( r ** 2 )/ np.sum( Ay * y )
        x = x + t*y 

    # print(r_norm)
    return x, [num_iter, r_norm]











        
        

