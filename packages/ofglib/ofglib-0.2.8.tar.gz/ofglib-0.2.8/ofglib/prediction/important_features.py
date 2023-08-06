from typing import List
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance


def get_important_features(X : pd.DataFrame,
                           y: pd.DataFrame,
                           n_features : int = 20,
                           random_state : int = 42) -> List[str]:
    print('getting important features')
    X = X.copy()
    y = y.copy()
    X = X.reset_index(drop=True)
    y = y.reset_index(drop=True)

    sl = ~np.logical_or(np.isnan(X).any(axis=1), np.isnan(y))
    X, y = X[sl], y[sl]

    model = RandomForestRegressor(n_estimators=200)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                        random_state=random_state)
    model.fit(X_train, y_train)

    result = permutation_importance(model, X_test, y_test, n_repeats=10,
                                    random_state=random_state, n_jobs=-1)
    sorted_idx = result.importances_mean.argsort()[::-1]
    return X.columns[sorted_idx[:n_features]]
