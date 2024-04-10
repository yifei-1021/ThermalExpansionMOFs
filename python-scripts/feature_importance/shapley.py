import pandas as pd
import pickle
import shap
import glob
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap


def partition_data(df):
    # Feature Space: 156 features
    X = df.iloc[:, 2:-1]
    #X = df.iloc[:20, 2:-2] ### TEST
    # Target space (WC, uptake)
    y1= df.iloc[:, -1], df.iloc[:, -1]

    return X.to_numpy(), y1.to_numpy()

def plot_summary(shap_values, X_test, columns):
    plt.figure(figsize=(16, 10))
    
    cmap = plt.get_cmap('plasma_r')
    cmap = truncate_colormap(cmap, 0.2, 1.0)
    # Summary plot to visualize feature importance
    shap.summary_plot(shap_values, X_test, feature_names=columns, max_display=10,cmap=cmap)
    plt.savefig('shap_summary_plot10.png')
    
    plt.figure(figsize=(16, 10))
    cmap = plt.get_cmap('plasma_r')
    cmap = truncate_colormap(cmap, 0.2, 1.0)
    # Summary plot to visualize feature importance
    shap.summary_plot(shap_values, X_test, feature_names=columns, max_display=20,
    cmap=cmap)
        
    # Save the summary plot using Matplotlib
    plt.savefig('shap_summary_plot20.png')

def plot_violin( shap_values, X_test, columns):
    plt.figure(figsize=(16, 10))
    # Summary plot to visualize feature importance
    #shap.summary_plot(shap_values, X_test, feature_names=columns)
    shap.plots.violin(
      shap_values, features=X_test, feature_names=columns, plot_type="layered_violin",max_display=10
    )
    # Save the summary plot using Matplotlib
    plt.savefig('shap_volin_plot_10.png')
    
    plt.figure(figsize=(16, 10))
    shap.plots.violin(
      shap_values, features=X_test, feature_names=columns, plot_type="layered_violin", max_display=20
    )
    # Save the summary plot using Matplotlib
    plt.savefig('shap_volin_plot_20.png')


if __name__ == '__main__':
    # Load the saved RandomForestRegressor model from a pkl file
    MODELPATH = 'trained_model/MODEL.pkl'  # Replace with the path to your pkl file
    DATAPATH = "DATASET.csv"
    with open(MODELPATH, 'rb') as file:
        rf_model = pickle.load(file)
      
    # Load your dataset for SHAP analysis (replace 'your_data.csv' with your actual dataset)
    data_path = glob.glob(DATAPATH)[0]  # Replace with the path to your CSV file
    traindf = pd.read_csv(data_path, index_col=0)

    ## Check for unlabelled data if any
    labels = 'y'
    unlabelled_df = traindf[traindf[labels].isnull()]
    unlabelled_df.to_csv(f"unlabelled_{unlabelled_df.shape[0]}samples.csv")
	
    X_test, y_test = partition_data(unlabelled_df)
  
    # Initialize a SHAP explainer with the RandomForestRegressor model
    columns = unlabelled_df.columns[2:-2] ; print(f"feature names {columns}"); print(f"X_test {X_test.shape}")
    explainer = shap.TreeExplainer(rf_model)
  
    # Calculate SHAP values for the entire dataset
    shap_values = explainer.shap_values(X_test)
        
    # Save SHAP values using pickle with a descriptive filename
    with open('trained_model/shap_values.pkl', 'wb') as file:
        pickle.dump(shap_values, file)
    
    plot_summary(shap_values, X_test, columns)
    plot_violin(shap_values, X_test, columns)
    
    # Individual SHAP value plots (adjust the index based on your dataset)
    #plot_summary(explainer, shap_values, X_test, sample_index=0)
    


