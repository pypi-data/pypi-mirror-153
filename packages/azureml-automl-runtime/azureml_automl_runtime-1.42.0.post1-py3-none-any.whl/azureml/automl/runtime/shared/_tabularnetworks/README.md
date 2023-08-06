# A PyTorch Implementation of TabNet

This repo provides an efficient [PyTorch](https://pytorch.org) implementation of [TabNet](https://arxiv.org/abs/1908.07442),
a neural network designed to sparsely attend to tabular data for regression and classification tasks.

This repo also provides an implementation of autogluon's tabular NN described in detail [here](https://arxiv.org/pdf/2003.06505.pdf)

## Model Training

The classes defined in train.py follow a standard sklearn api for fitting and training with numpy arrays.

The general template for training this model is as follows:

1. Prepare your dataset
2. Define the model andtraining configuration via an sklearn style API
3. Run script
