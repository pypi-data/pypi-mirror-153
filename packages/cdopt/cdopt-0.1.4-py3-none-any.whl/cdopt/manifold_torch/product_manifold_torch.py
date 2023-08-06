import numpy as np
import torch
from torch import nn

from numpy.linalg import svd

from .basic_manifold_torch import basic_manifold_torch


class product_manifold_torch(basic_manifold_torch):
    def __init__(self, list_manifold, device = torch.device('cpu'), dtype = torch.float64) -> None:
        # self._n = n
        # self._p = p
        # self.dim = n*p 

        self.name = 'Product Manifold'
        self.manifold_type = 'P'
        self.list_manifold = list_manifold
        self.var_shape = tuple(M.var_shape for M in list_manifold)
        self.dim_tuple = tuple(np.prod(var_shape) for var_shape in self.var_shape)
        self.dim = np.sum(self.dim_tuple)
        self.shape = (self.dim,)

        self.device = device
        self.dtype = dtype
        



    def v2m(self, x):
        x_tuple_tmp = torch.split(x, self.dim_tuple)
        return tuple( torch.reshape(x_local, shape_local ) for x_local, shape_local in zip(x_tuple_tmp, self.var_shape)  )

    def m2v(self, X_tuple):
        return torch.cat(tuple( var.flatten() for var in X_tuple ),0)

    def A(self, X_list):
        return tuple( self.list_manifold[i].A(X) for i, X in enumerate(X_list) )


    def JA(self, X_list, G_list):
        return  tuple(M.JA(X, G) for M, X, G in zip(self.list_manifold, X_list, G_list) )

    def JA_transpose(self,X_list, G_list):
        # JA is self-adjoint
        return  tuple(M.JA_transpose(X, G) for M, X, G in zip(self.list_manifold, X_list, G_list)) 

    def hessA(self, X_list, G_list, D_list):
        return tuple( M.hessA(X,G, D) for M, X, G, D in zip(self.list_manifold, X_list, G_list, D_list) )


    def JC(self, X_list, Lambda_list):
        return tuple( M.JC(X,Lambda) for M, X, Lambda in zip(self.list_manifold, X_list, Lambda_list) )

    
    def C(self, X_list):
        return tuple(M.C(X) for M, X in zip(self.list_manifold, X_list) )

    def C_quad_penalty(self, X_list):
        # tol = 0
        # for i, X in enumerate(X_list):
        #     tol = tol + torch.sum(self.list_manifold[i].C(X) ** 2)
        # return tol
        return torch.sum( torch.as_tensor(tuple( torch.sum(M.C(X) ** 2) for M, X in zip(self.list_manifold, X_list)) )) 


    def hess_feas(self, X_list, D_list):
        return tuple( M.hess_feas(X,D) for M, X, D in zip(self.list_manifold, X_list, D_list) )

    



    def Feas_eval(self, X_list):
        return torch.sqrt( self.C_quad_penalty(X_list) )

    def Init_point(self, Xinit_list = None):
        if Xinit_list is None:
            return tuple(M.Init_point() for M in self.list_manifold)
        else:
            return tuple(M.Init_point(Xinit) for M, Xinit in zip(self.list_manifold, Xinit_list))

    def Post_process(self,X_list):
        
        return tuple(M.Post_process(X) for M, X in zip(self.list_manifold, X_list) )



    def generate_cdf_fun(self, obj_fun, beta):
        def local_obj_fun(*args):
            
            return obj_fun(*self.A(args)) + (beta/2) * self.C_quad_penalty(args)

        



        return local_obj_fun  


    # def to_cdf_fun(self, beta = 0):
    #     def decorator_cdf_obj(obj_fun):
    #         return self.generate_cdf_fun(obj_fun, beta )
    #         # return lambda X: obj_fun(self.A(X)) + (beta) * self.C_quad_penalty(X)
            
    #     return decorator_cdf_obj



    def generate_cdf_grad(self, obj_grad, beta):
        def local_grad(*args):
            
            # AX = self.A(args)
            grad_g = self.JA(args, obj_grad(*self.A(args))) 
            Jc_c = self.JC( args, self.C(args) )
            # local_JA_gradf = gradf @ (np.eye(self._p) - 0.5 * CX) - X @ XG 
            
            # local_JC_CX = 2 * X @(CX)

            return tuple(G + beta*JCC for G, JCC in zip(grad_g, Jc_c))

        return local_grad  

    # def to_cdf_grad(self, beta = 0):
    #     def decorator_cdf_grad(obj_grad):
    #         return self.generate_cdf_grad(obj_grad, beta )
    #         # return lambda X: obj_fun(self.A(X)) + (beta) * self.C_quad_penalty(X)
            
    #     return decorator_cdf_grad



    #TODO 
    # 2022/01/05
    # The simplest expression for self.generate_cdf_hess()  is
    # self.JA( X, hessf( self.JA_transpose(X,D) ) ) + self.hessA(X, gradf, D) + beta * self.hess_feas(X, D)
    # However, it repeatively computes A(X), X.T @ D and C(X), leading to inferior efficiency in practice.
    # A better implementation is presented below.
    # However, the function self.generate_cdf_hess()  is still not well-optimized. 
    # In the nest version I will rewrite this function for a better performance.

    
    # 2022/01/07
    # Rewite  self.generate_cdf_grad() and self.generate_cdf_hess()
    


    # def generate_cdf_hess(self, obj_grad, obj_hess, beta):
    #     def local_hess(X, D):
    #         CX = self.C(X)
    #         AX = X - 0.5 * X@CX
    #         gradf = obj_grad(AX)
    #         XG = self.Phi(X.T @ gradf)
    #         XD = self.Phi(X.T @ D)

    #         local_JAT_D = D @ (np.eye(self._p) - 0.5 * CX) - X @ XD 
    #         local_objhess_JAT_D = obj_hess(AX, local_JAT_D)
    #         local_JA_objhess_JAT_D = local_objhess_JAT_D @ (np.eye(self._p) - 0.5 * CX) -  X @ self.Phi( X.T @ local_objhess_JAT_D )


    #         local_hessA_objgrad_D = - D @ XG - X @ self.Phi(D.T @ gradf) - gradf @ XD

    #         local_hess_feas = 4*X @ XD + 2*D @ CX


    #         return local_JA_objhess_JAT_D + local_hessA_objgrad_D + beta * local_hess_feas

    #     return local_hess




    def generate_cdf_hess(self, obj_grad, obj_hess, beta):
        def local_hess(X_list, D_list):
            gradf_list = obj_grad(*X_list)

            D1 = self.JA( X_list, obj_hess(self.A(X_list), self.JA_transpose(X_list,D_list) ) )
            D2 = self.hessA(X_list, gradf_list, D_list)
            D3 = beta * self.hess_feas(X_list, D_list)

            return tuple( d1+ d2 + d3 for d1, d2, d3 in zip(D1, D2, D3))


        return local_hess



    # def np_wrapper_single(self, func):
    #     # input: func(*args) -> tensor,
    #     # args: numpy arrays
    #     # output: function that maps array to array
    #     def wrapped_fun(x):
    #         x = torch.as_tensor(x).to(device = self.device, dtype = self.dtype)
    #         x.requires_grad = True
    #         X = self.v2m(x)
    #         return self.m2v(func(*X)).detach().cpu().numpy()
    #     return wrapped_fun



    # def np_wrapper_hvp(self, func):
    #     # input: func(*args) -> tensor,
    #     # args: numpy arrays
    #     # output: function that maps array to array
    #     def wrapped_fun(x, d):
    #         x = torch.as_tensor(x).to(device = self.device, dtype = self.dtype)
    #         x.requires_grad = True
    #         d = torch.as_tensor(d).to(device = self.device, dtype = self.dtype)
    #         d.requires_grad = True
    #         X = self.v2m(x)
    #         D = self.v2m(d)
    #         return self.m2v(func(X, D)).detach().cpu().numpy()
    #     return wrapped_fun



    


