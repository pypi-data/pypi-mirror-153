import numpy as np
import pandas as pd
from . import utils
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def series_to_supervised(series):
	"""
		Función que sirve para pasar la serie al formato de datos y observaciones del próximo tiempo con un solo *lag* o resago de tiempo

		Parámetros:
		- series -- Arreglo de numpy, los datos a procesar

		Retorna:
		- x -- Arreglo de numpy, datos para entrenar
		- y -- Arreglo de numpy, observaciones para comparar las predicciones
	"""
	x = series[:-1, :]
	y = series[1:, 0]
	return x, y

def select_features_stepwise_forward(dataFrame, n_news, original_cols, n_lags=6, time_steps=1, norm_data=False, linear_reg=True, print_df=False):
	"""
		*stepwise selection* de varaibles, utiliza las importancias de un modelo de random forest para clasificar las mejores variables

		Parámetros:
		- dataFrame -- *DataFrame* de pandas, datos de todas las variables que van a ser seleccionadas
		- n_news -- Entero, máximo número de variables que van a ser seleccionadas
		- original_cols -- Lista, lista con los nombres de las columnas originales del problema para reconocer las variables seleccionadas

		Retorna:
		NADA
		(no retorna nada pero escribe las variables seleccioandas en el archivo 'data_selected.csv' en el directorio data)

	"""
	n_features = dataFrame.shape[1]
	dataFrame.columns = original_cols

	# params
	n_news -= 1
	features = set(dataFrame.columns)
	features.remove(list(dataFrame.columns)[0])
	missing = features.copy()
	inside = [list(dataFrame.columns)[0]]
	from sklearn.ensemble import RandomForestRegressor

	if linear_reg:
		while(n_news):
			fts = list(inside)
			best = ''
			ref_loss = np.Inf
			ft = missing
			for ft in missing:
				fts = fts + [ft]
				if norm_data:
					values, scaler = utils.normalize_data(dataFrame[fts].values)
				else:
					values = dataFrame[fts].values

				train_X, test_X, val_X, train_y, test_y, val_y = transform_values(values, n_lags, time_steps, 0, train_size=0.8, test_size=0.2, val_size=0)
				model = LinearRegression()
				model.fit(train_X, train_y.mean(axis=1).ravel())
				pred = model.predict(test_X).ravel()
				loss = mean_squared_error(pred, test_y.mean(axis=1).ravel())
				if(loss <= ref_loss):
					best = fts[-1]
					ref_loss = loss
			inside.append(best)
			missing.remove(best)
			n_news -= 1
	else:
		model = RandomForestRegressor(n_estimators=100)
		while(n_news):
			fts = list(inside)
			best = ''
			best_importance = 0
			ft = missing
			for ft in missing:
				fts = fts + [ft]
				if norm_data:
					values, scaler = utils.normalize_data(dataFrame[fts].values)
				else:
					values = dataFrame[fts].values

				train_X, test_X, val_X, train_y, test_y, val_y = transform_values(values, n_lags, time_steps, 0, train_size=1, test_size=0, val_size=0)
				model.fit(train_X, train_y.mean(axis=1).ravel())
				importances = model.feature_importances_
				if(importances[-1] > best_importance):
					best = fts[-1]
					best_importance = importances[-1]
			inside.append(best)
			missing.remove(best)
			n_news -= 1
	df = dataFrame[inside]
	if print_df:
		df.to_csv('data/data_selected.csv')
	return {'df':df, 'cols':inside}

def select_features_ga(dataFrame, max_vars, original_cols, n_lags=6, time_steps=1, norm_data=False, linear_reg=True, n_generations=1000, print_df=False):
	"""
		Algoritmo genético para selección de variables, utiliza maquinas de soporte vectorial con un kernel de función de base radial para seleccionar las mejores variables
		Este algoritmo es una implementación propia

		Parámetros:
		- dataFrame -- *DataFrame* de pandas, datos de todas las variables que van a ser seleccionadas
		- max_vars -- Entero, número máximo de variables a ser seleccionadas
		- original_cols -- Lista, lista con los nombres de las columnas originales del problema para reconocer las variables seleccionadas

		Retorna:
		NADA
		(no retorna nada pero escribe las variables seleccioandas en el archivo 'data_selected.csv' en el directorio data)
	"""
	import random
	import time
	from matplotlib import pyplot as plt
	from sklearn.svm import SVR
	from tqdm import tqdm
	from termcolor import colored

	n_chars = dataFrame.shape[1]
	n_villagers = max(1, int(n_chars / 2))

	villagers = np.random.randint(2, size=(n_villagers, n_chars))
	villagers = np.array([[bool(villagers[i,j]) for i in range(villagers.shape[0])] for j in range(villagers.shape[1])]).T
	n_best_parents = int(n_villagers / 2)
	historic_losses = []
	print_gen = int(n_generations / 10)

	columns = np.array(dataFrame.columns)
	if linear_reg:
		model = LinearRegression()
	else:
		model = SVR(gamma='scale')
		#model = SVR(kernel='linear')

	print(colored('\n\nseleccionando variables:', 'cyan', attrs=['bold']))
	bar_1 = tqdm(range(n_generations), total=n_generations, unit='iteraciónes')
	for generation in bar_1:
		bar_1.set_description('iteración %d de %d' % (generation + 1, n_generations))
		# start_time = time.time()
		# if((generation + 1) % print_gen == 0): print('generation: %d of %d' % (generation + 1, n_generations))
		losses = []
		for villager in villagers:
			# asure that target variable is in the solution
			villager[0] = True

			cols = columns[villager]
			df = dataFrame[cols]
			if norm_data:
				values, scaler = utils.normalize_data(df.values)
			else:
				values = df.values

			train_X, test_X, val_X, train_y, test_y, val_y = utils.transform_values(values, n_lags, time_steps, 0, train_size=0.8, test_size=0.2, val_size=0)
			model.fit(train_X, train_y.mean(axis=1).ravel())
			pred = model.predict(test_X).ravel()

			loss = mean_squared_error(pred, test_y.mean(axis=1).ravel())
			losses.append(loss)

		losses = np.array(losses)
		temp_losses = losses.copy()
		historic_losses.append(np.min(losses))

		# Select best parents
		parents = []
		for n in range(n_best_parents):
			idx = np.where(temp_losses == np.min(temp_losses))[0][0]
			parents.append(villagers[idx])
			temp_losses[idx] = np.Inf

		# Cross over
		cross_over = []
		one_point = int(n_chars / 2)
		for n in range(n_villagers - n_best_parents):
			tmp = np.zeros(n_chars)
			tmp[:one_point] = parents[n % len(parents)][:one_point]
			tmp[one_point:] = parents[(n + 1) % len(parents)][one_point:]
			cross_over.append(tmp)

		# Mutation
		for i in range(len(cross_over)):
			for j in range(n_chars):
				#if(np.random.rand() < 5.0/n_chars):
				if(np.random.rand() < 1.0/10.0):
					cross_over[i][j] = not(cross_over[i][j])

		# Max vars trim

		for i in range(len(cross_over)):
			suma = np.sum(cross_over[i])
			if(suma > max_vars):
				# how many to drop
				leftover = int(suma - max_vars)
				# take the positives
				positives = [i for i, x in enumerate(cross_over[i]) if x]
				# select the ones to drop
				random.shuffle(positives)
				positives = positives[:leftover]
				# drop those ones
				cross_over[i][positives] = False


		villagers[:n_best_parents] = parents
		villagers[n_best_parents:] = cross_over

	cols = columns[villagers[np.where(losses == np.min(losses))[0][0]]]
	df = dataFrame[cols]
	df.columns = np.array(original_cols)[cols]
	print('se seleccionaron: ', colored('%d variables' % (df.shape[1]), 'green'), end='\n\n\n')

	if print_df:
		df.to_csv('data/data_selected.csv')
	return {'df':df, 'cols':cols}


def select_features_sa(dataFrame, max_vars, original_cols, n_lags=6, time_steps=1, norm_data=False, linear_reg=True, print_df=False):
	"""
		*simulated annealing* para selección de variables

		Parámetros:
		- dataFrame -- *DataFrame* de pandas, datos de todas las varaibles que van a ser seleccionadas
		- max_vars -- Entero, número máximo de variables a ser seleccionadas
		- original_cols -- Lista, lista con los nombres de las columnas originales del problema para reconocer las variables seleccionadas

		Retorna:
		NADA
		(no retorna nada pero escribe las variables seleccioandas en el archivo 'data_selected.csv' en el directorio data)

	"""
	from simanneal import Annealer


	class Sas(Annealer):
		def __init__(self, state, df, norm_data, model):
			self.df = df.copy()
			self.norm_data = norm_data
			self.model = model
			super(Sas, self).__init__(state)

		def move(self):
			"""
				Función que define un paso en el algoritmo
			"""
			idx = np.random.randint(0, len(self.state))
			self.state[idx] = not(self.state[idx])

		def energy(self):
			"""
				Función que define la energía o el error del paso
			"""
			from sklearn.svm import SVR

			cols = list(self.df.columns[self.state])
			df = self.df[cols]

			if self.norm_data:
				values, scaler = utils.normalize_data(df.values)
			else:
				values = df.values

			train_X, test_X, val_X, train_y, test_y, val_y = utils.transform_values(values, n_lags, time_steps, 0, train_size=0.8, test_size=0.2, val_size=0)
			self.model.fit(train_X, train_y)
			pred = model.predict(test_X)

			mse = mean_squared_error(pred, test_y)
			return mse

	n_chars = dataFrame.shape[1]
	initial = np.random.randint(2, size=n_chars)
	initial[0] = 1
	initial = np.array([bool(x) for x in initial])

	if linear_reg:
		model = LinearRegression()
	else:
		model = SVR(gamma='scale')

	ga = Sas(initial, dataFrame, norm_data, model)
	ga.steps = 10000
	ga.copy_strategy = "slice"
	result, mse = ga.anneal()
	cols = np.array(dataFrame.columns)
	cols = cols[result]
	df = dataFrame[cols]
	df.columns = np.array(original_cols)[cols]
	if print_df:
		df.to_csv('data/data_selected.csv')
	return {'df':df, 'cols':cols}
