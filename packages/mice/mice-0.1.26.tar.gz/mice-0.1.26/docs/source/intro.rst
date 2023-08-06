.. _introduction:

============
Introduction
============

The MICE estimator is a gradient estimator for stochastic optimization that exploits the correlation between the gradients of subsequent iterations in order to control the estimate's statistical error.
This is achieved by building a hierarchy of gradient differences computed at previous iterates and sampling gradients at this hierarchy in order to achieve the desired error tolerance with the smallest gradient sampling cost possible.
Moreover, MICE also controls the hierarchy by choosing which iterations to keep in the hierarchy, when to restart the hierarchy, and when to discard older iterates.

For a detailed description of the method, convergence analysis and numerical results, check the `MICE manuscript`_.

.. _MICE manuscript: https://arxiv.org/abs/2011.01718