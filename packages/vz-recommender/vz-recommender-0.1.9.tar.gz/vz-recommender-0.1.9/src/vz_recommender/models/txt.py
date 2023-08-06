import math
import torch
import torch.nn as nn
from torch.nn import TransformerEncoder, TransformerEncoderLayer


class MeanMaxPooling(nn.Module):
    """
    [B, S, E] -> [B, 2*E]
    """
    def __init__(self, axis=1, dropout=0.0):
        super().__init__()
        self.axis = axis
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, inputs, valid_length=None):
        """
        :param inputs: Tensor, shape [batch_size, seq_len, embedding_dim]
        :param valid_length: None or Tensor, valid len of token in the sequence with shape [batch_size]
        :return: Tensor, shape [batch_size, 2 * embedding_dim]
        """
        # TODO: broadcast indexing to mean over first vl
        mean_out = torch.mean(inputs, dim=self.axis) if valid_length is None \
            else torch.sum(inputs, dim=self.axis) / valid_length.add(1E-7).unsqueeze(1)
        max_out = torch.max(inputs, dim=self.axis).values
        outputs = torch.cat((mean_out, max_out), dim=1)
        outputs = self.dropout(outputs)
        return outputs


class PositionalEncoding(nn.Module):
    """
    [B, S, E] -> [B, S, E]
    """
    def __init__(self, d_model, max_len=5000, dropout=0.1):
        """
        Constant layer of positional encoding

        :param d_model: int, dimension of token embedding
        :param max_len: int, max length of sequence
        :param dropout: float
        """
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(1, max_len, d_model)
        pe[0, :, 0::2] = torch.sin(position * div_term)
        pe[0, :, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x):
        """
        :param x: Tensor, shape [batch_size, seq_len, embedding_dim]
        :return: : Tensor, shape [batch_size, seq_len, embedding_dim]
        """
        x = x + self.pe[:, :x.size(1), :]
        return self.dropout(x)


class ContextTransformer(nn.Module):
    """
    [[B, ] * C] -> [B, cross_size]
    """
    def __init__(self, ctx_nums, cross_size, ctx_embed_size=100, ctx_num_heads=2,
                 ctx_hidden_size=512, ctx_num_layers=1, ctx_transformer_dropout=0.0,
                 ctx_pooling_dropout=0.0, ctx_pe=False):
        super().__init__()
        self.ctx_embedding = nn.ModuleList([
            nn.Embedding(ctx_num, ctx_embed_size)
            for ctx_num in ctx_nums
        ])
        self.ctx_pe = ctx_pe
        self.ctx_embed_size = ctx_embed_size
        if ctx_pe:
            self.pos_encoder = PositionalEncoding(d_model=ctx_embed_size,
                                                  dropout=ctx_transformer_dropout,
                                                  max_len=len(ctx_nums))
        encoder_layers = TransformerEncoderLayer(d_model=ctx_embed_size,
                                                 nhead=ctx_num_heads,
                                                 dropout=ctx_transformer_dropout,
                                                 dim_feedforward=ctx_hidden_size,
                                                 activation='relu',
                                                 batch_first=True)
        self.ctx_encoder = TransformerEncoder(encoder_layers, num_layers=ctx_num_layers)
        self.ctx_pooling_dp = MeanMaxPooling(dropout=ctx_pooling_dropout)
        self.ctx_dense = torch.nn.Linear(in_features=2 * ctx_embed_size, out_features=cross_size)

    def forward(self, ctx_in):
        """
        :param ctx_in: list, a list of Tensor of shape [batch_size, 1]
        :return: Tensor, shape [batch_size, cross_size]
        """
        # [[B, ] * C]
        ctx_embedding_list = [self.ctx_embedding[i](input_ctx).unsqueeze(1)
                                  for i, input_ctx in enumerate(ctx_in)]  # -> [(B, 1, E) * C]
        ctx_out = torch.cat(ctx_embedding_list, dim=1)  # -> (B, C, E)
        if self.ctx_pe:
            ctx_out = ctx_out * math.sqrt(self.ctx_embed_size)
            ctx_out = self.pos_encoder(ctx_out)
        ctx_out = self.ctx_encoder(ctx_out)  # -> (B, C, E)
        ctx_out = self.ctx_pooling_dp(ctx_out)  # -> (B, 2*E)
        ctx_out = self.ctx_dense(ctx_out)  # -> (B, cross_size)
        # print(ctx_out.shape)
        return ctx_out


class SequenceTransformerHistory(nn.Module):
    """
    [B, S] -> [B, cross_size]
    """

    def __init__(self, seq_num, cross_size, seq_embed_dim=200, seq_max_length=8, seq_num_heads=4,
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
        self.seq_dense = torch.nn.Linear(in_features=2 * seq_embed_dim, out_features=cross_size)

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
        seq_out = self.seq_dense(seq_out)  # -> (B, cross_size)
        return seq_out


class TxT(nn.Module):
    def __init__(self, ctx_nums, seq_num, act_type="gelu", cross_size=200,
                 context_transformer_kwargs=None, sequence_transformer_kwargs=None):
        super().__init__()
        context_transformer_kwargs = context_transformer_kwargs if context_transformer_kwargs else {}
        sequence_transformer_kwargs = sequence_transformer_kwargs if sequence_transformer_kwargs else {}
        self.features_dim = cross_size
        self.context_transformer = ContextTransformer(
            ctx_nums=ctx_nums,
            cross_size=cross_size,
            **context_transformer_kwargs,
        )
        self.sequence_transformer = SequenceTransformerHistory(
            seq_num=seq_num,
            cross_size=cross_size,
            **sequence_transformer_kwargs,
        )
        self.dense1 = nn.Linear(cross_size, seq_num // 2)
        if act_type == "relu":
            self.act = nn.ReLU()
        elif act_type == "gelu":
            self.act = nn.GELU()
        elif act_type == "leakyRelu":
            self.act = nn.LeakyReLU(0.2)
        else:
            raise NotImplementedError
        self.dense2 = nn.Linear(seq_num // 2, seq_num)

    def forward(self, ctx_in, seq_in, vl_in, seq_history=None):
        """
        :param ctx_in: list, a list of Tensor of shape [batch_size]
        :param seq_in: Tensor, shape [batch_size, seq_len]
        :param vl_in: Tensor, shape [batch_size]
        :param seq_history: Tensor, shape [batch_size, history_len]
        :return:
        """
        # input [[B, ] * C] and [B, 5]
        ctx_out = self.context_transformer(ctx_in=ctx_in)
        seq_out = self.sequence_transformer(seq_in=seq_in, vl_in=vl_in, seq_history=seq_history)
        outs = torch.mul(seq_out, ctx_out)  # -> [B, cross_size]
        outs = self.dense1(outs)  # -> [B, seq_num//2]
        outs = self.act(outs)
        outs = self.dense2(outs)  # -> [B, seq_num]
        return outs
