import argparse
import os
import time

os.environ['CUDA_VISIBLE_DEVICES'] = '3'

import torch
import torch.nn as nn
import torch.nn.parallel
import torch.backends.cudnn as cudnn
import torch.optim
import torch.utils.data

import numpy as np

from model.wideresnet import WideResNet
from model.densenet import DenseNet
from data.matek_dataset import MatekDataset
from utils import save_checkpoint, AverageMeter, accuracy, create_loaders
from active_learning.uncertainty_sampling import UncertaintySampling

parser = argparse.ArgumentParser(description='Active Learning Basic Medical Imaging')
parser.add_argument('--epochs', default=200, type=int,
                    help='number of total epochs to run')
parser.add_argument('--start-epoch', default=0, type=int,
                    help='manual epoch number (useful on restarts)')
parser.add_argument('-b', '--batch-size', default=512, type=int,
                    help='mini-batch size (default: 512)')
parser.add_argument('--lr', '--learning-rate', default=0.1, type=float,
                    help='initial learning rate')
parser.add_argument('--momentum', default=0.9, type=float, help='momentum')
parser.add_argument('--nesterov', default=True, type=bool, help='nesterov momentum')
parser.add_argument('--weight-decay', '--wd', default=5e-4, type=float,
                    help='weight decay (default: 5e-4)')
parser.add_argument('--print-freq', '-p', default=10, type=int,
                    help='print frequency (default: 10)')
parser.add_argument('--layers', default=28, type=int,
                    help='total number of layers (default: 28)')
parser.add_argument('--widen-factor', default=2, type=int,
                    help='widen factor (default: 2)')
parser.add_argument('--drop-rate', default=0.2, type=float,
                    help='dropout probability (default: 0.0)')
parser.add_argument('--no-augment', dest='augment', action='store_false',
                    help='whether to use standard augmentation (default: True)')
parser.add_argument('--resume', default='', type=str,
                    help='path to latest checkpoint (default: none)')
parser.add_argument('--name', default='densenet-least-confidence', type=str,
                    help='name of experiment')
parser.add_argument('--add-labeled-epochs', default=5, type=int,
                    help='if the test accuracy stays stable for add-labeled-epochs epochs then add new data')
parser.add_argument('--add-labeled-ratio', default=0.05, type=int,
                    help='what percentage of labeled data to be added')
parser.add_argument('--labeled-ratio-start', default=0.05, type=int,
                    help='what percentage of labeled data to start the training with')
parser.add_argument('--labeled-ratio-stop', default=0.35, type=int,
                    help='what percentage of labeled data to stop the training process at')
parser.add_argument('--arch', default='densenet', type=str, choices=['wideresnet', 'densenet'],
                    help='arch name')
parser.add_argument('--uncertainty-sampling-method', default='least_confidence', type=str,
                    choices=['least_confidence', 'margin_confidence', 'ratio_confidence', 'entropy_based'],
                    help='the uncertainty sampling method to use')
parser.add_argument('--root', default='/home/qasima/datasets/thesis/stratified/', type=str,
                    help='the root path for the datasets')

parser.set_defaults(augment=True)

best_prec1 = 0
args = parser.parse_args()


def main():
    global args, best_prec1
    args.name = f"{args.arch}@{args.uncertainty_sampling_method}"

    dataset_class = MatekDataset(root=args.root,
                                 labeled_ratio=args.labeled_ratio_start,
                                 add_labeled_ratio=args.add_labeled_ratio)

    base_dataset, labeled_idx, unlabeled_idx, test_dataset = dataset_class.get_dataset()

    kwargs = {'num_workers': 2, 'pin_memory': False}
    train_loader, unlabeled_loader, val_loader = create_loaders(args, base_dataset, test_dataset, labeled_idx,
                                                                unlabeled_idx, kwargs)

    uncertainty_sampler = UncertaintySampling(verbose=True,
                                              uncertainty_sampling_method=args.uncertainty_sampling_method)

    if args.arch == 'wideresnet':
        model = WideResNet(args.layers,
                           num_classes=dataset_class.num_classes,
                           widen_factor=args.widen_factor,
                           drop_rate=args.drop_rate,
                           input_size=dataset_class.input_size)
    elif args.arch == 'densenet':
        model = DenseNet(num_classes=dataset_class.num_classes, growth_rate=32,
                         block_config=(6, 12, 24, 16),
                         num_init_features=64,
                         drop_rate=args.drop_rate)
    else:
        raise NotImplementedError

    print('Number of model parameters: {}'.format(
        sum([p.data.nelement() for p in model.parameters()])))

    # doc: for training on multiple GPUs.
    # doc: Use CUDA_VISIBLE_DEVICES=0,1 to specify which GPUs to use
    # doc: model = torch.nn.DataParallel(model).cuda()
    model = model.cuda()

    if args.resume:
        if os.path.isfile(args.resume):
            print("=> loading checkpoint '{}'".format(args.resume))
            checkpoint = torch.load(args.resume)
            args.start_epoch = checkpoint['epoch']
            best_prec1 = checkpoint['best_prec1']
            model.load_state_dict(checkpoint['state_dict'])
            print("=> loaded checkpoint '{}' (epoch {})"
                  .format(args.resume, checkpoint['epoch']))
        else:
            print("=> no checkpoint found at '{}'".format(args.resume))

    cudnn.benchmark = True

    criterion = nn.CrossEntropyLoss().cuda()
    optimizer = torch.optim.SGD(model.parameters(), args.lr,
                                momentum=args.momentum, nesterov=args.nesterov,
                                weight_decay=args.weight_decay)

    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, len(train_loader) * args.epochs, eta_min=0)

    last_best_epochs = 0
    current_labeled_ratio = args.labeled_ratio_start
    acc_ratio = {}

    for epoch in range(args.start_epoch, args.epochs):
        train(train_loader, model, criterion, optimizer, scheduler, epoch)
        prec1 = validate(val_loader, model, criterion)

        is_best = prec1 > best_prec1
        last_best_epochs = 0 if is_best else last_best_epochs + 1

        if last_best_epochs == args.add_labeled_epochs:
            acc_ratio.update({current_labeled_ratio: best_prec1})
            samples_idx = uncertainty_sampler.get_samples(epoch, args, model,
                                                          unlabeled_loader,
                                                          number=dataset_class.add_labeled_num)
            unlabeled_mask = torch.ones(size=(len(unlabeled_idx), ), dtype=torch.bool)
            unlabeled_mask[samples_idx] = 0
            labeled_idx = np.hstack([labeled_idx, unlabeled_idx[~unlabeled_mask]])
            unlabeled_idx = unlabeled_idx[unlabeled_mask]

            train_loader, unlabeled_loader, val_loader = create_loaders(args, base_dataset, test_dataset, labeled_idx,
                                                                        unlabeled_idx, kwargs)

            current_labeled_ratio += args.add_labeled_ratio
            last_best_epochs = 0

        best_prec1 = max(prec1, best_prec1)
        save_checkpoint(args, {
            'epoch': epoch + 1,
            'state_dict': model.state_dict(),
            'best_prec1': best_prec1,
        }, is_best)

        if current_labeled_ratio > args.labeled_ratio_stop:
            continue

    for k, v in acc_ratio.items():
        print(f'Ratio: {int(k*100)}%\t'
              f'Accuracy: {v}')
    print('Best accuracy: ', best_prec1)


def train(train_loader, model, criterion, optimizer, scheduler, epoch):
    batch_time = AverageMeter()
    losses = AverageMeter()
    top1 = AverageMeter()

    model.train()

    end = time.time()
    for i, (data_x, target) in enumerate(train_loader):
        target = target.cuda(non_blocking=True)
        data_x = data_x.cuda(non_blocking=True)

        output = model(data_x)
        loss = criterion(output, target)

        prec1 = accuracy(output.data, target, topk=(1,))[0]
        losses.update(loss.data.item(), data_x.size(0))
        top1.update(prec1.item(), data_x.size(0))

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        scheduler.step()

        batch_time.update(time.time() - end)
        end = time.time()

        if i % args.print_freq == 0:
            print('Epoch: [{0}][{1}/{2}]\t'
                  'Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                  'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                  'Prec@1 {top1.val:.3f} ({top1.avg:.3f})'
                  .format(epoch, i, len(train_loader), batch_time=batch_time, loss=losses, top1=top1))


def validate(val_loader, model, criterion):
    batch_time = AverageMeter()
    losses = AverageMeter()
    top1 = AverageMeter()

    model.eval()

    end = time.time()
    for i, (data_x, target) in enumerate(val_loader):
        target = target.cuda(non_blocking=True)
        data_x = data_x.cuda(non_blocking=True)

        with torch.no_grad():
            output = model(data_x)
        loss = criterion(output, target)

        prec1 = accuracy(output.data, target, topk=(1,))[0]
        losses.update(loss.data.item(), data_x.size(0))
        top1.update(prec1.item(), data_x.size(0))

        batch_time.update(time.time() - end)
        end = time.time()

        if i % args.print_freq == 0:
            print('Test: [{0}/{1}]\t'
                  'Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                  'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                  'Prec@1 {top1.val:.3f} ({top1.avg:.3f})'
                  .format(i, len(val_loader), batch_time=batch_time, loss=losses, top1=top1))

    print(' * Prec@1 {top1.avg:.3f}'.format(top1=top1))

    return top1.avg


if __name__ == '__main__':
    main()
