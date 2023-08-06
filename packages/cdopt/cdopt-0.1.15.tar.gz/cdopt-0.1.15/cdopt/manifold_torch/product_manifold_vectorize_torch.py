import numpy as np
import torch
from torch import nn

from numpy.linalg import svd

from .basic_manifold_torch import basic_manifold_torch


class product_manifold_vectorize_torch(basic_manifold_torch):
    def __init__(self, list_manifold, device = torch.device('cpu'), dtype = torch.float64) -> None:
        # self._n = n
        # self._p = p
        # self.dim = n*p 

        # the routine is the vector, not the tuple of variables

        self.name = 'Product Manifold'
        self.manifold_type = 'P'
        self.list_manifold = list_manifold
        self.var_shape = tuple(M.var_shape for M in list_manifold)
        self.dim_tuple = tuple(np.prod(var_shape) for var_shape in self.var_shape)
        self.var_num = self.dim_tuple

        self.dim = np.sum(self.dim_tuple)
        # self.var_shape = (self.dim,)

        self.device = device
        self.dtype = dtype
        



    def v2m(self, x):
        x_tuple_tmp = torch.split(x, self.dim_tuple)
        return tuple( torch.reshape(x_local, shape_local ) for x_local, shape_local in zip(x_tuple_tmp, self.var_shape)  )

    def m2v(self, X_tuple):
        return torch.cat(tuple( var.flatten() for var in X_tuple ),0)


    

    def A(self, x_vec):
        X_list = self.v2m(x_vec)
        return self.m2v(tuple( self.list_manifold[i].A(X) for i, X in enumerate(X_list) ))


    def JA(self, x_vec, g_vec):
        X_list = self.v2m(x_vec)
        G_list = self.v2m(g_vec)
        return  self.m2v(tuple(M.JA(X, G) for M, X, G in zip(self.list_manifold, X_list, G_list) ))

    def JA_transpose(self,x_vec, g_vec):
        X_list = self.v2m(x_vec)
        G_list = self.v2m(g_vec)
        return  self.m2v(tuple(M.JA_transpose(X, G) for M, X, G in zip(self.list_manifold, X_list, G_list)) )

    def hessA(self, x_vec, g_vec, d_vec):
        X_list = self.v2m(x_vec)
        G_list = self.v2m(g_vec)
        D_list= self.v2m(d_vec)
        return self.m2v(tuple( M.hessA(X,G, D) for M, X, G, D in zip(self.list_manifold, X_list, G_list, D_list) ))


    def JC(self, x_vec, Lambda_list):
        X_list = self.v2m(x_vec)
        # Lambda_list = self.v2m(lambda_vec)
        return self.m2v(tuple( M.JC(X,Lambda) for M, X, Lambda in zip(self.list_manifold, X_list, Lambda_list) ))

    
    def C(self, x_vec):
        X_list = self.v2m(x_vec)
        return tuple(M.C(X) for M, X in zip(self.list_manifold, X_list) )

    def C_quad_penalty(self, x_vec):
        X_list = self.v2m(x_vec)
        # tol = 0
        # for i, X in enumerate(X_list):
        #     tol = tol + torch.sum(self.list_manifold[i].C(X) ** 2)
        # return tol
        return torch.sum( torch.as_tensor(tuple( torch.sum(M.C(X) ** 2) for M, X in zip(self.list_manifold, X_list)) )) 


    def hess_feas(self, X_list, D_list):
        return self.m2v(tuple( M.hess_feas(X,D) for M, X, D in zip(self.list_manifold, X_list, D_list) ))

    



    def Feas_eval(self, X_list):
        return torch.sqrt( self.C_quad_penalty(X_list) )

    def Init_point(self, Xinit = None):
        x_vec = Xinit
        if x_vec is None:
            return tuple(M.Init_point() for M in self.list_manifold)
        else:
            X_list = self.v2m(x_vec)
            return tuple(M.Init_point(Xinit) for M, Xinit in zip(self.list_manifold, X_list))

    def Post_process(self,x_vec):
        X_list = self.v2m(x_vec)
        return self.m2v(self.m2v(tuple(M.Post_process(X) for M, X in zip(self.list_manifold, X_list) )))



    def generate_cdf_fun(self, obj_fun, beta):
        def local_obj_fun(x):
            
            return obj_fun(*self.v2m(self.A(self.m2v(x)))) + (beta/2) * self.C_quad_penalty(self.m2v(x))

        



        return local_obj_fun  


    # def to_cdf_fun(self, beta = 0):
    #     def decorator_cdf_obj(obj_fun):
    #         return self.generate_cdf_fun(obj_fun, beta )
    #         # return lambda X: obj_fun(self.A(X)) + (beta) * self.C_quad_penalty(X)
            
    #     return decorator_cdf_obj



    def generate_cdf_grad(self, obj_grad, beta):
        def local_grad(x):
            
            # AX = self.A(args)
            # print(self.v2m(self.A(self.m2v(x))))
            return self.JA(self.m2v(x), self.m2v(obj_grad(*self.v2m(self.A(self.m2v(x))))) ) + beta * self.JC(self.m2v(x), self.C(self.m2v(x)))
            # local_JA_gradf = gradf @ (np.eye(self._p) - 0.5 * CX) - X @ XG 
            
            # local_JC_CX = 2 * X @(CX)

            # return tuple(G + beta*JCC for G, JCC in zip(grad_g, Jc_c))

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
        def local_hess(x, d):
            x_vec = self.m2v(x)
            d_vec = self.m2v(d)
            gradf = self.m2v(obj_grad(*self.v2m(self.A(x_vec))))
            return self.JA( x_vec, self.m2v(obj_hess( self.v2m(self.A(x_vec)),     self.v2m(self.JA_transpose(x_vec, d_vec)) )) ) + self.hessA(x_vec, gradf, d_vec) + beta * self.hess_feas(x, d)



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