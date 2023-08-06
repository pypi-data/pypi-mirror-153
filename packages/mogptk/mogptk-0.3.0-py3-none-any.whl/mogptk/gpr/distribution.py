import torch
from . import config

class Distribution:
    def log_p(self, x):
        raise NotImplementedError()

class Gaussian(Distribution):
    def __init__(self, mu=torch.tensor(0.0), sigma=torch.tensor(1.0)):
        if mu.shape != sigma.shape:
            raise ValueError("mu and sigma need to have the same shape")

        self.mu = mu.to(config.device, config.dtype)
        self.sigma = sigma.to(config.device, config.dtype)
        self.log_p_constant = -0.5*torch.log(2.0*np.pi*sigma)

    def log_p(self, x):
        if x.shape != self.mu.shape:
            raise ValueError("x must match shape of mu and sigma")
        return self.log_p_constant - 0.5*(x-self.mu).T.mm(self.sigma.mm(x-self.mu))
