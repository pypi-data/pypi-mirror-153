import pandas as pd
import numpy as np
import datetime as dt
import pymysql
import sys
import os
from PyCondorInvestmentAnalytics.utils import extract_data_s3select

from datetime import datetime

class database:
    def __init__(self, hostname = None, user = None, password = None, db_name = None, connect_timeout=10):
        # For MySQL connections
        self.hostname = hostname
        self.user = user
        self.password = password
        self.db_name = db_name
        self.connect_timeout = connect_timeout

    def trained_models(self, target_var, time_steps, period, output_currency=None):
        db = pymysql.connect(self.hostname, self.user,
                             self.password, self.db_name, connect_timeout=self.connect_timeout)
        cur = db.cursor()

        # Query model based on target var and model_id
        query_models = """select model_id from Variables where is_output=1 and id like '%%%s%%'""" % (
            target_var)
        sol = cur.execute(query_models)
        if sol==0:
            query_models = """select model_id from Variables where is_output=1 and model_id like '%%%s%%'""" % (target_var)
            cur.execute(query_models)

        models = np.array([x[0] for x in cur.fetchall()])
        if output_currency is None:
            query_params = """select model_id from Parameters where time_steps=%s and period='%s'""" % (
                time_steps, period)
        else:
            query_params = """select model_id from Parameters where time_steps=%s and period='%s' and output_currency='%s'""" % (
                time_steps, period, output_currency)
        cur.execute(query_params)
        ts = np.array([x[0] for x in cur.fetchall()])
        models = models[np.isin(models, ts)]
        db.close()
        return models

    def save_model(self, model_name, features, period, time_steps, n_lags, output_currency, model_desc="", data_trans_method="rets"):
        db = pymysql.connect(self.hostname, self.user,
                             self.password, self.db_name, connect_timeout=self.connect_timeout)
        cur = db.cursor()
        query_model = """INSERT INTO Models (id,description,model_date) VALUES ('%s','%s', '%s')"""
        query_variables = """INSERT INTO Variables (id,model_id,is_output, var_order) VALUES ('%s','%s',%s, %s)"""

        query_del_params = """DELETE FROM Parameters WHERE model_id='%s'""" % (
            model_name)
        cur.execute(query_del_params)
        query_del_variables = """DELETE FROM Variables WHERE model_id='%s'""" % (
            model_name)
        cur.execute(query_del_variables)
        query_del_model = """DELETE FROM Models WHERE id='%s'""" % (model_name)
        cur.execute(query_del_model)

        query = query_model % (model_name, model_desc,
                               dt.date.today().strftime("%Y-%m-%d"))
        cur.execute(query)

        for i in range(len(features)):
            if i == 0:
                is_output = 'true'
            else:
                is_output = 'false'
            query = query_variables % (features[i], model_name, is_output, i)
            cur.execute(query)

        if output_currency is None:
            output_currency = "NULL"
            query_parameters = """INSERT INTO Parameters (model_id,data_trans_method,period,time_steps,n_lags, output_currency) VALUES ('%s','%s','%s',%s,%s,%s)"""
        else:
            query_parameters = """INSERT INTO Parameters (model_id,data_trans_method,period,time_steps,n_lags, output_currency) VALUES ('%s','%s','%s',%s,%s,'%s')"""

        query = query_parameters % (
            model_name, data_trans_method, period, time_steps, n_lags, output_currency)
        cur.execute(query)

        db.commit()
        db.close()

    def model_params(self, model_name):
        db = pymysql.connect(self.hostname, self.user,
                             self.password, self.db_name, connect_timeout=self.connect_timeout)
        cur = db.cursor()

        query_variables = """select id,is_output,var_order from Variables where model_id='%s'""" % (
            model_name)
        query_params = """select data_trans_method, period, time_steps, n_lags, output_currency from Parameters where model_id='%s'""" % (
            model_name)

        cur.execute(query_variables)
        vars = cur.fetchall()
        if len(vars) == 0:
            raise Exception('Modelo no se encuentra en Base de Datos!')

        input_vars_temp = np.array([x[0] for x in vars])
        vars_order = np.array([x[2] for x in vars])

        if all(vars_order == None):
            is_output = [bool(x[1]) for x in vars]
            vars_ordered = np.append(input_vars_temp[is_output], np.setdiff1d(
                input_vars_temp, input_vars_temp[is_output]))
        else:
            vars_ordered = [input_vars_temp[vars_order == x][0]
                            for x in range(len(vars_order))]

        cur.execute(query_params)
        pars = cur.fetchall()
        data_trans_method, period, time_steps, n_lags, output_currency = pars[0]
        db.close()

        return vars_ordered, data_trans_method, period, time_steps, n_lags, output_currency

    def get_port(self, port_id):
        ref_date = None
        db_conn = pymysql.connect(
            self.hostname, self.user, self.password, self.db_name, connect_timeout=self.connect_timeout)
        cur = db_conn.cursor()
        query_w = """Select DatePort, Asset, Weight from Weights where PortId='%s'""" % (
            port_id)
        sol = cur.execute(query_w)
        if sol > 0:
            port_df = pd.DataFrame(np.array([[x[0], x[1], np.float16(
                x[2])] for x in cur.fetchall()]), columns=["Date", "Asset", "Weight"])
            ref_date = port_df.Date.max().strftime("%Y-%m-%d")
            port_w = port_df[port_df.Date.eq(port_df.Date.max())].set_index("Asset")[
                "Weight"]
            port_w.astype(np.float)
        else:
            port_w = None
        db_conn.close()
        return port_w, ref_date

    def save_port(self, port_id, port_df, desc, fase, fx, ref_curr, te, w_dev_max, w_dev_type, fase_prob=0):
        db_conn = pymysql.connect(
            self.hostname, self.user, self.password, self.db_name, connect_timeout=self.connect_timeout)
        ref_date = dt.datetime.today().strftime("%Y-%m-%d")
        cur = db_conn.cursor()
        query_w = """INSERT INTO Weights (PortId,DatePort,Asset,Weight) VALUES ('%s','%s','%s',%s)"""
        query_del_w = """DELETE FROM Weights WHERE PortId='%s' and DatePort='%s'""" % (
            port_id, ref_date)
        cur.execute(query_del_w)

        for i in range(len(port_df)):
            port_values = np.round(port_df.values.flatten(), 4)
            query = query_w % (port_id, ref_date,
                               port_df.index[i], np.float16(port_values[i]))
            cur.execute(query)

        if w_dev_type is None or w_dev_type == "NULL":
            query_port = """INSERT INTO Portfolios (Id,Description,Fase,FxSep,Currency,Te,DevMax,DevType,FaseProb) VALUES ('%s','%s',%s,%s,'%s',%s,%s,%s,%s)"""
        else:
            query_port = """INSERT INTO Portfolios (Id,Description,Fase,FxSep,Currency,Te,DevMax,DevType,FaseProb) VALUES ('%s','%s',%s,%s,'%s',%s,%s,'%s',%s)"""
        query_del_port = """DELETE FROM Portfolios WHERE Id='%s'""" % (port_id)
        cur.execute(query_del_port)
        cur.execute(query_port % (port_id, desc, fase, fx,
                                  ref_curr, te, w_dev_max, w_dev_type, fase_prob))

        db_conn.commit()
        db_conn.close()

    def save_table(self, db_table_name, table):
        """
        Saves pandas dataframe records to table in MySQL
        """
        db_conn = pymysql.connect(
            self.hostname, self.user, self.password, self.db_name, connect_timeout=self.connect_timeout)
        query_in = """SELECT * FROM """ + db_table_name
        cur = db_conn.cursor()
        cur.execute(query_in)
        col_names = [x[0] for x in cur.description]
        assert sorted(col_names) == sorted(table.columns.values.tolist(
        )), "Columns in table are not equal to columns in " + db_table_name
        table = table.loc[:, col_names]
        for col_type in enumerate(table.dtypes):
            if col_type[1] == 'datetime64[ns]':
                table.iloc[:, col_type[0]] = table.iloc[:, col_type[0]].apply(
                    lambda x: x.strftime('%Y-%m-%d'))

        db_data = self.fetch_table(db_table_name).loc[:, col_names]
        db_data['temp'] = db_data.astype(str).apply(''.join, axis=1)
        table['temp'] = table.astype(str).apply(''.join, axis=1)
        table = table.loc[table.index[~table['temp'].isin(
            db_data['temp'])], ~table.columns.isin(['temp'])]

        if not table.empty:
            for i in range(len(table)):
                insert_vals = table.iloc[i, :].values
                query_out = """INSERT INTO """ + db_table_name + ' ' + \
                    str(tuple(col_names)).replace(" ", "").replace(
                        "'", "") + ' VALUES ' + str(tuple(insert_vals))
                cur.execute(query_out)

        db_conn.commit()
        db_conn.close()

    def fetch_table(self, db_table_name):
        """
        Fetches table from MySQL
        """
        db_conn = pymysql.connect(
            self.hostname, self.user, self.password, self.db_name, connect_timeout=self.connect_timeout)
        cur = db_conn.cursor()
        query_in = """SELECT * FROM """ + db_table_name
        cur.execute(query_in)
        output_df = pd.DataFrame(list(cur.fetchall()), columns=[
                                 x[0] for x in cur.description])

        db_conn.close()

        return output_df

    def fetch_target_vars(self, target_ticker_campo, s3client, make_transf = False, transf_target = None,
                          model_vars = None, ticker_campo = None, file_name = 'series_list_raven.csv', bucket = 'suraraven'):

        """
        Fetches variables used to predict target_ticker_campo.
        Parameters
        -- target_ticker_campo - target variable from target_ticker_campo column in target_variable table in raven_db
        -- data_dict - dictionary with series. Key structure must be ticker | field
        -- make_transf - True if user wants series to be transformed according to the transformation method defined in the transformation column in target_variable
        -- transf_target - transformation to be applied to target variable. pct_change, diff or none

        Returns
        -- Pandas Dataframe
        """

        import sys
        from scipy import stats

        if make_transf:
            assert transf_target != None, 'Target transformation must be passed if make_transf = True'

        if model_vars is None:
            model_vars = self.fetch_table('target_variable')
        variables = model_vars[model_vars['target_ticker_campo'] == target_ticker_campo]
        var_dict = tuple([target_ticker_campo]) + tuple(variables['varpred_ticker_campo'])
        data = extract_data_s3select(s3client, var_dict, file_name = file_name, bucket_name = bucket)
        transformations = {k: np.nan for k in list(data.keys())}

        if make_transf:
            for key, value in data.items():
                if not key == target_ticker_campo:
                    transf = variables[variables['varpred_ticker_campo'] == key]['transformacion'].values
                else:
                    transf = transf_target
                if transf == 'pct_change':
                    data[key] = value.pct_change()
                    transformations[key] = 'pct_change'
                elif transf == 'diff':
                    data[key] = value.diff()
                    transformations[key] = 'diff'
                elif transf == 'rolling_mean':
                    data[key] == value.rolling(12).mean()
                    transformations[key] = 'rolling_mean'
                elif transf == 'none':
                    data[key] == value
                    transformations[key] = 'none'

        df = pd.concat(data.values(), axis = 1)
        df.columns = list(tuple([target_ticker_campo]) + tuple(variables['varpred_ticker_campo']))

        if ticker_campo is None:
            ticker_campo = self.fetch_table('ticker_campo')
        shift_vals = ticker_campo[ticker_campo['ticker_campo'].isin(list(var_dict))]
        shift_vals = dict(zip(list(shift_vals['ticker_campo']), (shift_vals['shift'])))
        for col in df.columns:
            df[col] = df[col].shift(shift_vals[col])

        return df, transformations

    def fetch_model_data(self, model_name, s3client, file_name = 'series_list_raven.csv', bucket = 'suraraven'):

        """
        Fetches data required to make predictions or to train/re-train the model from series_list_raven

        Parameters
        -- model_name - model_name from nombre_modelo column in modelo table from raven_db
        -- data_dict - dictionary with series. Keys must be with the following structure: ticker | field

        Returns
        -- Pandas dataframe
        """

        import sys
        from scipy import stats

        req_data = self.fetch_table('modelo_ticker_campo')
        model_data = self.fetch_table('modelo')

        req_data['ticker_campo'] = req_data['ticker'] + ' | ' + req_data['campo']
        model_data['ticker_campo'] = model_data['ticker_target'] + ' | ' + model_data['campo_target']
        lag_all_vars = all(req_data[req_data['nombre_modelo'] == model_name]['lag_all'])

        target = model_data[model_data['nombre_modelo'] == model_name]['ticker_campo']
        features = req_data[req_data['nombre_modelo'] == model_name]['ticker_campo']

        if model_data[model_data['nombre_modelo'] == model_name]['lag_target'].values[0] == 1:
            lag_target = True
        else:
            lag_target = False

        fetch_data = tuple(target) + tuple(features)
        raven_sliced = extract_data_s3select(s3client, fetch_data, file_name = file_name, bucket_name = bucket)
        raven_concat = pd.concat(raven_sliced.values(), axis = 1)
        if lag_target:
            raven_concat['temp'] = raven_concat.iloc[:, 0]
            raven_concat.columns = list(dict.fromkeys(list(fetch_data))) + [list(dict.fromkeys(list(fetch_data)))[0]]
        else:
            raven_concat.columns = list(dict.fromkeys(fetch_data))

        ticker_campo = self.fetch_table('ticker_campo')
        shift_vals = ticker_campo[ticker_campo['ticker_campo'].isin(raven_concat.columns)]
        shift_vals = dict(zip(list(shift_vals['ticker_campo']), (shift_vals['shift'])))
        for col in raven_concat.columns:
            raven_concat[col] = raven_concat[col].shift(shift_vals[col])

        output_df = pd.DataFrame(index = raven_concat.index)

        for j in range(raven_concat.shape[1]):
            col = raven_concat.columns[j]
            if j == 0:
                req_cols = model_data[model_data['nombre_modelo'] == model_name]
                timestep = req_cols['timestep'].values[0]
                period = req_cols['periodo'].values[0]
                if req_cols['transformacion'].values[0] != 'none':
                    if req_cols['transformacion'].values[0] == 'pct_change':
                        if req_cols['output_type'].values[0] == 'mode':
                            output_df[col + ' t+ ' + str(timestep)] = raven_concat.iloc[:, j].pct_change(period).rolling(window = timestep).apply(lambda x: stats.mode(x)[0]).shift(-timestep)
                        elif req_cols['output_type'].values[0] == 'mean':
                            output_df[col + ' t+ ' + str(timestep)] = raven_concat.iloc[:, j].pct_change(period).rolling(window = timestep).apply(lambda x: np.mean(x)).shift(-timestep)
                        elif req_cols['output_type'].values[0] == 'simple':
                            output_df[col + ' t+ ' + str(timestep)] = raven_concat.iloc[:, j].pct_change(period).shift(-timestep)
                        elif req_cols['output_type'].values[0] == 'jurik_ma':
                            output_df[col + ' t+ ' + str(timestep)] = jurik(raven_concat.iloc[:, j].pct_change(period).rolling(window = timestep).apply(lambda x: np.mean(x)).shift(-timestep))
                    elif req_cols['transformacion'].values[0] == 'diff':
                        if req_cols['output_type'].values[0] == 'mode':
                            output_df[col + ' t+ ' + str(timestep)] = raven_concat.iloc[:, j].diff(period).rolling(window = timestep).apply(lambda x: stats.mode(x)[0]).shift(-timestep)
                        elif req_cols['output_type'].values[0] == 'mean':
                            output_df[col + ' t+ ' + str(timestep)] = raven_concat.iloc[:, j].diff(period).rolling(window = timestep).apply(lambda x: np.mean(x)).shift(-timestep)
                        elif req_cols['output_type'].values[0] == 'simple':
                            output_df[col + ' t+ ' + str(timestep)] = raven_concat.iloc[:, j].diff(period).shift(-timestep)
                        elif req_cols['output_type'].values[0] == 'jurik_ma':
                            output_df[col + ' t+ ' + str(timestep)] = jurik(raven_concat.iloc[:, j].diff(period).rolling(window = timestep).apply(lambda x: np.mean(x)).shift(-timestep))
                else:
                    if req_cols['output_type'].values[0] == 'mode':
                        output_df[col + ' t+ ' + str(timestep)] = raven_concat.iloc[:, j].rolling(window = timestep).apply(lambda x: stats.mode(x)[0]).shift(-timestep)
                    elif req_cols['output_type'].values[0] == 'mean':
                        output_df[col + ' t+ ' + str(timestep)] = raven_concat.iloc[:, j].rolling(window = timestep).apply(lambda x: np.mean(x)).shift(-timestep)
                    elif req_cols['output_type'].values[0] == 'simple':
                        output_df[col + ' t+ ' + str(timestep)] = raven_concat.iloc[:, j].shift(-timestep)
                    elif req_cols['output_type'].values[0] == 'jurik_ma':
                        output_df[col + ' t+ ' + str(timestep)] = jurik(raven_concat.iloc[:, j].rolling(window = timestep).apply(lambda x: np.mean(x)).shift(-timestep))
            else:
                req_data_tick = req_data[(req_data['nombre_modelo'] == model_name) & (req_data['ticker_campo'] == col)]
                for i in range(len(req_data_tick['ticker_campo'])):
                    req_data_temp = req_data_tick.iloc[i, :]
                    period_ticker = req_data_temp['periodo']
                    if req_data_temp['lag_all'] == 1:
                        if req_data_temp['transformacion'] == 'pct_change':
                            for i in range(1, req_data_temp['lag']):
                                output_df[col + ' t- ' + str(i)] = raven_concat.iloc[:, j].pct_change(period_ticker).shift(i)
                            output_df[col] = raven_concat.iloc[:, j].pct_change(period_ticker)
                        elif req_data_temp['transformacion'] == 'diff':
                            for i in range(1, req_data_temp['lag']):
                                output_df[col + ' t- ' + str(i)] = raven_concat.iloc[:, j].diff(period_ticker).shift(i)
                            output_df[col] = raven_concat.iloc[:, j].diff(period_ticker)
                        elif req_data_temp['transformacion'] == 'none':
                            for i in range(1, req_data_temp['lag']):
                                output_df[col + ' t- ' + str(i)] = raven_concat.iloc[:, j].shift(i)
                        elif req_data_temp['transformacion'] == 'rolling_mean':
                            for i in range(1, req_data_temp['lag']):
                                output_df[col + ' rolling_mean t- ' + str(i)] = raven_concat.iloc[:, j].rolling(period_ticker).mean().shift(i)
                            output_df[col] = raven_concat.iloc[:, j].rolling(period_ticker).mean()
                    else:
                        if req_data_temp['transformacion'] == 'pct_change':
                            output_df[col + ' t- ' + str(req_data_temp['lag'])] = raven_concat.iloc[:, j].pct_change(period_ticker).shift(req_data_temp['lag'])
                        elif req_data_temp['transformacion'] == 'diff':
                            output_df[col + ' t- ' + str(req_data_temp['lag'])] = raven_concat.iloc[:, j].diff(period_ticker).shift(req_data_temp['lag'])
                        elif req_data_temp['transformacion'] == 'none':
                            output_df[col + ' t- ' + str(req_data_temp['lag'])] = raven_concat.iloc[:, j].shift(req_data_temp['lag'])
                        elif req_data_temp['transformacion'] == 'rolling_mean':
                            output_df[col + ' rolling_mean t- ' + str(req_data_temp['lag'])] = raven_concat.iloc[:, j].rolling(period_ticker).mean().shift(req_data_temp['lag'])

        if not lag_all_vars:
            output_df.columns = [x.replace('t- 0', '') for x in output_df.columns]
            return output_df
        else:
            output_df = pd.concat([output_df, raven_concat], axis = 1)
            output_df = output_df[[output_df.columns[0]] + sorted(output_df.columns[output_df.columns != output_df.columns[0]])]
            output_df = output_df.loc[:, ~output_df.columns.duplicated()]

            if not lag_target:
                output_df = output_df.drop(labels = [raven_concat.columns[0]], axis = 1)

            return output_df


if __name__ == "__main__":
    pass
