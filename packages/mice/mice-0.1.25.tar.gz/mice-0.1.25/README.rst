Multi-iteration Stochastic Estimator
------------------------------------

The `Multi-Iteration stochastiC Estimator`_ (MICE) is an estimator of gradients to be used in stochastic optimization. It uses control variates to build a hierarchy of iterations, adaptively sampling to keep the statistical variance below tolerance in an optimal fashion, cost-wise. The tolerance on the statistical error decreases proportionally to the square of the gradient norm, thus, SGD-MICE converges linearly in strongly convex L-smooth functions.

.. _Multi-Iteration stochastiC Estimator: https://arxiv.org/abs/2011.01718

This python implementation of MICE is able to

* estimate expectations or finite sums of gradients of functions;

* choose the optimal sample sizes in order to minimize the sampling cost;

* build a hierarchy of iterations that minimizes the total work;

* use a resampling technique to compute the gradient norm, thus enforcing stability;

* define a tolerance on the norm of the gradient estimate or a maximum number of evaluations as a stopping criterion.

Using MICE
----------

Using MICE is as simple as

    >>> import numpy as np
    >>> from mice import MICE
    >>>
    >>>
    >>> def gradient(x, thts):
    >>>     return x - thts
    >>>
    >>>
    >>> def sampler(n):
    >>>     return np.random.random((n, 1))
    >>>
    >>>
    >>> df = MICE(gradient , sampler=sampler)
    >>> x = 10
    >>> for i in range(10):
    ...    grad = df(x)
    ...    x = x - grad


However, it is flexible enough to tackle more complex problems.
For more information on how to use MICE and examples, check the `documentation`_.

.. _documentation: https://mice.readthedocs.io