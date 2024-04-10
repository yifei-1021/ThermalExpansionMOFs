import glob
import numpy as np
from scipy.stats import uniform
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error


def parition_data(df):
    # Feature Space: 156 features
    X = df.iloc[:, 2:-1]
    #X = df.iloc[:20, 2:-2] ### TEST
    # Target space (WC, uptake)
    y1= df.iloc[:, -1], df.iloc[:, -1]



def train(RF, X_train,y_train, name="GSCV"):
	RF.fit(X_train, y_train)
	import pickle
	with open(f'trained_model/RF-{name}-GSCV.pkl', 'wb') as file:
		pickle.dump(RF, file)

def GSCV(X_train, y_train, reg, param_grid):
  # Perform GridSearchCV for hyperparameter tuning
  X_train_tune, X_val, y1_train_tune, y_val = train_test_split(X_train, y1_train, test_size=0.2, random_state=42)
  grid_search = GridSearchCV(estimator=reg, param_grid=param_grid, scoring='neg_mean_squared_error', cv=3)
  grid_search.fit(X_train_tune, y1_train_tune)
  
  # Get the best model from hyperparameter tuning
  best_reg = grid_search.best_estimator_
  
  # Save the results to a CSV file
  results_df = pd.DataFrame(grid_search.cv_results_)
  results_df.to_csv('grid_search_results.csv', index=False)
  return best_reg, X_train_tune, y1_train_tune
  

if __name__ == "__main__":
	CSV = glob.glob(f"./DATABASE/DATASET.csv")[0] #CSV = glob.glob(f"./DATABASE/update.{CYCLE_NUM-1}.*csv")[0]
	assert len(CSV) > 0, f"CSV not found!!!"
  
	random_state = np.random.RandomState(0)
	traindf = pd.read_csv(CSV, index_col=0)

	labels = 'y'
	labelled_df = traindf[~traindf[labels].isnull()]; #labelled_df.to_csv(f"labelled_{labelled_df.shape[0]}samples.csv")
	ulablled_df = traindf[traindf[labels].isnull()];	#ulablled_df.to_csv(f"ulablled_{ulablled_df.shape[0]}samples.csv")
  
	X_train, y1_train, _, cifname_train = parition_data(labelled_df)
  # Define the parameter grid for hyperparameter tuning
	param_grid = {'n_estimators': [50, 100, 200, 400, 1000],'max_depth': [None, 10, 20], 'min_samples_split': [2, 5, 10],'min_samples_leaf': [1, 2, 4]}
	best_reg, X_train_tune, y1_train_tune = GSCV(X_train, y1_train, RandomForestRegressor(random_state=42), param_grid)
	train(best_reg, X_train_tune, y1_train_tune)
  
	### Prediction
	X_test, y1_test_Na, y2_test_Na, cifname_test = parition_data(ulablled_df)
	prediction = best_reg.predict(X_test)
	print(cifname_test)
	print(prediction)
	
	# Save prediction
	cifname_test[labels] =  prediction
	cifname_test.describe()
	cifname_test.to_csv(f'predicted_WC_{len(prediction)}.csv')

	
