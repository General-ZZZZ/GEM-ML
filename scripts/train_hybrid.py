# -*- coding: utf-8 -*-
'''
训练残差神经网络：预测 u-产酸率 = FBA预测 + NN校正
'''

import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# 1 read FBA data
df = pd.read_csv("../data/fba_data.csv")
X = df[["glc_update", "growth_rate"]].values
y = df["muconate_rate"].values.reshape(-1,1)

# 2 split and standard
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
scalerX = StandardScaler().fit(X_tr)
scalerY = StandardScaler().fit(y_tr)
X_trs, X_tes = scalerX.transform(X_tr), scalerX.transform(X_te)
y_trs, y_tes = scalerY.transform(y_tr), scalerY.transform(y_te)

# 3. MLP
class Residual(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Sequential(nn.Linear(2,64), nn.ReLU(), nn.Linear(64,1))
    def forward(self, x, fba):
        return fba + self.fc(x)

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
model = Residual().to(device)
criterion, optimizer = nn.MSELoss(), torch.optim.Adam(model.parameters(), lr=1e-3)

# 4. loop train
Xtr = torch.tensor(X_trs, dtype=torch.float32).to(device)
Xte = torch.tensor(X_tes, dtype=torch.float32).to(device)
Ftr = torch.tensor(y_trs, dtype=torch.float32).to(device)
Fte = torch.tensor(y_tes, dtype=torch.float32).to(device)
Ytr = Ftr; Yte = Fte

for epoch in range(1,201):
    model.train()
    pred = model(Xtr, Ftr)
    loss = criterion(pred, Ytr)
    optimizer.zero_grad(); loss.backward(); optimizer.step()
    if epoch % 50 == 0:
        model.eval()
        with torch.no_grad():
            val_loss = criterion(model(Xte, Fte), Yte).item()
        print(f"Epoch: {epoch}, Train Loss: {loss.item():.4f}, Val Loss: {val_loss:.4f}")

# 5. save model
torch.save(model.state_dict(), "../models/hybrid_muconic_m1.pth")
print("training done, Model saved: ../models/hybrid_muconic_m1.pth")
