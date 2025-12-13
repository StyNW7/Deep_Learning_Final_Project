import torch
import torch.nn as nn
import math
import numpy as np

adj_matrix = torch.load("ai_models/adj_matrix_best.pt")

NUM_NODES = 13
NUM_FEATURES = 10
TARGET_DIM = 6

class GraphConv(nn.Module):
    def __init__(self, in_features, out_features, adj_matrix):
        super(GraphConv, self).__init__()
        self.adj = adj_matrix
        self.fc = nn.Linear(in_features, out_features)

    def forward(self, x):
        out = torch.bmm(self.adj.unsqueeze(0).repeat(x.size(0), 1, 1), x)
        return self.fc(out)

class TGCN(nn.Module):
    def __init__(self, num_nodes, num_features, hidden_dim, output_dim, adj_matrix, dropout_prob=0.0):
        super(TGCN, self).__init__()
        self.gc1 = GraphConv(num_features, hidden_dim, adj_matrix)
        self.gru = nn.GRU(hidden_dim, hidden_dim, batch_first=True)
        self.dropout = nn.Dropout(dropout_prob)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        B, T, N, F = x.shape
        out = []
        for t in range(T):
            xt = x[:, t, :, :]
            xt = torch.relu(self.gc1(xt))
            out.append(xt)
        out = torch.stack(out, dim=1)
        out = out.transpose(1, 2)
        out = out.reshape(B * N, T, -1)
        out, _ = self.gru(out)
        out = out[:, -1, :]
        out = self.dropout(out)
        out = self.fc(out)
        out = out.view(B, N, -1)
        return out

def get_model():
    model = TGCN(NUM_NODES, NUM_FEATURES, 128, TARGET_DIM, adj_matrix, 0.1)
    state_dict = torch.load(
        'ai_models/best_tuned_model.pth',
        map_location=torch.device('cpu')
    )
    model.load_state_dict(state_dict)
    return model

def predict_torch(tensor_input, model):
    model.eval()
    with torch.no_grad():
        return model(tensor_input)