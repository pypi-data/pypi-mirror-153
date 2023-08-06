import numpy as np
import pandas as pd
import datetime as dt
from .utils import graph_plot
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn import cluster, covariance, manifold
import matplotlib.pylab as pl
from .preprocess_dataset import series_sync, series_normalize, series_merge
from PyCondorInvestmentAnalytics.returns import assets as ac
from PyCondorInvestmentAnalytics.utils import returns
from PyCondorInvestmentAnalytics.risks import series_drawdown
from PyCondorInvestmentAnalytics.optim import portfolio_optim as opt
from scipy.cluster import hierarchy as hc
from scipy.cluster.hierarchy import fcluster
from PyCondorInvestmentAnalytics.factors import factors
from dtaidistance import dtw

class fund_selection:
	def __init__(self, series_dict, asset_data, funds_df, groups_df, ref_curr="USD", key=None, values=[], period="monthly", ignore=None):
		self.funds_df = funds_df.copy()
		if ignore is not None:
			is_valid = [np.any(funds_df.index==x) for x in ignore]
			self.funds_df.drop(np.array(ignore)[is_valid], inplace=True)
		self.series_dict = series_dict
		self.groups_df = groups_df
		self.features = funds_df.columns
		self.key = key
		self.values = values
		self.rets_period = period
		self.freq = dict(monthly=12, quarterly=4, yearly=1, daily=252).get(period, 252)

		if key is not None:
			if not np.any(self.features==key):
		 		raise ValueError('Feature not in table')
		if key is not None and len(values)>0:
			self.names = []
			for value in values:
				self.names = self.names + list(self.funds_df[self.funds_df[key]==value].index)
		else:
			self.names = list(funds_df.index)
		self.n_funds = len(self.names)
		if groups_df is not None:
			groups_df = groups_df[[np.any(self.funds_df.loc[self.names][x.Key].values==x.Value) for _,x in groups_df.iterrows()]]
			n_cons = groups_df.shape[0]
			if n_cons > 0:
				self.linCons = np.zeros((n_cons, len(self.names)))
				self.consUB = np.zeros(n_cons)
				self.consLB = np.zeros(n_cons)
				for i in range(n_cons):
				    self.linCons[i,(funds_df.loc[self.names][groups_df.Key.values[i]]==groups_df.Value.values[i]).values] = 1
				    self.consLB[i] = groups_df.Min.values[i]
				    self.consUB[i] = groups_df.Max.values[i]
				if np.sum(self.consUB)<1:
					self.consUB = self.consUB/np.sum(self.consUB)
			else:
				self.linCons, self.consLB, self.consUB = None, None, None
		else:
			self.linCons, self.consLB, self.consUB = None, None, None

		self.series_dates = pd.DataFrame([[dt.datetime.strftime(series_dict[x].index[0], "%Y-%m-%d"), dt.datetime.strftime(series_dict[x].index[-1], "%Y-%m-%d")] for x in asset_data['TickerBenchmark'][self.names].values], index=asset_data['TickerBenchmark'][self.names].index, columns=["Start", "End"])

		self.series = series_sync(series_dict, asset_data, self.names, ref_curr=ref_curr, dates=None, currencies=[], convert_to_ref=True, invest_assets=None, ref_per_unit_foreign = False)
		self.series_norm = series_normalize(self.series)
		self.returns = returns(self.series, self.rets_period)
		self.assets = ac(self.series, rets_period = self.rets_period, returns=False)
		self.cluster_df = None

	def rets_summary(self, sort_var='Regret', top=None, dd_hor="12M", names=None, box_plot=False, regret_period=None, regret_norm=True, include=[]):
		if names is None:
			returns_temp = self.returns
			series_temp = self.series
			regret_vals = self.regret(period=regret_period, norm=regret_norm).values
		else:
			sum_df = 100*self.returns[names].describe().iloc[1:,:]
			series_temp = self.series[names]
			returns_temp = self.returns[names]
			regret_vals = self.regret(period=regret_period, norm=regret_norm).loc[names].values
		sum_df = 100*returns_temp.describe().iloc[1:,:]
		sharpe = sum_df.loc["mean"].values/sum_df.loc["std"].values
		sum_df.loc["mean"] = sum_df.loc["mean"]*self.freq
		sum_df.loc["std"] = sum_df.loc["std"]*np.sqrt(self.freq)
		dds, dds_t = [], []
		sum_df = sum_df.T
		for i in range(series_temp.shape[1]):
			_, _, _, _, _, max_dd_obs, _, _, t_dd_obs = series_drawdown(series_temp.iloc[:,i], horizon=dd_hor, quant=0.9, type="arit")
			dds.append(max_dd_obs*100)
			dds_t.append(t_dd_obs)
		sum_df['Sharpe'] = sharpe
		sum_df["Drawdown"] = dds
		sum_df["TTR"] = dds_t
		sum_df["Regret"] = regret_vals
		if len(include)>0:
			for x in include:
				sum_df[x] = self.funds_df[x].loc[sum_df.index]
		if sort_var is not None:
			sum_df = sum_df.sort_values(by=sort_var, ascending=False)
		if top is not None:
			sum_df = sum_df.iloc[:top, :]
		sum_df.columns = ["Retorno Promedio Anual.", "Volatilidad Anual.", "Min.", "25%", "50%", "75%", "Max", "Sharpe", "Drawdown", "TTR", "Regret"] + include
		if box_plot:
			bp = self.returns[sum_df.index].boxplot(rot=90, return_type="both")
		return sum_df

	def clustering(self, use_pca=True, use_corr=False, orientation="right", ncluster=None, add_label=None, plot=True):
		rets_temp = self.returns.copy()
		if add_label is not None:
			rets_temp.columns = [x+" ("+self.funds_df.loc[x][add_label]+")"  for x in rets_temp.columns]
		if use_pca:
			from sklearn.decomposition import PCA
			pca = PCA(n_components=3)
			pca.fit(self.returns.T)
			coord =  pca.components_ @ self.returns.values
			z = hc.linkage(coord.T, method='average')
			dendrogram = hc.dendrogram(z, labels=rets_temp.columns, orientation=orientation, color_threshold=0, above_threshold_color="#003c71", no_plot=not plot)
		else:
			if use_corr:
				corr = rets_temp.corr()
				z = hc.linkage(corr.values, method='average')
				dendrogram = hc.dendrogram(z, labels=corr.columns, orientation=orientation, color_threshold=0, above_threshold_color="#003c71", no_plot=not plot)
			else:
				corr = rets_temp.T
				z = hc.linkage(corr.values, method='average')
				dendrogram = hc.dendrogram(z, labels=corr.index, orientation=orientation, color_threshold=0, above_threshold_color="#003c71", no_plot=not plot)

		if ncluster is not None:
			fl = fcluster(z,ncluster,criterion='maxclust')
			self.cluster_df = pd.Series(fl, index=rets_temp.columns)
		else:
			self.cluster_df = None
		return dendrogram


	def factor_clustering(self, series_factors, orientation="right", ncluster=None, add_label=None, plot=True):
		from PyCondorInvestmentAnalytics.factors import factors
		import seaborn as sns
		factor_map = factors(series_factors, self.series, w_asset = None, w_factor = None, rets_period = self.rets_period)
		A = factor_map.asset_to_factor_exp()
		z = hc.linkage(A.values, method='average')
		dendrogram = hc.dendrogram(z, labels=A.index, orientation=orientation, color_threshold=0, above_threshold_color="#003c71", no_plot=not plot)
		if ncluster is not None:
			fl = fcluster(z,ncluster,criterion='maxclust')
			self.cluster_df = pd.Series(fl, index=A.index)
		else:
			self.cluster_df = None
		return dendrogram, A

	def graph_clustering(self, plot=True):
	    # Graphical structure from the correlations
	    # Graphical Lasso for precision matrix
	    edge_model = covariance.GraphicalLassoCV(max_iter=1000)
	    # Normalize:
	    X_std = self.returns / self.returns.std(axis=0)
	    edge_model.fit(X_std)
	    # Cluster using affinity propagation
	    _, labels = cluster.affinity_propagation(edge_model.covariance_)
	    n_labels = labels.max()
	    for i in range(n_labels + 1):
	        print('Cluster %i: %s' % ((i + 1), ', '.join(np.array(self.names)[labels == i])))
	    self.cluster_df = pd.Series(labels, index=X_std.columns)

	    plot_config = None
	    if plot:
	        node_position_model = manifold.MDS(n_components=2, random_state=0)
	        embedding = node_position_model.fit_transform(X_std.T).T
	        color_list = pl.cm.jet(np.linspace(0,1,n_labels+1))
	        my_colors = [color_list[i] for i in labels]

	        # Partial correlations
	        partial_correlations = edge_model.precision_.copy()
	        d = 1 / np.sqrt(np.diag(partial_correlations))
	        partial_correlations *= d
	        partial_correlations *= d[:, np.newaxis]
	        non_zero = (np.abs(np.triu(partial_correlations, k=1)) > 0.02)

	        # Compute the edge values based on the partial correlations
	        values = np.abs(partial_correlations[non_zero])
	        val_max = values.max()

	        # Display the partial correlation graph
	        title = 'Graphical Network (%s / %s)' % (dt.datetime.strftime(self.series.index[0], "%Y-%m-%d"), dt.datetime.strftime(self.series.index[-1], "%Y-%m-%d"))
	        graph_plot(d, partial_correlations, my_colors,self.names, labels, embedding, val_max, title)
	        # The configuration of the plot
	        plot_config = [d, partial_correlations, my_colors, self.names, labels, embedding, val_max, title]
	    return [edge_model.covariance_, edge_model.precision_], plot_config


	def select(self, cluster_strategy, criteria="Regret", top_per_cluster=1, dd_hor="12M", required=None, ncluster=None, key=None, series_factors=None, funds_sel_every=None, include=None):
		'''
		cluster_strategy:
			performance
			qualitative
			factors
			graph
		'''
		n_req = 0 if required is None else len(required)
		if cluster_strategy[:3]=='per':
			if ncluster is None:
				raise ValueError('ncluster required.')
			_ = self.clustering(use_pca=True, ncluster=ncluster-n_req, add_label=None, plot=False)
		elif cluster_strategy[:3]=='qua':
			if key is None:
				raise ValueError('key required.')
			self.cluster_df = self.funds_df[key]
		elif cluster_strategy[:3]=='fac':
			if ncluster is None or series_factors is None:
				raise ValueError('ncluster and series_factors required.')
			_ = self.factor_clustering(series_factors=series_factors, ncluster=ncluster-n_req, add_label=None, plot=False)
		elif cluster_strategy[:3]=='gra':
			_, _ = self.graph_clustering(plot=False)

		cluster_temp = self.cluster_df if required is None else self.cluster_df.drop(required)
		sel_funds_df = None if required is None else self.rets_summary(sort_var=None, top=None, dd_hor=dd_hor, names=required, box_plot=False)
		for i in np.unique(cluster_temp.values):
			names = np.array(cluster_temp.loc[cluster_temp.values==i].index)
			if len(names)>0:
				top_per_cluster= top_per_cluster if funds_sel_every is None else np.max([int(top_per_cluster*len(names)/funds_sel_every),1])
				sel_fund = self.rets_summary(sort_var=criteria, top=top_per_cluster, dd_hor=dd_hor, names=names, box_plot=False, include=include)
				include_sel_fund = sel_fund.Sharpe.values > 0
				if np.any(include_sel_fund):
					sel_funds_df = pd.concat([sel_funds_df, sel_fund.loc[include_sel_fund]], axis=0)
		return sel_funds_df

	def optim_port(self, risk_obj, type="relative", bench_ts=None, M=1000, lb_val=0.1, ub_val=1, use_lc=True, plot_port=True, resamp=True, selected_funds=None, ref_date=None, port_label="Portafolio"):
		if (type[:3]=="rel" and (risk_obj is None or bench_ts is None)) or (type[:3]=="abs" and risk_obj is None or bench_ts is None):
			raise ValueError('Not enough parameters for optimization. Please check.')
		series_temp = self.series if selected_funds is None else self.series[selected_funds]
		if bench_ts is not None:
			bench_name = bench_ts.columns[0]
			ser_merge_all, _ = series_merge([bench_ts, series_temp])
			assets_all = ac(ser_merge_all.dropna(), rets_period = self.rets_period, returns=False)
			if ref_date is not None:
				ser_merge, _ = series_merge([bench_ts, series_temp[series_temp.index<=ref_date]])
				assets = ac(ser_merge.dropna(), rets_period = self.rets_period, returns=False)
			else:
				assets = assets_all
			w_bench = pd.Series([1], index=[bench_name])
			bench_series, port_tr = assets_all.portfolio_backtest(w_bench)
			bench_risk, bench_vol = assets.portfolio_risk(w_bench)
			bench_risk = bench_risk.rename(bench_name)
		else:
			bench_risk, bench_series = None, None
			assets_all = ac(series_temp, rets_period = self.rets_period, returns=False)
			if ref_date is not None:
				assets = ac(series_temp[series_temp.index<=ref_date], rets_period = self.rets_period, returns=False)
			else:
				assets = assets_all
		if risk_obj is None and type[:3]=="abs":
			risk_obj = bench_vol

		if use_lc:
			if selected_funds is None:
				linCons_temp, consLB_temp, consUB_temp = self.linCons, self.consLB, self.consUB
			else:
				linCons_temp, consLB_temp, consUB_temp = self.linCons[:, [self.names.index(x) for x in selected_funds]], self.consLB, self.consUB
				pos_valid = np.any(linCons_temp!=0, axis=1)
				linCons_temp = linCons_temp[pos_valid,:]
				consLB_temp = consLB_temp[pos_valid]
				consUB_temp = consUB_temp[pos_valid]
		else:
			linCons_temp, consLB_temp, consUB_temp = None, None, None

		if type[:3]=="rel":
			opt_te = opt(assets.series, period=self.rets_period, asset_names=self.names if selected_funds is None else selected_funds, mu=None, ra_coef=0, type = type, risk_obj=risk_obj, w_bench = w_bench, lb=[lb_val], ub=[ub_val], linCons=linCons_temp, consLB=consLB_temp, consUB=consUB_temp)
			if resamp:
				port_resamp_te = opt_te.portfolio_resamp(N=200, M=M, mom=False, k = None, sample_window=False, len_window=36, dyn_mu=True, q_sel=0.2, conf_int = 0.9)
				port_opt = port_resamp_te['w_optim_resamp'].drop(bench_name).rename(port_label)
			else:
				port_opt, _ = opt_te.minimize_util()
				port_opt = port_opt.drop(bench_name).rename(port_label)
			port_opt_series, _ = assets_all.portfolio_backtest(port_opt)
			port_opt_risk, _ = assets.portfolio_risk(port_opt)
			port_opt_risk = port_opt_risk.rename(port_label)
		else:
			opt_tr = opt(assets.series, period=self.rets_period, asset_names=self.names if selected_funds is None else selected_funds, mu=None, ra_coef=0, type = "absolute", risk_obj=risk_obj, w_bench = None, lb=[lb_val], ub=[ub_val], linCons=linCons_temp, consLB=consLB_temp, consUB=consUB_temp)
			if resamp:
				port_resamp_tr = opt_tr.portfolio_resamp(N=200, M=M, mom=False, k = None, sample_window=False, len_window=36, dyn_mu=True, q_sel=0.2, conf_int = 0.9)
				port_opt = port_resamp_tr['w_optim_resamp'].rename("Target Risk")
			else:
				port_opt, _ = opt_tr.minimize_util()
				port_opt = port_opt.rename("Target Risk")
			port_opt_series, _ = assets_all.portfolio_backtest(port_opt)
			port_opt_risk, _ = assets.portfolio_risk(port_opt)
			port_opt_risk = port_opt_risk.rename("Target Risk")

		port_risk = pd.concat([bench_risk, port_opt_risk], axis=1) if bench_risk is not None else port_opt_risk
		if plot_port:
			(100*port_opt.sort_values()).plot.barh(color="#768692")
		return port_opt, port_risk, port_opt_series, bench_series

	def group_by(self, port, key):
		group_df = pd.concat([self.funds_df.loc[port.index][key].to_frame(key), port.to_frame('Peso')], axis=1, sort=False).groupby(key).sum()
		return group_df

	def regret(self, period=None, norm=True):
		exp_weights = pd.Series(np.zeros(self.n_funds), index=self.names)
		if period is not None:
			rets = returns(self.series, period)
		else:
			rets = self.returns
		n_rets = rets.shape[0]
		max_rets = rets.max(axis=1)
		for i in range(self.n_funds):
			fund_i = self.names[i]
			se = np.abs(rets[fund_i] - max_rets)
			cum_se = np.cumsum(se)
			nu = np.sqrt(8*np.log(self.n_funds)/n_rets)
			exp_weights[fund_i] = np.exp(-nu*cum_se[-1])
		w = exp_weights/exp_weights.sum() if norm else exp_weights
		return(w)
