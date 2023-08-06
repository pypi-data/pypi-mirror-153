Hyperparameter optimization (Optuna)
====================================

`Optuna <https://optuna.org/>`_ is a popular Python library for hyperparameter
optimization. This example walks through a workload using Optuna to optimize an
`XGBoost <https://xgboost.readthedocs.io/en/latest/>`_ classification model. and
then how to scale the same workload using Dask and Coiled. You can also view the
`full notebook <https://github.com/coiled/notebooks/blob/main/optuna-xgboost/optuna-xgboost.ipynb>`_
for this example.

Optuna in a nutshell
--------------------

Optuna has three primary concepts:

- Objective function: This is some function that depends on the hyperparameters
  in your model that you would like to optimize. For example, it's common to
  maximum a classification model's prediction accuracy (i.e. the objective
  function would be the accuracy score).

- Optimization trial: A trial is a single evaluation of the objective function
  with a given set of hyperparameters.

- Optimization study: A study is a collection of optimization trials where each
  trial uses hyperparameters sampled from a set of allowed values.

The set of hyperparameters for the trial which gives the optimal value for the
objective function are chosen as the best set of hyperparameters.


Scaling Optuna with Dask
------------------------

Below is a snippet which uses Optuna to optimize several hyperparameters for an
XGBoost classifier trained on the
`breast cancer dataset <https://scikit-learn.org/stable/datasets/toy_dataset.html#breast-cancer-wisconsin-diagnostic-dataset>`_.
We also use `Dask-Optuna <https://jrbourbeau.github.io/dask-optuna>`_ and
`Joblib <https://joblib.readthedocs.io/en/latest/>`_ to run Optuna trials in
parallel on a Coiled cluster.

.. code-block::

    import numpy as np
    import sklearn.datasets
    import sklearn.metrics
    from sklearn.model_selection import train_test_split
    import xgboost as xgb

    def objective(trial):
        # Load our dataset
        X, y = sklearn.datasets.load_breast_cancer(return_X_y=True)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)
        dtrain = xgb.DMatrix(X_train, label=y_train)
        dtest = xgb.DMatrix(X_test, label=y_test)

        # Get set of hyperparameters
        param = {
            "silent": 1,
            "objective": "binary:logistic",
            "booster": trial.suggest_categorical("booster", ["gbtree", "dart"]),
            "lambda": trial.suggest_float("lambda", 1e-8, 1.0, log=True),
            "alpha": trial.suggest_float("alpha", 1e-8, 1.0, log=True),
            "max_depth": trial.suggest_int("max_depth", 1, 9),
            "eta": trial.suggest_float("eta", 1e-8, 1.0, log=True),
            "gamma": trial.suggest_float("gamma", 1e-8, 1.0, log=True),
            "grow_policy": trial.suggest_categorical("grow_policy", ["depthwise", "lossguide"]),
        }

        # Train XGBoost model
        bst = xgb.train(param, dtrain)
        preds = bst.predict(dtest)

        # Compute and return model accuracy
        pred_labels = np.rint(preds)
        accuracy = sklearn.metrics.accuracy_score(y_test, pred_labels)
        return accuracy

    from dask.distributed import Client
    import coiled
    import dask_optuna
    import joblib

    # Create a Dask cluster with Coiled
    cluster = coiled.Cluster(n_workers=10, configuration="jrbourbeau/optuna")
    # Connect Dask to our cluster
    client = Client(cluster)
    print(f"Dask dashboard is available at {client.dashboard_link}")
    client.wait_for_workers(10)

    # Create Dask-compatible Optuna storage class
    storage = dask_optuna.DaskStorage()

    # Run 500 optimizations trial on our cluster
    study = optuna.create_study(direction="maximize", storage=storage)
    with joblib.parallel_backend("dask"):
        study.optimize(objective, n_trials=500, n_jobs=-1)

And with that, you're able to run distributed hyperparameter optimizations using
Optuna, Dask, and Coiled!
