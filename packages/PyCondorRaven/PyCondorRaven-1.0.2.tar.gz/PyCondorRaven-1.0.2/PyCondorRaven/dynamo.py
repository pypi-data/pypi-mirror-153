# -*- coding: utf-8 -*-
"""
Created on Tue June 1 16:30:41 2018
@author: daniel.velasquez
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from .preprocess_dataset import *
from PyCondorInvestmentAnalytics.optim import portfolio_optim
from PyCondorInvestmentAnalytics.utils import returns


class Dynamo:
    """Testing predictions with portafolios."""
    def __init__(self, w_bench, series, returns_obs, returns_pred, period="monthly", te_obj=0.01,  lb=None, ub=None, lb_act=None, ub_act=None, pred_horizon_in_months=None):
        self.asset_names = np.array(w_bench.index)
        self.n_assets = len(self.asset_names)
        self.w_bench = w_bench
        self.returns_obs = returns_obs[self.asset_names]
        self.returns_pred = returns_pred[self.asset_names]
        self.te_obj = te_obj
        self.series_train = series[series.index <= returns_pred.index[0]]
        self.optimizer = portfolio_optim(self.series_train, returns=False, period=period, asset_names=self.asset_names, mu=None, ra_coef=1.2, type = "relative", risk_obj=self.te_obj, w_bench = self.w_bench, lb=lb, ub=ub, lb_act=lb_act, ub_act=ub_act)
        pred_freq = None if pred_horizon_in_months is None else 12/pred_horizon_in_months
        self.freq = np.round(np.mean(365/(self.returns_pred.index[1:] - self.returns_pred.index[:-1]).days)) if pred_freq is None else pred_freq
        self.n_pred = len(self.returns_pred.values)

    def simulation(self, te_obj, tc_coef, reg_coef, plot_tr=False, sequential=True):
        score_obs = []
        score_neutral = []
        n_pred = len(self.returns_pred.values)
        policy_array = np.zeros((n_pred, self.n_assets))
        w_current = self.w_bench.copy()
        w_bench_current = self.w_bench.copy()
        for i in range(self.n_pred):
            util_fun = self.optimizer.utility_fun(mu=self.returns_pred.values[i,:], Sigma=None, ra_coef=None, tc_coef=tc_coef, reg_coef=reg_coef, w_current=w_current)
            w_act, _  = self.optimizer.minimize_util(util_fun=util_fun, risk_obj=te_obj)
            score_obs.append(np.dot((w_act + self.w_bench).values, self.returns_obs.values[i,:]) - tc_coef * np.sum(np.abs(w_act + self.w_bench - w_current)))
            score_neutral.append(np.dot(self.w_bench.values, self.returns_obs.values[i,:]) - tc_coef * np.sum(np.abs(self.w_bench - w_bench_current)))
            if sequential:
                w_upt = (w_act + self.w_bench) * (1+self.returns_obs.values[i,:])
                w_current = self.w_bench.sum() * w_upt / w_upt.sum()
                w_bench_upt = self.w_bench * (1+self.returns_obs.values[i,:])
                w_bench_current = self.w_bench.sum() * w_bench_upt / w_bench_upt.sum()

            policy_array[i,:] = (w_act + self.w_bench).values
        policy_df = pd.DataFrame(policy_array, index=self.returns_pred.index, columns=self.returns_pred.columns)
        if plot_tr:
            plt.plot(self.returns_pred.index, np.cumprod(1 + np.array(score_obs)), label="Portafolio")
            plt.plot(self.returns_pred.index, np.cumprod(1 + np.array(score_neutral)), label="Benchmark")
            plt.legend()
        return (score_obs, score_neutral, policy_df)

    def forward_ef(self, te_objs, tc_coefs, reg_coefs, plot_ef=True, sequential=True, figsize=(10, 6)):
        results = np.zeros((3, len(tc_coefs), len(te_objs), len(reg_coefs)))
        for i in range(len(tc_coefs)):
            for j in range(len(te_objs)):
                for k in range(len(reg_coefs)):
                    score_obs, score_neutral, policy_df = self.simulation(te_objs[j], tc_coefs[i], reg_coefs[k], False, sequential)
                    active_rets = np.array(score_obs) - np.array(score_neutral)
                    alpha = np.mean(active_rets)
                    te_anual = np.std(active_rets)
                    results[0, i, j, k] = te_anual * np.sqrt(self.freq) * 100
                    results[1, i, j, k] = alpha * 10000
                    results[2, i, j, k] = alpha/te_anual
        # Index of max. information ratio parameters:
        max_ind = np.unravel_index(np.argmax(results[2,:,:,:], axis=None), results[2,:,:,:].shape)
        te_opt = te_objs[max_ind[1]]
        tc_opt = tc_coefs[max_ind[0]]
        reg_opt = reg_coefs[max_ind[2]]

        if plot_ef:
            fig, axes = plt.subplots(nrows=1, ncols=2, figsize=figsize)
            for i in range(len(tc_coefs)):
                axes[0].plot(results[0,i,:,max_ind[2]], results[1,i,:,max_ind[2]], label="TC %s%%"% (tc_coefs[i]*100) )
            axes[0].legend()
            axes[0].set_title("Coef. Reg.: " + str(reg_opt))
            axes[0].set_xlabel('TE Realizado')
            axes[0].set_ylabel('PB Alpha')

            for i in range(len(reg_coefs)):
                axes[1].plot(results[0,max_ind[0],:,i], results[1,max_ind[0],:,i], label="Reg %s%%"% (reg_coefs[i]*100) )
            axes[1].legend()
            axes[1].set_title("TC: " + str(tc_opt))
            axes[1].set_xlabel('TE Realizado')
            axes[1].set_ylabel('PB Alpha')
        return results, te_opt, tc_opt, reg_opt, max_ind


class portfolio_hyper_optim:
    """Hyperparameter Optimization."""
    def __init__(self, series, asset_names=None, period="monthly", type='relative',  ref_date=None, lb=None, ub=None, lb_act=None, ub_act=None, w_bench=None, train_perc=0.8, dec_period=None):
        self.period = period
        self.asset_names = asset_names if asset_names is not None else np.array(series.columns)
        self.series = series
        self.n_assets = len(self.asset_names)
        self.w_bench = w_bench
        self.type = type
        if ref_date is None:
            ref_date = series.index[int(series.shape[0] * train_perc)]
        self.ref_date = ref_date
        self.series_train = self.series.loc[self.series.index <= ref_date]
        self.series_test = self.series.loc[self.series.index > ref_date]
        self.returns_test = returns(self.series_test, period)
        self.optimizer = portfolio_optim(self.series_train, returns=False, period=period, asset_names=self.asset_names, mu=None, ra_coef=1.2, type = self.type, risk_obj=None, w_bench = self.w_bench)
        self.freq = {'monthly':12, 'quarterly':4}[period]
        self.dec_period=dec_period

    def simulation(self, ra_coef, reg_coef):
        """
        Simulation
        """
        if self.dec_period is None:
            util_fun = self.optimizer.utility_fun(mu=None, Sigma=None, ra_coef=ra_coef, reg_coef=reg_coef)
            w, _  = self.optimizer.minimize_util(util_fun=util_fun)
            freq = self.freq
            port_rets = self.returns_test[w.index] @ w
        else:
            self.returns_dec_dates = returns(self.series_test, self.dec_period)
            dec_dates = self.returns_dec_dates.index
            series_temp = self.series_train.copy()
            freq = {'monthly':12, 'quarterly':4, 'semiannualy':2, 'yearly':1}[self.dec_period]
            port_rets = []
            w = None
            for date_i in dec_dates:
                optimizer_temp = portfolio_optim(series_temp, returns=False, period=self.period, asset_names=self.asset_names, mu=None, ra_coef=1.2, type = self.type, risk_obj=None, w_bench = self.w_bench)
                util_fun = optimizer_temp.utility_fun(mu=None, Sigma=None, ra_coef=ra_coef, reg_coef=reg_coef)
                w_temp, _  = optimizer_temp.minimize_util(util_fun=util_fun)
                w = pd.concat([w, w_temp.to_frame(date_i)], axis=1, sort=False)
                if self.type=='relative':
                    bench_ret_i = np.dot(self.returns_dec_dates.loc[date_i].loc[self.w_bench.index],self.w_bench)
                    port_rets.append(np.dot(self.returns_dec_dates.loc[date_i].loc[w_temp.index],w_temp)-bench_ret_i)
                else:
                    port_rets.append(np.dot(self.returns_dec_dates.loc[date_i].loc[w_temp.index],w_temp))
                series_temp = self.series.loc[self.series.index <= date_i]
        port_mean = np.mean(port_rets)*freq
        port_sd = np.std(port_rets)*np.sqrt(freq)
        return port_mean, port_sd, w

    def forward_ef(self, ra_coeffs, reg_coeffs, plot_ef=True, max_te=None):
        """
        Forward efficient frontier
        """
        scores_df = pd.DataFrame(np.zeros((len(ra_coeffs), len(reg_coeffs))), index=ra_coeffs, columns=reg_coeffs)
        scores = dict(sd=scores_df.copy(), mean=scores_df.copy(), sharpe=scores_df.copy())
        w_dict = dict()
        for i in range(len(ra_coeffs)):
            reg_dict = dict()
            for j in range(len(reg_coeffs)):
                port_mean, port_sd, w = self.simulation(ra_coeffs[i], reg_coeffs[j])
                scores['sd'].iloc[i,j] = port_sd
                scores['mean'].iloc[i,j] = port_mean
                scores['sharpe'].iloc[i,j] = 0 if port_sd==0 else port_mean/port_sd
                reg_dict[reg_coeffs[j]] = w
            w_dict[ra_coeffs[i]] = reg_dict
        ra_best = scores['sharpe'].index[int(np.argmax(scores['sharpe'].values)/scores['sharpe'].values.shape[1])]
        reg_best = scores['sharpe'].iloc[int(np.argmax(scores['sharpe'].values)/scores['sharpe'].values.shape[1])].idxmax()
        w_best = w_dict[ra_best][reg_best]
        port_series_test, port_tr_test = series_total_return(self.returns_test, w_best, self.period)
        if self.w_bench is not None:
            bench_series_test, bench_tr_test = series_total_return(self.returns_test, self.w_bench, self.period)
        else:
            bench_series_test, bench_tr_test = None, None
        if plot_ef:
            for k in range(len(reg_coeffs)):
                plt.plot(scores['sd'].iloc[:,0], scores['mean'].iloc[:,0], label="Reg. %s"% (reg_coeffs[k]) )
            plt.legend()
            plt.xlabel('Riesgo Realizado')
            plt.ylabel('Retorno Realizado')

        optim = portfolio_optim(self.series, returns=False, period=self.period, asset_names=self.asset_names, mu=None, ra_coef=1.2, type = self.type, risk_obj=None, w_bench = self.w_bench)
        util_fun = optim.utility_fun(mu=None, Sigma=None, ra_coef=ra_best, reg_coef=reg_best)
        w, _  = optim.minimize_util(util_fun=util_fun)

        return w, scores, w_dict, port_series_test, bench_series_test, port_tr_test, ra_best, reg_best
