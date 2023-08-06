Using SGD-MICE to train a logistic regression model
===================================================

*Run this example in* colab_!

.. _colab: https://colab.research.google.com/drive/1R0X1BqbtQTPfT2T6fUJ7O24Ua_ZOZxcE?usp=sharing

The goal of this example is to use SGD-MICE to train a logistic
regression model with :math:`\ell_2` regularization to perform binary
classification. The idea is to use the logistic function,

.. math::


   h(z) = \frac{1}{1 + \exp(-z)},

of an affine transformation of a data point as the probability of it
belonging to a class. Here, a data point
:math:`(\boldsymbol{x}_\alpha, y_\alpha)` is such that
:math:`\boldsymbol{x}_\alpha \in \mathbb{R}^{d}` is a vector of features
and :math:`y_\alpha \in \{-1,1\}` denotes that this data point belongs
to a class encoded as :math:`-1` or :math:`1`. Then, for a vector of
weights :math:`\boldsymbol{w}`,

.. math::


   h(\boldsymbol{w}^\intercal \boldsymbol{x}_\alpha) = \mathbb{P}(y_\alpha = 1 | \boldsymbol{x}_\alpha; \boldsymbol{w}).

We want to find the optimal vector :math:`\boldsymbol{w}` that better
predicts the class of a vector :math:`\boldsymbol{x}_\alpha`.

To measure how well the model with parameter :math:`\boldsymbol{w}`
performs classification, we use the :math:`\ell_2`-regularized log-loss
function

.. math::


   F(\boldsymbol{w}) = \frac{1}{N} \sum_{\alpha=1}^N f\left(\boldsymbol{w}, \boldsymbol{\theta}_\alpha= (\boldsymbol{x}_\alpha, y_\alpha)\right) = \frac{1}{N} \sum_{\alpha=1}^N \log(1 + \exp(-y_\alpha \boldsymbol{w}^\intercal \boldsymbol{x}_\alpha))
   + \frac{\lambda}{2} \|\boldsymbol{w}\|^2.

This class of problems is :math:`L`-smooth and strongly-convex, thus, we
expect SGD-MICE to converge linearly in this case.

We start by importing NumPy, matplotlib and MICE.

.. code:: ipython3

    !pip install mice
    import numpy as np
    import matplotlib.pyplot as plt
    from mice import MICE, plot_mice

We will train the model on synthetic two-dimensional data that allows
for visualization of the feature space. Moreover, we need a set of data
for training and another one, independent from the first, for
cross-validation. Both the training and testing sets have 1000 points,
500 for each class. We assume the feature vectors to be multivariate
Gaussian-distributed as

.. math::


   \boldsymbol{X}_1 \sim \mathbb{N}
   \left(
   \begin{bmatrix}
   -3\\
   -4
   \end{bmatrix}
   ,
   \begin{bmatrix}
           10 & -4 \\
           -4 & 5
   \end{bmatrix}
   \right)
   , \quad
   \text{and }
   \boldsymbol{X}_{-1} \sim \mathbb{N}
   \left(
   \begin{bmatrix}
   1\\
   3
   \end{bmatrix}
   ,
   \begin{bmatrix}
           6 & 2 \\
           2 & 5
   \end{bmatrix}
   \right),

and draw each :math:`\boldsymbol{x}_\alpha` from its respective
distribution depending on :math:`\boldsymbol{y}_\alpha`.

To account for a translation of the decision boundary, we introduce a
bias in the model by including a feature equaling one in all generated
data.

.. code:: ipython3

    np.random.seed(0)

    datasize = 1000
    n_features = 2
    reg_param = 1e-3

    X_1_mean = np.array([-3, -4])
    X_1_cov = np.array([[10, -4], [-4, 5]])
    X_1_train = np.random.multivariate_normal(X_1_mean, X_1_cov, int(datasize/2))
    X_1_train = np.hstack([X_1_train, np.ones((int(datasize/2), 1))])

    X_m1_mean = np.array([1, 3])
    X_m1_cov = np.array([[6, 2], [2, 4]])
    X_m1_train = np.random.multivariate_normal(X_m1_mean, X_m1_cov, int(datasize/2))
    X_m1_train = np.hstack([X_m1_train, np.ones((int(datasize/2), 1))])

    Y_1_train = np.ones(int(datasize/2))
    Y_m1_train = -1*np.ones(int(datasize/2))

    X = np.vstack([X_1_train, X_m1_train])
    Y = np.hstack([Y_1_train, Y_m1_train])

    train_data = [*zip(X, Y)]
    np.random.shuffle(train_data)


    X_1_test = np.random.multivariate_normal(X_1_mean, X_1_cov, int(datasize/2))
    X_1_test = np.hstack([X_1_test, np.ones((int(datasize/2), 1))])

    X_m1_test = np.random.multivariate_normal(X_m1_mean, X_m1_cov, int(datasize/2))
    X_m1_test = np.hstack([X_m1_test, np.ones((int(datasize/2), 1))])

    Y_1_test = np.ones(int(datasize/2))
    Y_m1_test = -1*np.ones(int(datasize/2))

    X_test = np.vstack([X_1_test, X_m1_test])
    Y_test = np.hstack([Y_1_test, Y_m1_test])

Now that both the training and testing sets are ready, let’s define the
log-loss function and its gradient.

.. code:: ipython3

    def sigmoid(z):
        return 1/(1+np.exp(-z))

    def loss_full(W):
        ls = (np.log(1 + np.exp(-Y * (X @ W)))) + .5*reg_param*(W @ W)
        return np.mean(ls)

    def lossgrad_full(W):
        grad = -(sigmoid(-Y * (X @ W))*Y) @ X / datasize + reg_param * W
        return grad

    def lossgrad(W, thetas):
        grad = np.zeros((len(thetas), n_features+1))
        for i, theta in enumerate(thetas):
            grad[i] = -sigmoid(-theta[1] * (theta[0] @ W)) * \
                theta[0] * theta[1] + reg_param * W
        return grad

Next, we define functions to measure the accuracy of the model in the
testing set.

.. code:: ipython3

    def accuracy_test(W):
        p_true = sigmoid(X_test @ W)
        p_false = sigmoid(-X_test @ W)
        P = p_true > p_false
        acc = np.mean((P*2-1) == Y_test)
        return acc

Finally, let’s define a function to plot the data and the decision
boundary of the model. We will plot one class (:math:`\boldsymbol{y}=1`)
in blue and the other (:math:`\boldsymbol{y}=-1`) in brown. The
background is colored according to the classification of the model.
Moreover, we will plot the training set with black edges and the testing
set with white edges.

.. code:: ipython3

    def plot_data(W):
        fig, ax = plt.subplots(figsize=(6,6), dpi=100)
        ax.scatter(X[:,0], X[:,1], c=Y, edgecolor='k', cmap=plt.cm.Paired)
        ax.scatter(X_test[:,0], X_test[:,1], c=Y_test, edgecolor='w', cmap=plt.cm.Paired)
        x_lims = ax.get_xlim()
        y_lims = ax.get_ylim()
        xs = np.linspace(x_lims[0], x_lims[1], 50)
        ys = np.linspace(y_lims[0], y_lims[1], 50)

        pred = np.zeros((50, 50))
        for i, x in enumerate(xs):
            for j, y in enumerate(ys):
                pred[j, -i-1] = sigmoid(np.array([x, y, 1]) @ W) < .5

        ax.imshow(pred, extent=[x_lims[0], x_lims[1], y_lims[0], y_lims[1]], cmap=plt.cm.Paired)
        return fig

Now, here we will initialize the weights vector with zeros and check the
loss and accuracy of the model with it,

.. code:: ipython3

    W = np.zeros(shape=(n_features+1))

    print(f'loss_full(W)={loss_full(W)}')
    print(f'accuracy_test(W)={accuracy_test(W)}')


.. parsed-literal::

    loss_full(W)=0.6931471805599454
    accuracy_test(W)=0.5


and plot the data with the decision boundary for the model with the
starting weights.

.. code:: ipython3

    fig = plot_data(W)



.. image:: output_13_0.png


It is clear that, with this choice of initializing the weights with
zeros, the model predicts blue (:math:`\boldsymbol{y}=1`) for all the
data points in both the training and testing sets.

To train the model using SGD-MICE with the optimal step-size, we need to
know the :math:`L`-smoothness constant of the loss function. Moreover,
we also set :math:`\epsilon`, the tolerance on the statistical error of
the gradient estimates, a parameter of MICE.

.. code:: ipython3

    L = 0.25 * np.mean((X**2).sum(axis=1)) + reg_param

    print(f'L={L}')

    eps = 0.5

    step_size = 2/(L+reg_param)/(1+eps**2)
    print(f'step_size = {step_size}')



.. parsed-literal::

    L=7.58716208768028
    step_size = 0.2108547473699424


Finally, we create an instance of the MICE class with the gradient of
the log-loss function, the list with the training data, the tolerance on
the statistical error :math:`\epsilon`, the maximum number of gradient
evaluations (here set as 10 epochs), and the minimum batch size,

.. code:: ipython3

    df = MICE(lossgrad,
              sampler=train_data,
              eps=eps,
              max_cost=10*datasize,
              min_batch=5)

and perform optimization until df.terminate returns True.

.. code:: ipython3

    losses = [loss_full(W)]
    accuracies = [accuracy_test(W)]
    while True:
        grad = df(W)
        if df.terminate:
            break
        W = W - step_size*grad
        losses.append(loss_full(W))
        accuracies.append(accuracy_test(W))
    print(W)


.. parsed-literal::

    [-0.57690229 -1.58362153 -1.81459809]


.. code:: ipython3

    print(f'Starting loss: {losses[0]}')
    print(f'Final loss: {losses[-1]}')


.. parsed-literal::

    Starting loss: 0.6931471805599454
    Final loss: 0.06614685480157584


.. code:: ipython3

    print(f'Starting accuracy: {accuracies[0]}')
    print(f'Final accuracy: {accuracies[-1]}')


.. parsed-literal::

    Starting accuracy: 0.5
    Final accuracy: 0.978


Training the logistic regression model greatly improved its accuracy in
comparison with the starting guess, as can also be observed in the next
Figure.

.. code:: ipython3

    fig = plot_data(W)



.. image:: output_23_0.png


Information with respect to MICE for all iterations is available in
df.log. This log is a pandas DataFrame and can be given as input to the
plot_mice function. For this reason, we will add information that we
computed (loss function values and accuracies) in this DataFrame to plot
them later.

.. code:: ipython3

    log = df.get_log()
    log['loss'] = losses
    log['accuracy'] = accuracies
    log




.. raw:: html

    <div>
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }

        .dataframe tbody tr th {
            vertical-align: top;
        }

        .dataframe thead th {
            text-align: right;
        }
    </style>
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>event</th>
          <th>num_grads</th>
          <th>vl</th>
          <th>bias_rel_err</th>
          <th>grad_norm</th>
          <th>iteration</th>
          <th>hier_length</th>
          <th>loss</th>
          <th>accuracy</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>0</th>
          <td>start</td>
          <td>50</td>
          <td>4.344155e+00</td>
          <td>0.000000</td>
          <td>2.214302</td>
          <td>1.0</td>
          <td>1.0</td>
          <td>0.693147</td>
          <td>0.500</td>
        </tr>
        <tr>
          <th>1</th>
          <td>restart</td>
          <td>110</td>
          <td>3.036002e-01</td>
          <td>0.000000</td>
          <td>0.451342</td>
          <td>2.0</td>
          <td>1.0</td>
          <td>0.213022</td>
          <td>0.946</td>
        </tr>
        <tr>
          <th>2</th>
          <td>dropped</td>
          <td>120</td>
          <td>1.011007e-02</td>
          <td>0.221457</td>
          <td>0.335490</td>
          <td>3.0</td>
          <td>2.0</td>
          <td>0.181227</td>
          <td>0.946</td>
        </tr>
        <tr>
          <th>3</th>
          <td>dropped</td>
          <td>140</td>
          <td>3.175136e-02</td>
          <td>0.255864</td>
          <td>0.290376</td>
          <td>4.0</td>
          <td>2.0</td>
          <td>0.163661</td>
          <td>0.946</td>
        </tr>
        <tr>
          <th>4</th>
          <td>dropped</td>
          <td>170</td>
          <td>3.701133e-02</td>
          <td>0.326740</td>
          <td>0.227388</td>
          <td>5.0</td>
          <td>2.0</td>
          <td>0.151987</td>
          <td>0.946</td>
        </tr>
        <tr>
          <th>...</th>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
          <td>...</td>
        </tr>
        <tr>
          <th>370</th>
          <td>MICE</td>
          <td>9943</td>
          <td>4.508993e-09</td>
          <td>1.255374</td>
          <td>0.016609</td>
          <td>371.0</td>
          <td>61.0</td>
          <td>0.066216</td>
          <td>0.978</td>
        </tr>
        <tr>
          <th>371</th>
          <td>dropped</td>
          <td>9963</td>
          <td>2.860285e-09</td>
          <td>1.255900</td>
          <td>0.016602</td>
          <td>372.0</td>
          <td>62.0</td>
          <td>0.066198</td>
          <td>0.978</td>
        </tr>
        <tr>
          <th>372</th>
          <td>dropped</td>
          <td>9983</td>
          <td>3.491157e-09</td>
          <td>1.257066</td>
          <td>0.016586</td>
          <td>373.0</td>
          <td>62.0</td>
          <td>0.066181</td>
          <td>0.978</td>
        </tr>
        <tr>
          <th>373</th>
          <td>MICE</td>
          <td>10003</td>
          <td>7.686893e-07</td>
          <td>1.264142</td>
          <td>0.016494</td>
          <td>374.0</td>
          <td>62.0</td>
          <td>0.066163</td>
          <td>0.978</td>
        </tr>
        <tr>
          <th>374</th>
          <td>end</td>
          <td>10003</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>NaN</td>
          <td>0.066147</td>
          <td>0.978</td>
        </tr>
      </tbody>
    </table>
    <p>375 rows × 9 columns</p>
    </div>



And, finally, let’s generate Figures with the loss function value,
accuracy, and gradient estimate norm versus the number of gradient
evaluations.

.. code:: ipython3

    fig, axs = plt.subplots(3, 1, figsize=(8, 8), sharex=True)
    axs[0] = plot_mice(log, axs[0], x='num_grads', y='loss', legend=True)
    axs[0].set_ylabel('Log-loss')
    axs[1] = plot_mice(log, axs[1], x='num_grads', y='accuracy', legend=False)
    axs[1].set_ylabel('Accuracy')
    axs[2] = plot_mice(log, axs[2], x='num_grads', y='grad_norm', legend=False)
    axs[2].set_ylabel('Estimate norm')
    axs[2].set_xlabel('Number of gradient evaluations')




.. parsed-literal::

    Text(0.5, 0, 'Number of gradient evaluations')




.. image:: output_27_1.png


And now, the exact same quantities versus iterations.

.. code:: ipython3

    fig, axs = plt.subplots(3, 1, figsize=(8, 8), sharex=True)
    axs[0] = plot_mice(log, axs[0], x='iteration', y='loss', style='semilogy', legend=True)
    axs[0].set_ylabel('Log-loss')
    axs[1] = plot_mice(log, axs[1], x='iteration', y='accuracy', style='semilogy',legend=False)
    axs[1].set_ylabel('Accuracy')
    axs[2] = plot_mice(log, axs[2], x='iteration', y='grad_norm', style='semilogy',legend=False)
    axs[2].set_ylabel('Estimate norm')
    axs[2].set_xlabel('Iterations')




.. parsed-literal::

    Text(0.5, 0, 'Iterations')




.. image:: output_29_1.png
