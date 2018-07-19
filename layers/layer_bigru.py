import torch
import torch.nn as nn

from layers.layer_birnn_base import LayerBiRNNBase

class LayerBiGRU(LayerBiRNNBase):
    def __init__(self, input_dim, hidden_dim, gpu):
        super(LayerBiGRU, self).__init__(input_dim, hidden_dim, gpu)
        self.rnn_forward_layer = nn.GRUCell(input_dim, hidden_dim)
        self.rnn_backward_layer = nn.GRUCell(input_dim, hidden_dim)

    def forward(self, input_tensor): #input_tensor shape: batch_size x max_seq_len x dim
        batch_size, max_seq_len, _ = input_tensor.shape
        # Init rnn's states by zeros
        rnn_forward_h = self.make_gpu(torch.zeros(batch_size, self.hidden_dim))
        rnn_backward_h = self.make_gpu(torch.zeros(batch_size, self.hidden_dim))
        # Forward pass in both directions
        output = self.make_gpu(torch.zeros(batch_size, max_seq_len, self.hidden_dim * 2))
        for l in range(max_seq_len):
            n = max_seq_len - l - 1
            rnn_forward_h = self.rnn_forward_layer(input_tensor[:, l, :], rnn_forward_h)
            rnn_backward_h = self.rnn_backward_layer(input_tensor[:, n, :], rnn_backward_h)
            output[:, l, :self.hidden_dim] = rnn_forward_h
            output[:, n, self.hidden_dim:] = rnn_backward_h
        return output
