
import operator
import datetime
import pandas as pd
import numpy as np
import joblib
from tpot import TPOTRegressor, TPOTClassifier
from xgboost import XGBRegressor, XGBClassifier
import torch
from sklearn.model_selection import RandomizedSearchCV, cross_val_score
from hyperopt import tpe, fmin, hp, space_eval, SparkTrials, atpe
import hyperopt

class Raven():

    def __init__(self, checkpoint_folder, target_ticker, target_df = None, s3client = None, db = None, raven_path = None, problem_type='regression', scoring='neg_mean_absolute_error', cv=5,
                 model_vars = None, ticker_campo = None, bucket = None, file_name = None, denoise = False):

        """
        Finds best pipeline using TPOT for regression and classification problems. Best pipeline is further optimized using hyperopt's tree parzen estimator.
        Performs variable selection using XGBoost's feature_importance method and PCA percentage cutoff method concept.
        Parameters
        -- raven_path - path to PyCondorAnalytics package
        -- db - database class with connection to raven_db
        -- checkpoint_folder - folder where TPOT's best pipelines and checkpoints are saved
        -- s3client - s3client
        -- target_ticker - dict:
            -- key: target_ticker to be optimized, for example, FACCRECGLOB Index | PX_LAST
            -- values: list: [transformation to be applied to target_variable, output_type for target_variable, last date for train_data (from this date
                            forward = test_data), True to apply jurik transform, True to shuffle train_set, True to lag target_variable]
                for example: {'FACCRECGLOB Index | PX_LAST': ['pct_change', 'mean', '2015-12-31', True, False, True]}
                This would create a regression problem for the FACCRECGLOB Index | PX_LAST, where the output transfomation is transformed by a pct_change calculation
                and a jurik_mean on the simple_mean (length to be decided on search_pipeline method). Train data will not be shuffled and target_variable will be lagged as well.
                Best model will be chosen based on self.cv neg_mean_absolute_error.
        -- problem_type - 'regression' or 'classification'
        -- scoring - sklearn's scoring metric. Metrics must be -higher_is_better-
        -- cv - number of folds for cv
        """

        if raven_path is not None:
            import sys
            sys.path.append(raven_path)

        from PyCondorRaven.preprocess_dataset import dataset
        from PyCondorRaven.utils import jurik

        self.db = db
        self.checkpoint_folder = checkpoint_folder
        self.target_ticker = target_ticker
        self.problem_type = problem_type
        self.scoring = scoring
        self.cv = cv
        self.dataset = dataset
        self.jurik = jurik
        self.target_df = target_df
        self.s3client = s3client
        self.model_vars = model_vars
        self.ticker_campo = ticker_campo
        self.bucket = bucket
        self.file_name = file_name
        self.denoise = denoise
        self.denoise_cols = None # Fix this!

    def calculate_feature_importances(self, dataframe, n_iter = 50):

        """
        Calculates feature importances using XGBoost's feature_importances_ method.
        - Parameters
        -- dataframe - pandas dataframe in which first column = target
        -- n_iter - number of iterations to perform on RandomizedSearchCV
        - Returns
        -- Pandas Series
        """

        use_gpu = torch.cuda.is_available()

        params = {'n_estimators': np.arange(50, 500, 50), 'eta': np.arange(0.01, 0.96, 0.1), 'max_depth': np.arange(1, 11, 1),
                 'min_child_weight': np.arange(1, 20, 1)}
        if self.problem_type == 'regression':
            estimator = XGBRegressor(n_jobs=-1 if not use_gpu else 1, tree_method = 'gpu_hist' if use_gpu else 'hist')
            selector = RandomizedSearchCV(estimator, params, random_state = 0, scoring = self.scoring, n_iter = n_iter, cv = self.cv)
            search = selector.fit(dataframe.iloc[:, 1:], dataframe.iloc[:, 0])
            estimator = estimator.set_params(**search.best_params_)
            estimator.fit(dataframe.iloc[:, 1:], dataframe.iloc[:, 0])
        else:
            estimator = XGBClassifier(n_jobs=-1 if not use_gpu else 1, tree_method = 'gpu_hist' if use_gpu else 'hist')
            selector = RandomizedSearchCV(estimator, params, random_state = 0, scoring = self.scoring, n_iter = n_iter, cv = self.cv)
            search = selector.fit(dataframe.iloc[:, 1:], dataframe.iloc[:, 0])
            estimator = estimator.set_params(**search.best_params_)
            estimator.fit(dataframe.iloc[:, 1:], dataframe.iloc[:, 0])

        feature_importances = pd.Series(data = estimator.feature_importances_, index = dataframe.columns[1:].values.tolist())

        return feature_importances

    def search_pipeline(self, lag_array, forecast_array, n_gen=50, n_pop = 50, use_dask = False, config_dict = None):

        """
        Searches best pipeline using TPOT.
        Parameters
        -- lag_array - numpy array or list containing the number of shifts (backwards) that will be evaluated in the process. This lags all of the variables in the df if not lag_target else all except target
        -- forecast_array - numpy array or list containing the number of shifts (forwards) that will be evaluated in the process (this is for predictions). Shifts only the target variable.
        -- n_gen - generations parameter from TPOT
        -- n_pop - population parameter from TPOT
        -- use_dask - true to use dask and create local cluster
        -- config_dict - tpot config_dict argument
        Returns
        -- cv_scores - dictionary containing the cv scores of the best pipeline per target_ticker, forecast_length and lag_length
        -- models - dictionary containing the best pipelines per target_ticker, forecast_length and lag_length
        """

        if use_dask:
            from dask.distributed import Client
            client = Client()

        cv_scores = {outer_k: {'Forecast: {}'.format(inner_k): dict() for inner_k in forecast_array} for outer_k in list(self.target_ticker.keys())}
        models = {outer_k: {'Forecast: {}'.format(inner_k): dict() for inner_k in forecast_array} for outer_k in list(self.target_ticker.keys())}
        for key, value in self.target_ticker.items():
            for f_length in forecast_array:
                for l_length in lag_array:
                    if self.target_df is None:
                        df, transf = self.db.fetch_target_vars(key, self.s3client, make_transf = True, transf_target = self.target_ticker[key][0],
                                                               model_vars = self.model_vars, ticker_campo = self.ticker_campo, file_name = self.file_name, bucket = self.bucket)
                        df.fillna(method = 'ffill', inplace = True)
                        if self.denoise:
                            df.dropna(inplace = True)
                            for col in self.denoise_cols:
                                df.loc[:, col] = self.jurik(df.loc[:, col].rolling(f_length).mean().dropna())
                        dtst = self.dataset([df])
                    else:
                        temp_df = self.target_df.copy()
                        if self.denoise:
                            temp_df.dropna(inplace = True)
                            for col in self.denoise_cols:
                                temp_df.loc[:, col] = self.jurik(temp_df.loc[:, col].rolling(f_length).mean().dropna())
                        dtst = self.dataset([temp_df])
                
                    df = dtst.shift_dataset(lag = True, forecast = True, nlag = l_length, nforecast = f_length, var_forecast = [key],
                                            var_lags = None if self.target_ticker[key][5] else [x for x in df.columns if x != key],
                                            output_type = self.target_ticker[key][1], dropna = True, drop_var_forecast = False if self.target_ticker[key][5] else True)
                    if not self.denoise:
                        if self.target_ticker[key][3]:
                            df.iloc[:, 0] = self.jurik(df.iloc[:, 0])
                            
                    train_df = df.loc[:self.target_ticker[key][2], :] if not self.target_ticker[key][4] else df.loc[:self.target_ticker[key][2], :].sample(frac=1, random_state = 1)
                    test_df = df.loc[self.target_ticker[key][2]:, :].iloc[1:, :]
                    if self.problem_type == 'regression':
                        tpot_model = TPOTRegressor(cv=self.cv, random_state=42, verbosity=2, scoring=self.scoring,
                                                  periodic_checkpoint_folder = self.checkpoint_folder + key.split(' | ')[0].lower() + '_forecast' + \
                                                  str(f_length) + '_lag' + str(l_length),
                                                  generations = n_gen, population_size = n_pop, config_dict = config_dict,
                                                  n_jobs = 1 if config_dict == 'TPOT cuML' else -1, use_dask = True if use_dask else False)
                    else:
                        tpot_model = TPOTClassifier(cv=self.cv, random_state=42, verbosity=2, scoring=self.scoring,
                                                  periodic_checkpoint_folder = self.checkpoint_folder + key.split(' | ')[0].lower() + '_forecast' + \
                                                  str(f_length) + '_lag' + str(l_length),
                                                  generations = n_gen, population_size = n_pop, config_dict = config_dict,
                                                  n_jobs = 1 if config_dict == 'TPOT cuML' else -1, use_dask = True if use_dask else False)
                    tpot_model.fit(train_df.iloc[:, 1:], train_df.iloc[:, 0])
                    cv_scores[key]['Forecast: {}'.format(str(f_length))]['Lag: {}'.format(str(l_length))] = np.average(cross_val_score(tpot_model.fitted_pipeline_, train_df.iloc[:, 1:],
                                                                                                            train_df.iloc[:, 0], cv = self.cv, scoring = self.scoring))
                    models[key]['Forecast: {}'.format(str(f_length))]['Lag: {}'.format(str(l_length))] = tpot_model.fitted_pipeline_
                    tpot_model.export(self.checkpoint_folder + key.split(' | ')[0].lower() + 'forecast' + str(f_length) + 'lag' + str(l_length) + '.py')

        return cv_scores, models

    def reoptimize_pipeline(self, best_pipelines, scores, max_evals, train_best = False, select_variables = True, use_spark = False):

        """
        Uses hyperopt's tree parze estimator to further optimize pipelines obtained from search_pipeline method.
        - Parameters
        -- best_pipelines - models output from search_pipeline method
        -- scores - scores output from search_pipeline method
        -- max_evals - number of iterations for each model
        -- train_best - True to optimize only the best performing lag for each forecast. False to optimize all lags for each forecast
        -- select_variables - True to perform variable selection
        - Returns
        -- best_pipelines: dict - adjusted optimized pipelines
        -- selected_variables: dict - selected variables for the problem
        -- best_scores: dict - scores
        """

        def objective_function(space, model, x, y, feature_importances):

            from sklearn.model_selection import cross_val_score
            hyperparamspace = self.preprocess_search_space(space, len(x))
            if feature_importances is not None:
                percentage_cutoff = hyperparamspace['select_vars__select_vars']
                selected_vars = list(feature_importances[np.cumsum(feature_importances.sort_values(ascending = False)) / np.sum(feature_importances) < percentage_cutoff].index)
                x = x.loc[:, selected_vars]
                hyperparamspace.pop('select_vars__select_vars', None)
            estimator = model.set_params(**hyperparamspace)
            score = np.average(cross_val_score(estimator, x, y, cv = self.cv, scoring = self.scoring))
            print(score * -1)
            return score * -1

        def deep_search(model, coef_variation, x, y, feature_importances = None):

            from functools import partial

            space = self.generate_search_space(model, coef_variation, select_variables, problem_type = self.problem_type)
            if space:
                fmin_objective = partial(objective_function, model = model, x = x, y = y, feature_importances = feature_importances)
                if use_spark:
                    spark_trials = SparkTrials()
                    best_model = fmin(fmin_objective, space = space, algo = tpe.suggest, max_evals = max_evals, trials = spark_trials)
                else:
                    best_model = fmin(fmin_objective, space = space, algo = tpe.suggest, max_evals = max_evals)
                return hyperopt.space_eval(space, best_model), True
            else:
                return model.get_params(), False

        if train_best:
            scores = {outer_k: {inner_k: max(inner_v.items(), key=operator.itemgetter(1))[0] for inner_k, inner_v in scores[outer_k].items()} for outer_k, v in scores.items()}
            selected_variables = {outer_k: {inner_k: np.nan for inner_k in list(scores[outer_k].keys())} for outer_k, v in scores.items()}
            top_models = {outer_k: {inner_k: np.nan for inner_k in list(scores[outer_k].keys())} for outer_k, v in scores.items()}
            for key1, value1 in scores.items():
                for key2, value2 in value1.items():
                    if self.target_df is None:
                        temp_df, transf = self.db.fetch_target_vars(key1, self.s3client, make_transf = True, transf_target = self.target_ticker[key1][0], model_vars = self.model_vars, ticker_campo = self.ticker_campo,
                                                                    file_name = self.file_name, bucket = self.bucket)
                        temp_df.fillna(method = 'ffill', inplace = True)
                        if self.denoise:
                            temp_df.dropna(inplace = True)
                            for col in self.denoise_cols:
                                temp_df.loc[:, col] = self.jurik(temp_df.loc[:, col].rolling(int(key2.split(': ')[1])).mean().dropna())
                        dtst = self.dataset([temp_df])
                    else:
                        temp_df = self.target_df.copy()
                        if self.denoise:
                            temp_df.dropna(inplace = True)
                            for col in self.denoise_cols:
                                temp_df.loc[:, col] = self.jurik(temp_df.loc[:, col].rolling(int(key2.split(': ')[1])).mean().dropna())
                        dtst = self.dataset([self.target_df])
                    temp_df = dtst.shift_dataset(lag = True, forecast = True, nlag = int(value2.split(': ')[1]), nforecast = int(key2.split(': ')[1]), var_forecast = [key1],
                                                var_lags = None if self.target_ticker[key1][5] else [x for x in temp_df.columns if x != key1],
                                                output_type = self.target_ticker[key1][1], dropna = True, drop_var_forecast = False if self.target_ticker[key1][5] else True)
                    if not self.denoise:
                        if self.target_ticker[key1][3]:
                            temp_df.iloc[:, 0] = self.jurik(temp_df.iloc[:, 0])

                    train_df = temp_df.loc[:self.target_ticker[key1][2], :] if not self.target_ticker[key1][4] else temp_df.loc[:self.target_ticker[key1][2], :].sample(frac=1, random_state = 1)
                    if select_variables:
                        var_importances = self.calculate_feature_importances(train_df)
                    else:
                        var_importances = None
                    x = train_df.iloc[:, 1:]
                    y = train_df.iloc[:, 0]
                    if var_importances is not None:
                        top_models[key1][key2], bool_resp = deep_search(best_pipelines[key1][key2][value2], 0.20, x, y, var_importances)
                    else:
                        top_models[key1][key2], bool_resp = deep_search(best_pipelines[key1][key2][value2], 0.20, x, y)
                    if bool_resp:
                        best_pipelines[key1][key2][value2] = best_pipelines[key1][key2][value2].set_params(**self.preprocess_search_space(top_models[key1][key2], len(x), drop_select_vars = True))
                        if select_variables:
                            selected_variables[key1][key2] = list(var_importances[np.cumsum(var_importances.sort_values(ascending = False)) / np.sum(var_importances) < self.preprocess_search_space(top_models[key1][key2], len(x), drop_select_vars = False)['select_vars__select_vars']].index)
            best_pipelines = {outer_k: {inner_k: best_pipelines[outer_k][inner_k][selected_model] for inner_k, selected_model in scores[outer_k].items()} for outer_k, v in best_pipelines.items()}
            return best_pipelines, selected_variables, scores
        else:
            selected_variables = {outer_k: {inner_k: {inner_inner_k: np.nan for inner_inner_k in scores[outer_k][inner_k]} for inner_k in list(scores[outer_k].keys())} for outer_k, v in scores.items()}
            top_models = {outer_k: {inner_k: {inner_inner_k: np.nan for inner_inner_k in scores[outer_k][inner_k]} for inner_k in list(scores[outer_k].keys())} for outer_k, v in scores.items()}
            for key1, value1 in scores.items():
                for key2, value2 in value1.items():
                    for key3, value3 in value2.items():
                        if self.target_df is None:
                            temp_df, transf = self.db.fetch_target_vars(key1, self.s3client, make_transf = True, transf_target = self.target_ticker[key1][0], model_vars = self.model_vars, ticker_campo = self.ticker_campo,
                                                               file_name = self.file_name, bucket = self.bucket)
                            temp_df.fillna(method = 'ffill', inplace = True)
                            if self.denoise:
                                temp_df.dropna(inplace = True)
                                for col in self.denoise_cols:
                                    temp_df.loc[:, col] = self.jurik(temp_df.loc[:, col].rolling(int(key2.split(': ')[1])).mean().dropna())
                            dtst = self.dataset([temp_df])
                        else:
                            temp_df = self.target_df.copy()
                            if self.denoise:
                                temp_df.dropna(inplace = True)
                                for col in self.denoise_cols:
                                    temp_df.loc[:, col] = self.jurik(temp_df.loc[:, col].rolling(int(key2.split(': ')[1])).mean().dropna())
                            dtst = self.dataset([self.target_df])
                        temp_df = dtst.shift_dataset(lag = True, forecast = True, nlag = int(key3.split(': ')[1]), nforecast = int(key2.split(': ')[1]), var_forecast = [key1],
                                                        var_lags = None if self.target_ticker[key1][5] else [x for x in temp_df.columns if x != key1],
                                                        output_type = self.target_ticker[key1][1], dropna = True, drop_var_forecast = False if self.target_ticker[key1][5] else True)

                        if not self.denoise:
                            if self.target_ticker[key1][3]:
                                temp_df.iloc[:, 0] = self.jurik(temp_df.iloc[:, 0])

                        train_df = temp_df.loc[:self.target_ticker[key1][2], :] if not self.target_ticker[key1][4] else temp_df.loc[:self.target_ticker[key1][2], :].sample(frac=1, random_state = 1)
                        if select_variables:
                            var_importances = self.calculate_feature_importances(train_df)
                        else:
                            var_importances = None
                        x = train_df.iloc[:, 1:]
                        y = train_df.iloc[:, 0]
                        if var_importances is not None:
                            top_models[key1][key2][key3], bool_resp = deep_search(best_pipelines[key1][key2][key3], 0.20, x, y, var_importances)
                        else:
                            top_models[key1][key2][key3], bool_resp = deep_search(best_pipelines[key1][key2][key3], 0.20, x, y)
                        if bool_resp:
                            best_pipelines[key1][key2][key3] = best_pipelines[key1][key2][key3].set_params(**self.preprocess_search_space(top_models[key1][key2][key3], len(x), drop_select_vars = True))
                            if select_variables:
                                selected_variables[key1][key2][key3] = list(var_importances[np.cumsum(var_importances.sort_values(ascending = False)) / np.sum(var_importances) < self.preprocess_search_space(top_models[key1][key2][key3], len(x), drop_select_vars = False)['select_vars__select_vars']].index)
            return best_pipelines, selected_variables, scores

    def generate_search_space(self, pipeline, coef_variation, select_variables, problem_type = 'regression'):

        """
        Returns hyperparameter search space.
        - Parameters
        -- pipeline - TPOT's pipeline
        -- coef_variation - coefficient of variation. Multiplies the mean value of a given hyperparameter to define its standard deviation
        -- select_variables - True to return search space for variable selection
        -- problem_type
        - Returns
        -- search_space
        """

        def search_config(model_type, pipeline_parts):


            if problem_type == 'regression':

                config_dict = [
                    {
                    'type': 'kneighborsregressor',
                    'params': {'n_neighbors': np.nan if 'kneighborsregressor' not in pipeline_parts.keys() else hp.qnormal(model_type + '_n_neighbors', {k.replace('estimator__', ''): v for k, v in pipeline_parts['kneighborsregressor'].get_params().items()}['n_neighbors'],
                                            {k.replace('estimator__', ''): v for k, v in pipeline_parts['kneighborsregressor'].get_params().items()}['n_neighbors'] * coef_variation, 1),
                            'weights': np.nan if 'kneighborsregressor' not in pipeline_parts.keys() else hp.choice(model_type + '_weights', ['distance', 'uniform']),
                            'leaf_size': np.nan if 'kneighborsregressor' not in pipeline_parts.keys() else hp.qnormal(model_type + '_leaf_size', 30, 5, 1),
                            'p': np.nan if 'kneighborsregressor' not in pipeline_parts.keys() else hp.choice(model_type + '_p', [1, 2, 3]),
                            'n_jobs': -1}
                        },
                    #{
                    #'type': 'normalizer',
                    #'params': {'norm': np.nan if 'normalizer' not in pipeline_parts.keys() else hp.choice('nlzr_norm', ['l1', 'l2', 'max'])}
                    #    },
                    {
                    'type': 'randomforestregressor',
                    'params': {
                            'n_estimators': np.nan if 'randomforestregressor' not in pipeline_parts.keys() else hp.quniform(model_type + '_n_estimators', 50, 400, 1),
                            'max_features': np.nan if 'randomforestregressor' not in pipeline_parts.keys() else None if {k.replace('estimator__', ''): v for k, v in pipeline_parts['randomforestregressor'].get_params().items()}['max_features'] == None else \
                                            hp.uniform(model_type + '_max_features', {k.replace('estimator__', ''): v for k, v in pipeline_parts['randomforestregressor'].get_params().items()}['max_features'] - 0.10,
                                            {k.replace('estimator__', ''): v for k, v in pipeline_parts['randomforestregressor'].get_params().items()}['max_features'] + 0.10),
                            'min_samples_split': np.nan if 'randomforestregressor' not in pipeline_parts.keys() else hp.quniform(model_type + '_min_samples_split', 2, 30, 1),
                            'min_samples_leaf': np.nan if 'randomforestregressor' not in pipeline_parts.keys() else hp.quniform(model_type + '_min_samples_leaf', 1, 30, 1),
                            'bootstrap': np.nan if 'randomforestregressor' not in pipeline_parts.keys() else hp.choice(model_type + '_bootstrap', [True, False]),
                            'n_jobs': -1
                        }
                    },
                    {
                    'type': 'elasticnetcv',
                    'params':{
                            'l1_ratio': np.nan if 'elasticnetcv' not in pipeline_parts.keys() else hp.uniform(model_type + '_l1_ratio', 0, 1.01),
                            'max_iter': 10000,
                            'n_jobs': -1
                        }
                    },
                    {
                    'type': 'extratreesregressor',
                    'params':{
                            'n_estimators': np.nan if 'extratreesregressor' not in pipeline_parts.keys() else hp.quniform(model_type +  '_n_estimators', 50, 400, 1),
                            'max_features': np.nan if 'extratreesregressor' not in pipeline_parts.keys() else None if  {k.replace('estimator__', ''): v for k, v in pipeline_parts['extratreesregressor'].get_params().items()}['max_features'] == None else \
                                            hp.uniform(model_type + '_max_features', {k.replace('estimator__', ''): v for k, v in pipeline_parts['extratreesregressor'].get_params().items()}['max_features'] - 0.10,
                                            {k.replace('estimator__', ''): v for k, v in pipeline_parts['extratreesregressor'].get_params().items()}['max_features'] + 0.10),
                            'min_samples_split': np.nan if 'extratreesregressor' not in pipeline_parts.keys() else hp.quniform(model_type + '_min_samples_split', 2, 30, 1),
                            'min_samples_leaf': np.nan if 'extratreesregressor' not in pipeline_parts.keys() else hp.quniform(model_type + '_min_samples_leaf', 1, 30, 1),
                            'bootstrap': np.nan if 'extratreesregressor' not in pipeline_parts.keys() else hp.choice(model_type + '_bootstrap', [True, False]),
                            'n_jobs': -1
                        }
                    },
                    {
                    'type': 'gradientboostingregressor',
                    'params':{
                            'n_estimators': np.nan if 'gradientboostingregressor' not in pipeline_parts.keys() else hp.quniform(model_type + '_n_estimators', 50, 400, 1),
                            'loss': np.nan if 'gradientboostingregressor' not in pipeline_parts.keys() else hp.choice(model_type + '_loss', ['ls', 'lad', 'huber']),
                            'learning_rate': np.nan if 'gradientboostingregressor' not in pipeline_parts.keys() else hp.uniform(model_type + '_learning_rate', 1e-3, 1),
                            'max_depth': np.nan if 'gradientboostingregressor' not in pipeline_parts.keys() else hp.quniform(model_type + '_max_depth', 1, 9, 1),
                            'min_samples_split': np.nan if 'gradientboostingregressor' not in pipeline_parts.keys() else hp.quniform(model_type + '_min_samples_split', 2, 30, 1),
                            'min_samples_leaf': np.nan if 'gradientboostingregressor' not in pipeline_parts.keys() else hp.quniform(model_type + '_min_samples_leaf', 1, 30, 1),
                            'subsample': np.nan if 'gradientboostingregressor' not in pipeline_parts.keys() else hp.uniform(model_type + '_subsample', 0.05, 1.01),
                            'max_features': np.nan if 'gradientboostingregressor' not in pipeline_parts.keys() else hp.uniform(model_type + '_max_features', {k.replace('estimator__', ''): v for k, v in pipeline_parts['gradientboostingregressor'].get_params().items()}['max_features'] - 0.10,
                                                        {k.replace('estimator__', ''): v for k, v in pipeline_parts['gradientboostingregressor'].get_params().items()}['max_features'] + 0.10),
                            'alpha': np.nan if 'gradientboostingregressor' not in pipeline_parts.keys() else hp.uniform(model_type + '_alpha', 0.01, 0.99)
                        }
                    },
                    {
                    'type': 'adaboostregressor',
                    'params':{
                            'n_estimators': np.nan if 'adaboostregressor' not in pipeline_parts.keys() else hp.quniform(model_type + '_n_estimators', 50, 400, 1),
                            'learning_rate': np.nan if 'adaboostregressor' not in pipeline_parts.keys() else hp.uniform(model_type + '_learning_rate', 1e-3, 1),
                            'loss': np.nan if 'adaboostregressor' not in pipeline_parts.keys() else hp.choice(model_type + '_loss', ["linear", "square", "exponential"]),
                        }
                    },
                    {
                    'type': 'decisiontreeregressor',
                    'params':{
                            'max_depth': np.nan if 'decisiontreeregressor' not in pipeline_parts.keys() else hp.quniform(model_type + '_n_estimators', 1, 11, 1),
                            'min_samples_split': np.nan if 'decisiontreeregressor' not in pipeline_parts.keys() else hp.quniform(model_type + '_min_samples_split', 2, 30, 1),
                            'min_samples_leaf': np.nan if 'decisiontreeregressor' not in pipeline_parts.keys() else hp.quniform(model_type + '_min_samples_leaf', 1, 30, 1)
                        }
                    },
                    {
                    'type': 'linearsvr',
                    'params':{
                            'loss': np.nan if 'linearsvr' not in pipeline_parts.keys() else hp.choice(model_type + '_loss', ["epsilon_insensitive", "squared_epsilon_insensitive"]),
                            'tol': np.nan if 'linearsvr' not in pipeline_parts.keys() else hp.normal(model_type + '_tol', {k.replace('estimator__', ''): v for k, v in pipeline_parts['linearsvr'].get_params().items()}['tol'] - 1e-3,
                                                        {k.replace('estimator__', ''): v for k, v in pipeline_parts['linearsvr'].get_params().items()}['tol'] * coef_variation),
                            'C': np.nan if 'linearsvr' not in pipeline_parts.keys() else hp.normal(model_type + '_c', {k.replace('estimator__', ''): v for k, v in pipeline_parts['linearsvr'].get_params().items()}['C'],
                                                        {k.replace('estimator__', ''): v for k, v in pipeline_parts['linearsvr'].get_params().items()}['C'] * coef_variation),
                            'epsilon': np.nan if 'linearsvr' not in pipeline_parts.keys() else hp.normal(model_type + '_epsilon', {k.replace('estimator__', ''): v for k, v in pipeline_parts['linearsvr'].get_params().items()}['epsilon'],
                                                        {k.replace('estimator__', ''): v for k, v in pipeline_parts['linearsvr'].get_params().items()}['epsilon'] * coef_variation),
                            'max_iter': np.nan if 'linearsvr' not in pipeline_parts.keys() else 10000
                        }
                    },
                    {
                    'type': 'xgbregressor',
                    'params':{
                            'n_estimators': np.nan if 'xgbregressor' not in pipeline_parts.keys() else hp.quniform(model_type + '_n_estimators', 50, 400, 1),
                            'learning_rate': np.nan if 'xgbregressor' not in pipeline_parts.keys() else hp.uniform(model_type + '_learning_rate', 1e-3, 1),
                            'max_depth': np.nan if 'xgbregressor' not in pipeline_parts.keys() else hp.quniform(model_type + '_max_depth', 1, 11, 1),
                            'subsample': np.nan if 'xgbregressor' not in pipeline_parts.keys() else hp.quniform(model_type + '_subsample', 0.05, 1.01),
                            'min_child_weight': np.nan if 'xgbregressor' not in pipeline_parts.keys() else hp.quniform(model_type + '_min_child_weight', 1, 25, 1),
                            'reg_lambda': np.nan if 'xgbregressor' not in pipeline_parts.keys() else hp.uniform(model_type + '_reg_lambda', 0.1, 100),
                            'alpha': np.nan if 'xgbregressor' not in pipeline_parts.keys() else hp.uniform(model_type + '_alpha', 0.1, 100),
                            'gamma': np.nan if 'xgbregressor' not in pipeline_parts.keys() else hp.uniform(model_type + '_gamma', 0.1, 15),
                            'colsample_bylevel': np.nan if 'xgbregressor' not in pipeline_parts.keys() else hp.uniform(model_type + '_colsample_bylevel', 0.5, 0.9),
                            'colsample_bynode': np.nan if 'xgbregressor' not in pipeline_parts.keys() else hp.uniform(model_type + '_colsample_bynode', 0.5, 0.9),
                            'colsample_bytree': np.nan if 'xgbregressor' not in pipeline_parts.keys() else hp.uniform(model_type + '_colsample_bytree', 0.5, 0.9),
                            'n_jobs': -1,
                            'tree_method': 'gpu_hist' if torch.cuda.is_available() else 'hist'
                        }
                    },
                    {
                    'type': 'sgdregressor',
                    'params':{
                            'loss': np.nan if 'sgdregressor' not in pipeline_parts.keys() else hp.choice(model_type + '_loss', ['squared_loss', 'huber', 'epsilon_insensitive']),
                            'penalty': np.nan if 'sgdregressor' not in pipeline_parts.keys() else hp.choice(model_type + '_penalty', ['l1', 'l2', 'elasticnet']),
                            'alpha': np.nan if 'sgdregressor' not in pipeline_parts.keys() else 0 if {k.replace('estimator__', ''): v for k, v in pipeline_parts['sgdregressor'].get_params().items()}['alpha'] == 0 else \
                                                        hp.normal(model_type + '_alpha', {k.replace('estimator__', ''): v for k, v in pipeline_parts['sgdregressor'].get_params().items()}['alpha'],
                                                        {k.replace('estimator__', ''): v for k, v in pipeline_parts['sgdregressor'].get_params().items()}['alpha'] * coef_variation),
                            'learning_rate': np.nan if 'sgdregressor' not in pipeline_parts.keys() else hp.choice(model_type + '_learning_rate', ['invscaling', 'constant']),
                            'fit_intercept': np.nan if 'sgdregressor' not in pipeline_parts.keys() else hp.choice(model_type + '_fit_intercept', [True, False]),
                            'l1_ratio': np.nan if 'sgdregressor' not in pipeline_parts.keys() else hp.normal(model_type + '_l1_ratio', {k.replace('estimator__', ''): v for k, v in pipeline_parts['sgdregressor'].get_params().items()}['l1_ratio'],
                                                        {k.replace('estimator__', ''): v for k, v in pipeline_parts['sgdregressor'].get_params().items()}['l1_ratio'] * coef_variation),
                            'eta0': np.nan if 'sgdregressor' not in pipeline_parts.keys() else hp.normal(model_type + '_eta0', {k.replace('estimator__', ''): v for k, v in pipeline_parts['sgdregressor'].get_params().items()}['eta0'],
                                                        {k.replace('estimator__', ''): v for k, v in pipeline_parts['sgdregressor'].get_params().items()}['eta0'] * coef_variation),
                            'power_t': np.nan if 'sgdregressor' not in pipeline_parts.keys() else hp.normal(model_type + '_power_t', {k.replace('estimator__', ''): v for k, v in pipeline_parts['sgdregressor'].get_params().items()}['power_t'],
                                                        {k.replace('estimator__', ''): v for k, v in pipeline_parts['sgdregressor'].get_params().items()}['power_t'] * coef_variation),
                            'max_iter': np.nan if 'sgdregressor' not in pipeline_parts.keys() else 10000
                        }
                    },
                    {
                    'type': 'binarizer',
                    'params':{
                            'threshold': np.nan if 'binarizer' not in pipeline_parts.keys() else hp.normal('brzr_threshold', pipeline_parts['binarizer'].get_params()['threshold'],
                                                        pipeline_parts['binarizer'].get_params()['threshold'] * coef_variation)
                        }
                    },
                    {
                    'type': 'fastica',
                    'params':{
                            'tol': np.nan if 'fastica' not in pipeline_parts.keys() else hp.normal('fica_tol', pipeline_parts['fastica'].get_params()['tol'],
                                                        pipeline_parts['fastica'].get_params()['tol'] * coef_variation)
                        }
                    },
                    {
                    'type': 'featureagglomeration',
                    'params':{
                            'linkage': np.nan if 'featureagglomeration' not in pipeline_parts.keys() else hp.choice('fagg_linkage', ['ward', 'complete', 'average']),
                            'affinity': np.nan if 'featureagglomeration' not in pipeline_parts.keys() else hp.choice('fagg_affinity', ['euclidean', 'l1', 'l2', 'manhattan', 'cosine']),
                            'n_clusters': np.nan if 'featureagglomeration' not in pipeline_parts.keys() else hp.quniform('fagg_n_clusters', 1, 10, 1)
                        }
                    },
                    {
                    'type': 'nystroem',
                    'params':{
                            'kernel': np.nan if 'nystroem' not in pipeline_parts.keys() else hp.choice('nstrm_kernel', ['rbf', 'cosine', 'chi2', 'laplacian', 'polynomial', 'poly', 'linear', 'additive_chi2', 'sigmoid']),
                            'gamma': np.nan if 'nystroem' not in pipeline_parts.keys() else hp.normal('nstrm_gamma', pipeline_parts['nystroem'].get_params()['gamma'],
                                                        pipeline_parts['nystroem'].get_params()['gamma'] * coef_variation),
                            'n_components': np.nan if 'nystroem' not in pipeline_parts.keys() else hp.qnormal('nstrm_n_components', pipeline_parts['nystroem'].get_params()['n_components'],
                                                        pipeline_parts['nystroem'].get_params()['n_components'] * coef_variation, 1)
                        }
                    },
                    {
                    'type': 'pca',
                    'params':{
                            'svd_solver': np.nan if 'pca' not in pipeline_parts.keys() else hp.choice('pca_svd_solver', ['randomized']),
                            'iterated_power': np. nan if 'pca' not in pipeline_parts.keys() else hp.qnormal('pca_iterated_power', pipeline_parts['pca'].get_params()['iterated_power'],
                                                        pipeline_parts['pca'].get_params()['iterated_power'] * coef_variation, 1)
                        }
                    },
                    {
                    'type': 'onehotencoder',
                    'params':{
                            'minimum_fraction': np.nan if 'onehotencoder' not in pipeline_parts.keys() else hp.normal('ohe_minimum_fraction', pipeline_parts['onehotencoder'].get_params()['minimum_fraction'],
                                                        pipeline_parts['onehotencoder'].get_params()['minimum_fraction'] * coef_variation)
                        }
                    }]
            else:
                config_dict = [
                    {
                    'type': 'kneighborsclassifier',
                    'params': {'n_neighbors': np.nan if 'kneighborsclassifier' not in pipeline_parts.keys() else hp.qnormal(model_type + '_n_neighbors', {k.replace('estimator__', ''): v for k, v in pipeline_parts['kneighborsclassifier'].get_params().items()}['n_neighbors'],
                                            {k.replace('estimator__', ''): v for k, v in pipeline_parts['kneighborsclassifier'].get_params().items()}['n_neighbors'] * 0.3, 1),
                            'weights': np.nan if 'kneighborsclassifier' not in pipeline_parts.keys() else hp.choice(model_type + '_weights', ['distance', 'uniform']),
                            'leaf_size': np.nan if 'kneighborsclassifier' not in pipeline_parts.keys() else hp.qnormal(model_type + '_leaf_size', 30, 5, 1),
                            'p': np.nan if 'kneighborsclassifier' not in pipeline_parts.keys() else hp.choice(model_type + '_p', [1, 2, 3]),
                            'n_jobs': -1}
                        },
                    {
                    'type': 'normalizer',
                    'params': {
                        'norm': np.nan if 'normalizer' not in pipeline_parts.keys() else hp.choice('nlzr_norm', ['l1', 'l2', 'max'])}
                    },
                    {
                    'type': 'logisticregression',
                    'params': {
                            'penalty': np.nan if 'logisticregression' not in pipeline_parts.keys() else hp.choice(model_type + '_penalty', [True, False]),
                            'C': np.nan if 'logisticregression' not in pipeline_parts.keys() else hp.normal(model_type + '_c', {k.replace('estimator__', ''): v for k, v in pipeline_parts['logisticregression'].get_params().items()}['C'],
                                                    {k.replace('estimator__', ''): v for k, v in pipeline_parts['logisticregression'].get_params().items()}['C'] * coef_variation),
                            'dual': np.nan if 'logisticregression' not in pipeline_parts.keys() else hp.choice(model_type + '_dual', [True, False]),
                            'n_jobs': -1
                        }
                    },
                    {
                    'type': 'randomforestclassifier',
                    'params': {
                            'n_estimators': np.nan if 'randomforestclassifier' not in pipeline_parts.keys() else hp.quniform(model_type + '_n_estimators', 50, 400, 1),
                            'max_features': np.nan if 'randomforestclassifier' not in pipeline_parts.keys() else hp.uniform(model_type + '_max_features', {k.replace('estimator__', ''): v for k, v in pipeline_parts['randomforestclassifier'].get_params().items()}['max_features'] - 0.10,
                                            {k.replace('estimator__', ''): v for k, v in pipeline_parts['randomforestclassifier'].get_params().items()}['max_features'] + 0.10),
                            'min_samples_split': np.nan if 'randomforestclassifier' not in pipeline_parts.keys() else hp.quniform(model_type + 'min_samples_split', 2, 30, 1),
                            'min_samples_leaf': np.nan if 'randomforestclassifier' not in pipeline_parts.keys() else hp.quniform(model_type + '_min_samples_leaf', 1, 30, 1),
                            'bootstrap': np.nan if 'randomforestclassifier' not in pipeline_parts.keys() else hp.choice(model_type + '_bootstrap', [True, False]),
                            'n_jobs': -1
                        }
                    },
                    {
                    'type': 'extratreesclassifier',
                    'params':{
                            'n_estimators': np.nan if 'extratreesclassifier' not in pipeline_parts.keys() else hp.quniform(model_type + '_n_estimators', 50, 400, 1),
                            'max_features': np.nan if 'extratreesclassifier' not in pipeline_parts.keys() else hp.uniform(model_type + '_max_features', {k.replace('estimator__', ''): v for k, v in pipeline_parts['extratreesclassifier'].get_params().items()}['max_features'] - 0.10,
                                            {k.replace('estimator__', ''): v for k, v in pipeline_parts['extratreesclassifier'].get_params().items()}['max_features'] + 0.10),
                            'min_samples_split': np.nan if 'extratreesclassifier' not in pipeline_parts.keys() else hp.quniform(model_type + '_min_samples_split', 2, 30, 1),
                            'min_samples_leaf': np.nan if 'extratreesclassifier' not in pipeline_parts.keys() else hp.quniform(model_type + '_min_samples_leaf', 1, 30, 1),
                            'bootstrap': np.nan if 'extratreesclassifier' not in pipeline_parts.keys() else hp.choice(model_type + '_bootstrap', [True, False]),
                            'n_jobs': -1
                        }
                    },
                    {
                    'type': 'gradientboostingclassifier',
                    'params':{
                            'n_estimators': np.nan if 'gradientboostingclassifier' not in pipeline_parts.keys() else hp.quniform(model_type + '_n_estimators', 50, 400, 1),
                            'learning_rate': np.nan if 'gradientboostingclassifier' not in pipeline_parts.keys() else hp.uniform(model_type + '_learning_rate', 1e-3, 1),
                            'max_depth': np.nan if 'gradientboostingclassifier' not in pipeline_parts.keys() else hp.quniform(model_type + '_max_depth', 1, 9, 1),
                            'min_samples_split': np.nan if 'gradientboostingclassifier' not in pipeline_parts.keys() else hp.quniform(model_type + '_min_samples_split', 2, 30, 1),
                            'min_samples_leaf': np.nan if 'gradientboostingclassifier' not in pipeline_parts.keys() else hp.quniform(model_type + '_min_samples_leaf', 1, 30, 1),
                            'subsample': np.nan if 'gradientboostingclassifier' not in pipeline_parts.keys() else hp.uniform(model_type + '_subsample', 0.05, 1.01),
                            'max_features': np.nan if 'gradientboostingclassifier' not in pipeline_parts.keys() else hp.uniform(model_type + '_max_features', {k.replace('estimator__', ''): v for k, v in pipeline_parts['gradientboostingclassifier'].get_params().items()}['max_features'] - 0.10,
                                                        {k.replace('estimator__', ''): v for k, v in pipeline_parts['gradientboostingclassifier'].get_params().items()}['max_features'] + 0.10)
                        }
                    },
                    {
                    'type': 'adaboostclassifier',
                    'params':{
                            'n_estimators': np.nan if 'adaboostclassifier' not in pipeline_parts.keys() else hp.quniform(model_type + '_n_estimators', 50, 400, 1),
                            'learning_rate': np.nan if 'adaboostclassifier' not in pipeline_parts.keys() else hp.uniform(model_type + '_learning_rate', 1e-3, 1)
                        }
                    },
                    {
                    'type': 'decisiontreeclassifier',
                    'params':{
                            'max_depth': np.nan if 'decisiontreeclassifier' not in pipeline_parts.keys() else hp.quniform(model_type + '_n_estimators', 1, 11, 1),
                            'min_samples_split': np.nan if 'decisiontreeclassifier' not in pipeline_parts.keys() else hp.quniform(model_type + '_min_samples_split', 2, 30, 1),
                            'min_samples_leaf': np.nan if 'decisiontreeclassifier' not in pipeline_parts.keys() else hp.quniform(model_type + '_min_samples_leaf', 1, 30, 1)
                        }
                    },
                    {
                    'type': 'linearsvc',
                    'params':{
                            'loss': np.nan if 'linearsvc' not in pipeline_parts.keys() else hp.choice(model_type + '_loss', ["squared_hinge"]),# "hinge"
                            'tol': np.nan if 'linearsvc' not in pipeline_parts.keys() else hp.normal(model_type + '_tol', {k.replace('estimator__', ''): v for k, v in pipeline_parts['linearsvc'].get_params().items()}['tol'],
                                                        {k.replace('estimator__', ''): v for k, v in pipeline_parts['linearsvc'].get_params().items()}['tol'] * coef_variation),
                            'C': np.nan if 'linearsvc' not in pipeline_parts.keys() else hp.normal(model_type + '_c', {k.replace('estimator__', ''): v for k, v in pipeline_parts['linearsvc'].get_params().items()}['C'],
                                                        {k.replace('estimator__', ''): v for k, v in pipeline_parts['linearsvc'].get_params().items()}['C'] * coef_variation),
                            'penalty': np.nan if 'linearsvc' not in pipeline_parts.keys() else hp.choice(model_type + '_penalty', ['l1', 'l2'])
                        }
                    },
                    {
                    'type': 'mlpclassifier',
                    'params':{
                            'alpha': np.nan if 'mlpclassifier' not in pipeline_parts.keys() else hp.normal(model_type + '_alpha', {k.replace('estimator__', ''): v for k, v in pipeline_parts['mlpclassifier'].get_params().items()}['alpha'],
                                                        {k.replace('estimator__', ''): v for k, v in pipeline_parts['mlpclassifier'].get_params().items()}['alpha'] * coef_variation),
                            'learning_rate_init': np.nan if 'mlpclassifier' not in pipeline_parts.keys() else hp.normal(model_type + '_learning_rate_init', {k.replace('estimator__', ''): v for k, v in pipeline_parts['mlpclassifier'].get_params().items()}['learning_rate_init'],
                                                        {k.replace('estimator__', ''): v for k, v in pipeline_parts['mlpclassifier'].get_params().items()}['learning_rate_init'] * coef_variation)
                        }
                    },
                    {
                    'type': 'xgbclassifier',
                    'params':{
                            'n_estimators': np.nan if 'xgbclassifier' not in pipeline_parts.keys() else hp.quniform(model_type + '_n_estimators', 50, 400, 1),
                            'learning_rate': np.nan if 'xgbclassifier' not in pipeline_parts.keys() else hp.uniform(model_type + '_learning_rate', 1e-3, 1),
                            'max_depth': np.nan if 'xgbclassifier' not in pipeline_parts.keys() else hp.quniform(model_type + '_max_depth', 1, 11, 1),
                            'subsample': np.nan if 'xgbclassifier' not in pipeline_parts.keys() else hp.uniform(model_type + '_subsample', 0.05, 1.01),
                            'min_child_weight': np.nan if 'xgbclassifier' not in pipeline_parts.keys() else hp.quniform(model_type + '_min_child_weight', 1, 25, 1),
                            'reg_lambda': np.nan if 'xgbclassifier' not in pipeline_parts.keys() else hp.uniform(model_type + '_reg_lambda', 0.1, 100),
                            'alpha': np.nan if 'xgbclassifier' not in pipeline_parts.keys() else hp.uniform(model_type + '_alpha', 0.1, 100),
                            'gamma': np.nan if 'xgbclassifier' not in pipeline_parts.keys() else hp.uniform(model_type + '_gamma', 0.1, 15),
                            'colsample_bylevel': np.nan if 'xgbclassifier' not in pipeline_parts.keys() else hp.uniform(model_type + '_colsample_bylevel', 0.5, 0.9),
                            'colsample_bynode': np.nan if 'xgbclassifier' not in pipeline_parts.keys() else hp.uniform(model_type + '_colsample_bynode', 0.5, 0.9),
                            'colsample_bytree': np.nan if 'xgbclassifier' not in pipeline_parts.keys() else hp.uniform(model_type + '_colsample_bytree', 0.5, 0.9),
                            'n_jobs': -1,
                            'tree_method': 'gpu_hist' if torch.cuda.is_available() else 'hist'
                        }
                    },
                    {
                    'type': 'sgdclassifier',
                    'params':{
                            'loss': np.nan if 'sgdclassifier' not in pipeline_parts.keys() else hp.choice(model_type + '_loss', ['log', 'hinge', 'modified_huber', 'squared_hinge', 'perceptron']),
                            'penalty': np.nan if 'sgdclassifier' not in pipeline_parts.keys() else hp.choice(model_type + '_penalty', ['l1', 'l2', 'elasticnet']),
                            'alpha': np.nan if 'sgdclassifier' not in pipeline_parts.keys() else 0 if {k.replace('estimator__', ''): v for k, v in pipeline_parts['sgdclassifier'].get_params().items()}['alpha'] == 0 else \
                                                        hp.normal(model_type + '_alpha', {k.replace('estimator__', ''): v for k, v in pipeline_parts['sgdclassifier'].get_params().items()}['alpha'],
                                                        {k.replace('estimator__', ''): v for k, v in pipeline_parts['sgdclassifier'].get_params().items()}['alpha'] * coef_variation),
                            'learning_rate': np.nan if 'sgdclassifier' not in pipeline_parts.keys() else hp.choice(model_type + '_learning_rate', ['invscaling', 'constant', 'adaptive']),
                            'fit_intercept': np.nan if 'sgdclassifier' not in pipeline_parts.keys() else hp.choice(model_type + '_fit_intercept', [True, False]),
                            'l1_ratio': np.nan if 'sgdclassifier' not in pipeline_parts.keys() else hp.normal(model_type + '_l1_ratio', {k.replace('estimator__', ''): v for k, v in pipeline_parts['sgdclassifier'].get_params().items()}['l1_ratio'],
                                                        {k.replace('estimator__', ''): v for k, v in pipeline_parts['sgdclassifier'].get_params().items()}['l1_ratio'] * coef_variation),
                            'eta0': np.nan if 'sgdclassifier' not in pipeline_parts.keys() else hp.normal(model_type + '_eta0', {k.replace('estimator__', ''): v for k, v in pipeline_parts['sgdclassifier'].get_params().items()}['eta0'],
                                                        {k.replace('estimator__', ''): v for k, v in pipeline_parts['sgdclassifier'].get_params().items()}['eta0'] * coef_variation),
                            'power_t': np.nan if 'sgdclassifier' not in pipeline_parts.keys() else hp.normal(model_type + '_power_t', {k.replace('estimator__', ''): v for k, v in pipeline_parts['sgdclassifier'].get_params().items()}['power_t'],
                                                        {k.replace('estimator__', ''): v for k, v in pipeline_parts['sgdclassifier'].get_params().items()}['power_t'] * coef_variation),
                            'n_jobs': -1
                        }
                    },
                    {
                    'type': 'binarizer',
                    'params':{
                            'threshold': np.nan if 'binarizer' not in pipeline_parts.keys() else hp.normal('brzr_threshold', pipeline_parts['binarizer'].get_params()['threshold'],
                                                        pipeline_parts['binarizer'].get_params()['threshold'] * coef_variation)
                        }
                    },
                    {
                    'type': 'fastica',
                    'params':{
                            'tol': np.nan if 'fastica' not in pipeline_parts.keys() else hp.normal('fica_tol', pipeline_parts['fastica'].get_params()['tol'],
                                                        pipeline_parts['fastica'].get_params()['tol'] * coef_variation)
                        }
                    },
                    {
                    'type': 'featureagglomeration',
                    'params':{
                            'linkage': np.nan if 'featureagglomeration' not in pipeline_parts.keys() else hp.choice('fagg_linkage', ['ward', 'complete', 'average']),
                            'affinity': np.nan if 'featureagglomeration' not in pipeline_parts.keys() else hp.choice('fagg_affinity', ['euclidean', 'l1', 'l2', 'manhattan', 'cosine']),
                            'n_clusters': np.nan if 'featureagglomeration' not in pipeline_parts.keys() else hp.quniform('fagg_n_clusters', 1, 10, 1)
                        }
                    },
                    {
                    'type': 'nystroem',
                    'params':{
                            'kernel': np.nan if 'nystroem' not in pipeline_parts.keys() else hp.choice('nstrm_kernel', ['rbf', 'cosine', 'chi2', 'laplacian', 'polynomial', 'poly', 'linear', 'additive_chi2', 'sigmoid']),
                            'gamma': np.nan if 'nystroem' not in pipeline_parts.keys() else hp.normal('nstrm_gamma', pipeline_parts['nystroem'].get_params()['gamma'],
                                                        pipeline_parts['nystroem'].get_params()['gamma'] * coef_variation),
                            'n_components': np.nan if 'nystroem' not in pipeline_parts.keys() else hp.qnormal('nstrm_n_components', pipeline_parts['nystroem'].get_params()['n_components'],
                                                        pipeline_parts['nystroem'].get_params()['n_components'] * coef_variation, 1)
                        }
                    },
                    {
                    'type': 'pca',
                    'params':{
                            'svd_solver': np.nan if 'pca' not in pipeline_parts.keys() else hp.choice('pca_svd_solver', ['randomized']),
                            'iterated_power': np. nan if 'pca' not in pipeline_parts.keys() else hp.qnormal('pca_iterated_power', pipeline_parts['pca'].get_params()['iterated_power'],
                                                        pipeline_parts['pca'].get_params()['iterated_power'] * coef_variation, 1)
                        }
                    },
                    {
                    'type': 'onehotencoder',
                    'params':{
                            'minimum_fraction': np.nan if 'onehotencoder' not in pipeline_parts.keys() else hp.normal('ohe_minimum_fraction', pipeline_parts['onehotencoder'].get_params()['minimum_fraction'],
                                                        pipeline_parts['onehotencoder'].get_params()['minimum_fraction'] * coef_variation)
                        }
                    }]

            try:
                if 'stackingestimator' in model_type or 'selectfrommodel' in model_type or 'rfe' in model_type:
                    return {'type': model_type + '__estimator', 'params': [x['params'] for x in config_dict if x['type'] == str(pipeline_parts[key.replace('_v2_', '')].get_params()['estimator']).split('(')[0].lower()][0]}
                if any(d['type'] == model_type for d in config_dict):
                    return {'type': model_type, 'params': [x['params'] for x in config_dict if x['type'] == model_type][0]}
            except:
                return None

        pipeline_parts = dict(zip([x[0] for x in pipeline.get_params()['steps']], [x[1] for x in pipeline.get_params()['steps']]))
        to_map = {}
        stacked_models = ['stackingestimator', 'selectfrommodel', 'rfe']
        actual_models = list(pipeline_parts.keys())
        for model in stacked_models:
            if any([model in x for x in list(pipeline_parts.keys())]):
                n_stacking = sum([model in x for x in list(pipeline_parts.keys())])
                if n_stacking == 1:
                    if str(pipeline_parts[model].get_params()['estimator']).split('(')[0].lower() not in actual_models:
                        pipeline_parts[str(pipeline_parts[model].get_params()['estimator']).split('(')[0].lower()] = pipeline_parts[model]
                        to_map[str(pipeline_parts[model].get_params()['estimator']).split('(')[0].lower()] = model
                    else:
                        pipeline_parts[str(pipeline_parts[model].get_params()['estimator']).split('(')[0].lower() + '_v2_'] = pipeline_parts[model]
                        to_map[str(pipeline_parts[model].get_params()['estimator']).split('(')[0].lower() + '_v2_'] = model
                else:
                    for i in range(1, n_stacking + 1):
                        if str(pipeline_parts[model + '-' + str(i)].get_params()['estimator']).split('(')[0].lower() not in actual_models:
                            pipeline_parts[str(pipeline_parts[model + '-' + str(i)].get_params()['estimator']).split('(')[0].lower()] = pipeline_parts[model + '-' + str(i)]
                            to_map[str(pipeline_parts[model + '-' + str(i)].get_params()['estimator']).split('(')[0].lower()] = model + '-' + str(i)
                        else:
                            pipeline_parts[str(pipeline_parts[model + '-' + str(i)].get_params()['estimator']).split('(')[0].lower() + '_v2_'] = pipeline_parts[model + '-' + str(i)]
                            to_map[str(pipeline_parts[model + '-' + str(i)].get_params()['estimator']).split('(')[0].lower() + '_v2_'] = model + '-' + str(i)

        output = []
        for key, value in pipeline_parts.items():
            output.append(search_config(key, pipeline_parts))

        if to_map:
            to_map = {k: v for k, v in to_map.items() if k not in pipeline.get_params().keys()}
            output = [x for x in output if x is not None and x['type'] not in to_map.keys()]
        else:
            output = [x for x in output if x is not None]

        if select_variables:
            output.append({'type': 'select_vars', 'params': {'select_vars': hp.choice('select_vars', [0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.01])}})

        return output

    def preprocess_search_space(self, search_space, n_samples, drop_select_vars = False):

        """
        Preprocess hyperparameter search space prior to passing it to the estimator. Hyperparameter bounds can be exceeded depending on the parameter distribution
        obtained in generate_search_space. Limits bounds and changes data types accordingly
        - Parameters
        -- search_space - hyperparameter search space obtained from generate_search_space
        -- n_samples - dataframe.shape[0], nrows
        -- drop_select_vars - True to drop select_vars from dictionary
        """

        bound_dict = {'n_neighbors': [1, n_samples, 'int'],
        'leaf_size': [1, 15000, 'int'],
        'p': [1, 15000, 'int'],
        'n_estimators': [1, 15000, 'int'],
        'epsilon': [0.0001, 15000, 'float'],
        'max_features': [0.01, 0.99, 'float'],
        'min_samples_split': [2, 15000, 'int'],
        'min_samples_leaf': [1, 15000, 'int'],
        'l1_ratio': [0.01, 0.99, 'float'],
        'tol': [0.000001, 0.99, 'float'],
        'n_alphas': [1, 15000, 'int'],
        'eps': [0.00001, 0.99, 'float'],
        'learning_rate': [0.000001, 15000, 'float'],
        'max_depth': [1, 15000, 'int'],
        'subsample': [0.00001, 1, 'float'],
        'alpha': [0.0001, 0.999999, 'float'],
        'C': [0.0001, 15000, 'float'],
        'min_child_weight': [1, 15000, 'int'],
        'reg_lambda': [0.00001, 15000, 'float'],
        'gamma': [0, 15000, 'float'],
        'colsample_bylevel': [0.00001, 0.99, 'float'],
        'colsample_bynode': [0.00001, 0.99, 'float'],
        'colsample_bytree': [0.00001, 0.99, 'float'],
        'eta0': [0.0001, 15000, 'float'],
        'power_t': [0.00001, 15000, 'float'],
        'threshold': [0, 15000, 'float'],
        'n_clusters': [1, 15000, 'int'],
        'n_components': [1, 15000, 'int'],
        'learning_rate_init': [0.0000001, 15000, 'float'],
        'iterated_power': [1, 15000, 'int']}

        for subspace in search_space:
            for param in subspace['params']:
                if param in bound_dict.keys():
                    if subspace['params'][param] is not None and type(subspace['params'][param]) != str:
                        if subspace['params'][param] < bound_dict[param][0]:
                            subspace['params'][param] = bound_dict[param][0]
                        elif subspace['params'][param] > bound_dict[param][1]:
                            subspace['params'][param] = bound_dict[param][1]
                        if bound_dict[param][2] == 'int':
                            subspace['params'][param] = int(subspace['params'][param])

        output = [dict(zip(list(pd.DataFrame(x)['type'] + '__' + pd.DataFrame(x).index), list(x['params'].values()))) for x in search_space]
        hyperparam_space = {}
        for dictionary in output:
            hyperparam_space.update(dictionary)

        if drop_select_vars:
            hyperparam_space.pop('select_vars__select_vars', None)

        return hyperparam_space

    def fit_and_save(self, best_models, export_scores, root_models, root_preds, root_variables, retrain_interval, selected_variables = None):

        """
        Fits, predict and save best models
        """

        def count(d):
            return max(count(v) if isinstance(v,dict) else 0 for v in d.values()) + 1

        if count(export_scores) == 2:
            for key1, value1 in export_scores.items():
                for key2, value2 in value1.items():
                    if self.target_df is None:
                        temp_df, transf = self.db.fetch_target_vars(key1, self.s3client, make_transf = True, transf_target = self.target_ticker[key1][0], model_vars = self.model_vars, ticker_campo = self.ticker_campo,
                                                               file_name = self.file_name, bucket = self.bucket)
                        temp_df.fillna(method = 'ffill', inplace = True)
                        if self.denoise:
                            temp_df.dropna(inplace = True)
                            for col in self.denoise_cols:
                                temp_df.loc[:, col] = self.jurik(temp_df.loc[:, col].rolling(int(key2.split(': ')[1])).mean().dropna())
                        dtst = self.dataset([temp_df])
                    else:
                        temp_df = self.target_df.copy()
                        if self.denoise:
                            temp_df.dropna(inplace = True)
                            for col in self.denoise_cols:
                                temp_df.loc[:, col] = self.jurik(temp_df.loc[:, col].rolling(int(key2.split(': ')[1])).mean().dropna())
                        dtst = self.dataset([self.target_df])
                    temp_df = dtst.shift_dataset(lag = True, forecast = True, nlag = int(value2.split(': ')[1]), nforecast = int(key2.split(': ')[1]), var_forecast = [key1],
                                                    var_lags = None if self.target_ticker[key1][5] else [x for x in temp_df.columns if x != key1],
                                                    output_type = self.target_ticker[key1][1], dropna = True, drop_var_forecast = False if self.target_ticker[key1][5] else True)
                    if self.target_ticker[key1][3]:
                        temp_df.iloc[:, 0] = self.jurik(temp_df.iloc[:, 0])
                        path = 'jurik'
                    else:
                        path = 'raw'
                    if selected_variables is not None:
                        if selected_variables[key1][key2]:
                            temp_df = temp_df.loc[:, [temp_df.columns.values.tolist()[0]] + selected_variables[key1][key2]]

                    sum_lags = sum(range(int(value2.split(': ')[1])))
                    vars_selected = pd.DataFrame({'Variables': [x.split(' | ')[0] for x in temp_df.columns.values.tolist()], 'Fields': [x.split(' | ')[1].split(' ')[0] for x in temp_df.columns.values.tolist()],
                                                    'lag': [int(x.split(' | ')[1].split(' ')[2]) if len(x.split( ' | ')[1].split(' ')) == 3 else 0 for x in temp_df.columns.values.tolist()]}).iloc[1:, :]
                    vars_selected['Temp'] = vars_selected['Variables'] + ' | ' + vars_selected['Fields']
                    vars_selected['Transformation'] = vars_selected['Temp'].replace(transf)
                    all_lags = vars_selected.groupby('Temp').sum() == sum_lags
                    vars_selected = vars_selected.merge(all_lags.reset_index(), on = 'Temp', how = 'left')
                    vars_selected.columns = ['Variables', 'Fields', 'Lag', 'Temp', 'Transformation', 'Lag all']

                    lag_all = vars_selected[vars_selected['Lag all'] == True]
                    lag_some = vars_selected[vars_selected['Lag all'] == False].loc[:, vars_selected.columns != 'Temp']
                    if not lag_all.empty:
                        lag_all = lag_all.groupby('Temp').max().reset_index(drop = True)
                        lag_all['Lag'] = lag_all['Lag'] + 1
                    else:
                        lag_all = lag_all.loc[:, vars_selected.columns != 'Temp']

                    vars_selected = pd.concat([lag_all, lag_some], axis = 0)
                    vars_selected['Lag all'] = vars_selected['Lag all'].astype(int)

                    dates_train = np.array(pd.date_range(self.target_ticker[key1][2], periods = 150, freq = retrain_interval))
                    dates_train = list(dates_train[dates_train < np.datetime64(datetime.datetime.now())])
                    dates_train = list(map(lambda x: pd.to_datetime(str(x)).strftime('%Y-%m-%d'), dates_train))
                    output_df = pd.DataFrame()
                    for date in dates_train:
                        df_train = temp_df.loc[:date, :]
                        df_test = temp_df.loc[date:, :].iloc[1:, :]
                        try:
                            best_models[key1][key2].fit(df_train.iloc[:, 1:], df_train.iloc[:, 0])
                            results = pd.DataFrame({'Observations': df_test.iloc[:, 0], 'Predictions': best_models[key1][key2].predict(df_test.iloc[:, 1:])}, index = df_test.index)
                            output_df = pd.concat([output_df, results], axis = 0)
                        except Exception as e:
                            print(e)

                    output_df = output_df.loc[~output_df.index.duplicated(keep='last')]
                    output_df.index = pd.date_range(output_df.index[int(key2.split(': ')[1])], periods = len(output_df.index), freq = 'M')
                    best_models[key1][key2].fit(temp_df.iloc[:, 1:], temp_df.iloc[:, 0])
                    best_models[key1][key2].feature_names = df_train.columns.values.tolist()[1:]
                    joblib.dump(best_models[key1][key2], root_models + key1.split(' | ')[0].split(' ')[0].lower() + '_' + path + '_forecast' + str(int(key2.split(': ')[1])) + '_lag' + str(int(value2.split(': ')[1])) + '.joblib')
                    output_df.iloc[1:, :].to_csv(root_preds + key1.split(' | ')[0].split(' ')[0].lower() + '_' + path + '_forecast' + str(int(key2.split(': ')[1])) + '_lag' + str(int(value2.split(': ')[1])) + '.csv')
                    vars_selected.to_csv(root_variables + key1.split(' | ')[0].split(' ')[0].lower() + '_' + path + '_forecast' + str(int(key2.split(': ')[1])) + '_lag' + str(int(value2.split(': ')[1])) + '.csv')
        else:
            for key1, value1 in export_scores.items():
                for key2, value2 in value1.items():
                    for key3, value3 in value2.items():
                        if self.target_df is None:
                            temp_df, transf = self.db.fetch_target_vars(key1, self.s3client, make_transf = True, transf_target = self.target_ticker[key1][0], model_vars = self.model_vars, ticker_campo = self.ticker_campo,
                                                               file_name = self.file_name, bucket = self.bucket)
                            temp_df.fillna(method = 'ffill', inplace = True)
                            if self.denoise:
                                temp_df.dropna(inplace = True)
                                for col in self.denoise_cols:
                                    temp_df.loc[:, col] = self.jurik(temp_df.loc[:, col].rolling(int(key2.split(': ')[1])).mean().dropna())
                            dtst = self.dataset([temp_df])
                        else:
                            temp_df = self.target_df.copy()
                            if self.denoise:
                                temp_df.dropna(inplace = True)
                                for col in self.denoise_cols:
                                    temp_df.loc[:, col] = self.jurik(temp_df.loc[:, col].rolling(int(key2.split(': ')[1])).mean().dropna())
                            dtst = self.dataset([self.target_df])
                        temp_df = dtst.shift_dataset(lag = True, forecast = True, nlag = int(key3.split(': ')[1]), nforecast = int(key2.split(': ')[1]), var_forecast = [key1],
                                                        var_lags = None if self.target_ticker[key1][5] else [x for x in temp_df.columns if x != key1],
                                                        output_type = self.target_ticker[key1][1], dropna = True, drop_var_forecast = False if self.target_ticker[key1][5] else True)
                        if self.target_ticker[key1][3]:
                            temp_df.iloc[:, 0] = self.jurik(temp_df.iloc[:, 0])
                            path = 'jurik'
                        else:
                            path = 'raw'
                        if selected_variables is not None:
                            if selected_variables[key1][key2][key3]:
                                temp_df = temp_df.loc[:, [temp_df.columns.values.tolist()[0]] + selected_variables[key1][key2][key3]]

                        sum_lags = sum(range(int(value2.split(': ')[1])))
                        vars_selected = pd.DataFrame({'Variables': [x.split(' | ')[0] for x in temp_df.columns.values.tolist()], 'Fields': [x.split(' | ')[1].split(' ')[0] for x in temp_df.columns.values.tolist()],
                                                        'lag': [int(x.split(' | ')[1].split(' ')[2]) if len(x.split( ' | ')[1].split(' ')) == 3 else 0 for x in temp_df.columns.values.tolist()]}).iloc[1:, :]
                        vars_selected['Temp'] = vars_selected['Variables'] + ' | ' + vars_selected['Fields']
                        vars_selected['Transformation'] = vars_selected['Temp'].replace(transf)
                        all_lags = vars_selected.groupby('Temp').sum() == sum_lags
                        vars_selected = vars_selected.merge(all_lags.reset_index(), on = 'Temp', how = 'left')
                        vars_selected.columns = ['Variables', 'Fields', 'Lag', 'Temp', 'Transformation', 'Lag all']

                        lag_all = vars_selected[vars_selected['Lag all'] == True]
                        lag_some = vars_selected[vars_selected['Lag all'] == False].loc[:, vars_selected.columns != 'Temp']
                        if not lag_all.empty:
                            lag_all = lag_all.groupby('Temp').max().reset_index(drop = True)
                            lag_all['Lag'] = lag_all['Lag'] + 1
                        else:
                            lag_all = lag_all.loc[:, vars_selected.columns != 'Temp']

                        vars_selected = pd.concat([lag_all, lag_some], axis = 0)
                        vars_selected['Lag all'] = vars_selected['Lag all'].astype(int)

                        dates_train = np.array(pd.date_range(self.target_ticker[key1][2], periods = 150, freq = retrain_interval))
                        dates_train = list(dates_train[dates_train < np.datetime64(datetime.datetime.now())])
                        dates_train = list(map(lambda x: pd.to_datetime(str(x)).strftime('%Y-%m-%d'), dates_train))

                        output_df = pd.DataFrame()
                        for date in dates_train:
                            df_train = temp_df.loc[:date, :]
                            df_test = temp_df.loc[date:, :].iloc[1:, :]
                            try:
                                best_models[key1][key2][key3].fit(df_train.iloc[:, 1:], df_train.iloc[:, 0])
                                results = pd.DataFrame({'Observations': df_test.iloc[:, 0], 'Predictions': best_models[key1][key2][key3].predict(df_test.iloc[:, 1:])}, index = df_test.index)
                                output_df = pd.concat([output_df, results], axis = 0)
                            except Exception as e:
                                print(e)

                        output_df = output_df.loc[~output_df.index.duplicated(keep='last')]
                        output_df.index = pd.date_range(output_df.index[int(key2.split(': ')[1])], periods = len(output_df.index), freq = 'M')
                        best_models[key1][key2][key3].fit(temp_df.iloc[:, 1:], temp_df.iloc[:, 0])
                        best_models[key1][key2][key3].feature_names = df_train.columns.values.tolist()[1:]
                        joblib.dump(best_models[key1][key2][key3], root_models + key1.split(' | ')[0].split(' ')[0].lower() + '_' + path + '_forecast' + str(int(key2.split(': ')[1])) + '_lag' + str(int(key3.split(': ')[1])) + '.joblib')
                        output_df.iloc[1:, :].to_csv(root_preds + key1.split(' | ')[0].split(' ')[0].lower() + '_' + path + '_forecast' + str(int(key2.split(': ')[1])) + '_lag' + str(int(key3.split(': ')[1])) + '.csv')
                        vars_selected.to_csv(root_variables + key1.split(' | ')[0].split(' ')[0].lower() + '_' + path + '_forecast' + str(int(key2.split(': ')[1])) + '_lag' + str(int(key3.split(': ')[1])) + '.csv')
