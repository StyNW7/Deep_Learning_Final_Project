import torch
import torch.nn as nn
import math
import numpy as np

adj_matrix = torch.load("ai_models/adj_matrix.pt")

NUM_NODES = 13
NUM_FEATURES = 10
TARGET_DIM = 1

class TGCN(nn.Module):
    def __init__(self, num_nodes, num_features, hidden_dim, output_dim, adj_matrix):
        super(TGCN, self).__init__()
        self.num_nodes = num_nodes
        self.hidden_dim = hidden_dim
        self.adj = adj_matrix

        self.gcn_weight = nn.Parameter(torch.FloatTensor(num_features, hidden_dim))
        self.gcn_bias = nn.Parameter(torch.FloatTensor(hidden_dim))

        self.lstm = nn.LSTM(input_size=hidden_dim, hidden_size=hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)
        self._init_weights()

    def _init_weights(self):
        stdv = 1.0 / math.sqrt(self.hidden_dim)
        self.gcn_weight.data.uniform_(-stdv, stdv)
        self.gcn_bias.data.uniform_(-stdv, stdv)

    def forward(self, x):
        batch_size, seq_len, num_nodes, _ = x.size()
        x_reshaped = x.view(-1, num_nodes, x.size(3))
        ax = torch.matmul(self.adj, x_reshaped)
        gcn_out = torch.relu(torch.matmul(ax, self.gcn_weight) + self.gcn_bias)
        gcn_out = gcn_out.view(batch_size, seq_len, num_nodes, self.hidden_dim)
        lstm_input = gcn_out.permute(0, 2, 1, 3).contiguous().view(batch_size * num_nodes, seq_len, self.hidden_dim)
        lstm_out, _ = self.lstm(lstm_input)
        out = self.fc(lstm_out[:, -1, :])
        return out.view(batch_size, num_nodes, -1)

def get_model():
    model = TGCN(NUM_NODES, NUM_FEATURES, 64, TARGET_DIM, adj_matrix)
    model.load_state_dict(torch.load('ai_models/model_weights.pth'))
    return model

def predict_torch(tensor_input, model):
    model.eval()
    with torch.no_grad():
        return model(tensor_input)