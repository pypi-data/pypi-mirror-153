import torch
import math
import numpy as np
from typing import *
from torch import nn, Tensor
from torch.nn import TransformerEncoder, TransformerEncoderLayer

from .txt import (ContextTransformer, MeanMaxPooling, PositionalEncoding)


class SequenceTransformerHistory(nn.Module):
    """
    [B, S] -> [B, cross_size]
    """

    def __init__(self, seq_num, seq_embed_dim=200, seq_max_length=8, seq_num_heads=4,
                 seq_hidden_size=512, seq_transformer_dropout=0.0, seq_num_layers=2, seq_pooling_dropout=0.0,
                 seq_pe=True):
        super().__init__()
        self.seq_embedding = nn.Embedding(seq_num, seq_embed_dim)
        self.seq_pos = seq_pe
        self.seq_embed_dim = seq_embed_dim
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
        # self.seq_dense = torch.nn.Linear(in_features=2 * seq_embed_dim, out_features=cross_size)

    @staticmethod
    def create_key_padding_mask(seq_in, valid_length):
        device = valid_length.device
        # mask = torch.arange(seq_in.size(1)).repeat(seq_in.size(0), 1).to(device)
        mask = torch.arange(seq_in.size(1)).repeat(seq_in.size(0), 1).to(device)
        mask = ~mask.lt(valid_length.unsqueeze(1))
        return mask

    def forward(self, seq_in, vl_in, seq_history=None):
        """
        :param seq_in: Tensor, shape [batch_size, seq_len]
        :param vl_in: Tensor, shape [batch_size]
        :param seq_history: Tensor, shape [batch_size, history_len]
        :return: Tensor, shape [batch_size, cross_size]
        """
        # print("initial_shape:",input_seq.shape)
        # (B, 5), (B, 10)
        seq_embed_out = self.seq_embedding(seq_in.long())  # -> (B, 5, E)
        # history_embed_out = self.seq_embedding(input_history_seq.long())
        # history_embed_out = history_embed_out.transpose(0, 1).mean(dim=0, keepdim=True)  # -> (1, B, E)
        # combined_embed_out = torch.cat([history_embed_out, seq_embed_out], dim=0)  # -> (6, B, E)
        seq_out = seq_embed_out
        if self.seq_pos:
            seq_out = seq_out * math.sqrt(self.seq_embed_dim)
            seq_out = self.pos_encoder(seq_out)
        mask = self.create_key_padding_mask(seq_in=seq_in, valid_length=vl_in)
        seq_out = self.seq_encoder(seq_out, src_key_padding_mask=mask)
        if mask[:, 0].any():
            seq_out = seq_out.nan_to_num(nan=0.0)
        seq_out = self.seq_pooling_dp(seq_out)  # -> (B, 2*E)
        # seq_out = self.seq_dense(seq_out)  # -> (B, cross_size)
        return seq_out


class SequenceTransformerHistoryLite(SequenceTransformerHistory):
    def __init__(self, item_embedding, seq_embed_dim, seq_max_length=8, seq_num_heads=4,
                 seq_hidden_size=512, seq_transformer_dropout=0.0, seq_num_layers=2, seq_pooling_dropout=0.0,
                 seq_pe=True):
        super(SequenceTransformerHistory, self).__init__()
        self.seq_embedding = item_embedding
        self.seq_pos = seq_pe
        self.seq_embed_dim = seq_embed_dim
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


class ContextHead(nn.Module):
    """
    [[B, ] * C] -> [B, cross_size]
    """
    def __init__(self, deep_dims, item_embedding, deep_embed_dims=100, num_wide=0, num_shared=1):
        super().__init__()
        if isinstance(deep_embed_dims, int):
            self.deep_embedding = nn.ModuleList([
                nn.Embedding(deep_dim, deep_embed_dims)
                for deep_dim in deep_dims
            ])
            dense_in = len(deep_dims) * deep_embed_dims
        elif isinstance(deep_embed_dims, list) or isinstance(deep_embed_dims, tuple):
            self.deep_embedding = nn.ModuleList([
                nn.Embedding(deep_dim, deep_embed_dim)
                for deep_dim, deep_embed_dim in zip(deep_dims, deep_embed_dims)
            ])
            dense_in = sum(deep_embed_dims)
        else:
            raise NotImplementedError()
        self.ctx_pe = False
        self.layer_norm = nn.LayerNorm(num_wide)
        self.deep_embed_dims = deep_embed_dims
        self.shared_embed = nn.ModuleList([
                item_embedding
                for _ in range(num_shared)
            ])
        # self.ctx_dense = torch.nn.Linear(in_features=dense_in+num_wide+item_embedding.embedding_dim, out_features=cross_size)


    def forward(self, deep_in:List[Tensor], wide_in:List[Tensor]=None, shared_in:List[Tensor]=None):
        """
        :param deep_in: list, a list of Tensor of shape [batch_size, 1]
        :param wide_in: list, a list of Tensor of shape [batch_size, 1]
        :param device_in: Tensor
        :return: Tensor, shape [batch_size, cross_size]
        """
        # [[B, ] * C]
        deep_embedding_list = [self.deep_embedding[i](input_deep).unsqueeze(1)
                              for i, input_deep in enumerate(deep_in)]  # -> [(B, 1, E_i) * C]
        if shared_in is not None:
            shared_in_list = [self.shared_embed[i](input_shared).unsqueeze(1)
                              for i, input_shared in enumerate(shared_in)] 
            # device_out = self.device_embed(shared_in).unsqueeze(1)
            # device_out = torch.nan_to_num(device_out)
            deep_embedding_list.extend(shared_in_list) # -> [(B, 1, E_i) * C]
        deep_out = torch.cat(deep_embedding_list, dim=2).squeeze(1) # -> [B, sum(E_i)]
        if wide_in is not None:
            wide_in_list = [wide_i.float() for wide_i in wide_in]
            wide_cat = torch.stack(wide_in_list, dim=0)
            wide_out = torch.transpose(wide_cat, dim1=1, dim0=0)
            wide_out_norm = self.layer_norm(wide_out)
            ctx_out = torch.cat((deep_out, wide_out_norm), dim=1) # -> [B, sum(E_i)]
        else:
            ctx_out = deep_out
        # ctx_out = self.ctx_dense(ctx_out)  # -> (B, cross_size)
        return ctx_out



class BST(nn.Module):
    def __init__(self, deep_dims, seq_dim, seq_embed_dim, deep_embed_dims, seq_hidden_size,
                 num_wide=0, num_shared=0, context_head_kwargs=None, sequence_transformer_kwargs=None):
        super().__init__()
        context_head_kwargs = context_head_kwargs if context_head_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        self.item_embedding = nn.Embedding(seq_dim, seq_embed_dim)
        self.context_head = ContextHead(
            deep_dims=deep_dims,
            num_wide=num_wide,
            item_embedding=self.item_embedding,
            deep_embed_dims=deep_embed_dims
        )
        self.sequence_transformer = SequenceTransformerHistoryLite(
            item_embedding=self.item_embedding,
            seq_embed_dim=seq_embed_dim,
            seq_hidden_size=seq_hidden_size,
            **sequence_transformer_kwargs,
        )
        self.dense1 = torch.nn.Linear(in_features=len(deep_dims)*deep_embed_dims+num_wide+seq_embed_dim+seq_embed_dim+(num_shared*seq_embed_dim), out_features=2 * seq_embed_dim)
        self.act1 = self.act2 = nn.LeakyReLU(0.2)
        self.dense2 = torch.nn.Linear(2 * seq_embed_dim, seq_embed_dim)
        self.dense3 = torch.nn.Linear(seq_embed_dim, seq_dim)

    def forward(self, deep_in, seq_in, vl_in, wide_in=None, shared_in=None):
        """
        :param ctx_in: list, a list of Tensor of shape [batch_size, 1]
        :param num_in: list, a list of Tensor of shape [batch_size, 1]
        :param seq_in: Tensor, shape [batch_size, seq_len]
        :param vl_in: Tensor, shape [batch_size]
        :param candidate_in: Tensor, shape [batch_size]
        :param seq_history: Tensor, shape [batch_size, history_len]
        :return:
        """
        # input [[B, 1] * C] and [B, 5]
        ctx_out = self.context_head(deep_in=deep_in, wide_in=wide_in, shared_in=shared_in)
        seq_out = self.sequence_transformer(seq_in=seq_in, vl_in=vl_in)
        outs = torch.cat([seq_out, ctx_out], dim=1)  # -> [B, CROSS_seq + CROSS_ctx]
        outs = self.dense1(outs)  # -> (B, cross_size)
        outs = self.act1(outs)
        outs = self.dense2(outs)
        user_out = self.act2(outs)
        outs = self.dense3(user_out)
        return (outs, user_out)