import torch
import torch.nn as nn


class MLP(nn.Module):
    def __init__(self, input_size, hidden_sizes, activation, last_layer_activation=False):
        super().__init__()
        self.num_features = (input_size,) + tuple(hidden_sizes)
        self.net = nn.Sequential()
        if isinstance(activation, str):
            act_fn = _get_activation_fn(activation, dim=1)
        else:
            act_fn = activation
        n = 0
        for i, (curr_in, curr_out) in enumerate(zip(self.num_features[0:-1], self.num_features[1:])):
            self.net.add_module(str(n), nn.Linear(in_features=curr_in, out_features=curr_out))
            n += 1
            if last_layer_activation or i < (len(hidden_sizes) - 1):
                self.net.add_module(str(n), act_fn)
                n += 1

    def forward(self, x):
        x = self.net(x)
        return x


class MMoE(nn.Module):
    def __init__(self, input_size, expert_num, expert_hidden_sizes,
                 task_num, task_hidden_sizes, task_last_activations):
        super().__init__()
        assert task_num == len(task_hidden_sizes) == len(task_last_activations), "task num does not match"

        self.input_size = input_size
        self.expert_num = expert_num
        self.expert_hidden_sizes = tuple(expert_hidden_sizes)
        self.task_num = task_num
        self.task_hidden_sizes = tuple(task_hidden_sizes)
        self.task_last_activations = nn.ModuleList([
            _get_activation_fn(act) if act is None or isinstance(act, str) else act
            for act in task_last_activations
        ])
        # print(self.task_last_activations)
        # self.tower_size = tower_size
        # self._param_expert = []

        self.experts = nn.ModuleDict()
        for i in range(self.expert_num):
            self.experts[f"expert_mlp_{i}"] = MLP(
                input_size=input_size,
                hidden_sizes=self.expert_hidden_sizes,
                activation="relu",
                last_layer_activation=True,
            )

        self.gates = nn.ModuleDict()
        self.tasks = nn.ModuleDict()
        for i in range(self.task_num):
            self.gates[f"gate_mlp_{i}"] = MLP(
                input_size=input_size,
                hidden_sizes=[expert_num],
                activation="softmax",
                last_layer_activation=True,
            )  # TODO: UserWarning: Implicit dimension choice for softmax has been deprecated. Change the call to include dim=X as an argument.
            self.tasks[f"task_mlp_{i}"] = MLP(
                input_size=self.expert_hidden_sizes[-1],
                hidden_sizes=self.task_hidden_sizes[i],
                activation="relu",
                last_layer_activation=False
            )

    def forward(self, features_in):
        expert_outs_list = []
        for i in range(0, self.expert_num):
            expert_out = self.experts[f"expert_mlp_{i}"](features_in)
            expert_outs_list.append(expert_out)  # (B, hidden] * E
        expert_outs = torch.stack(expert_outs_list, dim=1)  # [B, E, expert_hidden]

        task_outs_list = []
        for i in range(self.task_num):
            gate_weight = self.gates[f"gate_mlp_{i}"](features_in)  # [B, E]
            gate_weight = gate_weight.unsqueeze(2)  # [B, E, 1]
            gate_out = expert_outs.mul(gate_weight).sum(dim=1)  # [B, expert_hidden]
            task_out = self.tasks[f"task_mlp_{i}"](gate_out)
            task_out = self.task_last_activations[i](task_out)  # [B, task_hidden]
            # task_out = torch.nan_to_num(task_out, 1e-15)
            # task_out = task_out.clamp(min=1e-15, max=1.0 - 1e-15)  # TODO: need clip?
            task_outs_list.append(task_out)
        
        return task_outs_list


def _get_activation_fn(activation, dim=None):
    if activation is None or activation.lower() == "none":
        return nn.Identity()
    elif activation == "relu":
        return nn.ReLU()
    elif activation == "gelu":
        return nn.GELU()
    elif activation == "sigmoid":
        return nn.Sigmoid()
    elif activation == "softmax":
        return nn.Softmax(dim=dim)
    elif activation == "tanh":
        return nn.Tanh()
    # elif activation == "leakyrelu":
    #     return nn.LeakyReLU()
    # elif activation == "softrelu":
    #     return nn.Softplus()

    raise RuntimeError("activation should be relu/gelu/sigmoid/softmax/tanh, not {}".format(activation))
