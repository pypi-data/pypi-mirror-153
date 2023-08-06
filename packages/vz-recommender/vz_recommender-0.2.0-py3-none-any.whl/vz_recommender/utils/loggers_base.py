import numpy as np
import torch
from torchmetrics.classification.auroc import AUROC
from torchmetrics.classification.f_beta import F1Score 
from torchmetrics.classification.accuracy import Accuracy 


def get_loss_scales(net, task1_criterion, task2_criterion, dataloader, device):
    net.eval()
    net.to(device)
    loss1_all = []
    loss2_all = []
    with torch.no_grad():
        for (ctx, seq, vl, candidate), (label_pos, label_price) in dataloader:
            out = net(
                ctx_in=[c.to(device) for c in ctx],
                seq_in=seq.to(device),
                vl_in=vl.to(device),
                candidate_in=candidate.to(device),
                seq_history=None
            )
            # print("*" * 10, f"torch.cuda.max_memory_allocated(): {torch.cuda.max_memory_allocated()}, "
            #       f"memory_allocated: {torch.cuda.memory_allocated()}", "*" * 10)
            loss1 = task1_criterion(out[0].squeeze(), label_pos.float().to(device))
            loss2 = task2_criterion(out[1].squeeze(), label_price.float().to(device))
            loss1_all.append(loss1.item())
            loss2_all.append(loss2.item())
    print("mean:", np.mean(loss1_all), np.mean(loss2_all))
    print("max:", np.max(loss1_all), np.max(loss2_all))
    loss1_scale = np.max(loss1_all)
    loss2_scale = np.max(loss2_all)
    return loss1_scale, loss2_scale


class BaseLogger:
    def __init__(self, metric):
        assert metric in ["acc", "f1", "mae", "mse", "loss", "auroc", "identity"]
        self.metric_name = metric
        if metric == "acc":
            self.metric_fn = self.get_acc
        elif metric == "f1":
            self.metric_fn = self.get_f1
        elif metric == "mae":
            self.metric_fn = self.get_mae
        elif metric == "mse":
            self.metric_fn = self.get_mse
        elif metric == "auroc":
            self.metric_fn = self.get_auroc
        elif metric == "identity" or metric == "loss":
            self.metric_fn = self.get_loss
        else:
            raise NotImplementedError()
        self.metrics_step = []

    def update(self, y_pred, y_true):
        self.metrics.append(self.metric_fn(y_pred, y_true))

    def get(self, reduce="mean"):
        if reduce == "mean":
            return np.mean(self.metrics)
        elif reduce == "count":
            return len(self.metrics)
        else:
            raise NotImplementedError()

    def reset(self):
        self.metrics = []

    @staticmethod
    def get_loss(loss, _):
        return loss.item()

    @staticmethod
    def get_acc(y_pred: torch.Tensor, y_true: torch.Tensor):
        acc = Accuracy()
        return acc(y_pred, y_true.int())

    @staticmethod
    def get_f1(y_pred, y_true):
        f1_score = F1Score()
        return f1_score(y_pred, y_true.int())

    @staticmethod
    def get_auroc(y_pred, y_true):
        auroc = AUROC()
        return auroc(y_pred, y_true.int())
    
    # @staticmethod
    # def get_f1(y_pred, y_true, epsilon=1e-7):
    #     y_pred = (y_pred > 0.5).float()
    #     tp = (y_true == y_pred).float().sum()
    #     negative = (y_true != y_pred).float()
    #     fp = (negative == 1).float().sum()
    #     fn = (negative == 0).float().sum()
    #     precision = tp / (tp + fp + epsilon)
    #     recall = tp / (tp + fn + epsilon)
    #     f1 = 2 * (precision * recall) / (precision + recall)
    #     return f1.item()

    @staticmethod
    def get_mae(y_pred: torch.Tensor, y_true: torch.Tensor):
        return (y_true - y_pred).abs().mean().item()

    @staticmethod
    def get_mse(y_pred: torch.Tensor, y_true: torch.Tensor):
        return (y_true - y_pred).pow(2).mean().item()


class MetricLogger:
    def __init__(self, names, metrics):
        self.metrics = {
            name: BaseLogger(metric=metric)
            for name, metric in zip(names, metrics)
        }

    def add(self, name, metric):
        self.metrics.update({name: metric})

    def update(self, metric_name, y_pred, y_true):
        if metric_name is None:
            for metric in self.metrics.values():
                metric.update(y_pred, y_true)
        else:
            self.metrics[metric_name].update(y_pred, y_true)

    def reset(self, metric_name):
        if metric_name is None:
            for metric in self.metrics.values():
                metric.reset()
        else:
            self.metrics[metric_name].reset()

    def get(self, metric_name, reduce="mean"):
        return self.metrics[metric_name].get(reduce=reduce)
