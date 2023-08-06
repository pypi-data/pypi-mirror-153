import torch
import math
import numpy as np
from typing import *
from torch import nn, Tensor
from torch.nn import TransformerEncoder, TransformerEncoderLayer

from .txt import (ContextTransformer, MeanMaxPooling, PositionalEncoding,
                  SequenceTransformerHistory)

# Transformer x Embedding x Embedding as Bottom

class CanGenTransformer(nn.Module):
    """
    [B, S] -> [B, seq_num]
    """

    def __init__(self, seq_dim, seq_embed_dim=200, seq_max_length=19, seq_num_heads=4,
                 seq_hidden_size=256, seq_transformer_dropout=0.0, seq_num_layers=2, seq_pooling_dropout=0.0,
                 seq_pe=True, act_type="leakyRelu"):
        super().__init__()
        self.seq_embedding = nn.Embedding(seq_dim, seq_embed_dim)
        self.seq_pos = seq_pe
        self.seq_embed_size = seq_embed_dim
        if seq_pe:
            self.pos_encoder = PositionalEncoding(d_model=seq_embed_dim,
                                                  dropout=seq_transformer_dropout,
                                                  max_len=seq_max_length)
        encoder_layers = TransformerEncoderLayer(d_model=seq_embed_dim,
                                                 nhead=seq_num_heads,
                                                 dropout=seq_transformer_dropout,
                                                 dim_feedforward=seq_hidden_size,
                                                 activation='relu',
                                                 batch_first=True)
        self.seq_encoder = TransformerEncoder(encoder_layers, num_layers=seq_num_layers)
        self.seq_pooling_dp = MeanMaxPooling(dropout=seq_pooling_dropout)
        self.dense1 = torch.nn.Linear(in_features=2 * seq_embed_dim, out_features=2 * seq_embed_dim)
        if act_type == "relu":
            self.act1 = self.act2 = nn.ReLU()
        elif act_type == "gelu":
            self.act1 = self.act2 = nn.GELU()
        elif act_type == "leakyRelu":
            self.act1 = self.act2 = nn.LeakyReLU(0.2)
        else:
            raise NotImplementedError
        self.dense2 = torch.nn.Linear(2 * seq_embed_dim, seq_embed_dim)
        self.dense3 = torch.nn.Linear(seq_embed_dim, seq_dim)

    @staticmethod
    def create_key_padding_mask(seq_in, valid_length):
        device = valid_length.device
        # mask = torch.arange(seq_in.size(1)).repeat(seq_in.size(0), 1).to(device)
        mask = torch.arange(seq_in.size(1)).repeat(seq_in.size(0), 1).to(device)
        mask = ~mask.lt(valid_length.unsqueeze(1))
        return mask

    def forward(self, seq_in, vl_in):
        """
        :param seq_in: Tensor, shape [batch_size, seq_len]
        :param vl_in: Tensor, shape [batch_size]
        :return: Tensor, shape [batch_size, cross_size]
        """
        # print("initial_shape:",input_seq.shape)
        # (B, 5), (B, 10)
        seq_out = self.seq_embedding(seq_in.long())  # -> (B, 5, E)
        if self.seq_pos:
            seq_out = seq_out * math.sqrt(self.seq_embed_size)
            seq_out = self.pos_encoder(seq_out)
        mask = self.create_key_padding_mask(seq_in=seq_in, valid_length=vl_in)
        seq_out = self.seq_encoder(seq_out, src_key_padding_mask=mask)
        if mask[:, 0].any():
            seq_out = seq_out.nan_to_num(nan=0.0)
        seq_out = self.seq_pooling_dp(seq_out)  # -> (B, 2*E)
        seq_out = self.dense1(seq_out)  # -> (B, cross_size)
        seq_out = self.act1(seq_out)
        seq_out = self.dense2(seq_out)
        user_out = self.act2(seq_out)
        seq_out = self.dense3(user_out)
        
        return (seq_out, user_out)