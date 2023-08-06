import pandas as pd
import numpy as np
from statsmodels.tsa.api import VAR
from .utils import cash_conv, iso_quote, fx_cross
import datetime as dt

def read_files(files_list, sep=',', index_col = [0], encoding = "latin1", parse_dates=[0], dayfirst=True, root=""):
    data_list = []
    vars_list = []
    for file_i in files_list:
        df = pd.read_csv(root + file_i, sep=',', index_col = [0], encoding = "latin1", parse_dates=[0], dayfirst=True)
        data_list = data_list + [df]
        vars_list = vars_list + list(df.columns)
    return data_list, np.unique(vars_list)

def available_dates(series_dict, var_names=None, asset_data=None):
    if asset_data is not None:
        var_ind = np.in1d(var_names, asset_data.index)
        if np.any(~var_ind):
             raise ValueError("%s not in asset data!" %( var_names[var_ind]))
        tks = asset_data.loc[var_names]['TickerBenchmark'].values
    else:
        tks = var_names
    avail_dates = pd.DataFrame([[np.array(['daily', 'monthly', 'quarterly', 'yearly'])[np.argmin(np.abs(np.array([1,30,90,360]) - np.mean((series_dict[tk].index[1:]-series_dict[tk].index[:-1]).days)))], len(series_dict[tk]), series_dict[tk].index[0], series_dict[tk].index[-1]] if len(series_dict[tk])>0 else [None, 0, None, None] for tk in tks], index=var_names, columns=["Period", "Obs", "Start", "End"])
    return avail_dates

def valid_series(series_dict, ini_date, end_date, var_names=None, asset_data=None):
    range_dates = '%s-%s' % (ini_date.strftime("%Y"), end_date.strftime("%Y"))
    avail_dates = available_dates(series_dict, var_names=var_names, asset_data=asset_data)
    avail_dates[range_dates] = (avail_dates.Start<ini_date) & (avail_dates.End>end_date)
    valid_series = avail_dates[avail_dates[range_dates]].index
    return valid_series

def series_data_to_dict(series, date_index=True):
    valid_cols = series.columns[[not x[:7]=="Unnamed" for x in series.columns]]
    series_dict = dict()
    for var in valid_cols:
        if date_index:
            series_temp = series[var].rename(var).dropna()
        else:
            pos_var = list(series.columns).index(var)
            series_temp = series.iloc[:,pos_var+1].rename(var)
            is_valid = series_temp.notna()
            series_temp = series_temp[is_valid]
            series_temp.index = [dt.datetime.strptime(x, "%d/%m/%Y") for x in series.iloc[is_valid.values,pos_var].values]
        series_dict[var] = series_temp.sort_index()
    return series_dict

def series_sync(series_dict, asset_data, assets, ref_curr, dates=None, currencies=[], convert_to_ref= False, invest_assets=None, ref_per_unit_foreign = False, join="inner"):
    '''
    dfs: Dataframes list. Each dataframe is a pandas index with date index.
    '''
    n_curr = len(currencies)
    if invest_assets == "ETF":
        ticker = asset_data.TickerETF[assets]
    elif invest_assets == "IA":
        ticker = asset_data.TickerInvestAsset[assets]
    else:
        ticker = asset_data.TickerBenchmark[assets]
    missing_ticker = [not np.any(np.array(list(series_dict.keys()))==x) for x in ticker.values]

    if np.any(missing_ticker):
        raise ValueError("Missing tickers: %s" % ticker[missing_ticker])
        ticker[missing_ticker] = asset_data.TickerBenchmark[list(np.array(assets)[missing_ticker])]
    series_out = pd.DataFrame()
    how = {0:'outer'}
    if len(assets)>0:
        if convert_to_ref:
            for asset, tk in ticker.items():
                if invest_assets =="ETF":
                    i_curr = asset_data.CurrencyETF[asset]
                elif invest_assets == "IA":
                    i_curr = asset_data.CurrencyIA[asset]
                else:
                    i_curr = asset_data.Currency[asset]
                if i_curr == ref_curr:
                    series_out = series_out.merge(pd.DataFrame(series_dict[tk].rename(asset)), left_index=True, right_index=True, how=how.get(len(series_out), join))
                else:
                    currs = np.array([i_curr, ref_curr])
                    if np.any(currs == "USD"):
                        i_curr_temp = currs[currs != "USD"][0]
                        series_temp = pd.merge(pd.DataFrame(series_dict[tk]),pd.DataFrame(series_dict[i_curr_temp]), left_index=True, right_index=True, how='inner')
                        series_conv = pd.Series([cash_conv(ci, i_curr, fxi, iso_quote(i_curr_temp)) for ci,fxi in zip(series_temp.iloc[:,0].values, series_temp.iloc[:,1].values)],
                                                index = series_temp.index).rename(asset)
                        series_out = series_out.merge(pd.DataFrame(series_conv), left_index=True, right_index=True, how=how.get(len(series_out), join))
                    else:
                        iso_cross = ref_curr + i_curr
                        series_temp_fx = pd.DataFrame(series_dict[tk]).merge(pd.DataFrame(series_dict[ref_curr]), left_index=True, right_index=True, how='inner').merge(pd.DataFrame(series_dict[i_curr]), left_index=True, right_index=True, how='inner')
                        series_fx_cross = pd.Series([fx_cross(ref_curr, i_curr, iso_quote(ref_curr), spot1, iso_quote(i_curr), spot2) for spot1,spot2 in zip(series_temp_fx.iloc[:,1].values, series_temp_fx.iloc[:,2].values)],
                                                     index = series_temp_fx.index)
                        series_temp = pd.merge(pd.DataFrame(series_dict[tk]),pd.DataFrame(series_fx_cross), left_index=True, right_index=True, how='inner')
                        series_conv = pd.Series([cash_conv(ci, i_curr, fxi, iso_cross) for ci,fxi in zip(series_temp.iloc[:,0].values, series_temp.iloc[:,1].values)],
                                                index = series_temp.index).rename(asset)
                        series_out = series_out.merge(pd.DataFrame(series_conv), left_index=True, right_index=True, how=how.get(len(series_out), join))

        else:
            for asset, tk in ticker.items():
                series_out = series_out.merge(pd.DataFrame(series_dict[tk].rename(asset)), left_index=True, right_index=True, how=how.get(len(series_out), join))

    if len(currencies)>0:
        for i in range(n_curr):
            if currencies[i] == ref_curr:
                series_out = series_out.merge(pd.DataFrame(pd.Series(np.ones(len(series_out)), index=series_out.index).rename(currencies[i])), left_index=True, right_index=True, how=how.get(len(series_out), join))
            else:
                currs = np.array([currencies[i], ref_curr])
                if np.any(currs == "USD"):
                    i_curr_temp = currs[currs != "USD"][0]
                    if ref_per_unit_foreign and iso_quote(i_curr_temp)[:3] == ref_curr:
                        series_out = series_out.merge(pd.DataFrame((1/series_dict[i_curr_temp]).rename(currencies[i])), left_index=True, right_index=True, how=how.get(len(series_out), join))
                    else:
                        series_out = series_out.merge(pd.DataFrame(series_dict[i_curr_temp].rename(currencies[i])), left_index=True, right_index=True, how=how.get(len(series_out), join))
                else:
                    iso_cross = currencies[i] + ref_curr
                    series_temp_fx = pd.merge(pd.DataFrame(series_dict[currencies[i]]),pd.DataFrame(series_dict[ref_curr]), left_index=True, right_index=True, how='inner')
                    series_fx_cross = pd.Series([fx_cross(currencies[i], ref_curr, iso_quote(currencies[i]), spot1, iso_quote(ref_curr), spot2) for spot1,spot2 in zip(series_temp_fx.iloc[:,0].values, series_temp_fx.iloc[:,1].values)],
                                                 index = series_temp_fx.index)
                    series_out = series_out.merge(pd.DataFrame(series_fx_cross.rename(iso_cross)), left_index=True, right_index=True, how=how.get(len(series_out), join))
    if dates is not None:
        series_out = series_out[[x >= dates[0] and x <= dates[1] for x in series_out.index]]
    series_out.index = pd.to_datetime(series_out.index)
    return series_out

def series_sync_factors(asset_factor_map, series_dict, asset_data, assets, ref_curr, dates=None, currencies=[], convert_to_ref= False, invest_assets=None, ref_per_unit_foreign = False):
    is_fx = np.in1d(assets, list(asset_data.Currency))
    if np.any(is_fx):
        currencies = currencies + list(assets[is_fx])
    assets = np.array(assets[~is_fx])
    in_series = np.in1d(assets, list(series_dict.keys()))
    assets_keys = assets.copy()
    assets_keys[~in_series] = asset_factor_map.reset_index().set_index("Factor").Asset[assets[~in_series]].values
    series = series_sync(series_dict, asset_data, list(assets_keys), ref_curr, dates=dates, currencies=currencies, convert_to_ref=convert_to_ref, invest_assets=invest_assets, ref_per_unit_foreign=ref_per_unit_foreign)
    series.columns = list(assets) + currencies
    return (series)

def series_normalize(series_df):
        series_rets = 1 + series_df.pct_change()
        series_rets.iloc[0,:] = np.ones(series_df.shape[1])
        return series_rets.cumprod()

def series_merge(dfs, var_names=None, max_date=None):
    '''
    dfs: Dataframes list. Each dataframe is a pandas index with date index.
    '''
    if len(dfs)>1:
        data = pd.DataFrame()
        sel_cols = []
        for i in range(len(dfs)):
            if var_names is not None:
                valid_cols = list(dfs[i].columns[np.in1d(dfs[i].columns,var_names)])
            else:
                valid_cols = list(dfs[i].columns)
            sel_cols = sel_cols + valid_cols
            data = data.merge(dfs[i].dropna(how="all")[valid_cols], left_index=True, right_index=True, how='outer')
    else:
        if var_names is not None:
            sel_cols = list(dfs[0].columns[np.in1d(dfs[0].columns,var_names)])
        else:
            sel_cols = list(dfs[0].columns)
        data = dfs[0].dropna(how="all")
    if max_date is not None:
        data = data.loc[data.index <= max_date]
    return data, sel_cols

def transform_df(df, method=None, roll=3):
    if method[:3]=="ret" or method[:3]=="pct":
        tf_df = df.pct_change()
        if method[-3:]=='log':
            tf_df = np.log(1 + tf_df)
    elif method[:3]=='dif':
        tf_df = df.diff()
    elif method[:3]=='rol':
        tf_df = df.rolling(roll).mean()
    else:
        tf_df = df
    return tf_df

class dataset(object):
    def __init__(self, series_list, guide=None, var_names=None, period='monthly', max_date=None, roll=3):
        '''
        Data preprocessing. By default input variables series are sliced to fit the output variables range.
        '''
        # Input and output variables:
        self.guide = guide
        if var_names is None:
            if guide is not None:
                var_names = guide.index
            else:
                var_names = None
        self.data, self.avail_vars = series_merge(series_list, var_names=var_names, max_date=max_date)
        self.period = period
        self.roll = roll

    def dataset_freq(self, var_names=None, period=None):
        if period is None:
            period = self.period
        if var_names is None:
            var_names = self.avail_vars
        if period == 'monthly':
            preproc_df = self.data[var_names].resample('M').last()
        elif period == 'quarterly':
            preproc_df = self.data[var_names].resample('3M').last()
        elif period == 'yearly':
            preproc_df = self.data[var_names].resample('12M').last()
        return preproc_df.dropna(how="all")

    def available_data(self, var_names=None):
        if var_names is None:
            var_names = self.avail_vars
        ind_vars = np.in1d(var_names, self.avail_vars)
        if np.any(~ind_vars):
            raise ValueError("Variables not available in dataset: %s" %(vars[~ind_vars]))
        proc_dataset = self.dataset_freq(var_names)
        n_rows = proc_dataset.shape[0]
        avail_dates = pd.DataFrame([[dt.datetime.strftime(proc_dataset[x].dropna().index[0], "%Y-%m-%d"), dt.datetime.strftime(proc_dataset[x].dropna().index[-1], "%Y-%m-%d")] for x in proc_dataset.columns], index=proc_dataset.columns, columns=["Start", "End"])
        avail_obs = pd.DataFrame((~np.isnan(proc_dataset.values)).sum(axis=0), index=proc_dataset.columns, columns=["Obs"])
        avail_data = pd.concat([avail_obs, avail_dates], axis=1, sort=False)
        return avail_data

    def transform(self, var_names=None, drop_how='any', method=None, period=None, drop_na = True, roll=None):
        if period is None:
            period = self.period
        if roll is None:
            roll = self.roll
        if method is None and self.guide is None:
            raise ValueError("method not found!")
        if var_names is None:
            var_names = self.avail_vars
        ind_vars = np.in1d(var_names, self.avail_vars)
        if np.any(~ind_vars):
            raise ValueError("Variables not available in dataset: %s" %(var_names[~ind_vars]))
        proc_dataset = self.dataset_freq(var_names, period=period)
        n_rows = proc_dataset.shape[0]
        if method is None:
            transf_method = self.guide.loc[var_names].values[:,0]
            for method in np.unique(transf_method):
                var_names_method = self.guide.loc[var_names].loc[transf_method == method].index
                proc_dataset[var_names_method] = transform_df(proc_dataset[var_names_method], method, roll)
        else:
            proc_dataset = transform_df(proc_dataset, method, roll)
        if drop_na:
            return proc_dataset.dropna(how=drop_how)
        else:
            return proc_dataset

    def plot_series(self, var_names=None, transformed=False, method=None, norm=False):
        from matplotlib import pyplot as plt
        if transformed:
            series = self.transform(var_names=var_names, method=method)
        else:
            series = self.dataset_freq(var_names)
            if norm:
                series = series_normalize(proc_dataset)
        plt.plot(series)
        plt.legend(asset_names)
        plt.xlabel('Tiempo')

    def shift_dataset(self, lag = True, forecast = False, nlag = None, nforecast = None, var_lags = None, var_forecast = None, drop_var_forecast = False,
                    output_all = False, output_type = 'single_value', dropna = True):
        """
        Shifts variables in dataset (forward, backward). Provides different methods for shifting variables forward, such as the mode output,
        which returns the mode of the next n periods.
        Parameters
        ----------
        lag: boolean
            True to shift variables backwards (lags).
        forecast: boolean
            True to shift variables forward (forecasts).
        nlag: int
            Lag period
        nforecast: int
            Forecast period
        var_lags: list
            If None, operations will be performed on the entire dataset. If a list is passed, only the variables in the list will be transformed
        var_forecast: list
            If None, operations will be performed on the entire dataset. If a list is passed,  only the variables in the list will be transformed
        output_all: boolean
            If True, range(forecasts) cols will be returned for each value in range, else, single output will be returned
        output_type: 'mode', 'mean', 'single_value'
            single_value -- X (t+nforecast) value will be returned
            mode -- the mode of the next nforecast values will be returned
            mean -- the mean of the next nforecast values will be returned
            jurik -- the jurik filter smoothed mean of the next nforecast values will be returned
        dropna: boolean

        Returns
        ----------
            Pandas dataframe
        """

        from scipy import stats

        series = self.data
        output = pd.DataFrame(index = series.index)
        if lag:
            if var_lags is None:
                for col in series.columns:
                    for i in range(1, nlag):
                        output[col + ' t- ' + str(i)] = series[col].shift(i)
            else:
                for var in var_lags:
                    for i in range(1, nlag):
                        output[var + ' t- ' + str(i)] = series[var].shift(i)

        if forecast:
            if var_forecast is None:
                if output_all:
                    if output_type == 'single_value':
                        for col in series.columns:
                            for i in range(1, nforecast):
                                output[col + ' t+ ' + str(i)] = series[col].shift(-i)
                    elif output_type == 'mode':
                        for col in series.columns:
                            for i in range(1, nforecast):
                                output[col + ' t+ ' + str(i)] = series[col].rolling(window = i).apply(lambda x: stats.mode(x)[0]).shift(-i)
                    elif output_type == 'mean':
                        for col in series.columns:
                            for i in range(1, nforecast):
                                output[col + ' t+ ' + str(i)] = series[col].rolling(window = i).apply(lambda x: np.mean(x)).shift(-i)
                    elif output_type == 'jurik_ma':
                        for col in series.columns:
                            for i in range(1, nforecast):
                                output[col + ' t+ ' + str(i)] = jurik(series[col].rolling(window = i).apply(lambda x: np.mean(x)).shift(-i))
                else:
                    if output_type == 'single_value':
                        for col in series.columns:
                            output[col + ' t+ ' + str(nforecast)] = series[col].shift(-nforecast)
                    elif output_type == 'mode':
                        for col in series.columns:
                            output[col + ' t+ ' + str(nforecast)] = series[col].rolling(window = nforecast).apply(lambda x: stats.mode(x)[0]).shift(-nforecast)
                    elif output_type == 'mean':
                        for col in series.columns:
                            output[col + ' t+ ' + str(nforecast)] = series[col].rolling(window = nforecast).apply(lambda x: np.mean(x)).shift(-nforecast)
                    elif output_type == 'jurik_ma':
                        for col in series.columns:
                            output[col + ' t+ ' + str(nforecast)] = jurik(series[col].rolling(window = nforecast).apply(lambda x: np.mean(x)).shift(-nforecast))
            else:
                if output_all:
                    if output_type == 'single_value':
                        for var in var_forecast:
                            for i in range(1, nforecast):
                                output[var + ' t+ ' + str(i)] = series[var].shift(-i)
                    elif output_type == 'mode':
                        for var in var_forecast:
                            for i in range(1, nforecast):
                                output[var + ' t+ ' + str(i)] = series[var].rolling(window = i).apply(lambda x: stats.mode(x)[0]).shift(-i)
                    elif output_type == 'mean':
                        for var in var_forecast:
                            for i in range(1, nforecast):
                                output[var + ' t+ ' + str(i)] = series[var].rolling(window = i).apply(lambda x: np.mean(x)).shift(-i)
                    elif output_type == 'jurik_ma':
                        for var in var_forecast:
                            for i in range(1, nforecast):
                                output[var + ' t+ ' + str(i)] = jurik(series[var].rolling(window = i).apply(lambda x: np.mean(x)).shift(-i))
                else:
                    if output_type == 'single_value':
                        for var in var_forecast:
                            output[var + ' t+ ' + str(nforecast)] = series[var].shift(-nforecast)
                    elif output_type == 'mode':
                        for var in var_forecast:
                            output[var + ' t+ ' + str(nforecast)] = series[var].rolling(window = nforecast).apply(lambda x: stats.mode(x)[0]).shift(-nforecast)
                    elif output_type == 'mean':
                        for var in var_forecast:
                            output[var + ' t+ ' + str(nforecast)] = series[var].rolling(window = nforecast).apply(lambda x: np.mean(x)).shift(-nforecast)
                    elif output_type == 'jurik_ma':
                        for var in var_forecast:
                            output[var + ' t+ ' + str(nforecast)] = jurik(series[var].rolling(window = nforecast).apply(lambda x: np.mean(x)).shift(-nforecast))

        output = pd.concat([series, output], axis = 1)

        if forecast:
            cols = output.columns.values.tolist()
            cols = cols[-1:] + cols[:-1]
            output = output[cols]

        output = output[[output.columns[0]] + sorted(output.columns[output.columns != output.columns[0]])]
        if drop_var_forecast:
            output.drop(labels = var_forecast, axis = 1, inplace = True)

        if dropna:
            return output.dropna()
        else:
            return output


class assets(object):
    def __init__(self, series, rets_period = 'monthly'):
        self.series = series
        self.rets_period = rets_period
        self.n = series.shape[1]
        if rets_period=='daily':
            self.per = 252
        elif rets_period=='monthly':
            self.per = 12
        elif rets_period=='quarterly':
            self.per = 4

        if self.rets_period == 'daily':
            self.returns = self.series.pct_change().dropna()
        elif self.rets_period == 'monthly':
            self.returns = self.series.asfreq('M', method='pad').fillna(method="ffill").pct_change().dropna()
        elif self.rets_period == 'quarterly':
            self.returns = self.series.asfreq('3M', method='pad').fillna(method="ffill").pct_change().dropna()
        self.Sigma = self.returns.cov() * self.per
        self.mu = self.returns.mean() * self.per

    def hf_sigmas(self, remove_cero=True):
        sigmas = pd.DataFrame(np.abs(np.log(np.array(self.series.iloc[1::]) / np.array(self.series.iloc[0:-1]))),
                              index=self.series.index[1:], columns=self.series.columns)
        pos_non_cero = [any(sigmas.iloc[i]!=0) for i in np.arange(sigmas.shape[0])]
        return(sigmas[pos_non_cero])

    def implied_returns(self, w, ra_coef, rfr = 0):
        '''
            w: pd Series
        '''
        implied_ret = pd.Series(ra_coef * 2 * (self.Sigma.loc[w.index][w.index].values @ w.values), index=w.index)
        return(implied_ret)

    def get_ra_coef(self, w):
        port_rets = self.returns[w.index] @ w
        ra = port_rets.mean()/port_rets.var()
        return(ra)

    def posterior_params(self, q, P, mu = None, tau = None, Omega = None, conf = 0.5):
        '''
        Asset return dist. is N(x, Sigma) and x is N(mu, tau*Sigma),
        P @ mu  is N(q, Omega).
        P: n_views x n_assets
        mu: prior returns mean,
        q: absolute or relative return
        '''
        if mu is None:
            mu = self.mu
        if tau is None:
            tau = 1/len(self.returns)

        if P is None:
            post_ret = mu
            post_var = self.Sigma
        else:
            if Omega is None:
                conf = (1 - conf)/conf
                Omega = np.diag(tau * np.diag(P @ self.Sigma.values @ P.T)) * conf
        omega_inv = np.linalg.inv(Omega)
        tSigma_inv = np.linalg.inv(tau * self.Sigma.values)
        post_ret = pd.Series(np.linalg.inv(tSigma_inv + P.T @ omega_inv @ P) @ (tSigma_inv @ mu + P.T @ omega_inv @ q), index=mu.index)
        post_var = (1 + tau) * self.Sigma.values - tau**2 * self.Sigma.values @ P.T @ np.linalg.inv(P @ (tau * self.Sigma.values) @ P.T + Omega) @ P @ self.Sigma.values
        return(post_ret, post_var)

if __name__=="__main__":
	pass
