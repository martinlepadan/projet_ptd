"""
Fichier avec la fonction d'entraînement du modèle
"""

import torch
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from src.Models.NeuralNetwork.neural_network import CustomNN, F1Dataset
from torch.utils.data import DataLoader
import torch.optim as optim
import torch.nn as nn


def train_model(df, features, target, hidden_sizes, dropout, lr, epochs, test_size=0.2):

    # Séparer variables catégorielles et numériques
    cat_cols = df[features].select_dtypes(include="object").columns.tolist()
    num_cols = [col for col in features if col not in cat_cols]

    # Encodage des variables catégorielles en entiers (label encoding)
    cat_encoded = []
    cat_nclasses = []
    for col in cat_cols:
        le = LabelEncoder()
        enc = le.fit_transform(df[col])
        cat_encoded.append(enc)
        cat_nclasses.append(len(le.classes_))

    categorical_data = (
        np.stack(cat_encoded, axis=1)
        if cat_encoded
        else np.empty((len(df), 0), dtype=np.int64)
    )

    # Standardisation des variables numériques
    if num_cols:
        scaler = StandardScaler()
        num_data = scaler.fit_transform(df[num_cols])
    else:
        num_data = np.empty((len(df), 0), dtype=np.float32)

    # Cible
    if df[target].dtype == "object":
        le_y = LabelEncoder()
        targets = le_y.fit_transform(df[target])
        is_regression = False
    else:
        targets = df[target].values
        is_regression = len(np.unique(targets)) > 10

    # Split
    idx_train, idx_test = train_test_split(
        np.arange(len(df)), test_size=test_size, random_state=42
    )
    train_ds = F1Dataset(
        categorical_data[idx_train],
        cat_nclasses,
        num_data[idx_train],
        targets[idx_train],
    )
    test_ds = F1Dataset(
        categorical_data[idx_test], cat_nclasses, num_data[idx_test], targets[idx_test]
    )
    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_ds, batch_size=32, shuffle=False)

    # Initialisation du modèle
    input_size = train_ds.data.shape[1]
    output_size = 1 if is_regression else max(2, len(np.unique(targets)))

    model = CustomNN(input_size, hidden_sizes, dropout, output_size)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss() if is_regression else nn.CrossEntropyLoss()

    # Entraînement avec suivi
    model.train()
    train_losses, train_accuracies, test_metrics = [], [], {}

    for epoch in range(epochs):
        total_loss, correct, total = 0.0, 0, 0
        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()
            out = model(X_batch).squeeze()
            loss = criterion(out, y_batch if is_regression else y_batch.long())
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

            if not is_regression:
                pred = torch.argmax(out, dim=1)
                correct += (pred == y_batch).sum().item()
                total += len(y_batch)

        train_losses.append(total_loss / len(train_loader))
        acc_train = correct / total if not is_regression else float("nan")
        train_accuracies.append(acc_train)

        # Évaluation test toutes les 10 époques
        if (epoch + 1) % 10 == 0:
            model.eval()
            with torch.no_grad():
                test_loss, correct_test, total_test = 0.0, 0, 0
                for X_batch, y_batch in test_loader:
                    out = model(X_batch).squeeze()
                    loss = criterion(out, y_batch if is_regression else y_batch.long())
                    test_loss += loss.item()
                    if not is_regression:
                        pred = torch.argmax(out, dim=1)
                        correct_test += (pred == y_batch).sum().item()
                        total_test += len(y_batch)
                acc_test = (
                    correct_test / total_test if not is_regression else float("nan")
                )
                test_metrics[epoch + 1] = {
                    "loss": test_loss / len(test_loader),
                    "accuracy": acc_test,
                }

    return model, train_losses, train_accuracies, test_metrics
