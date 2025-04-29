import torch
from torch import nn
from torch.utils.data import Dataset
import pandas as pd
from Analysis.utils import get_pd_df


class CustomNN(nn.Module):
    def __init__(
        self,
        n_var: int,
        layers_params: list[int],
        dropout: float = 0.0,
        num_classes: int = 1,
    ) -> None:

        if len(layers_params) < 2:
            raise ValueError("Il doit y avoir au moins une couche cachée")
        if dropout < 0 or dropout > 1:
            raise ValueError("Le taux de dropout doit être compris entre 0 et 1")
        if not isinstance(layers_params, list):
            raise TypeError("layers_params doit être une liste")
        if not isinstance(n_var, int):
            raise TypeError("n_var doit être un entier")
        if not isinstance(num_classes, int):
            raise TypeError("num_classes doit être un entier")

        super(CustomNN, self).__init__()

        layers_params = [n_var] + layers_params

        self.layers = nn.ModuleList(
            [
                self._create_hidden_layer(
                    layers_params[i], layers_params[i + 1], dropout
                )
                for i in range(len(layers_params) - 1)
            ]
        )

        self.layers.append(nn.Linear(layers_params[-1], num_classes))

    def _create_hidden_layer(n_in: int, n_out: int, dropout: float) -> nn.Sequential:
        return nn.Sequential(nn.Linear(n_in, n_out), nn.ReLU(), nn.Dropout(dropout))

    def forward(self, x) -> nn.Tensor:
        for layer in self.layers:
            x = layer(x)
        return x


def get_data(selected_vars: list[str], target_var: str) -> pd.DataFrame:
    dfs = ["constructor_standing", "results", "drivers", "driver_standings"]
    keys = ["raceId", "driverId", "driverId"]

    data = get_pd_df(dfs, keys)
    features = data[selected_vars]
    target = data[target_var]

    numerical = features.select_dtypes(include=["number"])
    categorical = features.select_dtypes(exclude=["number"])

    return numerical, categorical, target


class F1Dataset(Dataset):
    def __init__(self, categorical_data, num_data, targets) -> None:
        self.targets = torch.tensor(targets, dtype=torch.float32)
        self.categorical_data = torch.tensor(categorical_data, dtype=torch.long)

        n = []
        one_hot_data = [
            self._categorical_to_onehot(cat, n)
            for cat, n in zip(self.categorical_data, n)
        ]

        self.onehot_data = torch.cat(one_hot_data, dim=1)

        self.data = torch.cat((self.onehot_data, num_data), dim=1)

    def _categorical_to_onehot(self, data: torch.Tensor, nclass: int) -> torch.Tensor:
        if not isinstance(data, torch.Tensor):
            raise TypeError("Les données doivent être un tenseur")
        if not isinstance(nclass, int):
            raise TypeError("nclass doit être un entier")

        data_onehot = torch.zeros(data.shape[0], nclass)
        data_onehot.scatter_(1, data.unsqueeze(1), 1.0)
        return data_onehot

    def __getitem__(self, index) -> tuple[torch.Tensor, torch.Tensor]:
        x = self.data[index]
        y = self.targets[index]
        return x, y

    def __len__(self) -> int:
        return len(self.data)
