import os
import torch
from tqdm import tqdm
from .metrics import Accuracy1D, AUROC1D, Metrics


class FileMixin:
    __slots__ = ('path', 'state_dict', 'load_state_dict')

    def save(self):
        torch.save(self.state_dict(), self.path)

    def load(self):
        return self.load_state_dict(torch.load(self.path))


class BaseDataset(object):
    def __init__(self, gen):
        self.gen = gen

    def __call__(self, *args, **kwargs):
        return self.gen(*args, **kwargs)


class Dataset(object):
    def __init__(self, train: BaseDataset, test: BaseDataset):
        self.train = train
        self.test = test


class Model(torch.nn.Module, FileMixin):
    def __init__(self, epoch=1, path=''):
        super(Model, self).__init__()
        self.epoch = epoch
        self.name = self.__class__.__name__
        self.path = os.path.join(path, self.name + '.pt')

        self._loss = None
        self._metrics = None
        self._optimizer = None

    def forward(self, *args, **kwargs):
        return

    def step_grad(self, loss):
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    @property
    def loss(self):
        self._loss = self.set_loss() if self._loss is None else self._loss
        return self._loss

    def set_loss(self):
        return torch.nn.MSELoss()

    @property
    def metrics(self):
        self._metrics = self.set_metrics() if self._metrics is None else self._metrics
        return self._metrics

    def set_metrics(self):
        metrics = Metrics(metrics=[Accuracy1D(), AUROC1D()])
        return metrics

    @property
    def optimizer(self):
        self._optimizer = self.set_optimizer() if self._optimizer is None else self._optimizer
        return self._optimizer

    def set_optimizer(self):
        return torch.optim.Adam(self.parameters(), lr=1e-3)

    # --- split line : unstable as follows ---
    def stage(self, name, step_function, epoch, dataset: BaseDataset, grad: bool = False):
        self._metrics = None
        for _epoch in range(epoch):
            bar = tqdm(dataset(), desc=name)
            bar.set_description('%s %s' % (name, _epoch))
            for batch in bar:
                if grad:
                    _step = step_function(batch=batch)
                    if len(_step) == 4:
                        loss, predict, target, weight = _step
                    else:
                        loss, predict, target = _step
                        weight = 1.
                    self.step_grad(loss)
                else:
                    _step = step_function(batch=batch)
                    if len(_step) == 3:
                        predict, target, weight = _step
                    else:
                        predict, target = _step
                        weight = 1.
                self.metrics.add(predict=predict, target=target, weight=weight)
                bar.set_postfix(
                    dict(zip([i.name for i in self.metrics.metrics],
                             [i.value for i in self.metrics.metrics])))

    def fit(self):
        self.train()
        dataset = self.dataset()
        self.stage(name='Train', step_function=self.train_step,
                    epoch=self.epoch, dataset=dataset.train, grad=True)
        self.save()

    def train_step(self, batch):
        x, y = batch
        predict = self.forward(x)
        loss = self.loss(predict, y)
        target = y
        return loss, predict, target

    def test(self):
        self.load()
        self.eval()
        dataset = self.dataset()
        self.stage(name='Test', step_function=self.test_step,
                    epoch=1, dataset=dataset.test, grad=False)

    def test_step(self, batch):
        x, y = batch
        predict = self.forward(x)
        target = y
        return predict, target

    def predict(self):
        ...

    def dataset(self) -> Dataset:
        ...


if __name__ == '__main__':
    m = Model().path
    print(m)
