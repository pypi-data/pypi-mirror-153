from datetime import datetime
import pandas as pd
import pymssql
import cx_Oracle as cx

# from .queries import *
from pandas import read_sql_query

cx.init_oracle_client(lib_dir= r'C:/Program Files/Oracle/instantclient_21_3')

class DB_Connector:
    def __init__(self,
                 server: str = '', user: str = '', password: str = '', db: str = '',
                 user_oracle = '', password_oracle = '', dsn_oracle = ''):
        self.conn = pymssql.connect(server, user, password, db)
        self.cursor = self.conn.cursor(as_dict=True)

        # cx.init_oracle_client(lib_dir= r'C:/Program Files/Oracle/instantclient_21_3')
        self.cx_conn = cx.connect(user=user_oracle, password=password_oracle, dsn=dsn_oracle)
        self.cx_cursor = self.cx_conn.cursor()

#######################################
# Functions that work with the database that stores the configurations and results of models
#######################################

    def get_columns_id(self, columns_names: list[str]) -> pd.DataFrame:
        query = '''select column_id from Columns where '''
        for name in columns_names:
            query += f'(Columns.name = \'{name}\') or '
        # erase extra ' or '
        query = query[:-4]

        df = read_sql_query(query, self.conn)

        return df

    def get_target_id(self, target:str) -> int:
        query = f'select target_id from Targets where name=\'{target}\''
        df = read_sql_query(query, self.conn)

        return df.iloc[0][0]

    def get_status(self, model_id: int):
        query = f'select status from Models where model_id={model_id}'
        df = read_sql_query(query, self.conn)

        return df.iloc[0][0]

    def update_status(self, model_id: int):
        query = '''update Models set status = 1
                   where model_id = %s'''
        self.cursor.execute(query, (model_id))
        self.conn.commit()

    def insert_features(self, model_id: int,
                        features: list[str]):
        df = self.get_columns_id(features)

        for column_id in df['column_id']:
            query = '''insert into ColumnsToModels(model_id, column_id)
                       values (%s, %s)'''
            self.cursor.execute(query, (int(model_id), int(column_id)))
        self.conn.commit()

    def insert_metrics(self, model_id:int,
                       metrics: dict[str, dict[str, str]],
                       target:str):
        target_id = self.get_target_id(target)

        df = read_sql_query('select * from Metrics', self.conn)
        metrics2ids = {i[1]:i[0] for i in df.to_numpy()}
        now_time = datetime.now()

        performance_dict = metrics[target]
        for metric_name in performance_dict:
            query = '''insert into
                    MetricToModels(model_id, target_id,
                    metric_id, value, time)
                    values (%s, %s, %s, %s, %s)'''
            self.cursor.execute(query, (model_id, int(target_id),
                                        metrics2ids[metric_name],
                                        performance_dict[metric_name],
                                        now_time))
        self.conn.commit()

    def get_targets(self, model_id:int) -> list[str]:
        model_id = (model_id, )

        query = """select name
                        from TargetsToModel as T1
                        inner join Targets as T2
                        on T1.target_id = T2.target_id
                        where T1.model_id=%s"""
        self.cursor.execute(query, (model_id))
        rows = self.cursor.fetchall()

        targets = [i['name'] for i in rows]
        return targets

    def get_columns(self, model_id: int) -> tuple[list, list]:
        def flatten(array: list[list[str]]) -> list[str]:
            return [item for sublist in array for item in sublist]

        model_id = (model_id, )

        query = """select name
                        from ColumnsToModels as T1
                        inner join Columns as T2
                        on T1.column_id = T2.column_id
                        where T1.model_id=%s
                        and T2.type=0"""
        self.cursor.execute(query, (model_id))

        rows = self.cursor.fetchall()

        feature_columns = [i['name'] for i in rows]
        target_columns = self.get_targets(model_id)

        if not target_columns:
            raise Exception('''No targets have been selected,
                            fitting is impossible.\n''')

        return target_columns, feature_columns

    def _create_where(self, filters, flag=True) -> str:
        def create_or(column_name: str, values: list[str], flag: bool = True):
            # for categorical filters
            if flag:
                return '(' + ' or '.join(f"{column_name}=\'%s\'" % str(x) if x else f"{column_name} is Null" for x in values ) + ')'
            else:
                return '(' + ' or '.join(f"{column_name} between %s and %s" % (str(x[0]), str(x[1])) for x in values) + ')'

        def create_and(values: str):
            return '(' + ' and '.join('%s' % str(x) for x in values) + ')'

        where_sql = create_and([create_or(i, filters[i], flag) for i in filters])

        return where_sql

    def _create_where_for_num_filters(self, model_id: int) -> str:

        query = """select "begin", "end", name from Filters_num as a1
                   inner join Columns as a2
                   on a1.column_id=a2.column_id
                   where model_id = %s """

        self.cursor.execute(query, (model_id))
        data = self.cursor.fetchall()
        df = pd.DataFrame(data)

        # works fine?
        if df.empty:
            return ''

        filters = df.groupby('name')[['begin', 'end']].apply(
            lambda x: x.values.tolist()
        ).to_dict()

        return self._create_where(filters, flag=False)

    def _create_where_for_cat_filters(self, model_id: int) -> str:

        query = """select name, value from Filters_cat as a1
                   inner join Columns as a2
                   on a1.column_id=a2.column_id
                   where model_id = %s """

        self.cursor.execute(query, (model_id))
        data = self.cursor.fetchall()
        df = pd.DataFrame(data)

        # works fine?
        if df.empty:
            return ''

        filters = df.groupby('name')['value'].apply(
            lambda x: x.values.tolist()
        ).to_dict()

        return self._create_where(filters)

#######################################
# Functions that work with the integrolayer database; /DataModel was used instead
#######################################

    def _create_where_query(self, model_id: int, TABLENAME:str=None, number_of_last_months:int=None) -> str:
        where_for_num_query = self._create_where_for_num_filters(model_id)
        where_for_cat_query = self._create_where_for_cat_filters(model_id)

        # if TABLENAME:
        query = f'select * from {TABLENAME} '
        if where_for_cat_query != '' and where_for_num_query == '':
            query = query + ' where ' + where_for_cat_query
        elif where_for_num_query != '' and where_for_cat_query == '':
            query = query + ' where ' + where_for_num_query
        elif where_for_num_query != '' and where_for_cat_query != '':
            query = (query + ' where ' + where_for_num_query
                        + ' and ' + where_for_cat_query)
        return query

        # query = 'select * from ( ' + query_before_group + add_where_for_last_months(number_of_last_months) + query_with_group

        # if where_for_cat_query != '' and where_for_num_query == '':
        #     query = query + ') where ' + where_for_cat_query
        # elif where_for_num_query != '' and where_for_cat_query == '':
        #     query = query + ') where ' + where_for_num_query
        # elif where_for_num_query != '' and where_for_cat_query != '':
        #     query = (query + ') where ' + where_for_num_query
        #                    + ' and ' + where_for_cat_query)
        # else:
        #     query += ')'

        return query

    def get_filtered_data(self, model_id: int, number_of_last_months: int = 6) -> pd.DataFrame:

        query = self._create_where_query(model_id, 'Data')
        df = read_sql_query(query, self.conn)

        return df

    # TO DO: to rewrite
    def get_data(self, data_id: int) -> pd.DataFrame:
        query = 'select * from Data  where id=%s'
        self.cursor.execute(query, (data_id))
        data = self.cursor.fetchall()
        return pd.DataFrame(data)

    # TO DO: to rewrite
    def get_reliability_and_data(self,
                                 model_id: int,
                                 data_id: int
                                 ) -> tuple[bool, pd.DataFrame]:

        query = self._create_where_query(model_id, 'Data') + ' and ID=%s'
        self.cursor.execute(query, (data_id))
        data = self.cursor.fetchall()
        is_reliable = bool(pd.DataFrame(data).shape[0])

        data = self.get_data(data_id)

        return is_reliable, data


if __name__=='__main__':

    USERNAME = 'u1359913_admin'
    PASSWORD = '2xFs0*1s'
    HOST = '31.31.196.202'
    DB = 'u1359913_mechpredic'
    user = 'READER'
    password = 'GdQBEY8N'
    dsn = '172.20.20.46:1521/OPTIM'

    model_id = 51
    data_id = 5

    dbm = DB_Connector(HOST, USERNAME, PASSWORD, DB, user, password, dsn)
    # is_reliable, data = dbm.get_reliability_and_data(model_id, data_id)

    # print(data, '\n', is_reliable)
