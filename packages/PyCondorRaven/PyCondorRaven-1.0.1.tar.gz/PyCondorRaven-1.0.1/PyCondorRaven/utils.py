import pandas as pd
import numpy as np
import csv
from sklearn.preprocessing import MinMaxScaler
from timeit import default_timer as timer
import datetime as dt
from dateutil.relativedelta import relativedelta
import os
import re
import joblib
import shap

def save_dfs(dfs, filename='dataframe.csv'):
    dfs[0].to_csv(filename)
    for df in dfs[1:]:
        df.to_csv(filename, mode='a')
    print('DFs saved!')


def returns(series, period, type='arithmetic'):
    if period == 'daily':
        rets = series.pct_change().dropna()
    elif period == 'monthly':
        rets = series.resample('M').last().pct_change().dropna()
    elif period == 'quarterly':
        rets = series.resample('3M').last().pct_change().dropna()
    elif period == 'semiannualy':
        rets = series.resample('6M').last().pct_change().dropna()
    elif period == 'yearly':
        rets = series.resample('12M').last().pct_change().dropna()
    if type[:3]=='log':
        rets = np.log(1+rets)

    return(rets)

def cash_conv(cash_in, curr_in, spot, spot_id):
    cash_out = None
    if spot_id[:3] == spot_id[3:]:
        cash_out = cash_in
    else:
        if curr_in == spot_id[:3]:
            cash_out = cash_in * spot
        if curr_in == spot_id[3:]:
            cash_out = cash_in/spot
    return cash_out

def series_total_return(rets, w, period='daily'):
    if isinstance(w, pd.Series) or  w.shape[1] == 1:
        dt_index = rets.index
        if period=='daily':
            first_date = dt_index[0] - relativedelta(days=1)
        else:
            first_date = dt_index[0] - relativedelta(months=dict(monthly=1, quarterly=3)[period])

        if len(w)>1:
            series = pd.Series(np.cumprod(1 + np.append([0], rets[w.index].values @ w.values)), index=dt_index.union([first_date]))
        else:
            series = pd.Series(np.cumprod(1 + np.append([0], rets[w.index].values)), index=dt_index.union([first_date]))
    else:
        dt_index = rets.index
        port_rets = []
        ref_date = dt_index[0] - dt.timedelta(days=1)
        for dec_date in w.columns:
            w_i = w[dec_date]
            port_rets = port_rets + list(1+rets.loc[(rets.index > ref_date) & (rets.index <= dec_date)][w_i.index].values @ w_i)
            ref_date = dec_date
        if period=='daily':
            first_date = dt_index[0] - relativedelta(days=1)
        else:
            first_date = dt_index[0] - relativedelta(months=dict(monthly=1, quarterly=3)[period])
        series = pd.Series(np.cumprod(np.append([1], port_rets)), index=dt_index.union([first_date]))
    total_return = series.values[-1] - 1
    return series, total_return

def fx_cross(base_curr, ref_curr, curr_mkt_base, fx_base, curr_mkt_ref, fx_ref):
    if base_curr == "USD" or ref_curr == "USD":
        raise ValueError("This function only applies to non-usd currencies.")
    mkt_codes = [curr_mkt_base[:3], curr_mkt_base[3:], curr_mkt_ref[:3], curr_mkt_ref[3:]]
    base_pos = mkt_codes.index(base_curr)
    ref_pos = mkt_codes.index(ref_curr)
    if base_pos == 0 and ref_pos == 3:
        cross = fx_base * fx_ref
    elif base_pos == 1 and ref_pos == 3:
        cross = (1/fx_base) * (fx_ref)
    elif base_pos == 1 and ref_pos == 2:
        cross = 1/(fx_base * fx_ref)
    return cross

def iso_quote (curr1, curr2 = None, base_currs=np.array(["NZD", "AUD","EUR", "GBP"]), short=False):
    if curr2 is None:
        if any(curr1 == base_currs):
            iso = curr1 + "USD"
        else:
            iso = "USD" + curr1
    else:
        iso = curr1 + curr2
        if any(curr1 == base_currs):
            iso = curr1 + curr2
        elif any(curr2 == base_currs):
            iso = curr2 + curr1
        else:
            if curr1 == "USD":
                iso = curr1 + curr2
            elif curr2 == "USD":
                iso = curr2 + curr1
    if short:
        base_curr = iso[:3]
        ref_curr = iso[3:]
        is_usd = "USD" == np.array([base_curr, ref_curr])
        if any(is_usd):
            iso =  str(np.array([base_curr, ref_curr])[np.logical_not(is_usd)][0])
    return iso



def tf_windowed_dataset(series, n_lags, time_steps, batch_size, shuffle_buffer=1000, output_all=False, output_mean=True):
    import tensorflow as tf
    if series.ndim == 1:
        series = tf.expand_dims(series, axis=-1)
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(n_lags + time_steps, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda window: window.batch(n_lags + time_steps))
    if time_steps>1 and output_mean:
        if series.shape[1] == 1 or output_all:
            ds = ds.map(lambda window: (window[:-time_steps], [tf.math.reduce_mean(window[-time_steps:], axis=0)]))
        else:
            ds = ds.map(lambda window: (window[:-time_steps], [tf.math.reduce_mean(window[-time_steps:][:,0])]))
    else:
        if time_steps>=1:
            if series.shape[1] == 1 or output_all:
                ds = ds.map(lambda window: (window[:-time_steps], window[-time_steps:]))
            else:
                ds = ds.map(lambda window: (window[:-time_steps], window[-time_steps:][:,0]))
        elif time_steps==0: #In this case the first column is the output
            ds = ds.map(lambda window: (window[:,1:], [window[-1,1]]))

    if shuffle_buffer is not None:
        ds = ds.shuffle(shuffle_buffer)
    ds = ds.batch(batch_size).prefetch(1)
    return ds

def tf_windowed_dataset_onehot(series, n_lags, time_steps, batch_size, train_perc=0.8, shuffle_buffer=1000):
    import tensorflow as tf
    train_size = int(len(series)*train_perc)

    n_classes = len(np.unique(series[:,0]))
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(n_lags + time_steps, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda window: window.batch(n_lags + time_steps))
    if time_steps>1:
        ds = ds.map(lambda window: (window[:-time_steps, 1:], tf.one_hot(tf.argmax(tf.math.bincount(tf.dtypes.cast(window[-time_steps:,0],tf.int32))), n_classes)))
    else:
        ds = ds.map(lambda window: (window[:-time_steps, 1:], tf.one_hot(tf.dtypes.cast(window[-time_steps:,0],tf.int32), n_classes)))
    train_dataset = ds.take(train_size)
    valid_dataset = ds.skip(train_size)

    if shuffle_buffer is not None:
            train_dataset = train_dataset.shuffle(shuffle_buffer)
    train_dataset = train_dataset.batch(batch_size).prefetch(1)
    valid_dataset = valid_dataset.batch(1).prefetch(1)
    return train_dataset, valid_dataset

def tf_model_forecast(model, series, n_lags, include_first=True):
    import tensorflow as tf
    if series.ndim == 1:
        series = tf.expand_dims(series, axis=-1)
    ds = tf.data.Dataset.from_tensor_slices(series)
    ds = ds.window(n_lags, shift=1, drop_remainder=True)
    ds = ds.flat_map(lambda w: w.batch(n_lags))
    ds = ds.batch(1).prefetch(1)
    forecast = model.predict(ds)
    return forecast

def create_target(df, target_as_string, timesteps = 1, target_name = 'Target', dropna = True):
    """
    Creates target variable shifting it by timesteps.
    Returns dataframe with target variable located in the first column.
    """
    df['Target'] = df.loc[:, target_as_string].shift(-timesteps)
    cols = df.columns.values.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    if dropna:
        return df.dropna()
    else:
        return df

def custom_predict_proba(x, model = None):

    def softmax(x):
        """Compute softmax values for each sets of scores in x."""
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)
    
    if model is not None:
        predict_proba_dist = model.decision_function(x)
    else:
        predict_proba_dist = x
    pred_probability = []
    for eachArr in predict_proba_dist:
        pred_probability.append(softmax(eachArr))
    
    return pred_probability

def sklearn_model_forecast(model, series, scaler = None, predict_proba = False, export = False, file_name = None, export_path = None, custom_predict_prob = False):
    """
    Takes an sklearn serialized model as an input to return forecasts
    model -- sklearn model .joblib
    series -- dataframe
    scaler -- preprocessing scaler if any
    predict_proba -- true if probabilities should be returned
    export -- true if .csv file is to be exported
    file_name -- name for exported .csv file
    export_path -- path for .csv file

    Returns
    -- Pandas Dataframe
    """
    

    if scaler is not None:
        series = pd.DataFrame(scaler.transform(series), index = series.index, columns = series.columns)

    if predict_proba:
        if not custom_predict_prob:
            preds = model.predict_proba(series)
            preds_df = pd.DataFrame(preds, index = series.index)
        else:
            preds = custom_predict_proba(series, model)
            preds_df = pd.DataFrame(preds, index = series.index)
    else:
        preds = model.predict(series)
        preds_df = pd.DataFrame({'Predicciones': preds}, index = series.index)

    if export:
        preds_df.to_csv(export_path + '/' + file_name + '.csv')

    return preds_df

def train_test_split(series, train_size = 0.9, test_size =0.1, val_size = 0):
    n_obs = series.shape[0]
    split_train = int(n_obs*train_size)
    time = np.arange(series.shape[0])
    data_train = series[:split_train]
    time_train = time[:split_train]
    if val_size == 0:
        data_test = series[split_train:]
        time_test = time[split_train:]
        data_val = None
        time_val = None
    else:
        split_test = int(n_obs*(train_size+test_size))
        data_test = series[split_train:split_test]
        time_test = time[split_train:split_test]
        data_val = series[split_test:]
        time_val = time[split_test:]
    return data_train, data_test, data_val, time_train, time_test, time_val


def preproc_series(series, period ="monthly", to_returns=False, print_file=False):

	"""
		Función para preprocesar la serie de entrada: primero seleccional las observaciones con base en la peridicidad. Luego, si se requiere, estima retornos.

		Parámetros:
		- series -- pandas dataframe, serie de observaciones ordenada según orden cronológico.
		- period -- Periodicidad de los datos.
		- to_return -- Convertir a retorno.
		- print_file -- Imprimir archivo con datos procesados.

		Retorna:
		- Pandas dataframe.
	"""

	freq = {'daily':365, 'monthly': 12, 'quarterly': 4}[period]
	if period == 'monthly':
		series_proc = series.asfreq('M', method='backfill')
	elif period == 'quarterly':
		series_proc = series.asfreq('3M', method='backfill')

	if to_returns:
		series_proc = series_proc.pct_change().dropna()

	if print_file:
		series_proc.to_csv('data/series_proc.csv')
	return(series_proc)


ID_TO_MODELNAME = {0:'lstm', 1:'randomForest', 2:'adaBoost', 3:'svm', 4:'arima', 5:'lstmNoSW'}

def inverse_transform(data, scaler, n_features):
	"""
		Función que invierte el escalamiento de los datos, es decir pasa de datos escalados a datos originales.

		Parámetros:
		- data -- Arreglo de numpy, arreglo con los valores escalados
		- scaler -- instancia de MinMaxScaler, escalador para invertir el escalamiento
		- n_features -- Entero, número de variables en los datos originales

		Retorna:
		- data -- Arreglo de numpy, arreglo con los valores en escala original

	"""
	data = data.copy()
	assert type(data) == np.ndarray
	if(data.ndim == 1): data = data.reshape(-1, 1)
	assert data.ndim == 2
	for i in range(data.shape[1]):
		tmp = np.zeros((data.shape[0], n_features))
		tmp[:, 0] = data[:, i]
		data[:, i] = scaler.inverse_transform(tmp)[:, 0]
	return data

def normalize_data(values, scale=(0,1), train_size=0.6):
	"""
		Función para normalizar los datos, es decir, escalarlos en una escala que por *default* es [-1, 1]

		Parámetros:
		- values -- Arreglo de numpy, los datos
		- scaler -- Tupla de 2 valores, escala a la cual se quiere escalar los datos

		Retorna:
		- scaled -- Arreglo de numpy, los datos escalados
		- scaler -- Instancia de MinMaxScaler, para luego revertir el proceso de escalamiento
	"""
	# Be sure all values are numbers
	n_train = int(values.shape[0] * train_size)
	values_train = values[:n_train, :].astype('float32')
	# scale the data
	scaler = MinMaxScaler(feature_range=scale)
	scaler.fit(values_train)
	scaled = scaler.transform(values)
	# All values are transformed based on scaler built on training data (not testing)
	return scaled, scaler

def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
	"""
		Función que convierte la serie de tiempo en datos supervisados para el modelo, es decir cambia el formato de (número de ejemplos, número de *features*)
		por (número de ejemplos, número de *lags*, número de *features*)

		Parámetros:
		- data -- Arreglo de numpy, la serie completa de los datos
		- n_in -- Entero, número de *lags* o resagos de tiempo, *default* es 1
		- n_out -- Entero, número de *time steps* a predecir en el futuro, *default* es 1
		- dropnan -- Booleano, indica si se eliminan los valores de Nan del *dataframe* resultante

		Retorna:
		- agg -- *Dataframe* de pandas, *dataframe* con todas las variables en el nuevo formato, sus nombres de columnas son del tipo: "var3(t+2)"

	"""
	n_vars = 1 if type(data) is list else data.shape[1]
	df = pd.DataFrame(data)
	cols, names = list(), list()
	# input sequence (t-n, ... t-1)
	for i in range(n_in, 0, -1):
		cols.append(df.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
	# forecast sequence (t, t+1, ... t+n)
	for i in range(0, n_out):
		cols.append(df.shift(-i))
		if i == 0:
			names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
		else:
			names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
	# put it all together
	agg = pd.concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)
	return agg

def series_with_lags(data, n_lags=4, dropnan=True):
	"""
		Función que convierte la serie de tiempo en datos supervisados para el modelo, es decir cambia el formato de (número de ejemplos, número de *features*)
		por (número de ejemplos, número de *lags*, número de *features*)

		Parámetros:
		- data -- Arreglo de numpy, la serie completa de los datos
		- n_lags -- Entero, número de *lags* o resagos de tiempo, *default* es 1
		- dropnan -- Booleano, indica si se eliminan los valores de Nan del *dataframe* resultante

		Retorna:
		- agg_df -- *Dataframe* de pandas, *dataframe* con todas las variables en el nuevo formato, sus nombres de columnas son del tipo: "var3(t+2)"
		- agg_array -- *array* con 3 dimensiones: [n_obs, n_lags, n_features]

	"""
	n_vars = 1 if type(data) is list else data.shape[1]
	df = pd.DataFrame(data)
	cols, names = list(), list()
	# input sequence (t-n, ... t-1)
	for i in range(n_lags, -1, -1):
		cols.append(df.shift(i))
		names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]

	# put it all together
	agg = pd.concat(cols, axis=1)
	agg.columns = names
	# drop rows with NaN values
	if dropnan:
		agg.dropna(inplace=True)

	agg_array = agg.values.reshape((agg.shape[0], n_lags+1, data.shape[1]))
	return {'agg_df':agg,  'agg_array': agg_array}


def transform_values(data, n_lags, n_series, nn, train_size = 0.8, test_size =0.1, val_size = 0.1, batch_size=None):
    """
    Función para preprocesar la serie de entrada, primero le cambia el formato a (número de ejemplos, número de *lags* X número de *features*), luego divide estos datos en
    entrenamiento, validación y *testing* adicionalmente retorna los últimos valores para la predicción.

    Parámetros:
    - data -- Arreglo de numpy, serie de observaciones ordenada según orden cronológico
    - n_lags -- Entero, el número de *lags* que se usaran para entrenar
    - n_series -- Entero, el número de *time steps* a predecir en el futuro
    - nn -- Booleano, denota si se comstruye dataset con keras para entrenamiento de redes neuronales (número de ejemplos, número de *lags*, número de *features*).

    Retorna:
    - train_X -- Arreglo de numpy, datos de entrenamiento
    - val_X -- Arreglo de numpy, datos de valdiación
    - test_X -- Arreglo de numpy, datos de *testing*
    - train_y -- Arreglo de numpy, observaciones de tiempos futuros de entrenamiento
    - val_y -- Arreglo de numpy, observaciones de tiempos futuros de validación
    - test_y -- Arreglo de numpy, observaciones de tiempos futuros de *testing
    """
    if nn:
        data_train, data_test, data_val, time_train, time_test, time_val = train_test_split(data, train_size=train_size, test_size=test_size, val_size=val_size)
        train_set = tf_windowed_dataset(data_train, n_lags, n_series, batch_size)
        return data_train, data_test, data_val, time_train, time_test, time_val
    else:
        n_features = data.shape[1]
        reframed = series_to_supervised(data, n_lags, n_series)

        values = reframed.values # if n_lags = 1 then shape = (349, 100), if n_lags = 2 then shape = (348, 150)
        # n_examples for training set
        n_train = int(values.shape[0] * train_size)
        n_test = int(values.shape[0] * test_size)
        train = values[:n_train, :]
        test = values[n_train:(n_train + n_test), :]
        val = values[(n_train + n_test):, :]
        # observations for training, that is to say, series in the times (t-n_lags:t-1) taking t-1 because observations in time t is for testing
        n_obs = n_lags * n_features

        # Var1 is the only target. Can be Var1 in different future times.
        cols = ['var1(t)']
        cols += ['var1(t+%d)' % (i) for i in range(1, n_series)]
        y_o = reframed[cols].values # Target variable can only be Var1.
        train_o = y_o[:n_train]
        test_o = y_o[n_train:(n_train + n_test)]
        val_o = y_o[(n_train + n_test):]

        train_X, train_y = train[:, :n_obs], train_o[:, -n_series:]
        test_X, test_y = test[:, :n_obs], test_o[:, -n_series:]
        val_X, val_y = val[:, :n_obs], val_o[:, -n_series:]
        return train_X, test_X, val_X, train_y, test_y, val_y

def transform_values_to_predict(data, n_lags, n_series, nn):
	"""
		Función para preprocesar la serie de entrada, primero le cambia el formato a (número de ejemplos, número de *lags* X número de *features*), luego divide estos datos en
		entrenamiento, validación y *testing* adicionalmente retorna los últimos valores para la predicción.

		Parámetros:
		- data -- Arreglo de numpy, serie de observaciones ordenada según orden cronológico
		- n_lags -- Entero, el número de *lags* que se usaran para entrenar
		- dim -- Booleano, denota si se reformatea los valores de entrenamiento resultantes, es decir si se cambia el formato de (número de ejemplos, número de *lags* X número de *features*) a (número de ejemplos, número de *lags*, número de *features*)

		Retorna:
		- input_X -- Arreglo de numpy, datos de para predecir transformados
	"""
	n_features = data.shape[1]
	if n_lags > 1:
		reframed = series_to_supervised(data, n_lags - 1, n_series)
		input_X = reframed.values # if n_lags = 1 then shape = (349, 100), if n_lags = 2 then shape = (348, 150)
	else:
		input_X = data
	# reshape train data to be 3D [n_examples, n_lags, features]
	if(nn):
		input_X = input_X.reshape((input_X.shape[0], n_lags, n_features))
	return input_X

def plot_data(data, labels, title):
    """
        Función para graficar los datos resultantes, solo sirve para las predicciones a 1 *time step*

        Parámetros:
        - data -- Lista de dos valores, lista con las predicciones y las observaciones
        - labels -- Lista de dos valores, lista con las etiquetas de los datos para mostrar en el gráfico
        - title -- String, título del gráfico
        Retorna:
        NADA
    """
    from matplotlib import pyplot as plt
    plt.figure()
    for i in range(len(data)):
    	plt.plot(data[i], label=labels[i])
    plt.suptitle(title, fontsize=16)
    plt.legend()
    plt.show()

def plot_data_lagged_blocks(data, labels, title):
    """
        Función para graficar los datos resultantes, sirve más que todo para las predicciones a más de un *time step*. Lo que hace es ponerle un *padding* a las predicciones
        para que queden en el tiempo que están prediciendo, es decir, si *time steps* es 10, la priemra predicción se hará para el tiempo 0 y tendrá las predicciones hasta el
        tiempo 9, la segunda predicción se hará en el tiempo 10 y tendra las predicciones del tiempo 10 al 19, etc.

        Parámetros:
        - data -- Lista de dos valores, lista con las predicciones y las observaciones, es necesario que la primera posición sean las observaciones y la segunda las predicciones
        - labels -- Lista de dos valores, lista con las etiquetas de los datos para mostrar en el gráfico
        - title -- String, título del gráfico

        Retorna:
        NADA

    """
    from matplotlib import pyplot as plt
    plt.figure()
    plt.plot(data[0], label=labels[0])
    for i in range(0, len(data[1]), len(data[1][0])):
    	padding = [None for _ in range(i)]
    	plt.plot(padding + list(data[1][i]), label=labels[1] + str(i+1))
    plt.suptitle(title, fontsize=16)
    plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=2)
    plt.show()

def diff(values):
	"""
		Función que sirve para diferenciar una serie

		Parámetros:
		- values -- Arreglo de numpy | lista, serie que va a ser diferenciada

		Retorna:
		- new -- Lista, lista con la serie diferenciada

	"""
	new = np.zeros(len(values)-1)
	for i in range(len(new)):
		new[i] = values[i+1] - values[i]
	return new


def calculate_diff_level_for_stationarity(values, scaler, maxi):
	"""
		Función que sirve para calcular el nivel de diferenciación necesario para que una serie sea estacionaria

		Parámetros:
		- values -- Arreglo de numpy, serie sobre la cual se va a calcular el nivel de diferenciación necesario
		- scaler -- Instancia de la clase MinMaxScaler de sklearn, sirve para revertir el escalamiento de la serie
		- maxi -- Entero, valor maximo de diferenciación permitido, si se llega a este limite y la serie no es estacionaria se devolverá maxi como el nivel de diferenciación

		Retorna:
		- maxi | i -- Entero, mínimo nivel de diferenciación para que la serie sea estacionaria, o máximo número en el que se diferenció en el caso de que la serie no se haya logrado poner estacionaria

	"""
	from statsmodels.tsa.stattools import adfuller
	real_values = scaler.inverse_transform(values)

	serie = real_values[:, 0]
	for i in range(maxi):
		result = adfuller(serie)
		if(result[0] < result[4]['5%']):
			return i
		serie = diff(serie)
	return maxi

def objective(params, id_model, values, scaler, n_features, n_series, lr, verbosity, model_file_name, MAX_EVALS, returns, train_size, test_size, val_size, dir='', error_type="mse"):
    """
    	Función objetivo que sirve para la optimización bayesiana, sirve para ejecutar el modelo con los parámetros recibidos, calcular el error de esta ejecución y así decidir
    	cuales parámetros son mejores.

    	Parámetros:
    	- params -- Diccionario, contien los parametros para la ejecución, estos parámetros son dados por la libreria de optimización bayesiana (bayes_opt) dentro de un espacio previamente definido
    	- id_model -- Entero, id del modelo que se va a entrenar
    	- values -- Arreglo de numpy, datos con los cuales se va a entrenar el modelo, es decir, la serie previamente preprocesada
    	- scaler -- Instancia de la clase MinMaxScaler de sklearn, sirve para el escalamiento de los datos y para revertir este escalamiento
    	- n_features -- Entero, número de *features* de la serie
    	- n_series -- Entero, número de *time steps*
    	- verbosity -- Entero, nivel de verbosidad de la ejecución
    	- model_file_name -- String, nombre del archivo donde se guardará y/o se cargará el modelo entrenado
    	- MAX_EVALS -- Entero, número máximo  de iteraciones de la optimización bayesiana, en esta función sirve para identificar el archivo de los logs

    	Retorna:
    	- [valor] -- Flotante, dicconario que retorna la "recompensa" de esta ejecución, la idea es maximizarla, por eso el "error" de la ejecución se invierte

    """
    # Keep track of evals
    global ITERATION
    from . import models

    ITERATION += 1
    out_file = dir + 'trials/gbm_trials_' + ID_TO_MODELNAME[id_model] + '_' + str(MAX_EVALS) + '.csv'
    # print(ITERATION, params)

    calc_val_error = True
    calc_test_error = True
    if(id_model == 0):
        if(model_file_name == None):
            model_file_name = dir + 'models/trials-lstm.h5'

		# Make sure parameters that need to be integers are integers
        for parameter_name in ['n_lags', 'n_epochs', 'batch_size', 'n_hidden', 'n_dense', 'n_rnn', 'activation']:
            params[parameter_name] = int(params[parameter_name])

        start = timer()
        data_train, data_test, data_val, time_train, time_test, time_val = transform_values(values, params['n_lags'], n_series, True, train_size, test_size, val_size, params['batch_size'])
        rmse, rmse_val, _, _, val_y, y_hat_val, dir_acc, _, _ = models.model_lstm(data_train, data_test, data_val, n_series, lr, params['n_epochs'], params['batch_size'], params['n_hidden'], n_features,params['n_lags'], scaler, calc_val_error, calc_test_error, verbosity, False, model_file_name, params['n_rnn'], params['n_dense'], params['activation'], params['drop_p'], returns, error_type=error_type)
        if(returns):
        	# mean = np.mean(np.abs(val_y))
        	# std = np.std(val_y)
        	print('rmse:', rmse_val) #, 'std: ', np.std(y_hat_val))
        	# print('mean: ', mean, 'std_y: ', std)
        	# print('inputs -> error: ', np.abs(rmse_val-mean)/mean, 'deviation: ', (np.abs(std-np.std(y_hat_val)))/std)
        	rmse = rmse_val #np.abs(rmse_val-mean)/mean + (np.abs(std-np.std(y_hat_val)))/std
        else:
        	mean = np.mean(np.abs(val_y))
        	rmse = rmse_val/mean + (1 - dir_acc)
        run_time = timer() - start
		# print('no_score: ', rmse)
		# print('time: ', run_time, end='\n\n')
    elif(id_model == 1):
    	if(model_file_name == None): model_file_name = dir + 'models/trials-randomForest.joblib'

    	# Make sure parameters that need to be integers are integers
    	for parameter_name in ['n_lags', 'n_estimators', 'max_features', 'min_samples']:
    		params[parameter_name] = int(params[parameter_name])

    	start = timer()
    	train_X, test_X, val_X, train_y, test_y, val_y = transform_values(values, params['n_lags'], n_series, 0, train_size, test_size, val_size)
    	rmse, rmse_val, _, _, _, _, _, dir_acc, _, _ = models.model_random_forest(train_X, test_X, val_X, train_y, test_y, val_y, n_series, params['n_estimators'], params['max_features'], params['min_samples'],
    															n_features, params['n_lags'], scaler, calc_val_error, calc_test_error, verbosity, False, model_file_name, returns)
    	if(returns):
    		rmse = rmse_val
    	else:
    		mean = np.mean(np.abs(val_y))
    		rmse = rmse_val/mean + (1 - dir_acc)
    	run_time = timer() - start
    	# print('no_score: ', rmse)
    	# print('time: ', run_time, end='\n\n')
    elif(id_model == 2):
    	if(model_file_name == None): model_file_name = dir + 'models/trials-adaBoost.joblib'
    	# Make sure parameters that need to be integers are integers
    	for parameter_name in ['n_lags', 'n_estimators', 'max_depth']:
    		params[parameter_name] = int(params[parameter_name])

    	start = timer()
    	train_X, test_X, val_X, train_y, test_y, val_y = transform_values(values, params['n_lags'], n_series, 0, train_size, test_size, val_size)
    	rmse, rmse_val, _, _, _, _, _, dir_acc, _, _ = models.model_ada_boost(train_X, test_X, val_X, train_y, test_y, val_y, n_series, params['n_estimators'], params['lr'], params['max_depth'], n_features,
    														params['n_lags'], scaler, calc_val_error, calc_test_error, verbosity, False, model_file_name, returns)
    	if(returns):
    		rmse = rmse_val
    	else:
    		mean = np.mean(np.abs(val_y))
    		rmse = rmse_val/mean + (1 - dir_acc)
    	rmse = rmse_val/mean + (1 - dir_acc)
    	run_time = timer() - start
    	# print('no_score: ', rmse)
    	# print('time: ', run_time, end='\n\n')
    elif(id_model == 3):
    	if(model_file_name == None): model_file_name = dir + 'models/trials-svm.joblib'
    	# Make sure parameters that need to be integers are integers
    	for parameter_name in ['n_lags']:
    		params[parameter_name] = int(params[parameter_name])

    	start = timer()
    	train_X, test_X, val_X, train_y, test_y, val_y = transform_values(values, params['n_lags'], n_series, 0, train_size, test_size, val_size)
    	rmse, rmse_val, _, _, _, _, _, dir_acc, _, _ = models.model_svm(train_X, test_X, val_X, train_y, test_y, val_y, n_series, n_features, params['n_lags'], scaler, calc_val_error, calc_test_error,
    												verbosity, False, model_file_name, returns)
    	if(returns):
    		rmse = rmse_val
    	else:
    		mean = np.mean(np.abs(val_y))
    		rmse = rmse_val/mean + (1 - dir_acc)
    		rmse = rmse_val/mean + (1 - dir_acc)
    	run_time = timer() - start
    	# print('no_score: ', rmse)
    	# print('time: ', run_time, end='\n\n')
    elif(id_model == 4):
    	if(model_file_name == None): model_file_name = dir + 'models/arima.pkl'
    	# Make sure parameters that need to be integers are integers
    	for parameter_name in ['n_lags', 'd', 'q']:
    		params[parameter_name] = int(params[parameter_name])

    	start = timer()
    	wall = int(len(values)*0.6)
    	wall_val= int(len(values)*0.2)
    	train_X, test_X, val_X, last_values = values[:wall, :], values[wall:wall+wall_val,:], values[wall+wall_val:-1,:], values[-1,:]
    	train_y, test_y, val_y = values[1:wall+1,0], values[wall+1:wall+wall_val+1,0], values[wall+wall_val+1:,0]
    	start = timer()
    	rmse, rmse_val, y, y_hat, y_valset, y_hat_val, dir_acc, model, scaler = models.model_arima(train_X, test_X, val_X, train_y, test_y, val_y, n_series, params['d'], params['q'], n_features, params['n_lags'], scaler, calc_val_error,
    													calc_test_error, verbosity, False, model_file_name, returns)
    	if(returns):
    		rmse = rmse_val
    	else:
    		mean = np.mean(np.abs(val_y))
    		rmse = rmse_val/mean + (1 - dir_acc)
    	run_time = timer() - start
    	# print('no_score: ', rmse)
    	# print('time: ', run_time, end='\n\n')

    # Write to the csv file
    of_connection = open(out_file, 'a')
    writer = csv.writer(of_connection)
    writer.writerow([rmse, params, ITERATION, run_time])
    of_connection.close()

    return -1 * rmse

def bayes_optimization(id_model, MAX_EVALS, values, scaler, n_features, n_series, lr, original, verbosity, model_file_name, returns, train_size, test_size, val_size, dir='', error_type="mse"):
	"""
		Función para encontrar los parámetros óptimos para un modelo

		Parámetros:
		- id_model -- Entero, id del modelo que se va a entrenar
		- MAX_EVALS -- Entero, número máximo  de iteraciones de la optimización bayesiana
		- values -- Arreglo de numpy, datos con los cuales se va a entrenar el modelo, es decir, la serie previamente preprocesada
		- scaler -- Instancia de la clase MinMaxScaler de sklearn, sirve para el escalamiento de los datos y para revertir este escalamiento
		- n_features -- Entero, número de *features* de la serie
		- n_series -- Entero, número de *time steps*
		- original -- Booleano, denota si se van a usar los *features* originales de la serie o los *features* seleccionados, en esta función serviría para identificar el archivo de salida
		- verbosity -- Entero, nivel de verbosidad de la ejecución
		- model_file_name -- String, nombre del archivo donde se guardará y/o se cargará el modelo entrenado

		Retorna:
		- best -- Diccionario, diccionario con los mejores parámetros encontrados en la optimización bayesiana
	"""
	from bayes_opt import BayesianOptimization

	global ITERATION
	ITERATION = 0

	if(id_model == 0):
		if(n_series == 1):
			space = {'activation': (0, 0),
					'batch_size': (5, 20), # depende del número de obsevaciones
					'drop_p': (0.05, 0.3),
					'n_dense': (1, 1),
					'n_epochs': (100, 200),
					'n_hidden': (5, 16),
					'n_lags': (3, 12),
					'n_rnn': (1, 1)}
		elif(n_series > 1):
			space = {'activation': (0, 0),
					'batch_size': (5, 20),
					'drop_p': (0.05, 0.3),
					'n_dense': (1, 1),
					'n_epochs': (100, 200),
					'n_hidden': (5, 16),
					'n_lags': (3, 12),
					'n_rnn': (1, 1)}
		func = lambda activation, batch_size, drop_p, n_dense, n_epochs, n_hidden, n_lags, n_rnn: objective({'activation':activation , 'batch_size':batch_size, 'drop_p':drop_p, 'n_dense':n_dense, 'n_epochs':n_epochs, 'n_hidden':n_hidden, 'n_lags':n_lags, 'n_rnn':n_rnn}, id_model, values, scaler, n_features, n_series, lr, verbosity, model_file_name, MAX_EVALS, returns, train_size, test_size, val_size, dir, error_type)
	elif(id_model == 1):
		space = {'max_features': (1, n_features),
				'min_samples': (1, 20),
				'n_estimators': (10, 1000),
				'n_lags': (1, 4)}
		func = lambda max_features, min_samples, n_estimators, n_lags: objective({'max_features': max_features, 'min_samples': min_samples, 'n_estimators': n_estimators, 'n_lags': n_lags}, id_model, values, scaler, n_features, n_series, lr, verbosity, model_file_name, MAX_EVALS, returns, train_size, test_size, val_size, dir)
	elif(id_model == 2):
		space = {'lr': (0.00001, 1.0),
				'max_depth': (2, 10),
				'n_estimators': (10, 1000),
				'n_lags': (1, min(50, int(len(values)/2)))}
		func = lambda lr, max_depth, n_estimators, n_lags: objective({'lr':lr, 'max_depth': max_depth, 'n_estimators': n_estimators, 'n_lags': n_lags}, id_model, values, scaler, n_features, n_series, lr, verbosity, model_file_name, MAX_EVALS, returns, train_size, test_size, val_size, dir)
	elif(id_model == 3):
		space = {'n_lags': (1, min(50, int(len(values)/2)))}
		func = lambda  n_lags: objective({'n_lags': n_lags}, id_model, values, scaler, n_features, n_series, lr, verbosity, model_file_name, MAX_EVALS, returns, train_size, test_size, val_size, dir)
	elif(id_model == 4):
		diff_level = calculate_diff_level_for_stationarity(values, scaler, 5)
		space={'n_lags': (1, 12),
				'q': (1, 12)}
		func = lambda  n_lags, q: objective({'d': diff_level, 'n_lags': n_lags, 'q': q}, id_model, values, scaler, n_features, n_series, lr, verbosity, model_file_name, MAX_EVALS, returns, train_size, test_size, val_size, dir)

	# File to save results
	out_file = dir + 'trials/gbm_trials_' + ID_TO_MODELNAME[id_model] + '_' + str(MAX_EVALS) + '.csv'
	of_connection = open(out_file, 'w')
	writer = csv.writer(of_connection)

	# Write the headers to the file
	writer.writerow(['id_model: ' + str(id_model), 'original: ' + str(original), 'returns: ' + str(returns), 'time_steps: ' + str(n_series)])
	writer.writerow(['rmse', 'params', 'iteration', 'train_time'])
	of_connection.close()

	optimizer = BayesianOptimization(f=func, pbounds=space, verbose=2, random_state=np.random.randint(np.random.randint(100)))
	# if(id_model == 0):
	# 	#optimizer.probe(params={'activation':1.0, 'batch_size':10.0, 'drop_p':0.0, 'n_dense':0.0, 'n_epochs':300.0, 'n_hidden':50.0, 'n_lags':10.0, 'n_rnn':0.0})
	# 	#optimizer.probe(params={'activation':1.0, 'batch_size':81.0, 'drop_p':0.0, 'n_dense':0.0, 'n_epochs':200.0, 'n_hidden':250.0, 'n_lags':15.0, 'n_rnn':0.0})
	# 	#optimizer.probe(params={'activation':1.0, 'batch_size':81.0, 'drop_p':0.0, 'n_dense':0.0, 'n_epochs':200.0, 'n_hidden':269.0, 'n_lags':9.0, 'n_rnn':0.0})
	# 	#optimizer.probe(params={'activation':1.0, 'batch_size':81.0, 'drop_p':0.0, 'n_dense':0.0, 'n_epochs':200.0, 'n_hidden':269.0, 'n_lags':25.0, 'n_rnn':0.0})
	# 	optimizer.probe(params={'activation':0.0, 'batch_size':47.0, 'drop_p':0.069, 'n_dense':0.0, 'n_epochs':382.0, 'n_hidden':130.0, 'n_lags':5.0, 'n_rnn':1.0})
	# 	optimizer.probe(params={'activation':0.0, 'batch_size':47.0, 'drop_p':0.3, 'n_dense':0.0, 'n_epochs':382.0, 'n_hidden':130.0, 'n_lags':5.0, 'n_rnn':1.0})
	# 	optimizer.probe(params={'activation':0.0, 'batch_size':47.0, 'drop_p':0.5, 'n_dense':0.0, 'n_epochs':382.0, 'n_hidden':130.0, 'n_lags':5.0, 'n_rnn':1.0})
	optimizer.maximize(init_points=10, n_iter=MAX_EVALS, acq='ucb', kappa=5, alpha=1e-3)


	# store best results
	best = optimizer.max['params']
	out_file = dir + 'trials/best_' + ID_TO_MODELNAME[id_model] + '.csv'
	of_connection = open(out_file, 'a')
	writer = csv.writer(of_connection)
	if(id_model == 0):
		writer.writerow([optimizer.max['target'], best['activation'], best['batch_size'], best['drop_p'], best['n_dense'], best['n_epochs'], best['n_hidden'], best['n_lags'], best['n_rnn'], MAX_EVALS])
	elif(id_model == 1):
		writer.writerow([optimizer.max['target'], best['n_lags'], best['n_estimators'], best['max_features'], best['min_samples'], MAX_EVALS])
	elif(id_model == 2):
		writer.writerow([optimizer.max['target'], best['n_lags'], best['n_estimators'], best['lr'], best['max_depth'], MAX_EVALS])
	elif(id_model == 3):
		writer.writerow([optimizer.max['target'], best['n_lags'], MAX_EVALS])
	elif(id_model == 4):
		best.update({'d': diff_level})
		writer.writerow([optimizer.max['target'], best['d'], best['n_lags'], best['q'], MAX_EVALS])
	of_connection.close()
	return best


def get_direction_accuracy(y, y_hat):
	"""
		Función para calcular el % de aciertos en la dirección, teniendo en cuenta las observaciones y las predicciones.
		Por dirección se entiende que si en la observación el valor sube, en la predicción también igualmente si baja.

		Parámetros:
		- y -- Arreglo de numpy, las observaciones
		- y_hat -- Arreglo de numpy, las predicciones

		Retorna:
		- [valor] -- % de aciertos en la dirección (valor entre 0 y 1)
	"""
	assert len(y) == len(y_hat)
	y_dirs = [1 if y[i] < y[i+1] else 0 for i in range(len(y) - 1)]
	y_hat_dirs = [1 if y_hat[i] < y_hat[i+1] else 0 for i in range(len(y_hat) - 1)]
	return sum(np.array(y_dirs) == np.array(y_hat_dirs))/len(y)

def get_returns_direction_accuracy(y, y_hat):
	"""
		Función para calcular el % de aciertos en la dirección de retornos, teniendo en cuenta las observaciones y las predicciones.
		Por dirección se entiende que si en la observación el valor sube, en la predicción también lo haga. De igual forma en el caso de que baje.

		Parámetros:
		- y -- Arreglo de numpy, las observaciones
		- y_hat -- Arreglo de numpy, las predicciones

		Retorna:
		- [valor] -- % de aciertos en la dirección (valor entre 0 y 1)
	"""
	assert len(y) == len(y_hat)
	y_dirs = [1 if y[i]>0 else 0 for i in range(len(y))]
	y_hat_dirs = [1 if y_hat[i]>0 else 0 for i in range(len(y_hat))]
	return sum(np.array(y_dirs) == np.array(y_hat_dirs))/len(y)

def get_returns_values_direction_accuracy(values, returns):
	"""
		Función para calcular el % de aciertos en la dirección de retornos teniendo una serie en valores y otra en retornos, teniendo en cuenta las observaciones y las predicciones.
		Por dirección se entiende que si en la observación el valor sube, en la predicción también lo haga. De igual forma en el caso de que baje.

		Parámetros:
		- values -- Arreglo de numpy, serie de valores
		- returns -- Arreglo de numpy, serie de retornos
		Retorna:
		- [valor] -- % de aciertos en la dirección (valor entre 0 y 1)
	"""
	assert len(values) == len(returns) + 1
	values_dirs = [1 if values[i] < values[i+1] else 0 for i in range(len(values) - 1)]
	returns_dirs = [1 if returns[i]>0 else 0 for i in range(len(returns))]
	return sum(np.array(values_dirs) == np.array(returns_dirs))/len(returns)

def calculate_rmse(y, y_hat):
	"""
		Función que calcula el rmse (raíz del error medio cuadrático) entre dos arreglos de datos

		Parámetros:
		- y -- Arreglo de numpy | Lista, serie de observaciones o valores reales
		- y_hat -- Arreglo de numpy | Lista, serie de predicciones
	"""
	assert len(y) == len(y_hat)
	from sklearn.metrics import mean_squared_error
	return np.sqrt(mean_squared_error(y, y_hat))

# Reinforce Portfolio:

def hf_sigmas(series, remove_cero=True):
    sigmas = pd.DataFrame(np.abs(np.log(np.array(series.iloc[1::]) / np.array(series.iloc[0:-1]))),
                          index=series.index[1:], columns=series.columns)
    any(sigmas.iloc[3] != 0)
    [x for x in sigmas.iterrows()]
    pos_cero = [any(sigmas.iloc[i]!=0) for i in np.arange(sigmas.shape[0])]
    return(sigmas)



#Tunninf LSTM Softmax
def hp_train_test_lstm(hparams, series, time_steps, batch_size, n_output, train_perc=0.8):
    import tensorflow as tf
    from .models import lstm_softmax
    optimizer = tf.keras.optimizers.Adam(lr=10e-4)
    train_ds, valid_ds = tf_windowed_dataset_onehot(series.values, hparams['HP_LAGS'], time_steps, batch_size, train_perc, shuffle_buffer=1000)
    model = lstm_softmax(series.shape[1]-1, n_output=4, n_hidden=hparams['HP_NUM_UNITS'], return_sequences=False, dropout=hparams['HP_DROPOUT'])
    model.compile(loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True),optimizer=optimizer,metrics=['accuracy'])
    model.fit(train_ds, epochs=hparams['HP_EPOCHS'], verbose=False)
    _, accuracy = model.evaluate(valid_ds)
    return accuracy

def hp_run(run_dir, hparams, series, time_steps, batch_size, n_output):
    import tensorflow as tf
    with tf.summary.create_file_writer(run_dir).as_default():
        # hp.hparams(hparams)
        accuracy = hp_train_test_lstm(hparams, series, time_steps, batch_size, n_output)
        tf.summary.scalar("accuracy", accuracy, step=1)

def hp_tunning_lstm(HP_LAGS, HP_NUM_UNITS, HP_DROPOUT, HP_EPOCHS, series, time_steps, n_output, batch_size, hp_dir=''):
    session_num = 0
    for n_lags in HP_LAGS.domain.values:
        for num_units in HP_NUM_UNITS.domain.values:
            for dropout_rate in (HP_DROPOUT.domain.min_value, HP_DROPOUT.domain.max_value):
                for epochs in HP_EPOCHS.domain.values:
                    hparams = {
                      'HP_NUM_UNITS': num_units,
                      'HP_DROPOUT': dropout_rate,
                      'HP_EPOCHS': epochs,
                      'HP_LAGS': n_lags,
                    }
                    run_name = "run-%d" % session_num
                    print('--- Starting trial: %s' % run_name)
                    print({h: hparams[h] for h in hparams.keys()})
                    hp_run(hp_dir + 'logs/lstm_tuning' + str(time_steps)+ 'm/' + run_name, hparams, series, time_steps, batch_size, n_output)
                    session_num += 1

def jurik(series, phase = 0, power = 2, smoothing = 8):

    """
    Smooths data with Jurik's moving average.

    Parameters
    -- series - pandas series with data
    -- phase
    -- power
    -- smoothing

    Returns
    -- Pandas series
    """

    if phase <= -100:
        phase_ratio = 0.5
    elif phase > 100:
        phase_ratio = 2.5
    else:
        phase_ratio = phase / 100 + 1.5

    beta = 0.45 * (smoothing - 1) / (0.45 * (smoothing - 1) + 2)
    alpha = beta ** power

    jma = [0]
    e0 = [series[0]]
    e1 = [0]
    e2 = [0]
    for i in range(1, len(series)):
        e0.append((1 - alpha) * series[i] + alpha * e0[i - 1])
        e1.append((series[i] - e0[i]) * (1 - beta) + beta * e1[i - 1])
        e2.append((e0[i] + phase_ratio * e1[i] - jma[i - 1]) * (1 - alpha) ** 2 + alpha ** 2 * e2[i - 1])
        jma.append(e2[i] + jma[i - 1])

    n_append = len(series) - len(jma[1:])
    output = [0] * (n_append)
    output = output + jma[1:]
    output = pd.Series(data = output, index = series.index)
    return output

def avg_return_econ_phase(ticker_list, s3client, econ_phase_series, shift, freq = 'M', file_name = 'series_list_py.csv', bucket = 'suraraven'):

    """
    Returns mean return of assets in ticker_list for each phase in cycle

    Parameters
    -- ticker_list - list with tickers of assets to be processed
    -- series_list - series_list
    -- econ_phase_series - economic cycle series
    -- shift - shift parameter for econ_phase_series
    -- freq - frequency for series_list. Accepted frequencies are pd.Grouper() freq argument possible values

    Returns
    -- Pandas dataframe
    """

    data = extract_data_s3select(s3client, tuple(ticker_list), file_name = file_name, bucket_name = bucket)
    data = pd.concat(data.values(), axis = 1).sort_index(ascending = True)
    data = data.fillna(method = 'ffill')
    data.columns = ticker_list
    data.index = pd.to_datetime(data.index)
    data = data.groupby(pd.Grouper(freq = freq)).last()
    data = data.pct_change(1).dropna()

    econ_phase_series = econ_phase_series.shift(-shift)
    econ_phase_series.dropna(inplace = True)

    joined_series = data.join(econ_phase_series).dropna()

    output_df = joined_series.groupby(by = 'Fase').mean()

    return output_df

def assets_avg_return_econ_phase(asset_names, series_dict, asset_data, econ_phase_series, shift = 0, period='monthly', ref_curr="USD",  currencies=[], convert_to_ref=True):
    """
    Returns mean return of assets for each phase in cycle

    Parameters
    -- asset_names - list of assets to be processed
    -- series_dict - series_dict
    -- asset_data - Assets dataframe
    -- econ_phase_series - economic cycle series
    -- period - return period
    -- ref_curr - reference currency
    -- currencies - currencies
    -- convert_to_ref - convert returns to ref_curr

    Returns
    -- Pandas dataframe
    """
    from .preprocess_dataset import series_sync, series_merge
    econ_phase_series = econ_phase_series.shift(-shift)
    series_assets = series_sync(series_dict, asset_data, asset_names, ref_curr=ref_curr, dates=None, currencies=currencies, convert_to_ref=convert_to_ref, invest_assets=None, ref_per_unit_foreign = False)
    data, sel_cols = series_merge([series_assets, econ_phase_series])
    rets = pd.concat([returns(data.iloc[:,:-1].fillna(method = 'ffill').loc[econ_phase_series.index], period='monthly'),econ_phase_series], axis=1,sort=False).dropna()
    return rets.groupby(['Fase']).mean()

def factor_rets_econ_phase(series_dict, asset_data, econ_phase_series, port=None, asset_names=None, factor="AssetClassMarket", keep_asset_sep=[], shift = 0, period='monthly', ref_curr="USD",  currencies=[], convert_to_ref=True, anual_ret=False):
    """
    Returns mean return of assets for each phase in cycle

    Parameters
    -- series_dict - series_dict
    -- asset_data - Assets dataframe
    -- econ_phase_series - economic cycle series
    -- port - portfolio ps.Series
    -- asset_names - list of assets to be processed
    -- period - return period
    -- ref_curr - reference currency
    -- currencies - currencies
    -- convert_to_ref - convert returns to ref_curr
    -- anual_ret - anualize mean returnos

    Returns
    -- Pandas dataframe
    """
    from .preprocess_dataset import series_sync, series_merge
    freq = dict(monthly=12, daily=252, quarterly=4)[period]
    if port is None and asset_names is None:
        raise ValueError('Either port or asset_names must be different to None.')

    asset_names = port.index if port is not None else asset_names
    econ_phase_series = econ_phase_series.shift(-shift)
    series_assets = series_sync(series_dict, asset_data, asset_names, ref_curr=ref_curr, dates=None, currencies=currencies, convert_to_ref=convert_to_ref, invest_assets=None, ref_per_unit_foreign = False)
    data, sel_cols = series_merge([series_assets, econ_phase_series])
    asset_rets = returns(data.iloc[:,:-1].fillna(method = 'ffill').loc[econ_phase_series.index], period=period)

    if factor is not None and port is not None:
        weighted_asset_rets = asset_rets * np.tile(port.values, (asset_rets.shape[0],1))
        asset_factor = asset_data.loc[asset_names][[factor]]
        if len(keep_asset_sep) > 0:
            pos_keep_assets = [np.where(x==weighted_asset_rets.columns)[0][0] for x in keep_asset_sep]
            asset_factor.iloc[pos_keep_assets,0] = asset_factor.index[pos_keep_assets]
            weighted_asset_rets.columns = asset_factor.values.flatten()
        factor_rets = weighted_asset_rets.groupby(weighted_asset_rets.columns, axis=1).sum()
        port.index = asset_factor.values.flatten()
        factor_w = port.groupby(level=0).sum()
        factor_rets = factor_rets[factor_w.index]/np.tile(factor_w.values, (factor_rets.shape[0],1))
    else:
        factor_rets = asset_rets
    rets = pd.concat([factor_rets,econ_phase_series], axis=1,sort=False).dropna()
    rets_mean = rets.drop(['Fase'], axis=1).mean(axis=0).values * (freq if anual_ret else 1)
    rets_std = rets.drop(['Fase'], axis=1).std(axis=0).values * np.sqrt(freq)

    rets_fase_abs_mean = rets.groupby(['Fase']).mean()*(freq if anual_ret else 1)
    rets_fase_abs_std = rets.groupby(['Fase']).std()*np.sqrt(freq)
    rets_fase_rel_mean = rets_fase_abs_mean - np.tile(rets_mean, (rets_fase_abs_mean.shape[0],1))
    rets_fase_rel_std = rets_fase_abs_std - rets_std

    return rets_fase_abs_mean, rets_fase_abs_std, rets_fase_rel_mean, rets_fase_rel_std

def weighted_groups_vars(port, port_vars, asset_data, factor="AssetClass", keep_asset_sep=[]):
    weighted_vars = port_vars.loc[port.index] * (np.tile(port.values, (port_vars.loc[port.index].shape[1],1)).T if isinstance(port_vars, pd.DataFrame) else port)
    asset_names = port.index
    asset_factor = asset_data.loc[asset_names][[factor]]
    if len(keep_asset_sep) > 0:
        pos_keep_assets = [np.where(x==weighted_vars.index)[0][0] for x in keep_asset_sep]
        asset_factor.iloc[pos_keep_assets,0] = asset_factor.index[pos_keep_assets]
    weighted_vars.index = asset_factor.values.flatten()
    factor_vars = weighted_vars.groupby(level=0).sum()
    port.index = asset_factor.values.flatten()
    factor_w = port.groupby(level=0).sum()
    factor_vars = factor_vars.loc[factor_w.index]/(np.tile(factor_w.values, (factor_vars.shape[1],1)).T if isinstance(factor_vars, pd.DataFrame) else factor_w)
    return factor_vars

def extract_cli(locations = None, request_tries = 10):
    """
    Extracts CLI data from the OECD webpage on a monthly timeframe. Returns dataframe.
    locations - countries or economic groups for which the data shall be returned. If None, all available data will be returned.
                If not none, a list of strings must be passed.
    request_tries - number of tries for OECD GET request. In case it fails, the function loops until its succesful or request_tries is exhausted.
    """

    import datetime
    from datetime import datetime as dt
    import time
    import pandasdmx as sdmx

    def parse_dates(dtDateTime):

        """
        Returns the last date of month.
        """
        def date_time(dateString,strFormat="%Y-%m-%d"):
            # Expects "YYYY-MM-DD" string
            # returns a datetime object
            eSeconds = time.mktime(time.strptime(dateString,strFormat))
            return datetime.datetime.fromtimestamp(eSeconds)

        dtDateTime = dt.strptime(dtDateTime, '%Y-%m')
        dYear = dtDateTime.strftime("%Y")        #get the year
        dMonth = str(int(dtDateTime.strftime("%m"))%12+1) #get next month, watch rollover
        if dMonth == str(1):
            dYear = str(int(dYear) + 1)
        dDay = "1"                               #first day of next month
        nextMonth = date_time("%s-%s-%s"%(dYear,dMonth,dDay)) #make a datetime obj for 1st of next month
        delta = datetime.timedelta(seconds=1)    #create a delta of 1 second
        output = nextMonth - delta
        output = output.strftime('%Y-%m-%d')
        return output

    for i in range(request_tries):
        try:
            print('Making OECD GET request')
            oecd = sdmx.Request('OECD', verify = False)
            cli_response = oecd.data(resource_id = 'MEI_CLI')
            print('Request succesful')
            break
        except Exception as e:
            print('OECD CLI request failed. Iteration {}. Will try again in 10 seconds'.format(str(i)))
            print(e)
            time.sleep(10)

    df = cli_response.write(cli_response.data.series, parse_time = False)
    df = df.xs('M', level = 'FREQUENCY', axis = 1).xs('LOLITOAA', level = 'SUBJECT', axis = 1)
    df.index.name = 'Fecha'
    del df.columns.name
    df = df.loc[~df.index.str.contains('Q'), :]
    df = df.loc[df.index.str.contains('-'), :]
    df = df.loc['1970-01':, :] # library's epoch

    df.index = df.index.map(parse_dates)

    symbol_equivalence = {'AUS': 'CLI Australia', 'AUT': 'CLI Austria', 'BEL': 'CLI Belgium', 'CAN': 'CLI Canada', 'CHL': 'CLI Chile',
                         'COL': 'CLI Colombia', 'CZE': 'CLI Czech Republic', 'DNK': 'CLI Denmark', 'EST': 'CLI Estonia', 'FIN': 'CLI Finland',
                         'FRA': 'CLI France', 'DEU': 'CLI Germany', 'GRC': 'CLI Greece', 'HUN': 'CLI Hungary', 'ISL': 'CLI Iceland', 'IRL': 'CLI Ireland',
                         'ISR': 'CLI Israel', 'ITA': 'CLI Italy', 'JPN': 'CLI Japan', 'KOR': 'CLI Korea', 'LVA': 'CLI Latvia', 'LTU': 'CLI Lithuania',
                         'LUX': 'CLI Luxembourg', 'MEX': 'CLI Mexico', 'NLD': 'CLI Netherlands', 'NZL': 'CLI New Zealand', 'NOR': 'CLI Norway',
                         'POL': 'CLI Poland', 'PRT': 'CLI Portugal', 'SVK': 'CLI Slovak Republic', 'SVN': 'CLI Slovenia', 'ESP': 'CLI Spain',
                         'SWE': 'CLI Sweden', 'CHE': 'CLI Switzerland', 'TUR': 'CLI Turkey', 'GBR': 'CLI UK', 'USA': 'CLI USA', 'EA19': 'CLI Euro area',
                         'G4E': 'CLI Four Big European', 'G-7': 'CLI G7', 'NAFTA': 'CLI NAFTA', 'OECDE': 'CLI OECD Europe', 'OECD': 'CLI OECD',
                         'OXE': 'CLI OECD exc. Euro Area', 'ONM': 'CLI OECD + Major six NME', 'A5M': 'CLI Major Five Asia', 'BRA': 'CLI Brazil',
                         'CHN': 'CLI China', 'IND': 'CLI India', 'IDN': 'CLI Indonesia', 'RUS': 'CLI Russia', 'ZAF': 'CLI South Africa'}

    df.columns = df.columns.map(symbol_equivalence)

    if locations is not None:
        df = df.loc[:, locations]

    return df

def predict_input(new_ob, model_name, model_id=0, time_steps=None, root=''): # falta incluir Scales, variables seleccionadas(si las hay, periodos, etc. )
    """
    Predictions.

    Parameters:
    ----------
    new_ob : pandas.DataFrame
        Observations.
    model_name: str
        model name in DB.
    model_id: int
        0 LSTM, 1 RandomForest, 2 adaBoots, 3 SVM, 4 time series.
    root : str
        Dir of models, parameters.
    Returns:
    -------
    'Predictions'
    """
    import joblib
    import tensorflow as tf
    model_ext = {'0': '.h5', '4':'.pkl'}
    model_file_name = root + 'models/' + model_name + model_ext.get(str(model_id), '.joblib')
    scaler = joblib.load("/".join(model_file_name.split('/')[0:-1] + ['scaler_' + model_file_name.split('/')[-1]]).replace("h5", "joblib"))
    if os.path.isfile(root + 'parameters/optimized_' + model_name + '.pars'):
        f =open(root + 'parameters/optimized_' + model_name + '.pars', 'r')
        lines = f.readlines()
        if(len(lines) > 1):
            raise Exception('File with parameters can\'t have more than 1 line ')
        readed_parameters = lines[0].strip().split(', ')
        if model_id==0:
            n_lags = int(readed_parameters[6])
        elif model_id==1:
            n_lags, n_estimators, max_features, min_samples = int(readed_parameters[0]), int(readed_parameters[1]), int(readed_parameters[2]), int(readed_parameters[3])
        elif model_id==2:
            activation, batch_size, drop_p, n_dense, n_epochs, n_hidden, n_lags, n_rnn = int(readed_parameters[0]), int(readed_parameters[1]), float(readed_parameters[2]), int(readed_parameters[3]), int(readed_parameters[4]), int(readed_parameters[5]), int(readed_parameters[6]), int(readed_parameters[7])
        elif model_id==4:
            n_lags, d, q = int(readed_parameters[0]), int(readed_parameters[1]), int(readed_parameters[2])
    if model_id==0:
        model = tf.keras.models.load_model(model_file_name, compile = False)
    else:
       model = joblib.load(model_file_name)

    values = scaler.transform(new_ob.values)
    if model_id==0:
        pred_norm = tf_model_forecast(model, values, n_lags)
        tmp = np.zeros((pred_norm.shape[0], new_ob.shape[1]))
        tmp[:, 0] = pred_norm[:,0]
        pred = scaler.inverse_transform(tmp)[:, 0]
    elif(model_id==4): # Arima
        last_values =  values
        pred = model.predict(len(values)-n_news, len(values) - 1, exog=last_values[:, 1:], endog=last_values[:, 0])
    else:
        X = transform_values_to_predict(values, n_lags, 1, False)
        pred_norm = self.model.predict(X)
        # transform last values
        tmp = np.zeros((pred_norm.shape[0], new_ob.shape[1]))
        tmp[:, 0] = pred_norm[:,0]
        pred = scaler.inverse_transform(tmp)[:, 0]
    pred_df = pd.Series(pred, index=[x + relativedelta(months=0 if time_steps is None else time_steps)  for x in new_ob.index[-len(pred)::]])
    return pred_df

def predict_mult_variables(target_vars, db, s3client, n_output=6, period='monthly', time_steps=6, root='', file_name='series_list_raven.csv', bucket='suraraven'):
    pred_next_per = pd.Series(0, index=target_vars).astype(np.float)
    pred_df = pd.DataFrame([])
    for target_var in target_vars:
        # target_var = target_vars[i]
        # print(target_var)
        try:
            models_id = db.trained_models(target_var, time_steps, period)
        except:
            models_id = []

        if len(models_id) > 1:
            models_dates = db.fetch_table('Models').set_index("id").loc[models_id]['model_date']
            model_name = models_id[np.argmax(models_dates)]
        elif len(models_id)==1:
            model_name = models_id[0]
        else:
            print("No hay modelo disponible o posible problema en conexión a Base de Datos para %s." % (target_var))
        vars_ordered, data_trans_method, period, time_steps, n_lags, output_currency = db.model_params(model_name)
        series_temp, _ = db.fetch_target_vars(vars_ordered[0], s3client, make_transf = True, transf_target = "pct_change", file_name=file_name, bucket=bucket)
        series_temp = series_temp[vars_ordered].dropna()
        new_ob =series_temp[-(n_output+n_lags-1)::]
        pred_df = pd.concat([pred_df, predict_input(new_ob, model_name=model_name, model_id=0, time_steps=time_steps, root=root).to_frame(target_var.split()[0])], axis=1, sort=False)
    pred_next_per = pd.DataFrame([[pred_df[x].dropna().tail(1).index[0], pred_df[x].dropna().tail(1).values[0]] for x in pred_df.columns], index=pred_df.columns)
    pred_next_per.columns = ['Fecha', 'Predicc']
    return pred_df, pred_next_per

def model_exp_weights(pred_df, loss_type='ae', loss_bound=1):
    """
    One period prediction based on experts panel.
    Parameters:
    ----------
    pred_df : pandas.DataFrame
        DF of observations and models predictions. The first column corresponds to the observed returns. If next_per_pred is None, the last row is used to predict next period.

    """
    model_names = pred_df.columns[1:]
    n_models = len(pred_df.columns)-1
    exp_weights = pd.Series(np.zeros(n_models), index=model_names)
    cum_loss = pd.Series(np.zeros(n_models), index=model_names)

    n_pred = len(pred_df)
    nu = np.sqrt(8*np.log(n_models)/n_pred)
    # max_loss = 0
    # model_id = model_names[0]
    observed_rets = pred_df.iloc[:,0]
    for model_id in model_names:
        loss = np.abs(pred_df[model_id] - observed_rets) if loss_type=='ae' else (pred_df[model_id] - observed_rets)**2
        cum_loss[model_id] = np.cumsum(loss)[-1]/loss_bound
    exp_weights = np.exp(-nu*cum_loss)
    model_weights = exp_weights/np.sum(exp_weights)
    return cum_loss, model_weights


def predict_panel(pred_df, loss_type='ae', model_w=None, next_per_pred=None, loss_bound=1):
    """
    One period prediction based on experts panel.

    Parameters:
    ----------
    pred_df : pandas.DataFrame
        DF of observations and models predictions. The first column corresponds to the observed returns. If next_per_pred is None, the last row is used to predict next period.
    lost_type : str
        Prediction loss for each time. Squared (se) or absolute (ae) error (default 'se').
    model_w : pands.Series
        Models weights for average prediction (default None).
    next_per_pred : pandas.Series
        Models predictions (default None).

    Returns:
    -------
    ('weighted_avg_pred', 'weights', 'best_model_id')
    """
    model_names = pred_df.columns[1:]
    if model_w  is None:
        _, model_weights = model_exp_weights(pred_df, loss_type, loss_bound)
    else:
        model_weights = model_w
    best_model_id = model_names[np.argmax(model_weights.values)]

    if next_per_pred is None:
        next_per_pred = pred_df.iloc[-1,1:]
    else:
        next_per_pred.index = [model_weights.index[[x in y for y in model_weights.index]][0] if len(model_weights.index[[x in y for y in model_weights.index]]) else np.nan for x in next_per_pred.index]
        next_per_pred = next_per_pred.loc[next_per_pred.index.dropna()]
    weighted_avg_pred = np.sum(next_per_pred * model_weights.loc[next_per_pred.index]/model_weights.loc[next_per_pred.index].sum())
    return weighted_avg_pred, model_weights, best_model_id

def predict_df(target_var, loc='', ref_date=None):
    """
    target_vat
    """
    pred_files = [x for x in os.listdir(loc) if re.match('.*%s.*' %(target_var.lower()), x.lower()) is not None or re.match('.*%s.*' %(target_var.lower()), x) is not None]
    pred_df = pd.read_csv(loc + pred_files[-1], index_col=[0], parse_dates=True, dayfirst=True).iloc[:,0].to_frame('Observado')
    for filei in pred_files:
        pred_df = pd.concat([pred_df, pd.read_csv(loc + filei, index_col=[0], parse_dates=True, dayfirst=True).iloc[:,1].to_frame(filei.split('.')[0])], axis=1, sort=False)
    if ref_date is not None:
        pred_df = pred_df[pred_df.loc[pred_df.index >= ref_date].iloc[0,:].dropna().index]
    pred_df = pred_df.dropna()
    return pred_df

def predict_mult_panel(target_vars, pred_expert, plots=True, loc='', ref_date=None, loss_type='ae', loss_bound=1):
    best_model = pd.Series('', index=target_vars)
    weighted_avg_pred = pd.Series(0, index=target_vars)
    model_weights = {}
    series_pred_df = pd.DataFrame([])
    series_obs_df = pd.DataFrame([])
    for target_var in target_vars:
        pred_df = predict_df(target_var, loc=loc, ref_date=ref_date)
        try:
            next_per_pred = pred_expert.loc[target_var].dropna()
        except:
            next_per_pred = None
        weighted_avg_pred.loc[target_var], model_weights[target_var], best_model.loc[target_var] = predict_panel(pred_df, loss_type=loss_type, model_w=None, next_per_pred=next_per_pred, loss_bound=loss_bound)
        series_pred = (pred_df[model_weights[target_var].index] @ model_weights[target_var])
        series_pred_df = pd.concat([series_pred_df, series_pred.to_frame(target_var)], axis=1, sort=False)
        series_obs_df = pd.concat([series_obs_df, pred_df.iloc[:,0].to_frame(target_var)], axis=1, sort=False)
        if plots:
            from matplotlib import pyplot as plt
            pd.concat([pred_df.iloc[:,0].to_frame('Observado'), series_pred.to_frame('Predicción')], axis=1, sort=False).plot(color=["#C7C9C7", "#BF9474"])
            plt.title(target_var)
        pred_error = (series_pred_df - series_obs_df).dropna()
        mae = np.mean(np.abs(pred_error), axis=0)
    return best_model, weighted_avg_pred, model_weights, series_pred_df, series_obs_df, mae

def times_to_labels(times):
    labels = np.array([str(int(x))+'Y' if x>0.95 else str(int(np.round(x*12)))+'M' for x in times])
    pos_d = times < 0.08
    if np.any(pos_d):
        labels[pos_d] = [str(int(np.round(times[i]*365))) + 'D' for i in np.where(pos_d)[0]]
    return list(labels)

def predict_fase(db, s3client, ts, model_names, root='', fillna_method = 'ffill',
                 file_name = 'series_list_raven.csv', bucket = 'suraraven'):
    ec_pred = np.zeros((len(ts),4))
    for i in range(len(ts)):
        time_steps = ts[i]
        if fillna_method == 'ffill':
            model_features = db.fetch_model_data(model_names[i], s3client, file_name = file_name, bucket = bucket).iloc[:, 1:].fillna(method = 'ffill').dropna()
        elif fillna_method == 'zeros':
            model_features = db.fetch_model_data(model_names[i], s3client, file_name = file_name, bucket = bucket).iloc[:, 1:].fillna(0).dropna()
        model = joblib.load(root + model_names[i] + '.joblib')
        ec_pred[i, :] = 100 * sklearn_model_forecast(model, model_features, predict_proba = True, custom_predict_prob=False).iloc[-1, :]
        #try:
        #    ec_pred[i, :] = 100 * sklearn_model_forecast(model, model_features, predict_proba = True, custom_predict_prob=True).iloc[-1, :]
        #except:
        #    ec_pred[i, :] = 100 * sklearn_model_forecast(model, model_features, predict_proba = True, custom_predict_prob=False).iloc[-1, :]
    ec_pred_df = pd.DataFrame(ec_pred, index=times_to_labels(ts/12), columns = np.arange(1, 5))
    ec_pred_date = 'Fecha: ' + model_features.index[-1].strftime("%Y-%m-%d")
    return ec_pred_df, ec_pred_date

def raven_predict(db, model_identifiers, s3client, root_models, return_last_n = 1, fillna_method = 'zeros', predict_proba = False,
                return_shap = False, file_name = 'series_list_raven.csv', bucket = 'suraraven'):

    from joblib import load
    assert type(model_identifiers) == list, "model_identifiers parameter must be a list"

    model_identifiers = list(map(lambda x: x.upper(), model_identifiers))
    modelo_ticker_campo = db.fetch_table('modelo_ticker_campo')
    modelo_ticker_campo['identificador'] = modelo_ticker_campo['nombre_modelo'].apply(lambda x: x.split('_')[0].upper())
    modelo_ticker_campo = modelo_ticker_campo[modelo_ticker_campo['identificador'].isin(model_identifiers)]
    output_preds = {}
    output_shap_grouped = pd.DataFrame()
    output_shap_ungrouped = pd.DataFrame()
    for model_to_predict in modelo_ticker_campo['nombre_modelo'].unique():
        if fillna_method == 'zeros':
            data = db.fetch_model_data(model_to_predict, s3client, file_name = file_name, bucket = bucket).iloc[:, 1:].fillna(0).dropna()
        else:
            data = db.fetch_model_data(model_to_predict, s3client, file_name = file_name, bucket = bucket).iloc[:, 1:].fillna(method = fillna_method).dropna()
        model = load(root_models + 'models/' + model_to_predict + '.joblib')
        print(model_to_predict)
        output_preds[model_to_predict] = [list(data.index[-return_last_n:].map(lambda x: x.strftime('%Y-%m-%d')).values), list(model.predict(data.iloc[-return_last_n:, :])) if not predict_proba else list(model.predict_proba(data.iloc[-return_last_n:, :]))]
        if return_shap:
            temp_ungrouped, temp_grouped = shap_values(model_to_predict, model, data, predict_type = 'predict')
            output_shap_grouped = pd.concat([output_shap_grouped, temp_grouped], axis = 0)
            output_shap_ungrouped = pd.concat([output_shap_ungrouped, temp_ungrouped], axis = 0)

    date_list = [val for sublist in [x[0] for x in output_preds.values()] for val in sublist]
    unique_dates = list(dict.fromkeys(date_list))
    output_preds = {k: dict(zip(v[0], v[1])) for k, v in output_preds.items()}
    index = np.unique(list(map(lambda x: x.split('_')[0].upper(), list(output_preds.keys()))))
    columns = np.unique(list(map(lambda x: '_'.join(x.split('_')[1:]).upper(), list(output_preds.keys()))))
    output_pred_dict = {k: pd.DataFrame(index = index, columns = columns) for k in unique_dates}

    for key, value in output_pred_dict.items():
        for index_pos in index:
            for col in columns:
                try:
                    output_pred_dict[key].loc[index_pos, col] = output_preds[index_pos.lower() + '_' + col.lower()][key]
                except:
                    output_pred_dict[key].loc[index_pos, col] = np.nan

    if return_shap:
        return output_pred_dict, unique_dates, output_shap_grouped, output_shap_ungrouped
    else:
        return output_pred_dict, unique_dates

def shap_values(model, estimator, data, predict_type = 'predict'):

    if predict_type == 'predict':
        try:
            explainer = shap.KernelExplainer(estimator.predict, data)
            shap_values = explainer.shap_values(data.iloc[-1, :])
        except:
            data_summary = shap.kmeans(data, 25)
            explainer = shap.KernelExplainer(estimator.predict, data_summary)
            shap_values = explainer.shap_values(data.iloc[-1, :])
        output_ungrouped = pd.DataFrame(shap_values, index = data.columns.values.tolist(), columns = ['SHAP Value'])
        output_grouped = output_ungrouped.reset_index()
        output_grouped['index'] = output_grouped['index'].apply(lambda x: x.split(' | ')[0]) + ' ' + output_grouped['index'].apply(lambda x: x.split(' | ')[1].split(' ')[0])
        output_grouped = output_grouped.groupby(by = 'index').sum().reset_index()
        output_grouped.columns = ['Variable', 'Valor SHAP']
        output_grouped['model'] = model
        output_ungrouped['model'] = model
        output_grouped['date'] = data.index[-1]
        output_ungrouped['date'] = data.index[-1]
        return output_ungrouped, output_grouped
    elif predict_type == 'predict_proba':
        try:
            explainer = shap.KernelExplainer(estimator.predict_proba, data)
            shap_values = explainer.shap_values(data.iloc[-1, :])
        except:
            data_summary = shap.kmeans(data, 25)
            explainer = shap.KernelExplainer(estimator.predict_proba, data_summary)
            shap_values = explainer.shap_values(data.iloc[-1, :])
        output_ungrouped = pd.DataFrame(shap_values, index = [1, 2, 3, 4], columns = data.columns.values.tolist()).T
        output_grouped = output_ungrouped.reset_index()
        output_grouped['index'] = output_grouped['index'].apply(lambda x: x.split(' | ')[0]) + ' ' + output_grouped['index'].apply(lambda x: x.split(' | ')[1].split(' ')[0])
        output_grouped = output_grouped.groupby(by = 'index').sum().reset_index()
        output_grouped.columns = ['Variable', 'SHAP fase 1', 'SHAP fase 2', 'SHAP fase 3', 'SHAP fase 4']
        output_grouped['model'] = model
        output_ungrouped['model'] = model
        output_grouped['date'] = data.index[-1]
        output_ungrouped['date'] = data.index[-1]
        return output_ungrouped, output_grouped

def graph_plot(d, partial_correlations, my_colors, names, labels, embedding, val_max, title):
    from matplotlib import pyplot as plt
    from matplotlib.collections import LineCollection #for plotting purposes
    non_zero = (np.abs(np.triu(partial_correlations, k=1)) > 0.02)
    n_labels = labels.max()

    #For correlation network graph
    fig = plt.figure(1, facecolor='w', figsize=(12, 5))
    plt.clf()
    ax = plt.axes([0., 0., 1., 1.])
    plt.axis('off')

    # Plot the nodes using the coordinates of our embedding
    plt.scatter(embedding[0], embedding[1], s=500 * d ** 2, c= my_colors)

    # Plot the edges
    start_idx, end_idx = np.where(non_zero)
    # a sequence of (*line0*, *line1*, *line2*), where::
    #            linen = (x0, y0), (x1, y1), ... (xm, ym)
    segments = [[embedding[:, start], embedding[:, stop]] for start, stop in zip(start_idx, end_idx)]
    values = np.abs(partial_correlations[non_zero])
    lc = LineCollection(segments,zorder=0, cmap=plt.cm.hot_r,norm=plt.Normalize(0, .7 * val_max))
    lc.set_array(values)
    temp = (15 * values)
    temp2 = np.repeat(5, len(temp))
    w = np.minimum(temp, temp2)
    lc.set_linewidths(w)
    ax.add_collection(lc)
    axcb = fig.colorbar(lc)
    axcb.set_label('Strength')

    for index, (name, label, (x, y)) in enumerate(zip(names, labels, embedding.T)):
        dx = x - embedding[0]
        dx[index] = 1
        dy = y - embedding[1]
        dy[index] = 1
        this_dx = dx[np.argmin(np.abs(dy))]
        this_dy = dy[np.argmin(np.abs(dx))]
        if this_dx > 0:
            horizontalalignment = 'left'
            x = x + .002
        else:
            horizontalalignment = 'right'
            x = x - .002
        if this_dy > 0:
            verticalalignment = 'bottom'
            y = y + .002
        else:
            verticalalignment = 'top'
            y = y - .002
        plt.text(x, y, name, size=10,horizontalalignment=horizontalalignment,verticalalignment=verticalalignment,bbox=dict(facecolor='w',edgecolor=plt.cm.nipy_spectral(label / float(n_labels)),alpha=.6))
    plt.xlim(embedding[0].min() - .15 * embedding[0].ptp(),embedding[0].max() + .10 * embedding[0].ptp(),)
    plt.ylim(embedding[1].min() - .03 * embedding[1].ptp(),embedding[1].max() + .03 * embedding[1].ptp())
    plt.title(title)
    plt.show()



if __name__=="__main__":
	pass
