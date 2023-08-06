import numpy as np
import torch.nn
import torchmetrics


class Metrics(object):
    def __init__(self, metrics=None):
        self.metrics = [] if metrics is None else metrics

    def add(self, predict, target, weight=1.):
        for metric in self.metrics:
            metric.add(predict=predict, target=target, weight=weight)
        return self

    @property
    def value(self):
        return [i.value for i in self.metrics] if self.metrics else []

    def __call__(self, *args, **kwargs):
        return self.add(*args, **kwargs)


class Metric(object):
    def __init__(self):
        self.name = self.__class__.__name__
        self.mean = RawMoments(n=1)

    def loss_function(self, predict, target):
        ...

    def add(self, predict, target, weight=1.):
        value = self.loss_function(predict, target) * weight
        self.mean.add(value)
        return self

    @property
    def value(self):
        return self.mean.value

    def __call__(self, *args, **kwargs):
        return self.add(*args, **kwargs)


class MSE(Metric):
    def loss_function(self, predict, target, *args, **kwargs):
        return torch.nn.MSELoss(reduction='mean')(predict, target)


class Accuracy1D(Metric):
    def loss_function(self, predict, target):
        target = target.detach().long()
        return torchmetrics.Accuracy(num_classes=1)(predict, target)


class AUROC1D(Metric):
    def loss_function(self, predict, target):
        target = target.detach().long()
        return torchmetrics.AUROC(pos_label=1)(predict, target)

    def add(self, predict, target, weight=1.):
        value = self.loss_function(predict, target) * weight
        if value:
            self.mean.add(value)
        return self


class RawMoments(object):
    """
    https://en.wikipedia.org/wiki/Moment_(mathematics)
    http://sofasofa.io/forum_main_post.php?postid=1022163
    """

    def __init__(self, n):
        self.n = n
        self.count = 0
        self.sum = 0

    def add(self, value):
        self.sum += value ** self.n
        self.count += 1
        return self

    @property
    def value(self):
        return (self.sum / self.count if self.count else torch.tensor(0.)).numpy()

    def __call__(self, *args, **kwargs):
        return self.add(*args, **kwargs)


class CentralMoments(object):
    """
    https://en.wikipedia.org/wiki/Moment_(mathematics)
    http://sofasofa.io/forum_main_post.php?postid=1022163
    """

    def __init__(self, n):
        self.n = n
        self.x = []
        self.raw_moments_1 = RawMoments(n=1)

    def add(self, value):
        self.x.append(value)
        self.raw_moments_1.add(value)
        return self

    @property
    def x_hat(self):
        return self.raw_moments_1.value

    @property
    def value(self):
        return ((np.array(self.x) - self.x_hat) ** self.n).mean()

    def __call__(self, *args, **kwargs):
        return self.add(*args, **kwargs)


def test():
    seq = [i for i in range(0, 10)]
    rm = RawMoments(1)
    [rm.add(v) for v in seq]
    print(rm.value)
    assert rm.value == 4.5

    cm = CentralMoments(2)
    [cm.add(v) for v in seq]
    print(cm.value)
    assert cm.value == 8.25

    predict = torch.tensor([0.1, 0.9, 0.1, 0.9, 0.9])
    target = torch.tensor([0, 0, 1, 1, 1])

    auroc = Accuracy1D()(predict, target).value
    print(auroc)


if __name__ == '__main__':
    test()
