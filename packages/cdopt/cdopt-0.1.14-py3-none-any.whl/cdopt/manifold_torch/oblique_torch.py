import numpy as np
import torch
from torch import nn


from .basic_manifold_torch import basic_manifold_torch

class oblique_torch(basic_manifold_torch):
    def __init__(self, var_shape, device = torch.device('cpu'), dtype = torch.float64) -> None:
        n = var_shape[0]
        p = var_shape[1]
        self.device = device
        self.dtype = dtype

        super().__init__('Oblique',(n,p), (p,),   device= self.device ,dtype= self.dtype)

    


    def A(self, X):
        X_rvec = torch.sum( X * X, 1 )[:, None]
        return (2*X)/( 1 + X_rvec )


    def JA(self, X, G):
        XG = torch.sum(X*G,1)[:, None ]
        X_rvec = torch.sum( X * X, 1 )[:, None] +1
        return (2*G - (4*X *XG)/X_rvec )/X_rvec

    def JA_transpose(self, X, D):
        return self.JA(X,D) 


    def hessA(self, X, gradf, D):
        XG = torch.sum(X*gradf,1)[:, None ]
        XD = torch.sum(X * D, 1)[:, None ]
        GD = torch.sum(gradf * D, 1)[:, None ]
        X_rvec = torch.sum( X **2, 1  )[:, None ] +1
        return -(4/(X_rvec**2))*( gradf * XD + D * XG + X * GD ) + 16/( X_rvec**3 ) * (X * XG * XD)


    def JC(self, X, Lambda):
        return X * Lambda

    
    def C(self, X):
        return torch.sum( X * X, 1 )[:, None] - 1

    


    def C_quad_penalty(self, X):
        return torch.sum( self.C(X) **2  )

    def Feas_eval(self, X):
        return torch.sqrt(self.C_quad_penalty(X))



    def hess_feas(self, X, D):
        return 2 * D * self.C(X) + 4 * X * torch.sum(X*D,1)[:, None]




    def Init_point(self, Xinit = None):
        if Xinit is None:
            Xinit = torch.randn(self._n, self._p)
        else:
            Xinit = Xinit.detach()
        
        Xinit = torch.as_tensor(Xinit).to(device=self.device, dtype=self.dtype)
        Xinit.requires_grad = True
        X_rvec = torch.sqrt(torch.sum( Xinit * Xinit, 1 )[:, None])
        Xinit = Xinit / X_rvec
        
        return Xinit

    def Post_process(self,X):
        X_rvec = torch.sqrt(torch.sum( X * X, 1 )[:, None])
        X = X / X_rvec
        return X
