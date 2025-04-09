from torch import nn
import torch.nn.functional as F


class CustomNN(nn.Module):
    def __init__(self, layers: list[int], num_classes: int = 1):
        super(CustomNN, self).__init__()

        for i in range(len(layers)):
