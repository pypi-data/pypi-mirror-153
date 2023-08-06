# -*- coding: utf-8 -*-
"""
Created on Tue June 1 16:30:41 2018
@author: daniel.velasquez
"""

import numpy as np
import pandas as pd
import numpy.random as rnd
from sklearn.preprocessing import PolynomialFeatures
from statsmodels.tsa.api import VAR
from scipy.optimize import differential_evolution as de
from scipy.optimize import minimize
from scipy.optimize import linprog
from statsmodels.tsa.api import VAR
from statsmodels.tsa.vector_ar.util import varsim
import datetime as dt
from dateutil.relativedelta import relativedelta as rd
from PyCondorInvestmentAnalytics.valuation import bond
from PyCondorInvestmentAnalytics.valuation import cash_flows as cf
from scipy.stats import beta
from scipy.optimize import differential_evolution as de
from PyCondorInvestmentAnalytics.utils import returns

#from numba import jit
def ports_onehot(n_times, years_per_port):
    x_ini = []
    for i,j in enumerate(reversed(range(len(years_per_port)))):
        x_ini = x_ini + [j]*int(years_per_port[i])
    x_ini = x_ini[:n_times] + [0]*np.max([n_times-len(x_ini),0])
    return one_hot(np.array(x_ini), len(years_per_port))

def one_hot(a, num_classes):
    return np.squeeze(np.eye(num_classes)[a.reshape(-1)])

def sample_rets(series, period='semiannualy', hor_in_y=5, M=1000):
    rets = returns(series, period)
    freq = {'daily':365, 'monthly': 12, 'quarterly': 4, 'semiannualy':2, 'yearly':1}[period]
    times = np.arange(1/freq, hor_in_y+(1/freq), 1/freq)
    n_times = len(times)
    sample_rt = np.zeros((n_times, M, len(series.columns)))
    for i in range(M):
        pos_ini = np.random.choice(np.arange(0, rets.shape[0]-n_times))
        sample_rt[:,i,:] = rets.values[np.arange(pos_ini, pos_ini+n_times),:]
    return sample_rt


class glidepath:
    def __init__(self, contrib, spot, mu, Sigma):
        self.contrib = contrib
        self.times=np.arange(1,len(contrib)+1)
        self.spot = spot
        self.mu = mu
        self.Sigma = Sigma
        self.asset_names = list(mu.index)

    def simul(self,  times=None, M=1000):
        if times is None:
            times = self.times
        n_assets = len(self.spot)
        dt = np.repeat(np.diff([0]+list(times)), n_assets).reshape(-1,n_assets)
        sigma = np.sqrt(np.diag(self.Sigma))
        nu = self.mu.values - sigma**2/2
        N = len(times)
        R = np.linalg.cholesky(self.Sigma)
        st = np.zeros((N+1, M, n_assets))
        rt = np.zeros((N, M, n_assets))
        for i in range(M):
            x = np.random.normal(size=(N, n_assets)) * np.sqrt(dt)
            w = x @ R
            rt[:, i, :] = np.tile(nu, (N, 1)) * dt + w
            cum_ret = np.cumsum(rt[:, i, :], axis=0)
            st[:, i, :] = np.vstack([self.spot, np.exp(cum_ret) @ np.diag(self.spot)])
        return st, rt

    def simul_ports(self, ports, times=None, M=1000):
        if times is None:
            times = self.times
        st, rt = self.simul(times, M)
        pt = np.zeros((rt.shape[0]+1,rt.shape[1],ports.shape[1]))
        ports_rt = np.zeros((rt.shape[0],rt.shape[1],ports.shape[1]))
        for i in range(rt.shape[1]):
            ports_rt[:,i,:] = rt[:,i,:] @ ports.loc[self.asset_names].values
            ports_cum_ret = np.cumsum(ports_rt[:,i,:], axis=0)
            pt[:,i,:] = np.vstack([np.ones(ports_cum_ret.shape[1]), np.exp(ports_cum_ret)])
        return pt, ports_rt

    def rr_glidepath_summary(self, params, ports_rt, annuity_pr,target_wage, conf=0.9):
        n_ports = ports_rt.shape[2]
        time_props = (np.arange(n_ports+1)/n_ports)[1:]
        cum_dist = beta.cdf(time_props, params[0], params[1])
        port_props = np.array([cum_dist[0]] + list(np.diff(cum_dist)))
        n_times=ports_rt.shape[0]
        years_per_port = np.rint(port_props*n_times)
        ports_ind = ports_onehot(n_times=ports_rt.shape[0], years_per_port=np.round(years_per_port))
        acum_savings = np.zeros(ports_rt.shape[1])
        for i in range(ports_rt.shape[1]):
            rets = np.sum(ports_rt[:,i,:]*ports_ind, axis=1)
            fwd_rets = np.sum(rets) - np.array([0]+list(np.cumsum(rets)[:-1]))
            acum_savings[i] = np.sum(self.contrib*np.exp(fwd_rets))
            replace_rate_dist = acum_savings*annuity_pr/target_wage
            min_rr = np.quantile(replace_rate_dist, 1-conf)
        return dict(years_per_port=years_per_port, ports_ind=ports_ind, acum_savings=acum_savings,replace_rate_dist=replace_rate_dist, min_rr=min_rr)

    def wealth_glidepath_summary(self, params, ports_rt, ports_ind=None, risk_fun=np.var):
        if ports_ind is None:
            n_ports = ports_rt.shape[2]
            time_props = (np.arange(n_ports+1)/n_ports)[1:]
            cum_dist = beta.cdf(time_props, params[0], params[1])
            port_props = np.array([cum_dist[0]] + list(np.diff(cum_dist)))
            n_times=ports_rt.shape[0]
            years_per_port = np.rint(port_props*n_times)
            ports_ind = ports_onehot(n_times=ports_rt.shape[0], years_per_port=np.round(years_per_port))
        else:
            years_per_port = None
        acum_savings = np.zeros(ports_rt.shape[1])
        risk_metric = np.zeros(ports_rt.shape[1])
        avg_ret = np.zeros(ports_rt.shape[1])
        for i in range(ports_rt.shape[1]):
            rets = np.sum(ports_rt[:,i,:]*ports_ind, axis=1)
            fwd_rets = np.sum(rets) - np.array([0]+list(np.cumsum(rets)[:-1]))
            acum_savings[i] = np.sum(self.contrib*np.exp(fwd_rets))
            risk_metric[i] = risk_fun(rets)
            avg_ret[i] = np.log(acum_savings[i]/self.contrib[0])/ports_rt.shape[0]
        return dict(years_per_port=years_per_port, ports_ind=ports_ind, acum_savings=acum_savings, avg_ret=avg_ret, risk_metric=risk_metric)

    def wealth_score_fun(self, params, time_props, ports_rt, util_fun):
        cum_dist = beta.cdf(time_props, params[0], params[1])
        port_props = np.array([cum_dist[0]] + list(np.diff(cum_dist)))
        n_times=ports_rt.shape[0]
        years_per_port = np.rint(port_props*n_times)
        ports_ind = ports_onehot(n_times=n_times, years_per_port=np.round(years_per_port))
        acum_savings = np.zeros(ports_rt.shape[1])
        for i in range(ports_rt.shape[1]):
            rets = np.sum(ports_rt[:,i,:]*ports_ind, axis=1)
            fwd_rets = np.sum(rets) - np.array([0]+list(np.cumsum(rets)[:-1]))
            acum_savings[i] = np.sum(self.contrib*np.exp(fwd_rets))
        return(util_fun(acum_savings))

    def wealth_score_fun2(self, params, time_props, ports_rt, risk_fun=np.var, alpha=1.5):
        cum_dist = beta.cdf(time_props, params[0], params[1])
        port_props = np.array([cum_dist[0]] + list(np.diff(cum_dist)))
        n_times=ports_rt.shape[0]
        years_per_port = np.rint(port_props*n_times)
        ports_ind = ports_onehot(n_times=n_times, years_per_port=np.round(years_per_port))
        acum_savings = np.zeros(ports_rt.shape[1])
        var = np.zeros(ports_rt.shape[1])
        for i in range(ports_rt.shape[1]):
            rets = np.sum(ports_rt[:,i,:]*ports_ind, axis=1)
            fwd_rets = np.sum(rets) - np.array([0]+list(np.cumsum(rets)[:-1]))
            acum_savings[i] = np.sum(self.contrib*np.exp(fwd_rets))
            var[i] = risk_fun(rets)
        return(-np.mean(np.log(acum_savings[i]/self.contrib[0])/ports_rt.shape[0]-alpha*var))

    def rr_score_fun(self, params, time_props, ports_rt, annuity_pr,target_wage, conf=0.9):
        cum_dist = beta.cdf(time_props, params[0], params[1])
        port_props = np.array([cum_dist[0]] + list(np.diff(cum_dist)))
        n_times=ports_rt.shape[0]
        years_per_port = np.rint(port_props*n_times)
        ports_ind = ports_onehot(n_times=n_times, years_per_port=np.round(years_per_port))
        acum_savings = np.zeros(ports_rt.shape[1])
        for i in range(ports_rt.shape[1]):
            rets = np.sum(ports_rt[:,i,:]*ports_ind, axis=1)
            fwd_rets = np.sum(rets) - np.array([0]+list(np.cumsum(rets)[:-1]))
            acum_savings[i] = np.sum(self.contrib*np.exp(fwd_rets))
            replace_rate_dist = acum_savings*annuity_pr/target_wage
            min_rr = np.quantile(replace_rate_dist, 1-conf)
        return(-min_rr)

    def rr_deoptim(self, ports_rt, annuity_pr, target_wage, conf=0.9, beta_par_bnds=(0,5), popsize=50):
        bnds = (beta_par_bnds, beta_par_bnds)
        n_ports = ports_rt.shape[2]
        time_props = (np.arange(n_ports+1)/n_ports)[1:]
        sol = de(self.rr_score_fun, bounds=bnds, popsize=popsize, strategy='best1bin', args=(time_props, ports_rt, annuity_pr,target_wage, conf))
        lp_summ = self.rr_glidepath_summary(sol.x, ports_rt, annuity_pr,target_wage, conf)
        return sol.x, lp_summ

    def wealth_deoptim(self, ports_rt, alpha=1.5, util_type='exp', beta_par_bnds=(0,5), popsize=50, risk_fun=np.var):
        '''
        util_type: if mdd risk penalized by risk function for each trayectory, else utility function over wealth at horizon.
        '''
        bnds = (beta_par_bnds, beta_par_bnds)
        n_ports = ports_rt.shape[2]
        time_props = (np.arange(n_ports+1)/n_ports)[1:]
        if util_type != 'mdd':
            if util_type[:3]=='exp':
                util_fun = lambda x: np.mean(np.exp(-alpha*x))
            elif util_type=='mv':
                util_fun = lambda x: -np.mean(x/self.contrib[0])+alpha*np.var(x/self.contrib[0])
            else:
                util_fun = lambda x: -np.mean((np.power(x, 1 - alpha)-1)/(1 - alpha))
            sol = de(self.wealth_score_fun, bounds=bnds, popsize=popsize, strategy='best1bin', args=(time_props, ports_rt, util_fun))
        else:
            sol = de(self.wealth_score_fun2, bounds=bnds, popsize=popsize, strategy='best1bin', args=(time_props, ports_rt, risk_fun, alpha))
        lp_summ = self.wealth_glidepath_summary(sol.x, ports_rt, risk_fun=risk_fun)
        return sol.x, lp_summ

    def rr_hyperoptim(self, ports_rt, annuity_pr, target_wage, conf=0.9, beta_par_bnds=(0,5), max_evals=50, par_interv=0.1):
        n_ports = ports_rt.shape[2]
        time_props = (np.arange(n_ports+1)/n_ports)[1:]
        from hyperopt import hp, tpe, fmin, Trials
        tpe_algo = tpe.suggest
        tpe_trials = Trials()
        par_range = tuple(np.arange(beta_par_bnds[0],beta_par_bnds[1],par_interv))
        space = [hp.choice('x', par_range),hp.choice('y', par_range)]
        tpe_best = fmin(fn=lambda x: self.rr_score_fun(x, time_props, ports_rt, annuity_pr,target_wage, conf), space=space,algo=tpe_algo, trials=tpe_trials, max_evals=max_evals)
        solx = [par_range[tpe_best['x']], par_range[tpe_best['y']]]
        lp_summ = self.rr_glidepath_summary(solx, ports_rt, annuity_pr,target_wage, conf)
        return solx, lp_summ

    def wealth_hyperoptim(self, ports_rt, alpha=1.5, util_type='exp', beta_par_bnds=(0,5), max_evals=50, par_interv=0.1, risk_fun=np.var):
        '''
        util_type: if mdd risk penalized by risk function for each trayectory, else utility function over wealth at horizon.
        '''
        n_ports = ports_rt.shape[2]
        time_props = (np.arange(n_ports+1)/n_ports)[1:]
        from hyperopt import hp, tpe, fmin, Trials
        tpe_algo = tpe.suggest
        tpe_trials = Trials()
        par_range = tuple(np.arange(beta_par_bnds[0],beta_par_bnds[1],par_interv))
        space = [hp.choice('x', par_range),hp.choice('y', par_range)]
        if util_type != 'mdd':
            if util_type[:3]=='exp':
                util_fun = lambda x: np.mean(np.exp(-alpha*x))
            elif util_type=='mv':
                util_fun = lambda x: -np.mean(x/self.contrib[0])+alpha*np.var(x/self.contrib[0])
            else:
                util_fun = lambda x: -np.mean((np.power(x, 1 - alpha)-1)/(1 - alpha))
            tpe_best = fmin(fn=lambda x: self.wealth_score_fun(x, time_props, ports_rt, util_fun), space=space,algo=tpe_algo, trials=tpe_trials, max_evals=max_evals)
        else:
            tpe_best = fmin(fn=lambda x: self.wealth_score_fun2(x, time_props, ports_rt, risk_fun, alpha), space=space,algo=tpe_algo, trials=tpe_trials, max_evals=max_evals)
        solx = [par_range[tpe_best['x']], par_range[tpe_best['y']]]
        lp_summ = self.wealth_glidepath_summary(solx, ports_rt, risk_fun=risk_fun)
        return solx, lp_summ

    def rr_bayesopt(self, ports_rt, annuity_pr, target_wage, conf=0.9, beta_par_bnds=[(0,5),(0,5)], n_iter=50, init_points=5):
        n_ports = ports_rt.shape[2]
        time_props = (np.arange(n_ports+1)/n_ports)[1:]
        from bayes_opt import BayesianOptimization as bo
        pbounds = {'x': beta_par_bnds[0], 'y': beta_par_bnds[1]}
        optimizer = bo(lambda x,y:-self.rr_score_fun([x,y], time_props, ports_rt, annuity_pr,target_wage, conf), pbounds)
        optimizer.maximize(init_points=init_points, n_iter=n_iter)
        params = optimizer.max['params']
        solx = [params['x'], params['y']]
        lp_summ = self.rr_glidepath_summary(solx, ports_rt, annuity_pr,target_wage, conf)
        return solx, lp_summ

    def wealth_bayesopt(self, ports_rt, alpha=1.5, util_type='exp', beta_par_bnds=[(0,5),(0,5)], n_iter=50, init_points=5, risk_fun=np.var):
        '''
        util_type: if mdd risk penalized by risk function for each trayectory, else utility function over wealth at horizon.
        '''
        n_ports = ports_rt.shape[2]
        time_props = (np.arange(n_ports+1)/n_ports)[1:]
        from bayes_opt import BayesianOptimization as bo
        pbounds = {'x': beta_par_bnds[0], 'y': beta_par_bnds[1]}
        if util_type != 'mdd':
            if util_type[:3]=='exp':
                util_fun = lambda x: np.mean(-np.exp(-alpha*x))
            elif util_type=='mv':
                util_fun = lambda x: np.mean(x/self.contrib[0])-alpha*np.var(x/self.contrib[0])
            else:
                util_fun = lambda x: -np.mean((np.power(x, 1 - alpha)-1)/(1 - alpha))
            optimizer = bo(lambda x,y:self.wealth_score_fun([x,y], time_props, ports_rt, util_fun), pbounds)
        else:
            optimizer = bo(lambda x,y:-self.wealth_score_fun2([x,y], time_props, ports_rt, risk_fun, alpha), pbounds)
        optimizer.maximize(init_points=init_points, n_iter=n_iter)
        params = optimizer.max['params']
        solx = [params['x'], params['y']]
        lp_summ = self.wealth_glidepath_summary(solx, ports_rt, risk_fun=risk_fun)
        return solx, lp_summ



class simul(object):
    def __init__(self):
        '''
        Simulation
        '''

    def varsim(self, coefs, intercept, sig_u, steps=100, initvalues=None, seed=None):
        """
        Simulate VAR(p) process, given coefficients and assuming Gaussian noise
        Parameters
        ----------
        coefs : ndarray
            Coefficients for the VAR lags of endog.
        intercept : None or ndarray 1-D (neqs,) or (steps, neqs)
            This can be either the intercept for each equation or an offset.
            If None, then the VAR process has a zero intercept.
            If intercept is 1-D, then the same (endog specific) intercept is added
            to all observations.
            If intercept is 2-D, then it is treated as an offset and is added as
            an observation specific intercept to the autoregression. In this case,
            the intercept/offset should have same number of rows as steps, and the
            same number of columns as endogenous variables (neqs).
        sig_u : ndarray
            Covariance matrix of the residuals or innovations.
            If sig_u is None, then an identity matrix is used.
        steps : None or int
            number of observations to simulate, this includes the initial
            observations to start the autoregressive process.
            If offset is not None, then exog of the model are used if they were
            provided in the model
        seed : None or integer
            If seed is not None, then it will be used with for the random
            variables generated by numpy.random.
        Returns
        -------
        endog_simulated : nd_array
            Endog of the simulated VAR process
        """
        rs = np.random.RandomState(seed=seed)
        rmvnorm = rs.multivariate_normal
        p, k, k = coefs.shape
        if sig_u is None:
            sig_u = np.eye(k)
        ugen = rmvnorm(np.zeros(len(sig_u)), sig_u, steps)
        result = np.zeros((steps, k))
        if intercept is not None:
            # intercept can be 2-D like an offset variable
            if np.ndim(intercept) > 1:
                if not len(intercept) == len(ugen):
                    raise ValueError('2-D intercept needs to have length `steps`')
            # add intercept/offset also to intial values
            result += intercept
            result[0:p] = self.returns.values[-p:]
            result[p:] += ugen[p:]
        else:
            result[p:] = ugen[p:]

        # add in AR terms
        for t in range(p, steps):
            ygen = result[t]
            for j in range(p):
                ygen += np.dot(coefs[j], result[t-j-1])
        return result

    def simulate_var(self, var_results, steps=None, offset=None, seed=None):
        """
        simulate the VAR(p) process for the desired number of steps
        Parameters
        ----------
        steps : None or int
            number of observations to simulate, this includes the initial
            observations to start the autoregressive process.
            If offset is not None, then exog of the model are used if they were
            provided in the model
        offset : None or ndarray (steps, neqs)
            If not None, then offset is added as an observation specific
            intercept to the autoregression. If it is None and either trend
            (including intercept) or exog were used in the VAR model, then
            the linear predictor of those components will be used as offset.
            This should have the same number of rows as steps, and the same
            number of columns as endogenous variables (neqs).
        seed : None or integer
            If seed is not None, then it will be used with for the random
            variables generated by numpy.random.
        Returns
        -------
        endog_simulated : nd_array
            Endog of the simulated VAR process
        """
        steps_ = None
        if offset is None:
            if var_results.k_exog_user > 0 or var_results.k_trend > 1:
                # if more than intercept
                # endog_lagged contains all regressors, trend, exog_user
                # and lagged endog, trimmed initial observations
                offset = var_results.endog_lagged[:,:var_results.k_exog].dot(
                                                     var_results.coefs_exog.T)
                steps_ = var_results.endog_lagged.shape[0]
            else:
                offset = var_results.intercept
        else:
            steps_ = offset.shape[0]

        # default, but over written if exog or offset are used
        if steps is None:
            if steps_ is None:
                steps = 1000
            else:
                steps = steps_
        else:
            if steps_ is not None and steps != steps_:
                raise ValueError('if exog or offset are used, then steps must'
                                 'be equal to their length or None')
        y = self.varsim(var_results.coefs, offset, var_results.sigma_u, steps=steps, seed=seed)
        return y

    def var_simul(self, M = 1e4, max_lags = 4, policy_date = None):
        '''
        period: returns period,
        M: Number of sample trajectories,
        N: Number of steps ahead.
        '''
        N = self.N

        if policy_date is None:
            model = VAR(self.returns)
        else:
            model = VAR(self.returns[self.ini_date:policy_date])
        results = model.fit(max_lags)
        self.lags = results.k_ar
        rets_simul = np.array(list(map(lambda x: self.simulate_var(results, x), [int(N) + results.k_ar]*int(M))))
        rets_simul_out = rets_simul[:,-N:,:]
        rets_simul_dec_per = np.zeros((int(M), len(self.dec_pers), self.n_assets), np.float64)
        for i in range(len(self.dec_pers)):
            dec_i = self.dec_pers[i]
            rets_simul_dec_per[:,i,:] = np.prod(1 + rets_simul_out[:, (dec_i - self.per*self.dec_per_in_years):dec_i, :], axis = 1)
        return({'per':rets_simul_out, 'dec_per':rets_simul_dec_per})

    def var_simul_simple(self, M = 1e4, N = 10, max_lags = 4):
        '''
        period: returns period,
        M: Number of sample trajectories,
        N: Number of steps ahead.
        '''
        model = VAR(self.returns)
        results = model.fit(max_lags, ic = "aic")
        rets_simul = np.zeros((int(M), int(N), self.n), np.float64)
        for i in range(int(M)):
            rets_simul[i] = results.simulate_var(int(N))
        return(rets_simul)

    def sm_var_simul(self, M = 1e4, max_lags = 4, policy_date = None):
        '''
        var_simul usanado stats model
        period: returns period,
        M: Number of sample trajectories,
        N: Number of steps ahead.
        '''
        N = self.N
        if policy_date is None:
            model = VAR(self.returns)
        else:
            model = VAR(self.returns[self.ini_date:policy_date])
        results = model.fit(max_lags, ic = "aic")
        self.lags = results.k_ar
        rets_simul = np.array(list(map(results.simulate_var, [int(N) + results.k_ar]*int(M))))
        rets_simul_out = rets_simul[:,-N:,:]
        rets_simul_dec_per = np.zeros((int(M), len(self.dec_pers), self.n_assets), np.float64)
        for i in range(len(self.dec_pers)):
            dec_i = self.dec_pers[i]
            rets_simul_dec_per[:,i,:] = np.prod(1 + rets_simul_out[:, (dec_i - self.per):dec_i, :], axis = 1)
        return({'per':rets_simul_out, 'dec_per':rets_simul_dec_per})
