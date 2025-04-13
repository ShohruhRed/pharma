import torch
import torch.nn as nn

class GaussianMF(nn.Module):
    def __init__(self, mu, sigma, trainable=True):
        super(GaussianMF, self).__init__()
        self.mu = nn.Parameter(torch.tensor(mu, dtype=torch.float32), requires_grad=trainable)
        self.sigma = nn.Parameter(torch.tensor(sigma, dtype=torch.float32), requires_grad=trainable)

    def forward(self, x):
        return torch.exp(-0.5 * ((x - self.mu) / self.sigma) ** 2)

    def __repr__(self):
        return f"GaussianMF(mu={self.mu.item():.2f}, sigma={self.sigma.item():.2f})"
