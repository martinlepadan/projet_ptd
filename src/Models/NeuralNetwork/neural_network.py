import torch
from torch import nn
from torch.utils.data import Dataset


class CustomNN(nn.Module):
    """
    Implémentation d'un réseau de neurones complètement personnalisable.

    Parameters
    ----------
        n_var (int): Nombre de variables en entrée (dimension de l'entrée).
        layers_params (list[int]): Liste contenant le nombre de neurones pour chaque
        couche cachée
        dropout (float, optional): Taux de dropout à appliquer après chaque couche
        cachée
        num_classes (int, optional): Nombre de classes en sortie (dimension de la sortie)

    Methodes
    --------
        forward(x: torch.Tensor) -> torch.Tensor:
            Effectue une forward propagation
    """

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

    def _create_hidden_layer(
        self, n_in: int, n_out: int, dropout: float
    ) -> nn.Sequential:
        return nn.Sequential(nn.Linear(n_in, n_out), nn.ReLU(), nn.Dropout(dropout))

    def forward(self, x) -> torch.Tensor:
        for layer in self.layers:
            x = layer(x)
        return x


class F1Dataset(Dataset):
    """
    Dataset personnalisé pour gérer des données catégoriques et numériques

    Parameters
    ----------
        categorical_data (list): Données catégoriques sous forme de liste ou tableau
        cat_nclasses (list): Liste contenant le nombre de classes pour chaque
                             colonne catégorique
        num_data (list ou ndarray): Données numériques sous forme de liste ou tableau
        targets (list ou ndarray): Cibles associées aux données

    Attributes
    ----------
        targets (torch.Tensor): Tenseur contenant les cibles
        categorical_data (torch.Tensor): Tenseur contenant les données catégoriques
        cat_nclasses (list): Liste contenant le nombre de classes pour chaque
                             colonne catégorique
        num_data (torch.Tensor): Tenseur contenant les données numériques
        onehot_data (torch.Tensor): Tenseur contenant les données catégoriques encodées
        data (torch.Tensor): Tenseur combinant toutes les données

    Methodes
    --------
        _categorical_to_onehot(col, nclass):
            Convertit une colonne catégorique en rone hot
    """

    def __init__(self, categorical_data, cat_nclasses, num_data, targets) -> None:
        if not isinstance(cat_nclasses, list):
            raise TypeError("cat_nclasses doit être une liste d'entiers")

        self.targets = torch.tensor(targets, dtype=torch.float32)
        self.categorical_data = torch.tensor(categorical_data, dtype=torch.long)
        self.cat_nclasses = cat_nclasses
        self.num_data = torch.tensor(num_data, dtype=torch.float32)

        onehot_cols = [
            self._categorical_to_onehot(self.categorical_data[:, i], nclass)
            for i, nclass in enumerate(self.cat_nclasses)
        ]

        self.onehot_data = (
            torch.cat(onehot_cols, dim=1)
            if onehot_cols
            else torch.empty((len(targets), 0))
        )
        self.data = torch.cat((self.onehot_data, self.num_data), dim=1)

    def _categorical_to_onehot(self, col: torch.Tensor, nclass: int) -> torch.Tensor:
        if not isinstance(col, torch.Tensor):
            raise TypeError("col doit être un tenseur")
        if not isinstance(nclass, int):
            raise TypeError("nclass doit être un entier")

        onehot = torch.zeros((len(col), nclass))
        onehot.scatter_(1, col.unsqueeze(1), 1.0)
        return onehot

    def __getitem__(self, index):
        return self.data[index], self.targets[index]

    def __len__(self):
        return len(self.targets)
