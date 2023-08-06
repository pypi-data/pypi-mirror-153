
import numpy as np
import pandas as pd
import math
from .utils import *
import os
from . import models
from sklearn.externals import joblib
from timeit import default_timer as timer
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils import data
from sklearn.preprocessing import MinMaxScaler



class LSTMModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, layer_dim, output_dim):
        super(LSTMModel, self).__init__()
        # Hidden dimensions
        self.hidden_dim = hidden_dim

        # Number of hidden layers
        self.layer_dim = layer_dim

        # Building your LSTM
        # batch_first=True causes input/output tensors to be of shape
        # (batch_dim, seq_dim, feature_dim)
        self.lstm = nn.LSTM(input_dim, hidden_dim, layer_dim, batch_first=True)

        # Readout layer
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        # Initialize hidden state with zeros
        h0 = torch.zeros(self.layer_dim, x.size(0), self.hidden_dim).requires_grad_()

        # Initialize cell state
        c0 = torch.zeros(self.layer_dim, x.size(0), self.hidden_dim).requires_grad_()

        # 28 time steps
        # We need to detach as we are doing truncated backpropagation through time (BPTT)
        # If we don't, we'll backprop all the way to the start even after going through another batch
        out, (hn, cn) = self.lstm(x, (h0.detach(), c0.detach()))

        # Index hidden state of last time step
        # out.size() --> 100, 28, 100
        # out[:, -1, :] --> 100, 100 --> just want last time step hidden states!
        out = self.fc(out[:, -1, :])
        # out.size() --> 100, 10
        return out


class LongTermPredictor():
	"""
		Clase para crear los modelos, entrenarlos y predecir con ellos, en general es la clase principal y mediante esta se interactua con los modelos.

	"""
	def __init__(self, data, time_steps, train_size=0.7, test_size=0.15, val_size=0.15, dir=''):
		"""
			Constructor de la clase, se encarga de cargar o entrenar el modelo según lo especificado en los hyperparámetros.

			Parámetros:
			- data -- Dataframe, arreglo con todos los datos, incluidos los de test (Todos los datos son necesarios para la selección de variables).
			- id_model -- Entero, id del modelo que se va a utilizar. LSTM:0, Random Forest:1, adaBoost:2, SVM:3, ARIMA: 4.
			- original -- Booleano, indica si entenar con las varaibles originales o con las eleccionadas. True para entrenar con las originales.
			- time_steps -- Entero, número de periodos en el futuro a predecir
			- returns -- Booleano, indica si se está trabajando con retornos o no (serie diferenciada). True es que si se trabaja con retornos.
			- to_returns -- Booleano, indica si se se deben transformar los datos a retornos.

			- model_file_name -- *string*, con el nombre del archivo que contiene el modelo que se quiere cargar
		"""
		self.data = data
		self.time_steps = time_steps
		self.train_size = train_size
		self.test_size = test_size
		self.val_size = val_size
		self.model = None
		self.freqs = {'daily':252, 'monthly':12, 'quarterly':4, 'yearly':1}

	def train_rnn(self, n_lags, batch_size, hidden_dim, layer_dim, output_dim, learning_rate=0.01, n_iters=10000):
		train_X, test_X, val_X, train_y, test_y, val_y, last_values = transform_values(data=self.data, n_lags=n_lags, n_series=self.time_steps, dim=True, train_size=self.train_size, test_size=self.test_size, val_size=self.val_size)
		train_tensor_X = torch.stack([torch.Tensor(i) for i in train_X]) # transform to torch tensors
		train_tensor_y = torch.stack([torch.Tensor(i) for i in train_y])
		train_dataset = data.TensorDataset(train_tensor_X,train_tensor_y) # create your datset
		train_loader = data.DataLoader(train_dataset, batch_size=batch_size, shuffle=True) # create your dataloader

		test_tensor_X = torch.stack([torch.Tensor(i) for i in test_X]) # transform to torch tensors
		test_tensor_y = torch.stack([torch.Tensor(i) for i in test_y])
		test_dataset = data.TensorDataset(test_tensor_X,test_tensor_y) # create your datset
		test_loader = data.DataLoader(test_dataset, batch_size=batch_size, shuffle=False) # create your dataloader

		val_tensor_X = torch.stack([torch.Tensor(i) for i in val_X]) # transform to torch tensors
		val_tensor_y = torch.stack([torch.Tensor(i) for i in val_y])
		val_dataset = data.TensorDataset(val_tensor_X,val_tensor_y) # create your datset
		val_loader = data.DataLoader(val_dataset, batch_size=batch_size, shuffle=False) # create your dataloader
		input_dim = train_X.shape[2] # Features
		model = LSTMModel(input_dim, hidden_dim, layer_dim, output_dim)

		criterion = torch.nn.MSELoss(reduction='sum') ##nn.CrossEntropyLoss()

		optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
		num_epochs = int(n_iters / (len(train_X) / batch_size))

		seq_dim = train_X.shape[1]
		mse_list = []
		iter = 0

		for epoch in range(num_epochs):
		    for i, (batch, obs) in enumerate(train_loader):
		        # Load images as a torch tensor with gradient accumulation abilities
		        batch = batch.view(-1, seq_dim, input_dim).requires_grad_()
		        # Clear gradients w.r.t. parameters
		        optimizer.zero_grad()

		        # Forward pass to get output/logits
		        # outputs.size() --> 100, 10
		        outputs = model(batch)

		        # Calculate Loss: softmax --> cross entropy loss
		        loss = criterion(outputs, obs)
		        # Getting gradients w.r.t. parameters
		        loss.backward()
		        # Updating parameters
		        optimizer.step()
		        iter += 1

		        if iter % 50 == 0: #iter % 50 == 0:
		            # Calculate Accuracy
		            # correct = 0
		            # total = 0
		            mse = 0
		            # Iterate through test dataset
		            for batch, obs in test_loader:
		                # Resize images
		                batch = batch.view(-1, seq_dim, input_dim)

		                # Forward pass only to get logits/output
		                outputs = model(batch)

		                # Get predictions from the maximum value
		                # _, predicted = torch.max(outputs.data, 1)
		                # print(obs)
		                mse += torch.sum((outputs.data - obs) ** 2)
		                #mse += (predicted - obs.squeeze()) #** 2

		                # Total number of labels
		                # total += labels.size(0)

		                # Total correct predictions
		                # correct += (predicted == labels).sum()

		            mse_list.append(mse.double())
		            # accuracy = 100 * correct / total

		            # Print Loss
		            # print('Iteration: {}. Loss: {}. Accuracy: {}'.format(iter, loss.item(), accuracy))
		            print('Iteration: {}. Loss: {}. Accuracy: {}'.format(iter, loss.item(), mse))
		self.model = model
		return test_tensor_X, test_y, val_tensor_X, val_y

	def recursive_pred(self, n_steps, input_tensor_X, period):
		freq = self.freqs[period]
		recur_pred = np.zeros((n_steps,1))
		temp_tensor_X = input_tensor_X.clone()
		for i in range(n_steps):
		    recur_pred[i,0] = self.model(temp_tensor_X).cpu().data.numpy()[0]
		    temp_tensor_X[0][0:-1] = temp_tensor_X[0][1::]
		    temp_tensor_X[0][-1] = recur_pred[i,0]

		data_ext = np.ma.row_stack((self.data,recur_pred))
		ret_mean = self.data.mean()*freq*100
		ret_mean_ext = data_ext.mean()*freq*100
		ret_mean_fut = recur_pred.mean()*freq*100

		return data_ext, recur_pred, ret_mean, ret_mean_ext, ret_mean_fut
		
	def train_sarimax(self, series, target_var):
			steps=-1
			dataset_for_prediction= pd.DataFrame(series.copy())
			dataset_for_prediction['Actual']=dataset_for_prediction.shift(steps)
			dataset_for_prediction=dataset_for_prediction.dropna()

			sc_in = MinMaxScaler(feature_range=(0, 1))
			scaled_input = sc_in.fit_transform(dataset_for_prediction[[target_var]])
			scaled_input =pd.DataFrame(scaled_input)
			X = scaled_input

			sc_out = MinMaxScaler(feature_range=(0, 1))
			scaler_output = sc_out.fit_transform(dataset_for_prediction[['Actual']])
			scaler_output =pd.DataFrame(scaler_output)
			y=scaler_output

			train_size=int(len(dataset_for_prediction) *0.7)
			test_size = int(len(dataset_for_prediction)) - train_size
			train_X, train_y = X[:train_size].dropna(), y[:train_size].dropna()
			test_X, test_y = X[train_size:].dropna(), y[train_size:].dropna()

			X.rename(columns={0:'Mean'}, inplace=True)
			X.index = dataset_for_prediction.index

			y.rename(columns={0:'Pred'}, inplace= True)
			y.index=dataset_for_prediction.index

			import statsmodels.api as sm
			seas_d=sm.tsa.seasonal_decompose(X['Mean'], model='add',freq=365);
			fig=seas_d.plot()
			fig.set_figheight(4)


if __name__=="__main__":
	pass
