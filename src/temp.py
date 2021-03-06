from __future__ import print_function, division

__author__ = 'amrit'

import numpy as np
from sklearn import metrics
y = np.array([1, 1, 2, 2])
pred = np.array([0.1, 0.4, 0.35, 0.8])
fpr, tpr, thresholds = metrics.roc_curve(y, pred, pos_label=2)
print(fpr, tpr, thresholds)
metrics.auc(fpr, tpr)