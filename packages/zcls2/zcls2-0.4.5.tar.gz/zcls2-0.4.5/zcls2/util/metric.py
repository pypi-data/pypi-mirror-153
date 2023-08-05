# -*- coding: utf-8 -*-

"""
@date: 2022/4/3 下午1:39
@file: metric.py
@author: zj
@description: 
"""

import torch


def accuracy(output: torch.Tensor, target: torch.Tensor, topk=(1,)) -> list:
    """Computes the precision@k for the specified values of k"""
    maxk = max(topk)
    batch_size = target.size(0)

    _, pred = output.topk(maxk, 1, True, True)
    pred = pred.t()
    correct = pred.eq(target.view(1, -1).expand_as(pred))

    res = []
    for k in topk:
        correct_k = correct[:k].reshape(-1).float().sum(0, keepdim=True)
        res.append(correct_k.mul_(100.0 / batch_size))
    return res
