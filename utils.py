import os
import torch
import shutil
from torch.utils.data import DataLoader, SubsetRandomSampler
from sklearn.model_selection import train_test_split
import numpy as np


def save_checkpoint(args, state, is_best, filename='checkpoint.pth.tar'):
    directory = "runs/%s/" % args.name
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = directory + filename
    torch.save(state, filename)
    if is_best:
        shutil.copyfile(filename, 'runs/%s/' % args.name + 'model_best.pth.tar')


class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


def accuracy(output, target, topk=(1,)):
    maxk = max(topk)
    batch_size = target.size(0)

    _, pred = output.topk(maxk, 1, True, True)
    pred = pred.t()
    correct = pred.eq(target.view(1, -1).expand_as(pred))

    res = []
    for k in topk:
        correct_k = correct[:k].view(-1).float().sum(0)
        res.append(correct_k.mul_(100.0 / batch_size))
    return res


def create_loaders(args, labeled_dataset, unlabeled_dataset, test_dataset, labeled_indices, unlabeled_indices, kwargs):
    labeled_dataset.indices = labeled_indices
    unlabeled_dataset.indices = unlabeled_indices

    labeled_loader = DataLoader(dataset=labeled_dataset, batch_size=args.batch_size, shuffle=True, **kwargs)
    unlabeled_loader = DataLoader(dataset=unlabeled_dataset, batch_size=args.batch_size, shuffle=True, **kwargs)
    val_loader = DataLoader(dataset=test_dataset, batch_size=args.batch_size, shuffle=True, **kwargs)

    return labeled_loader, unlabeled_loader, val_loader


def stratified_random_sampling(base_dataset, unlabeled_indices, number):
    ratio = (number / unlabeled_indices.shape[0])

    _, samples_indices = train_test_split(
                        np.arange(unlabeled_indices.shape[0]),
                        test_size=ratio,
                        shuffle=True,
                        stratify=[base_dataset.targets[x] for x in unlabeled_indices])
    return samples_indices


def postprocess_indices(labeled_indices, unlabeled_indices, samples_indices):
    unlabeled_mask = torch.ones(size=(len(unlabeled_indices),), dtype=torch.bool)
    unlabeled_mask[samples_indices] = 0
    labeled_indices = np.hstack([labeled_indices, unlabeled_indices[~unlabeled_mask]])
    unlabeled_indices = unlabeled_indices[unlabeled_mask]

    return labeled_indices, unlabeled_indices


def print_args(args):
    print('Arguments:\n'
          f'Model name: {args.name}\t'
          f'Epochs: {args.epochs}\t'
          f'Batch Size: {args.batch_size}\n'
          f'Architecture: {args.arch}\t'
          f'Weak Supervision Strategy: {args.weak_supervision_strategy}\n'
          f'Uncertainty Sampling Method: {args.uncertainty_sampling_method}\t'
          f'Semi Supervised Method: {args.semi_supervised_method}\n'
          f'Dataset root: {args.root}')
