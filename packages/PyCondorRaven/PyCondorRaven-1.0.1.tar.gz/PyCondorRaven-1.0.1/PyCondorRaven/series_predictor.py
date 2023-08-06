
import numpy as np
import pandas as pd
import math
from .utils import *
import os
from . import models
import joblib
import tensorflow as tf
from timeit import default_timer as timer

class Predictor():
	"""
		Clase para crear los modelos, entrenarlos y predecir con ellos, en general es la clase principal y mediante esta se interactua con los modelos.

	"""
	def __init__(self, data, id_model, original, time_steps, period="monthly", returns=False, to_returns=False, target_var=None, predictor_id=None, variable_selection_method=0, train_size=0.7, test_size=0.15, val_size=0.15, model_name=None, root=''):
		"""
			Constructor de la clase, se encarga de cargar o entrenar el modelo según lo especificado en los hyperparámetros.

			Parámetros:
			- data -- Dataframe, arreglo con todos los datos, incluidos los de test (Todos los datos son necesarios para la selección de variables).
			- id_model -- Entero, id del modelo que se va a utilizar. LSTM:0, Random Forest:1, adaBoost:2, SVM:3, ARIMA: 4.
			- original -- Booleano, indica si entenar con las varaibles originales o con las eleccionadas. True para entrenar con las originales.
			- time_steps -- Entero, número de periodos en el futuro a predecir
			- returns -- Booleano, indica si se está trabajando con retornos o no (serie diferenciada). True es que si se trabaja con retornos.
			- to_returns -- Booleano, indica si se se deben transformar los datos a retornos.

			- model_name -- *string*, con el nombre del modelo.
		"""
		if type(id_model)==str:
			switcher = {"lstm": 0, "rand":1, "adab":2, "svm":3, "arim": 4}
			self.id_model = switcher.get(id_model.lower()[0:4], "Error")
			if self.id_model=="Error":
				raise Exception('Invalid model!')
		else:
			self.id_model = id_model


		self.root = root
		self.original = original

		if time_steps is None:
			self.time_steps = 1
		else:
			self.time_steps = time_steps
		if period is not None:
			self.period = period
		else:
			self.period = "monthly" # default value

		self.freq = dict(monthly=12, quarterly=4, yearly=1)[period]
		self.target_var = target_var
		self.retrain_cont = 0 # contador de iteraciones para reentrenar
		self.retrain_rate = 10 # taza de reentreno para modelos que se necesiten reentrenar
		self.evaluating = False # parámetro para saber si el paso de training se hace al principio o luego cuando se está evaluando
		self.returns = returns
		self.variable_selection_method = variable_selection_method
		self.train_size = train_size
		self.test_size = test_size
		self.val_size = val_size
		self.model_name = model_name
		self.model = None
		if data is not None:
			self.series_proc = preproc_series(data, period=period, to_returns=to_returns)
			self.series_proc.index = np.arange(len(self.series_proc))

			if target_var==None: # Por default e target es la primera variable
				self.data_train = self.series_proc.values
				self.original_cols = self.series_proc.columns
			else:
				self.original_cols = list(self.series_proc.columns)
				self.original_cols.remove(target_var)
				self.original_cols = [target_var, *self.original_cols]
				self.data_train = self.series_proc.values[:, [list(self.series_proc.columns).index(i) for i in self.original_cols]]
			self.selected_features = list(self.original_cols)
			if predictor_id==None:
				self.predictor_id = self.original_cols[0].strip().replace(" ","").replace("/","")
		else:
			self.data_train = None

		# Default parameters:
		if(self.id_model == 0 and self.time_steps > 0):
			if(time_steps <= 1):
				if(self.original):
					if(self.returns):
						self.n_rnn, self.n_dense, self.activation, self.drop_p = 1, 0, 1, 0.20 # bayes optim 2
						self.batch_size, self.n_epochs, self.n_hidden, self.n_lags = 8, 100, 5, 6 # bayes optim 2
					else:
						self.n_rnn, self.n_dense, self.activation, self.drop_p = 1, 0, 1, 0.20 # bayes optim 2
						self.batch_size, self.n_epochs, self.n_hidden, self.n_lags = 8, 100, 5, 6 # bayes optim 2
				else:
					if(self.returns):
						self.n_rnn, self.n_dense, self.activation, self.drop_p = 1, 0, 1, 0.2 # bayes optim 2
						self.batch_size, self.n_epochs, self.n_hidden, self.n_lags = 8, 100, 5, 6 # bayes optim 2
					else:
						self.n_rnn, self.n_dense, self.activation, self.drop_p = 1, 0, 1, 0.20 # bayes optim 2
						self.batch_size, self.n_epochs, self.n_hidden, self.n_lags = 8, 100, 5, 6 # bayes optim 2
			else:
				if(self.original):
					if(self.returns):
						self.n_rnn, self.n_dense, self.activation, self.drop_p = 1, 0, 1, 0.2 # bayes optim 2
						self.batch_size, self.n_epochs, self.n_hidden, self.n_lags = 8, 100, 5, 6 # bayes optim 2
					else:
						self.n_rnn, self.n_dense, self.activation, self.drop_p = 1, 0, 1, 0.2 # bayes optim 2
						self.batch_size, self.n_epochs, self.n_hidden, self.n_lags = 8, 100, 5, 6 # bayes optim 2
				else:
					if(self.returns):
						self.n_rnn, self.n_dense, self.activation, self.drop_p = 1, 0, 1, 0.2 # bayes optim 2
						self.batch_size, self.n_epochs, self.n_hidden, self.n_lags = 8, 100, 8, 6 # bayes optim 2
					else:
						self.n_rnn, self.n_dense, self.activation, self.drop_p = 1, 0, 1, 0.2 # bayes optim 2
						self.batch_size, self.n_epochs, self.n_hidden, self.n_lags = 8, 100, 8, 6 # bayes optim 2

		elif(self.id_model == 1 and self.time_steps == 1):
			if(self.original):
				self.n_lags, self.n_estimators, self.max_features, self.min_samples = 4, 762, 18, 3 # for selected features
			else:
				# self.n_lags, self.n_estimators, self.max_features, self.min_samples = 6, 80, 12, 4
				self.n_lags, self.n_estimators, self.max_features, self.min_samples = 13, 749, 5, 1

		elif(self.id_model == 2 and self.time_steps == 1):
			if(self.original):
				self.n_lags, self.n_estimators, self.lr, self.max_depth = 4, 808, 0.33209425848535884, 3
			else:
				self.n_lags, self.n_estimators, self.lr, self.max_depth = 5, 916, 0.6378995385153448, 4

		elif(self.id_model == 3 and self.time_steps == 1):
			self.n_lags = 4

		elif(self.id_model == 4 and self.time_steps == 1):
			self.n_lags, self.d, self.q = 1, 1, 2
			# self.n_lags, self.d, self.q = 3, 0, 6

		else:
			raise Exception('hyperparameters combination is not in the valid options.')

	def train(self, tune, lr=0.01, select=False, max_vars=10, verbosity=3, max_evals=100, saved_model=False, norm_data=False, linear_reg_vs=True, nn_error_type="mse", prob_model=False):
		"""
		Función que recibe como entrada los datos de entrenamiento junto con los parámetros y retorna el modelo entrenado.

		Parámetros:
		- tune -- *booleano* o entero que define si se hace tuning de parametros usando optimizacion bayesiana.
		- select -- *booleano* o entero que define si se hace selección de variables
		- max_vars -- entero que denota la cantidad maxima de variables a seleccionar a la hora de hacer selección de variables
		- verbosity -- entero que denota el nivel de verbosidad de la ejecución, entre más alto más graficos o información se mostrará (tiene un límite diferente para cada algoritmo)
		- max_evals -- entero que define el número de evaluciones de la optimización bayesiana para encontrar los mejores hyperparámetros.
		- saved_model -- Booleano, indica si se desea entrenar el modelo o cargar uno guardado. Si True se carga un modelo guardado, si False se entrena un nuevo modelo.
		- norm_data -- Booleano, indica si se transforman los datos usando MinMaxScaler.
		- linear_reg_vs -- Booleano, indica si se utiliza regr. lineal para seleccion de variables
		- nn_error_type -- str, indica métrica de entrenamiento de redes. (mse, mae, huber)

		Retorna:
		- model -- Modelo(varios tipos), modelo entrenado
		"""
		if self.data_train is None:
			raise ValueError("No training data available. Please create a series_predictor instance with a data object.")
		self.lr = lr
		if select:
			self.original = 0
			# feature selection
			from . import feature_selection as fs
			if(self.variable_selection_method == 0):
				select_data = fs.select_features_ga(pd.DataFrame(self.data_train), max_vars, self.original_cols, self.n_lags, self.time_steps, norm_data, linear_reg_vs)
			elif(self.variable_selection_method == 1):
				select_data = fs.select_features_sa(pd.DataFrame(self.data_train), max_vars, self.original_cols, norm_data, linear_reg_vs)
			elif(self.variable_selection_method == 2):
				select_data = fs.select_features_stepwise_forward(pd.DataFrame(self.data_train), int(len(self.original_cols)**(1/2)), self.original_cols, norm_data, linear_reg_vs)
		if(not self.original and not self.evaluating):
			df = select_data['df']
			self.data_train = df.values[:len(self.data_train), :]
			self.selected_features = list(df.columns)

		self.model = None

		if norm_data:
			values, self.scaler = normalize_data(self.data_train, scale=(-1, 1), train_size=self.train_size) #Scales based on train data.
		else:
			from sklearn.preprocessing import StandardScaler
			values, self.scaler = self.data_train, StandardScaler(with_mean=False, with_std=False).fit(self.data_train) # scaler is identity function

		self.n_features = values.shape[1] if self.time_steps>0 else values.shape[1]-1

		calc_val_error = False if verbosity < 2 else True
		calc_test_error = True
		# calc_val_error = True
		# calc_test_error = False
		if self.id_model != 0 and self.time_steps > 1:
			raise Exception('The only model that support multi-step prediction is model RNN with LSTM.')

		# Model 0 is the only one supporting multi-step ahead predictions.
		if(self.id_model == 0):
			if self.model_name == None: self.model_name =  'lstm_%s_ret%s_%s_%dts' % (self.predictor_id, self.returns, self.period, self.time_steps)
			model_file_name = self.root + 'models/' + self.model_name + '.h5'
			if tune:
				best = bayes_optimization(self.id_model, max_evals, values, self.scaler, self.n_features, self.time_steps, self.lr, self.original, 0, model_file_name, self.returns, self.train_size, self.test_size, self.val_size, self.root, error_type='mse' if prob_model else nn_error_type)
				# Parameters
				self.n_lags, self.n_epochs, self.batch_size, self.n_hidden = int(best['n_lags']), int(best['n_epochs']), int(best['batch_size']), int(best['n_hidden'])
				self.n_rnn, self.n_dense, self.activation, self.drop_p = int(best['n_rnn']), int(best['n_dense']), int(best['activation']), best['drop_p']
				f = open(self.root + 'parameters/optimized_' + self.model_name + '.pars', 'w')
				#f.write('%d, %d, %d, %d\n' % (self.n_lags, self.n_epochs, self.batch_size, self.n_hidden))
				f.write('%d, %d, %s, %d, %d, %d, %d, %d\n' % (self.activation, self.batch_size, self.drop_p, self.n_dense, self.n_epochs, self.n_hidden, self.n_lags, self.n_rnn))
				f.close()
			else:
				if os.path.isfile(self.root + 'parameters/optimized_' + self.model_name + '.pars'):
					f = open(self.root + 'parameters/optimized_' + self.model_name + '.pars', 'r')
					lines = f.readlines()
					if(len(lines) > 1):
						raise Exception('File with parameters can\'t have more than 1 line ')
					readed_parameters = lines[0].strip().split(', ')
					self.activation, self.batch_size, self.drop_p, self.n_dense, self.n_epochs, self.n_hidden, self.n_lags, self.n_rnn = int(readed_parameters[0]), int(readed_parameters[1]), float(readed_parameters[2]), int(readed_parameters[3]), int(readed_parameters[4]), int(readed_parameters[5]), int(readed_parameters[6]), int(readed_parameters[7])

			data_train, data_test, data_val, time_train, time_test, time_val = transform_values(values, self.n_lags, self.time_steps, True, self.train_size, self.test_size, self.val_size, self.batch_size)
			start = timer()
			rmse, _, y, y_hat, y_valset, y_hat_val, dir_acc, self.model, self.scaler = models.model_lstm(data_train, data_test, data_val, self.time_steps, self.lr, self.n_epochs, self.batch_size, self.n_hidden, self.n_features, self.n_lags,
															self.scaler, calc_val_error, calc_test_error, verbosity, saved_model, model_file_name, self.n_rnn, self.n_dense, self.activation, self.drop_p, self.returns, error_type=nn_error_type, prob_model=prob_model)

			print('time elapsed: ', timer() - start)
			print('rmse: %s ' % rmse)
			print('direction accuracy: %f%%' % (dir_acc*100))
			if(verbosity > 1):
				plot_data([y_valset, y_hat_val], ['y', 'y_hat'], 'Validation plot')
				# if(self.time_steps > 1):
				# 	plot_data_lagged_blocks([y_valset[:, 0].ravel(), y_hat_val], ['y', 'y_hat'], 'Validation plot')
				# else:
				# 	plot_data([y_valset, y_hat_val], ['y', 'y_hat'], 'Validation plot')

			if(verbosity > 0):
				# if(self.time_steps > 1):
				# 	plot_data_lagged_blocks([y[:, 0].ravel(), y_hat], ['y', 'y_hat'], 'Test plot')
				# else:
				# 	plot_data([y, y_hat], ['y', 'y_hat'], 'Test plot')
				plot_data([y, y_hat], ['y', 'y_hat'], 'Test plot')
		elif(self.id_model == 1 and self.time_steps == 1):
			if(self.model_name == None): self.model_name = 'randomForest_%s_ret%s_%s_%dts' % (self.predictor_id, self.returns, self.period, self.time_steps)
			model_file_name = self.root + 'models/' + self.model_name + '.joblib'

			if tune:
				best = bayes_optimization(self.id_model, max_evals, values, self.scaler, self.n_features, self.time_steps, self.original, 0, self.model_name, self.returns, self.train_size, self.test_size, self.val_size, self.root)
				self.n_lags, self.n_estimators, self.max_features, self.min_samples = int(best['n_lags']), int(best['n_estimators']), int(best['max_features']), int(best['min_samples'])
				f = open(self.root + 'parameters/optimized_' + self.model_name + '.pars', 'w')
				f.write('%d, %d, %d, %d\n' % (self.n_lags, self.n_estimators, self.max_features, self.min_samples))
				f.close()
			else:
				if os.path.isfile(self.root + 'parameters/optimized_' + self.model_name + '.pars'):
					f = open(self.root + 'parameters/optimized_' + self.model_name + '.pars', 'r')
					lines = f.readlines()
					if(len(lines) > 1):
						raise Exception('File with parameters can\'t have more than 1 line ')
					readed_parameters = lines[0].strip().split(', ')
					self.n_lags, self.n_estimators, self.max_features, self.min_samples = int(readed_parameters[0]), int(readed_parameters[1]), int(readed_parameters[2]), int(readed_parameters[3])

			train_X, test_X, val_X, train_y, test_y, val_y = transform_values(values, self.n_lags, self.time_steps, False, self.train_size, self.test_size, self.val_size)
			start = timer()
			rmse, _, y, y_hat, y_valset, y_hat_val, dir_acc, self.model, self.scaler = models.model_random_forest(train_X, test_X, val_X, train_y, test_y, val_y, self.time_steps, self.n_estimators, self.max_features, self.min_samples,
																	self.n_features, self.n_lags, self.scaler, calc_val_error, calc_test_error, verbosity, saved_model, model_file_name, self.returns)
			print('time elapsed: ', timer() - start)
			print('rmse: %s ' % rmse)
			print('direction accuracy: %f%%' % (dir_acc*100))
			if(verbosity > 1):
				plot_data([y_valset, y_hat_val], ['y', 'y_hat'], 'Validation plot')
			if(verbosity > 0):
				plot_data([y, y_hat], ['y', 'y_hat'], 'Test plot')

		elif(self.id_model == 2 and self.time_steps == 1):
			if(self.model_name == None): self.model_name = 'adaBoost_%s_ret%s_%s_%dts' % (self.predictor_id, self.returns, self.period, self.time_steps)
			model_file_name = self.root + 'models/' + self.model_name + '.joblib'

			if tune:
				best = bayes_optimization(self.id_model, max_evals, values, self.scaler, self.n_features, self.time_steps, self.original, 0, model_file_name, self.returns, self.train_size, self.test_size, self.val_size, self.root)
				self.n_lags, self.n_estimators, self.lr, self.max_depth = int(best['n_lags']), int(best['n_estimators']), best['lr'], best['max_depth']
				f = open(self.root + 'parameters/optimized_' + self.model_name + '.pars', 'w')
				f.write('%d, %d, %f\n' % (self.n_lags, self.n_estimators, self.lr))
				f.close()
			else:
				if os.path.isfile(self.root + 'parameters/optimized_' + self.model_name + '.pars'):
					f = open(self.root + 'parameters/optimized_' + self.model_name + '.pars', 'r')
					lines = f.readlines()
					if(len(lines) > 1):
						raise Exception('File with parameters can\'t have more than 1 line ')
					readed_parameters = lines[0].strip().split(', ')
					self.n_lags, self.n_estimators, self.lr = int(readed_parameters[0]), int(readed_parameters[1]), float(readed_parameters[2])

			train_X, test_X, val_X, train_y, test_y, val_y = transform_values(values, self.n_lags, self.time_steps, False, self.train_size, self.test_size, self.val_size)
			start = timer()
			rmse, _, y, y_hat, y_valset, y_hat_val, dir_acc, self.model, self.scaler = models.model_ada_boost(train_X, test_X, val_X, train_y, test_y, val_y, self.time_steps, self.n_estimators, self.lr, self.max_depth, self.n_features,
																self.n_lags, self.scaler, calc_val_error, calc_test_error, verbosity, saved_model, model_file_name, self.returns)
			print('time elapsed: ', timer() - start)
			print('rmse: %s ' % rmse)
			print('direction accuracy: %f%%' % (dir_acc*100))
			if(verbosity > 1):
				plot_data([y_valset, y_hat_val], ['y', 'y_hat'], 'Validation plot')
			if(verbosity > 0):
				plot_data([y, y_hat], ['y', 'y_hat'], 'Test plot')

		elif(self.id_model == 3 and self.time_steps == 1):
			if(self.model_name == None): self.model_name = 'svm_%s_ret%s_%s_%dts' % (self.predictor_id, self.returns, self.period, self.time_steps)
			model_file_name = self.root + 'models/' + self.model_name + '.joblib'

			if tune:
				best = bayes_optimization(self.id_model, max_evals, values, self.scaler, self.n_features, self.time_steps, self.original, 0, model_file_name, self.returns, self.train_size, self.test_size, self.val_size, self.root)
				self.n_lags = int(best['n_lags'])
				f = open(self.root + 'parameters/optimized_' + self.model_name + '.pars', 'w')
				f.write('%d\n' % (self.n_lags))
				f.close()
			else:
				if os.path.isfile(self.root + 'parameters/optimized_' + self.model_name + '.pars'):
					f = open(self.root + 'parameters/optimized_' + self.model_name + '.pars', 'r')
					lines = f.readlines()
					if(len(lines) > 1):
						raise Exception('File with parameters can\'t have more than 1 line ')
					readed_parameters = lines[0].strip().split(', ')
					self.n_lags = int(readed_parameters[0])

			train_X, test_X, val_X, train_y, test_y, val_y = transform_values(values, self.n_lags, self.time_steps, False, self.train_size, self.test_size, self.val_size)
			start = timer()
			rmse, _, y, y_hat, y_valset, y_hat_val, dir_acc, self.model, self.scaler = models.model_svm(train_X, test_X, val_X, train_y, test_y, val_y, self.time_steps, self.n_features, self.n_lags, self.scaler, calc_val_error,
														calc_test_error, verbosity, saved_model, model_file_name, self.returns)
			print('time elapsed: ', timer() - start)
			print('rmse: %s ' % rmse)
			print('direction accuracy: %f%%' % (dir_acc*100))
			if(verbosity > 1):
				plot_data([y_valset, y_hat_val], ['y', 'y_hat'], 'Validation plot')
			if(verbosity > 0):
				plot_data([y, y_hat], ['y', 'y_hat'], 'Test plot')

		elif(self.id_model == 4 and self.time_steps == 1):
			if(self.model_name == None): self.model_name = 'arima_%s_ret%s_%s_%dts' % (self.predictor_id, self.returns, self.period, self.time_steps)
			model_file_name = self.root + 'models/' + self.model_name + '.pkl'

			if tune:
				best = bayes_optimization(self.id_model, max_evals, values, self.scaler, self.n_features, self.time_steps, self.original, 0, model_file_name, self.returns, self.train_size, self.test_size, self.val_size, self.root)
				self.n_lags, self.d, self.q = int(best['n_lags']), int(best['d']), int(best['q'])
				f = open(self.root + 'parameters/optimized_' + self.model_name + '.pars', 'w')
				f.write('%d, %d, %d\n' % (self.n_lags, self.d, self.q))
				f.close()
			else:
				if os.path.isfile(self.root + 'parameters/optimized_' + self.model_name + '.pars'):
					f = open(self.root + 'parameters/optimized_' + self.model_name + '.pars', 'r')
					lines = f.readlines()
					if(len(lines) > 1):
						raise Exception('File with parameters can\'t have more than 1 line ')
					readed_parameters = lines[0].strip().split(', ')
					self.n_lags, self.d, self.q = int(readed_parameters[0]), int(readed_parameters[1]), int(readed_parameters[2])

			wall = int(len(values)*0.6)
			wall_val= int(len(values)*0.2)
			train_X, test_X, val_X, last_values = values[:wall, :], values[wall:wall+wall_val,:], values[wall+wall_val:-1,:], values[-1,:]
			train_y, test_y, val_y = values[1:wall+1,0], values[wall+1:wall+wall_val+1,0], values[wall+wall_val+1:,0]
			start = timer()
			rmse, _, y, y_hat, y_valset, y_hat_val, dir_acc, self.model, self.scaler = models.model_arima(train_X, test_X, val_X, train_y, test_y, val_y, self.time_steps, self.d, self.q, self.n_features, self.n_lags, self.scaler, calc_val_error,
															calc_test_error, verbosity, saved_model, model_file_name, self.returns)
			print('time elapsed: ', timer() - start)
			print('rmse: %s ' % rmse)
			print('direction accuracy: %f%%' % (dir_acc*100))
			if(verbosity > 1):
				plot_data([y_valset, y_hat_val], ['y', 'y_hat'], 'Validation plot')
			if(verbosity > 0):
				plot_data([y, y_hat], ['y', 'y_hat'], 'Test plot')
		else:
			raise Exception('hyperparameters combination is not in the valid options.')

		return y, y_hat, y_valset, y_hat_val, rmse, dir_acc


	def predict_input(self, new_ob, model_name=None, root=''): # falta incluir Scales, variables seleccionadas(si las hay, periodos, etc. )
		"""
			Función que predice usando el modelo previamente entrenado usando nuevos valores. Con estos nuevos valores hace una iteración de entrenamiento antes de predecir
			Parámetros:
			- new_ob -- Arreglo de numpy, arreglo con la o las nuevas observaciones, sin incluir el output.
			Retorna:
			- pred -- Arreglo de numpy | Lista | Entero, predicciones de los últimos valores dados, predicciones *out of sample*
		"""
		if model_name != None:
			model_ext = {'0': '.h5', '4':'.pkl'}
			model_file_name = root + 'models/' + model_name + model_ext.get(str(self.id_model), '.joblib')
			self.scaler = joblib.load("/".join(model_file_name.split('/')[0:-1] + ['scaler_' + model_file_name.split('/')[-1]]).replace("h5", "joblib"))
			if os.path.isfile(self.root + 'parameters/optimized_' + model_name + '.pars'):
				f =open(self.root + 'parameters/optimized_' + model_name + '.pars', 'r')
				lines = f.readlines()
				if(len(lines) > 1):
					raise Exception('File with parameters can\'t have more than 1 line ')
				readed_parameters = lines[0].strip().split(', ')
				if self.id_model==0:
					self.n_lags = int(readed_parameters[6])
				elif self.id_model==1:
					self.n_lags, self.n_estimators, self.max_features, self.min_samples = int(readed_parameters[0]), int(readed_parameters[1]), int(readed_parameters[2]), int(readed_parameters[3])
				elif self.id_model==2:
					self.activation, self.batch_size, self.drop_p, self.n_dense, self.n_epochs, self.n_hidden, self.n_lags, self.n_rnn = int(readed_parameters[0]), int(readed_parameters[1]), float(readed_parameters[2]), int(readed_parameters[3]), int(readed_parameters[4]), int(readed_parameters[5]), int(readed_parameters[6]), int(readed_parameters[7])
				elif self.id_model==4:
					self.n_lags, self.d, self.q = int(readed_parameters[0]), int(readed_parameters[1]), int(readed_parameters[2])
			if self.id_model==0:
				self.model = tf.keras.models.load_model(model_file_name)
			else:
				self.model = joblib.load(model_file_name)

		if self.model == None:
			raise Exception('No available model. Please train parameters.')

		values = self.scaler.transform(new_ob)

		if self.id_model==0:
			pred_norm = tf_model_forecast(self.model, values, self.n_lags)
			tmp = np.zeros((pred_norm.shape[0], new_ob.shape[1]))
			tmp[:, 0] = pred_norm[:,0]
			pred = self.scaler.inverse_transform(tmp)[:, 0]
		elif(self.id_model==4): # Arima
			last_values =  values
			pred = self.model.predict(len(values)-n_news, len(values) - 1, exog=last_values[:, 1:], endog=last_values[:, 0])
		else:
			X = transform_values_to_predict(values, self.n_lags, 1, False)
			pred_norm = self.model.predict(X)
			# transform last values
			tmp = np.zeros((pred_norm.shape[0], new_ob.shape[1]))
			tmp[:, 0] = pred_norm[:,0]
			pred = self.scaler.inverse_transform(tmp)[:, 0]
		return pred

	def predict_input_panel(self, dataset, model_names, n_output, db, plots=False, root=''): # falta incluir Scales, variables seleccionadas(si las hay, periodos, etc. )
		"Predict input from experts advice"
		n_models = len(model_names)
		next_per_pred = pd.Series(np.zeros(n_models), index=model_names)
		mse = pd.Series(np.zeros(n_models), index=model_names)
		exp_weights = pd.Series(np.zeros(n_models), index=model_names)

		for i in range(n_models):
			model_id = model_names[i]
			vars_ordered, data_trans_method, period, time_steps, n_lags, output_currency = db.model_params(model_id)
			new_ob = dataset.transform(vars_ordered, period=period)[-(n_output+n_lags+time_steps)::].values
			pred = self.predict_input(new_ob, model_name=model_id, root=root)
			predicc_rets = pred[:-time_steps]
			n_pred = len(predicc_rets)
			observed_rets = pd.DataFrame(new_ob).iloc[:,0:1].rolling(window=time_steps).mean().values[-n_pred:,-1]

			se = (predicc_rets - observed_rets)**2
			mse[model_id] = np.sum(se)/n_pred
			cum_se = np.cumsum(se)
			nu = np.sqrt(8*np.log(n_models)/n_pred)
			exp_weights[model_id] = np.exp(-nu*cum_se[-1])
			next_per_pred[model_id] = pred[-1]

		pred_panel = np.sum(exp_weights.values*next_per_pred.values)/np.sum(exp_weights)
		best_model_id = model_names[np.argmax(exp_weights.values)]
		if plots:
			freq = dict(monthly=12, quarterly=4, yearly=1)[period]
			next_per_pred["Panel"] = pred_panel
			ax = (next_per_pred*freq*100).plot.barh()
			ax.set_facecolor("white")
			plt.tight_layout()
			plt.title("Predicciones Próximo Periodo")
			plt.show()

			ax = mse.plot.barh()
			ax.set_facecolor("white")
			plt.tight_layout()
			plt.title("MSE")
			plt.show()

			ax = exp_weights.plot.barh()
			ax.set_facecolor("white")
			plt.tight_layout()
			plt.title("Pesos Exponenciales por Modelo")
			plt.show()

		return next_per_pred, mse, exp_weights, pred_panel, best_model_id


	def save_model(self, db, model_desc="", output_currency=None, data_trans_method="rets"):
 		db.save_model(self.model_name, self.selected_features, self.period, self.time_steps, self.n_lags, output_currency, model_desc, data_trans_method)


if __name__=="__main__":
	pass
