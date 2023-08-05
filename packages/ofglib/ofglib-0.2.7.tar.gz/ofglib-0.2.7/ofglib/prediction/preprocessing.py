import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from pyod.models.abod import ABOD
from autofeat import FeatureSelector

# import time as timecounter

from .columns import targets, time_columns, label_encoders, error_codes, groups, exclude, predictors, item_to_group, group_starts_with


def encode(df, output_df, label_encoders, cols):
    for column in label_encoders:  # for each column where label encoding is necessary
        if column in cols:
            for i, label in enumerate(label_encoders[column]):  # for each label in column
                df.loc[df[column]==label, column] = i
            x = df[column]
            x = x.fillna(i+1)
            output_df[column] = x
    return


def process_error_codes(df, output_df, code_columns, cols):
    for column in code_columns:
        if column in cols:
            output_df[column] = df[column].fillna(0)
    return


def reduce_dim(df, columns, dim, pca):
    X = df[columns]
    X = X.fillna(0)
    temp = list(X.columns)
    temp.sort()

    group_key = ','.join(temp)
    # print('group_key : ', group_key)
    if group_key not in pca:
        pca[group_key] = PCA(n_components=dim)
        pca[group_key].fit(X)

    X = pca[group_key].transform(X)
    return X


def load_columns(df, output_df, groups, cols, kvr_duo_delta_columns, dim, pca):
    '''Load columns

    Parameters
    ----------
        df : pd.DataFrame
            original dataframe with all 262 columns
        output_df : pd.DataFrame
            resulting dataframe
        groups : list of str and list[str]
            imported list
        cols : list
            self.features
        kvr_duo_delta_columns : list or []
            list of columns as 'ДУО_ОБЖ_01', 'DELTA1_2', etc.
        dim : int
            number of dimensions (default: 1)
        pca : dict
            dictionary of PCA-transformers

    Notes
    -----
    Главный принцип работы с признаками: поле self.features объекта
    DataPreprocessor после предобработки данных содержит
    наиболее __важные__ признаки. Следовательно, может отличаться
    по содержанию от признаков, хранящихся для соответствующей модели
    в базе данных.

    Правило для групповы признаков:
    для признаков, собираемых в каждом проходе ('ДУО_ОБЖ_01', 'DELTA1_2', ...),
    даже если был выбран из базы данных столбец для одного прохода,
    информация обо всех проходах будет использована в обучении модели
    и, соответственно, для предсказания.
    '''
    # duo_uss = group_starts_with['Group_ДУО_УСС_01']
    # kvr_uss = group_starts_with['Group_КВР_УСС_01']
    # for col in duo_uss+kvr_uss:
    #     ind = df[df[col]<0].index
    #     temp = df[col].copy()
    #     df[col].loc[ind] = 0

    for columns in groups:
        if isinstance(columns, list): # convolve
            columns_in_df = list(set(columns) & set(kvr_duo_delta_columns))
            if not columns_in_df:
                continue
            output_df[f'Group_{columns[0]}'] = reduce_dim(
                df, columns, dim, pca
            )
        else:
            # if features set by user, only these features will be added
            if columns not in cols and cols:
                continue
            output_df[columns] = df[columns]
    return


def load_targets(df, Y, targets):
    for y in targets:
        Y[y] = df[targets[y]].mean(axis=1)
    return


# TO DO: to delete
def time2num(df, columns, cols):
    for column in columns:
        if column in cols:
            df[column] = df[column].astype(str)
            df[column] = df[column].apply(lambda x: np.dot(np.array(x.split(':'), dtype=float), np.array([1.0, 1.0/60])))
    return


def flatten(t):
    # ex: [1, 2, 2, [3], [4, 5]] => [1, 2, 2, 3, 4, 5]
    # but: [1, 2, 2, [3], [4, [5]]] => [1, 2, 2, 3, 4, [5]]
    flat_list = []
    for sublist in t:
        if isinstance(sublist, list):
            for item in sublist:
                flat_list.append(item)
        else:
            flat_list.append(sublist)
    return flat_list


def gather(t):
    # ex: 'ДУО_ОБЖ_01'=> 'Group_ДУО_ОБЖ_01',
    #     'ДУО_ОБЖ_02' => 'Group_ДУО_ОБЖ_01'
    gathered_list = set(item_to_group[col] if col in item_to_group
                        else col
                        for col in t)

    return list(gathered_list)


def get_pca_key_for_features(columns):
    keys = []
    for col in columns:
        if isinstance(col, list):
            temp = col
            temp.sort()
            key = ','.join(temp)
            keys.append(key)
    return keys


class Data_Preprocessor:
    '''
    A class to represent a data preprocessor.

    ...

    Attributes
    ----------
    features : list
        list of column names from database, will be replaced with
        the most important features using FeatureSelector
    targets : list
        list of only one target name in a form: ['TARGET_NAME']
    pca : dict
        dictionary of PCA-transformers (default: empty dictionary)

    Methods
    -------
    get_pca():
        Returns self.pca.

    Notes
    -----
    Главный принцип работы с признаками: поле self.features объекта
    DataPreprocessor после предобработки данных содержит
    наиболее __важные__ признаки. Следовательно, может отличаться
    по содержанию от признаков, хранящихся для соответствующей модели
    в базе данных.

    Правило для групповы признаков:
    для признаков, собираемых в каждом проходе ('ДУО_ОБЖ_01', 'DELTA1_2', ...),
    даже если был выбран из базы данных столбец для одного прохода,
    информация обо всех проходах будет использована в обучении модели
    и, соответственно, для предсказания.

    '''

    def __init__(self, features, targets, pca={}, TRAIN=False):
        '''
        Constructs the necessary attributes for the DataPreprocessor object.

        Parameters
        ----------
            features : list
                list of column names from database, will be replaced with
                the most important features using FeatureSelector
            targets : list
                list containing only one target name in a form: ['TARGET_NAME']
            pca : dict
                dictionary of PCA-transformers (default: empty dictionary)
            TRAIN : bool
                default: False

        Raises
        ------
        ValueError
            If more than one target was passed.
        '''

        if len(targets)!=1:
            raise ValueError(f'targets should have length equal to 1, not {len(targets)}')
        self.pca = pca
        self.features = list(features)
        self.targets = list(targets)

        if len(features):
            self.is_features_invoked = True
        else:
            # default
            self.is_features_invoked = False

        self.mode = 'train' if TRAIN else 'predict'

    def get_pca(self):
        return self.pca

    def get_features(self):
        return self.features

    def select_features_few_nan(self, df, threshold=.8):
        # return features where nan's percentage < 80%
        return list((df.loc[:, df.isnull().mean() < threshold]).columns)

    def preprocess(self, df):
        '''Preprocess the dataframe.

        Parameters
        ----------
        df : pd.DataFrame
            A table with both features and targets


        Returns
        -------
        pd.DataFrame
            Preprocessed table with features and targets


        Raises
        ------
        ValueError
            If 0 rows in dataset after filtering or
            if 0 samples without NaN for fitting or
            if 0 samples after outliers filtering.

        '''
        reduced_group_dim = 1

        # 1. drop
        if self.mode == 'train':
            filtered = set(df[df['NOMP'].str.contains('П')].index) | set(df[df['NOMP'].str.contains('У')].index) | set(df[df['NOMP'].str.startswith('9')].index)
            df.drop(index=list(filtered), inplace=True)

        not_startswith = ['ДУО_ПРОХ', 'ДУО_ХОЛОСТ', 'ДУО_Т_3_ПР', 'ДУО_Т_ПОСЛ',
                          'КВР_Т_ПЛАН', 'КВР_Т_1_ПР', 'КВР_Т_ПОСЛ', 'КВР_ПРОХ',
                          'КВР_ХОЛОСТ', 'ДУО_ВРЕМЯ', 'ДУО_КВР', 'КВР_ВРЕМЯ']

        data = pd.DataFrame()
        Y = pd.DataFrame()

        # this way there is no need in rewriting whole preproccessing
        # for case when df is pd.Series, not pd.DataFrame
        # it will be used ONLY when self.predict is invoked
        # because no fitting with 1 test rows is possible
        if isinstance(df, pd.Series):
            df = pd.DataFrame(columns=df.keys(), data=[df, df], index=[0, 1])

        if self.is_features_invoked:
            # time2num(df, time_columns, self.features)
            encode(df, data, label_encoders, self.features)
            process_error_codes(df, data, error_codes, self.features)
        else:
            # time2num(df, time_columns, df.columns.values)
            encode(df, data, label_encoders, df.columns.values)
            process_error_codes(df, data, error_codes, df.columns.values)

        # an array with КВР, ДУО и DELTA columns for correct PCA compression
        print("features: ", self.features)
        kvr_duo_delta_columns = []
        if self.is_features_invoked:
            kvr_duo_delta_columns = [col for col in self.features
                                    if ((col.startswith('КВР') or col.startswith('ДУО') or col.startswith('DELTA'))
                                    and not (col in not_startswith))]
        else:
            kvr_duo_delta_columns = df.columns
        # print("kvr_duo_delta_columns: ", kvr_duo_delta_columns)

        load_columns(
            df, data, groups,
            self.features, kvr_duo_delta_columns,
            reduced_group_dim, self.pca)

        if data.shape[0] == 0:
            raise ValueError('0 rows in dataset after filtering')

        # print('Inside preprocessing:\n', data.shape)

        if self.mode == 'predict':
            data = data.astype('float64')
            data[gather(self.features)].fillna(np.nan, inplace=True)
            return data

        elif self.mode == 'train':
            load_targets(df, Y, {target:targets[target] for target in self.targets})
            # print('Inside preprocessing, Y = \n', Y.shape)
            data = data.astype('float64')

            self.features = data.columns.values
            print(self.features)
            X, Y = data.values, Y.values
            print('Shapes: X, Y - ', X.shape, Y.shape)

            sl = ~np.logical_or(np.isnan(X).any(axis=1), np.isnan(Y).any(axis=1))
            X, Y = X[sl], Y[sl]
            # print('N:', np.sum(sl))
            print('After NaNs removed: ', X.shape)

            if X.shape[0]==0:
                raise ValueError('0 samples without NaN for fitting')

            print('outliers...')
            outlier_detector = ABOD(contamination=0.1, n_neighbors=5, method='fast')
            XY = np.hstack((X, Y))

            xy_ptp = XY.ptp(0)  # min-max, axis=0 (for columns)
            xy_ptp[xy_ptp==0] = 1
            XY = (XY-XY.min(0))/xy_ptp

            outlier_detector.fit(XY)
            outliers = outlier_detector.predict(XY)
            normal = outliers!=1
            XY = XY[normal]
            X, Y = X[normal], Y[normal]

            print('count: ', np.sum(outliers))

            if X.shape[0]==0:
                raise ValueError('0 samples after outliers filtering')

            #------------------------------------------------------------
            ptp = X.ptp(0)
            X = X[:, ptp!=0]
            self.features = self.features[ptp!=0]
            # print('self.features before featureSelector: ', self.features)

            #------------------------------------------------------------
            X_train, _, Y_train, __ = train_test_split(X, Y.ravel(), test_size=0.3)
            fsel = FeatureSelector(verbose=1)
            new_X = fsel.fit_transform(
                        pd.DataFrame(X_train, columns=self.features),
                        Y_train
                    )

            #-------------------------------------------------------------

            columns = self.features
            self.features = list(new_X.columns.astype(str))
            # print('Feature Selector selects: ', list(new_X.columns))

            temp = [
                    col if col in predictors
                    else group_starts_with[col]
                    for col in self.features
            ]
            # print("----->", temp)

            # leave in self.pca only important pca transformers
            # print(self.pca)
            important_pca_keys = get_pca_key_for_features(temp)
            # print(important_pca_keys)
            self.pca = {key: self.pca[key] for key in important_pca_keys}

            data = pd.DataFrame(X, columns=columns)[self.features]
            self.features = list(flatten(temp))
            print('\tself.features: ', self.features)

            self.targets = [str(i) for i in self.targets]
            Y = pd.DataFrame(Y, columns=self.targets)

            return pd.concat([data, Y], axis=1)
