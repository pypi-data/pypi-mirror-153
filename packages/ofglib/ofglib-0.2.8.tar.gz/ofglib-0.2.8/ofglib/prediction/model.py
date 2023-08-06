import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import io

from autofeat import AutoFeatRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error as mae, r2_score as r2
from sklearn.model_selection import train_test_split

import time

from .columns import exclude
sns.set()


class MechModel:
    '''A class to represent a model.

    ...

    Attributes
    ----------
    features : list
        list of column names
    targets : list
        list of __only one__ target name in a form: ['TARGET_NAME']
    pca : dict
        dictionary of PCA-transformers (default: empty dictionary)
    autofeat : autofeat.AutoFeatRegressor
        feature generator (default: None)
    performance : dict
        dictionary of metrics (default: empty dictionary)
    model : RandomForestRegressor
        machine learning model (default: None)

    Methods
    -------
    _list_replace(lst: list[str], to_replace: str, value: str):
        A function to replace string elements in list
    _colapse_features_list():
        Returns collapsed form for column names like:
        ['ДУО_СКР_01', 'ДУО_СКР_02] -> Group_ДУО_СКР_01
    to_features(data, targets=''):
        Returns pd.DataFrame using self.features in a collapsed form for
        column names like: ['ДУО_СКР_01', 'ДУО_СКР_02] -> Group_ДУО_СКР_01
    fit(df):
        Starts model fitting, returns 0
    fit_model(X, Y):
        Fitting model, returns 0
    predict(data):
        Returns predictions as pd.DataFrame


    Notes
    -----
    Главный принцип работы с признаками: поле self.features объекта
    MechModel получен как одноименное поле объекта DataPreprocessor
    после предобработки данных и содержит наиболее __важные__ признаки.
    Следовательно, может отличаться по содержанию от признаков,
    хранящихся для соответствующей модели в базе данных.

    Правило для групповых признаков:
    для признаков, собираемых в каждом проходе ('ДУО_ОБЖ_01', 'DELTA1_2', ...),
    даже если был выбран из базы данных столбец для одного прохода,
    информация обо всех проходах будет использована в обучении модели
    и, соответственно, для предсказания.

    '''

    def __init__(self, targets, features, pca):
        self.features = features
        self.features.sort()

        self.targets = targets
        self.targets.sort()

        self.pca = pca

        self.autofeat = None
        self.performance = {key: {} for key in self.targets}
        self.model = None

    def _list_replace(self, lst: list[str], to_replace: str, value: str):
        for i, element in enumerate(lst):
            if element == to_replace:
                if 'DELTA' in value:
                    lst[i] = value[:-2]+'11'
                else:
                    lst[i] = value[:-2]+'01'
        return lst

    def _colapse_features_list(self):
        prefixes_to_replace = [
            'ДУО_ОБЖ', 'ДУО_УСС', 'ДУО_УСП', 'ДУО_СКР',
            'КВР_ОБЖ', 'КВР_УСС', 'КВР_УСП', 'КВР_СКР',
            'DELTA'
        ]

        features_temp = list(self.features)

        for prefix in prefixes_to_replace:
            columns_with_prefix = [col for col in features_temp
                                   if col.startswith(prefix)]
            for column in columns_with_prefix:
                features_temp = self._list_replace(features_temp, column,
                                                   f'Group_{columns_with_prefix[0]}')
            features_temp = list(set(features_temp))
            features_temp.sort()
        return features_temp

    def to_features(self, data, targets=''):

        # ex: ['ДУО_СКР_01', 'ДУО_СКР_02] -> Group_ДУО_СКР_01
        features_temp = self._colapse_features_list()

        set_exclude = set(exclude[self.targets[0]])
        for tar in self.targets:
            if tar != self.targets[0]:
                set_exclude &= set(exclude[tar])

        features_temp = list(set(features_temp)-set_exclude)
        features_temp.sort()
        # print(features_temp)

        return data[features_temp]

    def fit(self, df):

        data, Y = df[df.columns.difference(self.targets)], df[self.targets]
        X = self.to_features(data)

        start_time = time.time()
        self.fit_model(X, Y)
        print("--- Fitting model: %s seconds ---" % (time.time() - start_time))
        return 0

    def fit_model(self, X, Y):

        X_train, X_test, Y_train, Y_test = train_test_split(
            X, Y.values.ravel(), test_size=0.3
        )

        #----------------------------------------------------------------------
        steps = 2
        print("### AutoFeat with %i feateng_steps" % steps)
        afreg = AutoFeatRegressor(verbose=1, feateng_steps=steps)
        afreg.fit(X_train, Y_train)
        r2score = afreg.score(X_train, Y_train)
        print("## Final R^2: %.4f" % r2score)

        X = afreg.transform(X)
        X_train = afreg.transform(X_train)
        X_test = afreg.transform(X_test)

        X.columns = X.columns.astype('str')
        X_train.columns = X_train.columns.astype('str')
        X_test.columns = X_test.columns.astype('str')

        self.autofeat = afreg


        #----------------------------------------------------------------------
        model = RandomForestRegressor(
                    n_estimators=200,
                    max_features=8,
                    max_depth=160,
                    min_samples_split=14,
                    min_samples_leaf=1,
                    bootstrap=False
        )
        #----------------------------------------------------------------------

        model.fit(X_train, Y_train)
        y_pred_train = model.predict(X_train).reshape(-1, 1)
        Y_train = Y_train.reshape(-1, 1)
        y_pred_test = model.predict(X_test).reshape(-1, 1)
        Y_test = Y_test.reshape(-1, 1)

        #----------------------------------------------------------------------

        model.fit(X, Y.values.ravel())

        y_pred = model.predict(X).reshape(-1, 1)
        Y = Y.values.reshape(-1, 1)

        # std_Y = np.std(Y, axis=0)[0]
        # std_Y_train = np.std(Y_train, ddof=0)
        # std_Y_test = np.std(Y_test, ddof=0)

        # ksi = np.array([1.96])

        for i, target in enumerate(self.targets):
            self.performance[target]['Samples'] = X.shape[0]
            self.performance[target]['MAE'] = np.round(mae(Y[:, i], y_pred[:, i]), 2)

            p95 = np.round(np.percentile(np.abs(Y[:, i]-y_pred[:, i]), 95), 2)
            # p95_train = np.round(np.percentile(np.abs(Y_train[:, i]-y_pred_train[:, i]), 95), 2)
            # p95_test = np.round(np.percentile(np.abs(Y_test[:, i]-y_pred_test[:, i]), 95), 2)
            self.performance[target]['P95'] = p95
            # self.performance[target]['P95 train'] = p95_train
            # self.performance[target]['P95 test'] = p95_test

            self.performance[target]['MAE train'] = np.round(mae(Y_train[:, i], y_pred_train[:, i]), 2)
            self.performance[target]['MAE test'] = np.round(mae(Y_test[:, i], y_pred_test[:, i]), 2)

            self.performance[target]['R2'] = np.round(r2(Y[:, i], y_pred[:, i]), 2)
            self.performance[target]['R2 train'] = np.round(r2(Y_train[:, i], y_pred_train[:, i]), 2)
            self.performance[target]['R2 test'] = np.round(r2(Y_test[:, i], y_pred_test[:, i]), 2)

            # D_train = ksi[i]*std_Y_train*np.sqrt(1-self.performance[target]['R2 train'])
            # D_test = ksi[i]*std_Y_test*np.sqrt(1-self.performance[target]['R2 test'])
            # self.performance[target]['D train'] = D_train
            # self.performance[target]['D test'] = D_test

            # self.performance[target]['p train'] = np.round((np.abs(Y_train[:, i] - y_pred_train[:, i]) < D_train).sum()*100/len(Y_train), 1)
            # self.performance[target]['p test'] = np.round((np.abs(Y_test[:, i] - y_pred_test[:, i]) < D_test).sum()*100/len(Y_test), 1)

        self.model = model
        return 0

    def predict(self, data):
        # print(data.shape)

        Y = ()
        X = data[self._colapse_features_list()]
        # print('X.columns: ', X.columns)
        X = self.autofeat.transform(X)
        # print(X)

        # X = X.values

        if X.shape[0]==1:
            sl = np.isnan(X)
            if np.any(sl):
                raise Exception('''Prediction from this data is impossible:
                                not enough data in the features.\n''')
            X = np.nan_to_num(X).reshape(1, -1)
            Y = self.model.predict(X)
        else:
            sl = np.isnan(X).any(axis=1)
            X = np.nan_to_num(X)
            Y = self.model.predict(X)
            Y[sl] = np.nan

        # print(Y)
        # return pd.DataFrame(index=df.index, columns=self.targets, data=Y) #.fillna(0)
        return pd.DataFrame(data=Y, columns=self.targets, index=data.index)

    def save_image(self, X, y, target):
        si = np.argsort(y)
        fig, ax = plt.subplots(1, figsize=(10,10))
        sns.scatterplot(x=X[si, 0], y=X[si, 1], hue=y[si],
                        legend=True,
                        s=50, alpha=0.8,
                        palette='icefire', linewidth=0.3, edgecolor='k')
        #sns.set(rc={'figure.figsize':(30,30)})

        plt.title(target, weight='bold').set_fontsize('14')
        plt.xlabel('Component 1', weight='bold').set_fontsize('14')
        plt.ylabel('Component 2', weight='bold').set_fontsize('14')

        # plt.show()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        self.tsne_images[target] = buf
        return

    def __fit_model(self, X, y, target):  # deprecated
        print('fitting ', target)
        X, y = X.values, y.values

        # 1. drop nan
        sl = ~np.logical_or(np.isnan(X).any(axis=1), np.isnan(y))
        X, y = X[sl], y[sl]

        if X.shape[0]==0:
            raise ValueError('0 samples without NaN for fitting')
        # 2. filter out

        # if mode==2:
        outlier_detector = ABOD(contamination=0.1, n_neighbors=5, method='fast')
        XY = np.hstack((X, y.reshape(-1, 1)))

        # normalization
        XY_scaled = (XY - XY.min(axis=0)) / (XY.max(axis=0) - XY.min(axis=0))

        outlier_detector.fit(XY_scaled)
        outliers = outlier_detector.predict(XY_scaled)
        normal = outliers!=1
        X, y = X[normal], y[normal]

        # elif mode==3:
        #     X_embedded = TSNE(
        #         n_components=2, learning_rate=200, init='random'
        #         ).fit_transform(X)
        #     # save image
        #     self.save_image(X_embedded, y, target)
        #     clustering = DBSCAN(eps=10, min_samples=5).fit(np.hstack((X_embedded, y.reshape(-1,1))))
        #     normal = clustering.labels_ != -1
        #     X, y = X[normal], y[normal]

        if X.shape[0]==0:
            raise ValueError('0 samples after outliers filtering')
        self.performance[target]['Samples'] = X.shape[0]
        print(X.shape[0])

        # 3. Set up model
        model = RandomForestRegressor(n_estimators=60)
        # 4. Calc performance
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
        model.fit(X_train, y_train)
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        # 5. Train model
        model.fit(X, y)
        self.model[target] = model

        y_pred = model.predict(X)
        self.performance[target]['MAE'] = np.round(mae(y, y_pred), 2)
        self.performance[target]['P95'] = np.round(np.percentile(np.abs(y-y_pred), 95), 2)
        self.performance[target]['MAE train'] = np.round(mae(y_train, y_pred_train), 2)
        self.performance[target]['MAE test'] = np.round(mae(y_test, y_pred_test), 2)

        return 0

    def __predict(self, data):  # deprecated
        print(data.shape)

        Y = ()
        for target in self.targets:
            X = data[self._colapse_features_list()].values
            print(target, X)
            if X.shape[0]==1:
                sl = np.isnan(X)
                if np.any(sl):
                    raise Exception('''Prediction from this data is impossible:
                                     not enough data in the features.\n''')
                X = np.nan_to_num(X).reshape(1, -1)
                y = self.model[target].predict(X)
            else:
                sl = np.isnan(X).any(axis=1)
                X = np.nan_to_num(X)
                y = self.model[target].predict(X)
                y[sl] = np.nan
            Y += (y,)

        Y = np.vstack(Y).T
        # print(Y)
        return pd.DataFrame(data=Y, columns=self.targets, index=data.index)



if __name__ == "__main__":
    model = MechModel(['FPT', 'FVS'])
    df = pd.read_csv('D:/work/17Г1С-У.csv')

    print(df.head(5))
    print(model.features)

    model.fit(df, None)
    print(model.features)
    print(model.performance)
