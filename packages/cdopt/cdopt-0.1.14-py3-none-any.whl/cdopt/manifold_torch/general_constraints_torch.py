import abc
import functools
import torch
from core.autodiff_torch import   linear_map_adjoint, auto_diff_vjp, auto_diff_jvp
import numpy as np
# from autograd import grad, jacobian
# from autograd.numpy.linalg import solve, pinv


# from autograd import grad, jacobian
# from autograd.numpy.linalg import solve, pinv

# from .basic_manifold_torch import basic_manifold_torch


class general_constraints_torch(metaclass=abc.ABCMeta):
    def __init__(self,name,var_shape,  ce_shape, ci_shape, manifold, device = torch.device('cpu'), dtype = torch.float64,  autodiff_type = "autograd", regularize_value = 0.01, safegurad_value = 0) -> None:
        self.name = name
        self.var_shape = var_shape 
        self.var_length = np.prod(var_shape)
        self.ce_shape = ce_shape
        self.ci_shape = ci_shape
        self.ce_length = np.prod(ce_shape)
        self.ci_length = np.prod(ci_shape)



        lb = -np.inf * np.ones(self.var_length + self.ci_length)
        lb[self.var_length :] = np.zeros(self.ci_length)
        ub = np.inf * np.ones(self.var_length + self.ci_length)

        self.lb = lb 
        self.ub = ub


        self.CM = manifold


        

        self.device = device
        self.dtype = dtype
        self.regularize_value = regularize_value
        self.safegurad_value = safegurad_value

        # self.Ip = torch.eye()

        
        
        
        # self.dir_grad = dir_grad
        self.linear_map_adjoint = linear_map_adjoint
        self.jacobian = lambda fun, X: torch.autograd.functional.jacobian(fun, X, create_graph=True, strict=False, vectorize=True)

        # def local_jacobian(fun):
        self.pinv = torch.linalg.pinv
        self.solve = torch.linalg.solve
        self.offset = 1e-5

        self.vjp = auto_diff_vjp
        self.jvp = auto_diff_jvp
            # autograd.vjp has low compatibality to the autograd.linalg.solve or autograd.linalg.pinv
            # hence we choose the linear_map_adjoint to generate jvp from vjp.
            # On the other hand, mathematically, jvp and vjp are equivalent. Therefore, it would be better 
            # directly generate jvp from vjp, rather than calling jvp from the autodiff backbone. 
            # In the current version, we still keep the self.jvp, but it may be modified or removed in the following versions. 



        

    # def __call__(self, name,var_shape,  ce_shape, ci_shape, manifold, device = torch.device('cpu'), dtype = torch.float64,  autodiff_type = "autograd", regularize_value = 0.01, safegurad_value = 0) -> Any:
        


        
    

    # In class basic_manifold, only the expression for C(X), v2m and m2v are required.
    # The generating graph can be expressed as 
    #  C -> JC -> JC_transpose -> hess_feas ----
    #  |                                        |-> generate_cdf_fun, generate_cdf_grad, generate_cdf_hess
    #  --> A -> JA -> JA_transpose -> hessA ----


    def _raise_not_implemented_error(method):
        """Method decorator which raises a NotImplementedError with some meta
        information about the manifold and method if a decorated method is
        called.
        """
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            raise NotImplementedError(
                "Manifold class '{:s}' provides no implementation for "
                "'{:s}'".format(self._get_class_name(), method.__name__))
        return wrapper





    @_raise_not_implemented_error
    def C_all(self, X, S):
        '''
        define all the constraints
        '''
    

    
    def C_mesh(self,X, S):
        return self.C_all(self.CM.A(X), S)



    def v2m_primal(self,x):
        """Converting vector to the elements in the matrix
        """
        return torch.reshape(x, self.var_shape)



    
    def m2v_primal(self,X):
        """Converting elements in the matrix to vector
        """
        return X.flatten()



    def m2v_auxiliary(self, S):
        return S.flatten()

    def v2m_auxiliary(self, s):
        return torch.reshape(s, self.ci_shape)

    


    


    def v2m(self, v):
        # v1 = v[:self.var_length]
        # v2 = v[self.var_length:]

        v1, v2 = torch.split(v, (self.var_length, self.ci_length))
        return (torch.reshape(v1, self.var_shape), torch.reshape(v2, self.ci_shape)  )


    def m2v(self, X, S):
        v1 = self.m2v_primal(X)
        v2 = S.flatten()
        return torch.cat( (v1, v2), 0 )




    
    # def A(self, X):
    #     local_JC =  lambda y: self.C(self.v2m(y)).flatten()
    #     JC_mat = self.jacobian(local_JC,self.m2v(X))
    #     # print(JC_mat.size())
    #     C_vec = (self.C(X)).flatten()
    #     # print((self.solve(  0.01 * torch.eye(C_vec.size()[0]).to(device = self.device, dtype = self.dtype) + (JC_mat @ JC_mat.T), C_vec   ) ).size())
    #     AX_vec = self.m2v(X) - self.pinv(JC_mat) @ C_vec
    #     return self.v2m(AX_vec)

    def A_Cmesh(self, X, S):
        local_JC =  lambda y, S: self.C_mesh(self.v2m_primal(y), S).flatten()
        JC_mat = self.jacobian(local_JC,(self.m2v_primal(X), S) )[0]
        C_vec = (self.C_mesh(X, S)).flatten()
        # AX_vec = self.m2v(X) - (JC_mat.T).detach() @ self.solve(  ((self.regularize_value* self.C_quad_penalty(X) + self.safegurad_value) * torch.eye(C_vec.size()[0]).to(device = self.device, dtype = self.dtype) + (JC_mat @ JC_mat.T)).detach(), C_vec   ) 

        # AX_vec = self.m2v(X) - self.pinv(JC_mat) @ C_vec
        AX_vec = self.m2v_primal(X) - JC_mat.T @ self.solve(  (self.regularize_value* self.C_quad_penalty(X, S) + self.safegurad_value) * torch.eye(C_vec.size()[0]).to(device = self.device, dtype = self.dtype) + (JC_mat @ JC_mat.T), C_vec   ) 
        return self.v2m_primal(AX_vec)


    def A(self, X, S):
        return self.CM.A(self.A_Cmesh(X, S))


    def JA(self, XS_tuple, D):
        out_results, XS_grad =   torch.autograd.functional.vjp(self.A, XS_tuple, v = D)
        return XS_grad



    def JC_mesh(self, XS_tuple, Lambda):
        out_results, XS_grad =   torch.autograd.functional.vjp(self.C_mesh, XS_tuple, v = Lambda)
        return XS_grad




    # def A(self, X):
    #     local_JC =  lambda y: self.C(self.v2m(y)).flatten()
    #     JC_mat = self.jacobian(local_JC)(self.m2v(X))
    #     C_vec = (self.C(X)).flatten()
        
    #     AX_vec = self.m2v(X) - JC_mat.T @ self.solve( self.offset * np.eye(np.size(C_vec)) + (JC_mat @ JC_mat.T), C_vec ) 
    #     return self.v2m(AX_vec)



    def C_quad_penalty(self, X, S):
        return torch.sum(self.C_mesh(X, S) **2) +  self.CM.C_quad_penalty(X) 





    def Feas_eval(self, X, S):
        return torch.sqrt(self.C_quad_penalty(X, S))

    def Init_point(self, Xinit = None):
        if not Xinit is None:
            Xinit = Xinit.detach()
        Xinit = self.CM.Init_point(Xinit = Xinit)
        # Sinit = torch.maximum(torch.randn(*self.ci_shape).to(device= self.device, dtype = self.dtype), torch.zeros(self.ci_shape).to(device= self.device, dtype = self.dtype))
        Sinit =torch.zeros(self.ci_shape).to(device= self.device, dtype = self.dtype)
        Sinit.requires_grad = True
        return Xinit, Sinit


    def Post_process(self,X):
        
        return self.CM.Post_process(X)



    def generate_cdf_fun(self, obj_fun, beta):
        cdf_fun =  lambda X, S: obj_fun(self.A(X, S)) + (beta/2) * self.C_quad_penalty(X, S)

        return cdf_fun

        # return cdf_fun_fin



    def generate_cdf_grad(self, obj_grad, beta):
        
        def local_cdf_grad(X, S):
            gradf = obj_grad(self.A(X,S))
            X_JAf, S_JAf = self.JA((X,S), gradf)
            X_JC_mesh, S_JC_mesh = self.JC_mesh((X,S), self.C_mesh(X, S)) 
            X_JC_CM = self.CM.JC(X, self.CM.C(X)  )

            return X_JAf + beta * (X_JC_CM + X_JC_mesh), S_JAf + beta * S_JC_mesh

        return local_cdf_grad
        
        