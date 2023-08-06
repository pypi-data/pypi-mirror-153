from sklearn.metrics import mean_squared_error
from matplotlib import pyplot as plt
import joblib
import numpy as np
import pandas as pd
import math
from . import utils
import tensorflow as tf
import tensorflow_probability as tfp

def calculate_rmse(n_series, n_features, n_lags, X, y, scaler, model):
	"""

		Función para calcular la raíz del error cuadrático medio, solo es utilizado por los algoritmos:
		*Random forest
		*Ada boost
		*SVM (máquinas de soporte vectorial o máquinas de soporte de vectores)
		 Los otros algoritmos tienen su propia forma de calcular este error.

		Parámetros:
		- n_series -- Entero, el número de time steps a predecir en el futuro, en estos metodos es siempre es 1 por ahora, hasta que se implementen para varios time steps
		- n_features -- Entero, el número de *features* con los que se entrena el modelo, también se conocen como variables exogenas
		- n_lags -- Entero, el número de *lags* que se usaron para entrenar, estos *lags* también son conocidos como resagos. Intuitivamente se pueden enterder como una ventana deslizante o como cuantos tiempos atrás en el tiempo tomo en cuenta para hacer mi predicción
		- X -- Arreglo de numpy, los datos con los que se quier hacer la rpedicción para calcular el error
		- y -- Arreglo de numpy, las observaciones contra las cuales se van a comparar las predicciones para luego calcular el error
		- scaler -- Instancia de la clase MinMaxScaler de la libreria sklearn, sirve para escalar los datos y devolverlos a la escala original posteriormente. En esta función se utiliza para revertir el escalamiento y obtener los datos reales
		- model -- Modelo de sklearn, el modelo entrenado con el cual se van a realizar las predicciones



		Retorna:
		- inv_y -- Arreglo de numpy, observaciones en la escala real
		- inv_yhat -- Arreglo de numpy, predicciones en la escala real
		- rmse -- Flotante, raíz del error curadrático medio entre las observaciones y las predicciones

	"""

	yhat = model.predict(X)
	inv_yhat = inverse_transform(yhat, scaler, n_features)
	inv_y = inverse_transform(y, scaler, n_features)

	# calculate RMSE
	rmse = math.sqrt(mean_squared_error(inv_y, inv_yhat))
	return inv_y, inv_yhat, rmse

def predict_last(n_series, n_features, n_lags, X, scaler, model, dim):
	"""

		Función para predecir los últimos valores y sacar la predicción que se le retorna al usuario

		Parámetros:
		- n_series -- Entero, el número de time steps a predecir en el futuro, en estos metodos es siempre es 1 por ahora, hasta que se implementen para varios time steps
		- n_features -- Entero, el número de *features* con los que se entrena el modelo, también se conocen como variables exogenas
		- n_lags -- Entero, el número de *lags* que se usaron para entrenar
		- X -- Arreglo de numpy, los datos con los que se quier hacer la rpedicción para calcular el error
		- scaler -- Instancia de la clase MinMaxScaler de la libreria sklearn, sirve para escalar los datos y devolverlos a la escala original posteriormente
		- model -- Modelo de sklearn, el modelo entrenado con el cual se van a realizar las predicciones
		- dim -- Booleano, Parámetro para controlar los problemas de formato, si se especifica este parámetro en True se agrega una dimensión extra a los datos.

		Retorna:
		- inv_yhat -- Arreglo de numpy, predicción de los últimos valores en escala real

	"""
	if(dim):
		X = np.expand_dims(X, axis=0)
	yhat = model.predict(X)
	if(not dim):
		yhat = yhat.reshape(-1, 1) # only for no dim
	Xs = np.ones((X.shape[0], n_lags * n_features))

	inv_yhats = []
	for i in range(n_series):
		inv_yhat = np.concatenate((Xs[:, -(n_features - 1):], yhat[:, i].reshape(-1, 1)), axis=1)
		inv_yhat = scaler.inverse_transform(inv_yhat)

		inv_yhat = inv_yhat[:, -1]
		inv_yhats.append(inv_yhat)

	inv_yhat = np.array(inv_yhats).T
	return inv_yhat

############################# LSTM ####################################
def weighted_mse_returns(yTrue, yPred):
	"""
		Función para calcular el error personalizado del modelo LSTM, este error personalizado es la raíz del error cuadrático medio dandole más importancia a los primeros *lags*

		Parámetros:
		- yTrue -- valores con los cuales e va a comaprar las predicciones
		- yPred -- predicciones para calcular el error

		Retorna:
		- [valor] -- error cuadrático medio ponderado
	"""
	from keras import backend as K

	ones = K.ones_like(yTrue[0,:]) # a simple vector with ones shaped as (n_series,)
	idx = K.cumsum(ones) # similar to a 'range(1,n_series+1)'

	std = K.std(yTrue)
	mean = K.mean(K.abs(yTrue))

	# weighted rmse
	l1 = K.abs(K.sqrt(K.mean((1/idx)*K.square(yTrue-yPred)))-mean)/mean
	# difference of standard deviation, for fluctuation (prevent under fitting)
	l2 = K.abs(std - K.std(yPred))/std
	# direction accuracy
	l3 = K.mean(K.cast(K.not_equal(K.sign(yTrue), K.sign(yPred)), dtype='float32'))

	return l1 + l2

def weighted_mse(yTrue, yPred):
	"""
		Función para calcular el error personalizado del modelo LSTM, este error personalizado es la raíz del error cuadrático medio dandole más importancia a los primeros *lags*

		Parámetros:
		- yTrue -- valores con los cuales e va a comaprar las predicciones
		- yPred -- predicciones para calcular el error

		Retorna:
		- [valor] -- error cuadrático medio ponderado
	"""
	from keras import backend as K

	ones = K.ones_like(yTrue[0,:]) # a simple vector with ones shaped as (n_series,)
	idx = K.cumsum(ones) # similar to a 'range(1,n_series+1)'

	std = K.std(yTrue)
	mean = K.mean(K.abs(yTrue))

	# weighted rmse
	l1 = K.abs(K.sqrt(K.mean((1/idx)*K.square(yTrue-yPred)))-mean)/mean
	# difference of standard deviation, for fluctuation (prevent under fitting)
	l2 = K.abs(std - K.std(yPred))/std
	# direction accuracy
	l3 = K.mean(K.cast(K.not_equal(K.sign(yTrue), K.sign(yPred)), dtype='float32'))
	return l1 + l2 +  l3



def model_lstm(data_train, data_test, data_val, n_series, lr, n_epochs, batch_size, n_hidden, n_features, n_lags, scaler, calc_val_error, calc_test_error, verbosity, saved_model, model_file_name, n_rnn, n_dense, activation, drop_p, returns, error_type="mse", prob_model=False):
	"""
		Función para crear, entrenar y calcular el error del modelo LSTM, también sirve para predecir
		Este modelo está hecho en Keras solamente tiene dos capas una de LSTM y otra Densa o totalmente conectada, utiliza el optimizador Adam y la función de error es personalizada para darle mayor importancia a los priemros *lags*
		El modelo inicialmente entrena con data de entrenamiento para evaluar desempeno sobre muestra de testing y validation. Posteriormente entrena sobre todos los datos  guarda el modelo.

		Parámetros:
		- train_X -- Arreglo de numpy, datos de entrenamiento
		- val_X -- Arreglo de numpy, datos de validación
		- test_X -- Arreglo de numpy, datos de *testing*
		- train_y -- Arreglo de numpy, observaciones de entrenamiento
		- val_y -- Arreglo de numpy, observaciones de validación
		- test_y -- Arreglo de numpy, observaciones de *testing*
		- n_series -- Entero, el número de time steps a predecir en el futuro
		- n_epochs -- Entero, número de epocas de entrenamiento
		- batch_size -- Entero, tamaño de los *bathcs* de entrenamiento
		- n_hidden -- Entero, número de estados escondidos de la red neuronal LSTM
		- n_features -- Entero, el número de *features* con los que se entrena el modelo, también se conocen como variables exogenas
		- n_lags -- Entero, el número de *lags* que se usaran para entrenar
		- scaler -- Instancia de la clase MinMaxScaler de la libreria sklearn, sirve para escalar los datos y devolverlos a la escala original posteriormente
		- calc_val_error -- Booleano, indica si se calcula el error de validación, si no se calcula se devuelve None en este campo
		- calc_test_error -- Booleano, indica si se calcula el error de *testing*, si no se calcula se devuelve None en este campo
		- verbosity -- Entero, nivel de verbosidad de la ejecución del modelo, entre más alto más información se mostrará el límite es 4 y debe ser mayor o igual a 0
		- saved_model -- Booleano, indica si se desea entrenar el modelo o cargar uno guardado. Si True se carga un modelo guardado, si False se entrena un nuevo modelo.
		- model_file_name -- *String*, nombre del archivo donde se guardará y/o se cargará el modelo.
		- n_rnn -- Entero, cantidad de redes neuronales recurrentes a usar antes de la por default
		- n_dense -- Entero, cantidad de capas densas a usar antes de la capa densa de salida
		- activation -- Entero, id de la activación que se quiere usar 0 para tanh, 1 para relu, se pueden agregar más
		- drop_p -- Flotante, porcentaje de las neuronas a volver 0 en la capa de dropout número entre 0 y 1
		- returns -- Booleano, indica si se está trabajando con retornos o no (serie diferenciada). True es que si se trabaja con retornos.

		Retorna:
		- rmse -- Flotante, raíz del error medio cuadrático de *testing*; retorna None si calc_test_error es False
		- rmse_val -- Flotante, raíz del error medio cuadrático de validación; retorna None si calc_val_error es False
		- test_y -- Arreglo de numpy, observaciones de la particón de *testing* en escala real
		- y_hat_test -- Arreglo de numpy, predicciones de la partición de *testing* en escala real
		- val_y -- Arreglo de numpy, observaciones de la particón de validación en escala real
		- y_hat_val -- Arreglo de numpy, predicciones de la partición de validación en escala real
		- dir_acc-- Flotante, % de acierto en la dirección
		- model -- Modelo, instancia de modelo de keras, retorna el modeo entrenado
	"""

	n_out = n_series

	if(not saved_model or not os.path.isfile(model_file_name)):
		verbose_dict = {0:0, 1:2, 2:1}
		# activation_dict = {0:'tanh', 1:'relu'}
		verbose = 0 if verbosity < 3 else min(verbosity - 2, 2)
		verbose = verbose_dict[verbose]
		train_set = utils.tf_windowed_dataset(data_train, n_lags, n_series, batch_size)
		if prob_model:
			tfd = tfp.distributions
			tfpl = tfp.layers
			model = tf.keras.models.Sequential([
			  # tf.keras.layers.Conv1D(filters=32, kernel_size=5,strides=1, padding="causal",activation="relu",input_shape=[None, 1]),
			  tf.keras.layers.LSTM(n_hidden, return_sequences=False, dropout=drop_p, recurrent_dropout=0, input_shape=[None, n_features]),
			  tf.keras.layers.Dense(tfpl.IndependentNormal.params_size(n_out)),
			  tfpl.IndependentNormal(n_out, convert_to_tensor_fn=tfd.Distribution.mean)
			])
		else:
			model = tf.keras.models.Sequential([
			  # tf.keras.layers.Conv1D(filters=32, kernel_size=5,strides=1, padding="causal",activation="relu",input_shape=[None, 1]),
			  tf.keras.layers.LSTM(n_hidden, return_sequences=False, dropout=drop_p, recurrent_dropout=0, input_shape=[None, n_features]),
			  tf.keras.layers.Dense(n_out)#,
			])

		tf.keras.backend.clear_session()
		opt = tf.keras.optimizers.Adam(lr=lr)

		if prob_model:
			def nll(y_true, y_pred):
  				return -y_pred.log_prob(y_true)
			model.compile(loss=nll, optimizer=opt)
		else:
			if error_type[:3]=="mse":
				model.compile(loss=tf.keras.losses.MeanSquaredError(), optimizer=opt, metrics=["mae"])
			elif error_type[:3]=="mae":
				model.compile(loss=tf.keras.losses.MeanAbsoluteError(), optimizer=opt, metrics=["mae"])
			else:
				model.compile(loss=tf.keras.losses.Huber(), optimizer=opt, metrics=["mae"])
		history = model.fit(train_set, epochs=n_epochs, verbose=False)
		if(verbosity > 0):
			plt.figure()
			plt.plot(history.history['loss'])
			#plt.plot(history.history['val_loss'])
			#plt.suptitle('Training loss')
			# change window position
			mngr = plt.get_current_fig_manager()
			import matplotlib
			backend = matplotlib.get_backend()
			if backend == 'TkAgg':
				mngr.window.wm_geometry("+%d+%d" % (25, 55))
			elif backend == 'WXAgg':
				mngr.window.SetPosition((25, 55))
			#else:
				# This works for QT and GTK
				# You can also use window.setGeometry
				# mngr.window.move(25, 55)

		data_all = np.vstack([data_train, data_test, data_val])
		rnn_forecast = utils.tf_model_forecast(model, data_all, n_lags)
		test_y = pd.DataFrame(data_all).iloc[:,0:1].rolling(window=n_series).mean().values[(-len(data_test)-len(data_val)):-len(data_val),-1]
		val_y = pd.DataFrame(data_all).iloc[:,0:1].rolling(window=n_series).mean().values[-len(data_val):,-1]
		y_hat_val = rnn_forecast[(-len(data_val)-n_series):-n_series][:,-1]
		y_hat_test = rnn_forecast[(-len(data_test)-len(data_val)-n_series):(-n_series-len(data_val))][:,-1]
		if(calc_val_error):
			rmse_val = tf.keras.metrics.mean_squared_error(val_y, y_hat_val).numpy()
		else:
			rmse_val = None

		if(calc_test_error):
			# for test
			rmse = rmse_val = tf.keras.metrics.mean_squared_error(test_y, y_hat_test).numpy()
		else:
			rmse = None

		train_set = utils.tf_windowed_dataset(data_all, n_lags, n_series, batch_size)
		model = tf.keras.models.Sequential([
		  tf.keras.layers.LSTM(n_hidden, return_sequences=False, dropout=drop_p, recurrent_dropout=0, input_shape=[None, n_features]),
		  tf.keras.layers.Dense(n_out)#,
		])
		opt = tf.keras.optimizers.Adam(lr=lr)
		#model.compile(loss=tf.keras.losses.MeanAbsoluteError(), optimizer=opt, metrics=["mae"])
		if error_type[:3]=="mse":
			model.compile(loss=tf.keras.losses.MeanSquaredError(), optimizer=opt, metrics=["mae"])
		elif error_type[:3]=="mae":
			model.compile(loss=tf.keras.losses.MeanAbsoluteError(), optimizer=opt, metrics=["mae"])
		else:
			model.compile(loss=tf.keras.losses.Huber(), optimizer=opt, metrics=["mae"])

		history = model.fit(train_set, epochs=n_epochs)#, verbose=False)
		model.save(model_file_name)
		print("/".join(model_file_name.split('/')[0:-1] + ['scaler_' + model_file_name.split('/')[-1]]).replace("h5", "joblib"))
		print(scaler)
		joblib.dump(scaler, "/".join(model_file_name.split('/')[0:-1] + ['scaler_' + model_file_name.split('/')[-1]]).replace("h5", "joblib"))

		if returns:
			dir_acc = utils.get_returns_direction_accuracy(val_y.ravel(), y_hat_val.ravel())
		else:
			dir_acc = utils.get_direction_accuracy(val_y.ravel(), y_hat_val.ravel())

		if verbosity > 0:
			plt.figure()
			plt.plot(history.history['loss'])
			plt.title('All data loss')
			plt.show()

	else:
		from keras.models import load_model
		model = load_model(model_file_name, custom_objects={'weighted_mse': weighted_mse})
		scaler = joblib.load("/".join(model_file_name.split('/')[0:-1] + ['scaler_' + model_file_name.split('/')[-1]]).replace("h5", "joblib"))

		rmse = None
		rmse_val = None
		test_y = None
		y_hat_test = None
		val_y = None
		y_hat_val = None
		dir_acc = None

	return rmse, rmse_val, test_y, y_hat_test, val_y, y_hat_val, dir_acc, model, scaler



###################### random forest ##########################
def model_random_forest(train_X, test_X, val_X, train_y, test_y, val_y, n_series, n_estimators, max_features, min_samples, n_features, n_lags, scaler, calc_val_error, calc_test_error, verbosity, saved_model, model_file_name, returns):
	"""

		Función para crear, entrenar y calcular el error del modelo *random forest*, también sirve para predecir
		Este modelo se crea con la libreria sklearn con el algoritmo RandomForestregressor

		Parámetros:
		- train_X -- Arreglo de numpy, datos de entrenamiento
		- val_X -- Arreglo de numpy, datos de validación
		- test_X -- Arreglo de numpy, datos de *testing*
		- train_y -- Arreglo de numpy, observaciones de entrenamiento
		- val_y -- Arreglo de numpy, observaciones de validación
		- test_y -- Arreglo de numpy, observaciones de *testing*
		- n_series -- Entero, el número de time steps a predecir en el futuro
		- n_estimators -- Entero, número de árboles que se generaran en el bosque
		- max_features -- Entero, número máximo de *features* que tendrá cada árbol dentro del bosque
		- min_samples -- Entero, número minimo de ejemplos encesarios para que la partición sea una hoja del árbol
		- n_features -- Entero, el número de *features* con los que se entrena el modelo, también se conocen como variables exogenas
		- n_lags -- Entero, el número de *lags* que se usaran para entrenar
		- scaler -- Instancia de la clase MinMaxScaler de la libreria sklearn, sirve para escalar los datos y devolverlos a la escala original posteriormente
		- calc_val_error -- Booleano, indica si se calcula el error de validación, si no se calcula se devuelve None en este campo
		- calc_test_error -- Booleano, indica si se calcula el error de *testing*, si no se calcula se devuelve None en este campo
		- verbosity -- Entero, nivel de verbosidad de la ejecución del modelo, entre más alto más información se mostrará el límite es 4 y debe ser mayor o igual a 0
		- saved_model -- Booleano, indica si se desea entrenar el modelo o cargar uno guardado. Si True se carga un modelo guardado, si False se entrena un nuevo modelo.
		- model_file_name -- *String*, nombre del archivo donde se guardará y/o se cargará el modelo
		- returns -- Booleano, indica si se está trabajando con retornos o no (serie diferenciada). True es que si se trabaja con retornos.

		Retorna:
		- rmse -- Flotante, raíz del error medio cuadrático de *testing*; retorna None si calc_test_error es False
		- rmse_val -- Flotante, raíz del error medio cuadrático de validación; retorna None si calc_val_error es False
		- y -- Arreglo de numpy, observaciones de la particón de *testing* en escala real
		- y_hat -- Arreglo de numpy, predicciones de la partición de *testing* en escala real
		- y_valset -- Arreglo de numpy, observaciones de la particón de validación en escala real
		- y_hat_val -- Arreglo de numpy, predicciones de la partición de validación en escala real
		- [valor] -- Flotante, % de acierto en la dirección

	"""
	if(not saved_model or not os.path.isfile(model_file_name)):
		# print('training...')
		from sklearn.ensemble import RandomForestRegressor
		dir_acc = None

		verbose = 0 if verbosity < 3 else min(verbosity - 2, 2)
		model = RandomForestRegressor(n_estimators=n_estimators, max_features=max_features, min_samples_leaf=min_samples, n_jobs=-1, verbose=verbose)
		model.fit(train_X, train_y.ravel())
		joblib.dump(model, model_file_name)
		joblib.dump(scaler, "/".join(model_file_name.split('/')[0:-1] + ['scaler_' + model_file_name.split('/')[-1]]))
		if(calc_val_error):
			y_valset, y_hat_val, rmse_val = calculate_rmse(n_series, n_features, n_lags, val_X, val_y, scaler, model)
			if(returns):
				dir_acc_valset = utils.get_returns_direction_accuracy(y_valset.ravel(), y_hat_val.ravel())
			else:
				dir_acc_valset = utils.get_direction_accuracy(y_valset.ravel(), y_hat_val.ravel())
		else:
			rmse_val, y_valset, y_hat_val = None, None, None

		if(calc_test_error):
			y, y_hat, rmse = calculate_rmse(n_series, n_features, n_lags, test_X, test_y, scaler, model)
			if(returns):
				dir_acc = utils.get_returns_direction_accuracy(y.ravel(), y_hat.ravel())
			else:
				dir_acc = utils.get_direction_accuracy(y.ravel(), y_hat.ravel())

		else:
			y, y_hat, rmse = calculate_rmse(n_series, n_features, n_lags, test_X, test_y, scaler, model)
			rmse = None

	else:
		model = joblib.load(model_file_name)
		scaler = joblib.load("/".join(model_file_name.split('/')[0:-1] + ['scaler_' + model_file_name.split('/')[-1]]))
		rmse = None
		rmse_val = None
		test_y = None
		y_hat_test = None
		val_y = None
		y_hat_val = None
		dir_acc = None

	return rmse, rmse_val, y, y_hat, y_valset, y_hat_val, dir_acc, model, scaler

####################### ada boost ###############################
def model_ada_boost(train_X, test_X, val_X, train_y, test_y, val_y, n_series, n_estimators, lr, max_depth, n_features, n_lags, scaler, calc_val_error, calc_test_error, verbosity, saved_model, model_file_name, returns):

	"""
		Función para crear, entrenar y calcular el error del modelo *ada boost*, también sirve para predecir
		Este modelo se construye con la libreria sklearn con el algoritmo AdaBoostRegressor y este ada boost se contruye a partir de árboles de decisión

		Parámetros:
		- train_X -- Arreglo de numpy, datos de entrenamiento
		- val_X -- Arreglo de numpy, datos de validación
		- test_X -- Arreglo de numpy, datos de *testing*
		- train_y -- Arreglo de numpy, observaciones de entrenamiento
		- val_y -- Arreglo de numpy, observaciones de validación
		- test_y -- Arreglo de numpy, observaciones de *testing*
		- n_series -- Entero, el número de time steps a predecir en el futuro
		- n_estimators -- Entero, número de árboles que se generaran en el bosque
		- lr -- Flotante, tasa de entrenamiento del modelo
		- max_depth -- Entero, profundida máxima del árbol de decisión que se utiliza para construir el *ada boost*
		- n_features -- Entero, el número de *features* con los que se entrena el modelo, también se conocen como variables exogenas
		- n_lags -- Entero, el número de *lags* que se usaran para entrenar
		- scaler -- Instancia de la clase MinMaxScaler de la libreria sklearn, sirve para escalar los datos y devolverlos a la escala original posteriormente
		- calc_val_error -- Booleano, indica si se calcula el error de validación, si no se calcula se devuelve None en este campo
		- calc_test_error -- Booleano, indica si se calcula el error de *testing*, si no se calcula se devuelve None en este campo
		- verbosity -- Entero, nivel de verbosidad de la ejecución del modelo, entre más alto más información se mostrará el límite es 4 y debe ser mayor o igual a 0
		- saved_model -- Booleano, indica si se desea entrenar el modelo o cargar uno guardado. Si True se carga un modelo guardado, si False se entrena un nuevo modelo.
		- model_file_name -- *String*, nombre del archivo donde se guardará y/o se cargará el modelo
		- returns -- Booleano, indica si se está trabajando con retornos o no (serie diferenciada). True es que si se trabaja con retornos.

		Retorna:
		- rmse -- Flotante, raíz del error medio cuadrático de *testing*; retorna None si calc_test_error es False
		- rmse_val -- Flotante, raíz del error medio cuadrático de validación; retorna None si calc_val_error es False
		- y -- Arreglo de numpy, observaciones de la particón de *testing* en escala real
		- y_hat -- Arreglo de numpy, predicciones de la partición de *testing* en escala real
		- y_valset -- Arreglo de numpy, observaciones de la particón de validación en escala real
		- y_hat_val -- Arreglo de numpy, predicciones de la partición de validación en escala real
		- [valor] -- Flotante, % de acierto en la dirección

	"""
	if(not saved_model or not os.path.isfile(model_file_name)):
		# print('training...')
		from sklearn.ensemble import AdaBoostRegressor
		from sklearn.tree import DecisionTreeRegressor

		model = AdaBoostRegressor(DecisionTreeRegressor(max_depth=max_depth), n_estimators=n_estimators, learning_rate=lr)
		model.fit(train_X, train_y.ravel())
		joblib.dump(model, model_file_name)
		joblib.dump(scaler, "/".join(model_file_name.split('/')[0:-1] + ['scaler_' + model_file_name.split('/')[-1]]))
		if(calc_val_error):
			y_valset, y_hat_val, rmse_val = calculate_rmse(n_series, n_features, n_lags, val_X, val_y, scaler, model)
		else:
			rmse_val, y_valset, y_hat_val = None, None, None

		if(calc_test_error):
			y, y_hat, rmse = calculate_rmse(n_series, n_features, n_lags, test_X, test_y, scaler, model)
		else:
			y, y_hat, rmse = calculate_rmse(n_series, n_features, n_lags, test_X, test_y, scaler, model)
			rmse = None

		if(returns):
			dir_acc = utils.get_returns_direction_accuracy(y_valset.ravel(), y_hat_val.ravel())
		else:
			dir_acc = utils.get_direction_accuracy(y_valset.ravel(), y_hat_val.ravel())

	else:
		model = joblib.load(model_file_name)
		scaler = joblib.load("/".join(model_file_name.split('/')[0:-1] + ['scaler_' + model_file_name.split('/')[-1]]))
		rmse = None
		rmse_val = None
		test_y = None
		y_hat_test = None
		val_y = None
		y_hat_val = None
		dir_acc = None

	return rmse, rmse_val, y, y_hat, y_valset, y_hat_val, dir_acc, model, scaler

####################################### SVM ##############################
def model_svm(train_X, test_X, val_X, train_y, test_y, val_y, n_series, n_features, n_lags, scaler, calc_val_error, calc_test_error, verbosity, saved_model, model_file_name, returns):
	"""

		Función para crear, entrenar y calcular el error del modelo SVM, también sirve para predecir
		Este modelo se construye con la libreria sklearn con el algoritmo SVR (*support vector regressor*) el kernel actual es polinomial de grado 1 por que dió mejores resultados
		con un dataset con el que probamos pero este se peude cambiar en el futuro

		Parámetros:
		- train_X -- Arreglo de numpy, datos de entrenamiento
		- val_X -- Arreglo de numpy, datos de validación
		- test_X -- Arreglo de numpy, datos de *testing*
		- train_y -- Arreglo de numpy, observaciones de entrenamiento
		- val_y -- Arreglo de numpy, observaciones de validación
		- test_y -- Arreglo de numpy, observaciones de *testing*
		- n_series -- Entero, el número de time steps a predecir en el futuro
		- n_features -- Entero, el número de *features* con los que se entrena el modelo, también se conocen como variables exogenas
		- n_lags -- Entero, el número de *lags* que se usaran para entrenar
		- scaler -- Instancia de la clase MinMaxScaler de la libreria sklearn, sirve para escalar los datos y devolverlos a la escala original posteriormente
		- calc_val_error -- Booleano, indica si se calcula el error de validación, si no se calcula se devuelve None en este campo
		- calc_test_error -- Booleano, indica si se calcula el error de *testing*, si no se calcula se devuelve None en este campo
		- verbosity -- Entero, nivel de verbosidad de la ejecución del modelo, entre más alto más información se mostrará el límite es 4 y debe ser mayor o igual a 0
		- saved_model -- Booleano, indica si se desea entrenar el modelo o cargar uno guardado. Si True se carga un modelo guardado, si False se entrena un nuevo modelo.
		- model_file_name -- *String*, nombre del archivo donde se guardará y/o se cargará el modelo
		- returns -- Booleano, indica si se está trabajando con retornos o no (serie diferenciada). True es que si se trabaja con retornos.

		Retorna:
		- rmse -- Flotante, raíz del error medio cuadrático de *testing*; retorna None si calc_test_error es False
		- rmse_val -- Flotante, raíz del error medio cuadrático de validación; retorna None si calc_val_error es False
		- y -- Arreglo de numpy, observaciones de la particón de *testing* en escala real
		- y_hat -- Arreglo de numpy, predicciones de la partición de *testing* en escala real
		- y_valset -- Arreglo de numpy, observaciones de la particón de validación en escala real
		- y_hat_val -- Arreglo de numpy, predicciones de la partición de validación en escala real
		- [valor] -- Flotante, % de acierto en la dirección

	"""
	if(not saved_model or not os.path.isfile(model_file_name)):
		# print('training...')
		from sklearn.svm import SVR

		verbose = 0 if verbosity < 3 else min(verbosity - 2, 2)
		# model = SVR(kernel='poly', degree=1, gamma='scale', verbose=verbose)
		model = SVR(verbose=verbose, gamma='auto')
		model.fit(train_X, train_y.ravel())
		joblib.dump(model, model_file_name)
		joblib.dump(scaler, "/".join(model_file_name.split('/')[0:-1] + ['scaler_' + model_file_name.split('/')[-1]]))
		if(calc_val_error):
			y_valset, y_hat_val, rmse_val = calculate_rmse(n_series, n_features, n_lags, val_X, val_y, scaler, model)
		else:
			rmse_val, y_valset, y_hat_val = None, None, None

		if(calc_test_error):
			y, y_hat, rmse = calculate_rmse(n_series, n_features, n_lags, test_X, test_y, scaler, model)
		else:
			y, y_hat, rmse = calculate_rmse(n_series, n_features, n_lags, test_X, test_y, scaler, model)
			rmse = None

		if(returns):
			dir_acc = utils.get_returns_direction_accuracy(y_valset.ravel(), y_hat_val.ravel())
		else:
			dir_acc = utils.get_direction_accuracy(y_valset.ravel(), y_hat_val.ravel())

	else:
		model = joblib.load(model_file_name)
		scaler = joblib.load("/".join(model_file_name.split('/')[0:-1] + ['scaler_' + model_file_name.split('/')[-1]]))
		rmse = None
		rmse_val = None
		test_y = None
		y_hat_test = None
		val_y = None
		y_hat_val = None
		dir_acc = None

	return rmse, rmse_val, y, y_hat, y_valset, y_hat_val, dir_acc, model, scaler

###################################### ARIMA #########################################
def model_arima(train_X, test_X, val_X, train_y, test_y, val_y, n_series, d, q, n_features, n_lags, scaler, calc_val_error, calc_test_error, verbosity, saved_model, model_file_name, returns):
	"""

		Función para crear, entrenar y calcular el error del modelo ARIMA, también sirve para predecir
		Este modelo se contruye con la libreria statsmodels con el algoritmo SARIMAX por que proporciona mayor estabilidad y por que el problema contiene variables exogenas
		la implementación de la libreria es un poco enredada y la documentación no es la mejor, pero en python en cuanto a modelos ARIMA es de lo mejor que hay
		Cuando se introducen parámetros que no se pueden calcular matematicamente por el modelo arima se devuelven errores de 90000000000 en validación y *testing* y las demás
		variables se retornan en None

		Parámetros:
		- train_X -- Arreglo de numpy, datos de entrenamiento
		- val_X -- Arreglo de numpy, datos de validación
		- test_X -- Arreglo de numpy, datos de *testing*
		- train_y -- Arreglo de numpy, observaciones de entrenamiento
		- val_y -- Arreglo de numpy, observaciones de validación
		- test_y -- Arreglo de numpy, observaciones de *testing*
		- n_series -- Entero, el número de time steps a predecir en el futuro
		- d -- Entero, cantidad de diferenciaciones necesarias para que la serie a predecir sea estacionaria
		- q -- Entero, parámetro para el componente de media móvil del modelo
		- n_features -- Entero, el número de *features* con los que se entrena el modelo, también se conocen como variables exogenas
		- n_lags -- Entero, el número de *lags* que se usaran para entrenar
		- scaler -- Instancia de la clase MinMaxScaler de la libreria sklearn, sirve para escalar los datos y devolverlos a la escala original posteriormente
		- calc_val_error -- Booleano, indica si se calcula el error de validación, si no se calcula se devuelve None en este campo
		- calc_test_error -- Booleano, indica si se calcula el error de *testing*, si no se calcula se devuelve None en este campo
		- verbosity -- Entero, nivel de verbosidad de la ejecución del modelo, entre más alto más información se mostrará el límite es 4 y debe ser mayor o igual a 0
		- saved_model -- Booleano, indica si se desea entrenar el modelo o cargar uno guardado. Si True se carga un modelo guardado, si False se entrena un nuevo modelo.
		- model_file_name -- *String*, nombre del archivo donde se guardará y/o se cargará el modelo
		- returns -- Booleano, indica si se está trabajando con retornos o no (serie diferenciada). True es que si se trabaja con retornos.

		Retorna:
		- rmse -- Flotante, raíz del error medio cuadrático de *testing*; retorna None si calc_test_error es False
		- rmse_val -- Flotante, raíz del error medio cuadrático de validación; retorna None si calc_val_error es False
		- test_y -- Arreglo de numpy, observaciones de la particón de *testing* en escala real
		- y_hat -- Arreglo de numpy, predicciones de la partición de *testing* en escala real
		- val_y -- Arreglo de numpy, observaciones de la particón de validación en escala real
		- y_hat_val -- Arreglo de numpy, predicciones de la partición de validación en escala real
		- inv_yhat[-1] -- arreglo de numpy, predicción de los últimos valores
		- [valor] -- Flotante, % de acierto en la dirección

	"""
	from statsmodels.tsa.statespace.sarimax import SARIMAX
	from statsmodels.tsa.statespace.mlemodel import MLEResults
	from numpy.linalg.linalg import LinAlgError
	import warnings

	y_hat = []
	y_hat_val = []
	try:
		if(not saved_model or not os.path.isfile(model_file_name)):
			# print('training...')
			verbose = 0 if verbosity < 3 else verbosity - 2
			model = SARIMAX(train_X[:, 0], exog=train_X[:, 1:], order=(n_lags, d, q), enforce_invertibility=False, enforce_stationarity=False, dynamic=False)
			model_fit = model.fit(disp=verbose, iprint=verbose, maxiter=200, method='powell')
			model_fit.save(model_file_name)

			final_endogs = np.append(test_X[:, 0], val_X[:, 0], axis=0)
			final_exogs = np.append(test_X[:, 1:], val_X[:, 1:], axis=0)
			diff_train_original_model = len(train_X) - model_fit.nobs
			if(diff_train_original_model > 0):
				final_endogs = np.insert(final_endogs, 0, train_X[-diff_train_original_model:, 0], axis=0)
				final_exogs = np.insert(final_exogs, 0, train_X[-diff_train_original_model:, 1:], axis=0)

			output = model_fit.predict(len(train_X), len(train_X) + len(test_X) + len(val_X) - 1, exog=final_exogs, endog=final_endogs)
			y_hat.extend(output[:len(test_y)])
			y_hat_val.extend(output[len(test_y):len(test_y)+len(val_y)])

			if(calc_val_error):
				tmp = np.zeros((len(y_hat_val), n_features))
				tmp[:, 0] = y_hat_val
				y_hat_val = scaler.inverse_transform(tmp)[:, 0]

				tmp = np.zeros((len(val_y), n_features))
				tmp[:, 0] = val_y
				val_y = scaler.inverse_transform(tmp)[:, 0]

				rmse_val = math.sqrt(mean_squared_error(val_y, y_hat_val))
			else:
				rmse_val, val_y, y_hat_val = None, None, None

			if(calc_test_error):
				tmp = np.zeros((len(y_hat), n_features))
				tmp[:, 0] = y_hat
				y_hat = scaler.inverse_transform(tmp)[:, 0]

				tmp = np.zeros((len(test_y), n_features))
				tmp[:, 0] = test_y
				test_y = scaler.inverse_transform(tmp)[:, 0]

				rmse = math.sqrt(mean_squared_error(test_y, y_hat))
			else:
				rmse, test_y, y_hat = None, None, None

			last = output[-1]
			last = last.reshape(-1, 1)
			Xs = np.ones((last.shape[0], n_lags * n_features))
			inv_yhat = np.concatenate((last, Xs[:, -(n_features - n_series):]), axis=1)
			inv_yhat = scaler.inverse_transform(inv_yhat)

			inv_yhat = inv_yhat[:, 0:n_series]

			if(returns):
				dir_acc = utils.get_returns_direction_accuracy(val_y.ravel(), y_hat_val.ravel())
			else:
				dir_acc = utils.get_direction_accuracy(val_y.ravel(), y_hat_val.ravel())

			# train with whole data

			#model = SARIMAX(whole_X[:, 0], exog=whole_X[:, 1:], order=(n_lags, d, q), enforce_invertibility=False, enforce_stationarity=False, dynamic=False)
			#model_fit = model.fit(disp=verbose, iprint=verbose, maxiter=200, method='powell')
			#model_fit.save(model_file_name)
			#joblib.dump(scaler, model_file_name.split('/')[0] + '/scaler_' + model_file_name.split('/')[1].split('.')[0] + '.joblib')

		else:
			model_fit = MLEResults.load(model_file_name)
			scaler = joblib.load("/".join(model_file_name.split('/')[0:-1] + ['scaler_' + model_file_name.split('/')[-1]]))
			rmse = None
			rmse_val = None
			test_y = None
			y_hat_test = None
			val_y = None
			y_hat_val = None
			dir_acc = None

	except (ValueError, LinAlgError) as exc:
		print('algo sucedió: ')
		print(exc)
		return 9e+10, 9e+10, None, None, None, None, None, 0, None

	return rmse, rmse_val, test_y, y_hat, val_y, y_hat_val, inv_yhat[-1], dir_acc, model_fit, scaler


def lstm_softmax(state_size, n_output, n_hidden, return_sequences=False, dropout=0):
    model = tf.keras.models.Sequential([
      tf.keras.layers.Conv1D(filters=32, kernel_size=5,
              strides=1, padding="causal",
              activation="relu",
              input_shape=[None, state_size]),
#           tf.keras.layers.LSTM(n_hidden, return_sequences=return_sequences, dropout=dropout, recurrent_dropout=0, stateful=False, input_shape=[None, state_size]),
      tf.keras.layers.LSTM(n_hidden, return_sequences=return_sequences, dropout=dropout, recurrent_dropout=0, stateful=False),
      tf.keras.layers.Dense(n_output, activation='softmax')
    ])
    return model

if __name__=="__main__":
	pass
