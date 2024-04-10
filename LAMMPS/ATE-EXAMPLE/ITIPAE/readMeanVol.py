import pandas as pd
import numpy as np
import os, csv, re
import matplotlib.pyplot as plt
plt.rcParams['font.size'] = 13
plt.rcParams['font.size'] = 14
plt.rcParams["axes.edgecolor"] = "black"
plt.rcParams["axes.linewidth"] = 4

def calRsq(actual, predict):
    return np.corrcoef(actual, predict)[0, 1]**2
    
def fit_lreg(xval, yval):
    coeff = np.polyfit(xval, yval, deg=1)
    predict = coeff[0] * xval + coeff[1]
    
    R_sq = calRsq(yval, predict)
    return coeff, R_sq
    
def plot_lreg(xval, yval, coeff,
            xlabel, ylabel, savename, R_sq, fig, ax):
            
    xlin = np.linspace(np.min(xval), np.max(xval),100)
    ylin = coeff[0] * xlin + coeff[1]       
    ax.plot(xlin, ylin, c='r', lw=4, label = r"$R^2$ ="f' {R_sq:.2f}')
    ax.scatter(xval, yval, marker='s', s = 28,label = f'Simulated Data')
    ax.set_ylabel(ylabel, fontsize=16)
    ax.set_xlabel(xlabel, fontsize=16)
    ax.legend(loc="best")
    ax.grid('on')
    
cwd = os.getcwd()
MOF_NAME = str(cwd).split("/")[-1]

subfiles = [i for i in  os.listdir() if i[-4:] == '.txt']
print(f'List of textfiles {subfiles} in {cwd}')
temp=[]
vol=[]
cella=[]
cellb=[]
cellc=[]

for subfile in subfiles:
    if 'results' in subfile:
      sim_temp = float(re.findall(r'\d+', subfile)[0])
      with open(subfile) as f:
        for line in f:
            pass
        last_line = line
        
      last_line = last_line.split(" ")
      final_vol, final_cella = float(last_line[1]), float(last_line[2])
      final_cellb, final_cellc = float(last_line[3]), float(last_line[4])
      
      temp.append(sim_temp)
      vol.append(final_vol)
      cella.append(final_cella)
      cellb.append(final_cellb)
      cellc.append(final_cellc)
      
      if sim_temp == 300:
        vol0 = final_vol
        a0 = final_cella
        b0 = final_cellb
        c0 = final_cellc
      
df = pd.DataFrame({"T(K)": temp, "Volume":vol, "Lattice Parameter (a)": cella, "Lattice Parameter (b)": cellb, "Lattice Parameter (c)": cellc})
df = df.sort_values(by=["T(K)"]).reset_index(drop=True)
df['V/V0'] = df["Volume"]/vol0

df['a/a0'] = df["Lattice Parameter (a)"]/a0
df['b/b0'] = df["Lattice Parameter (b)"]/b0
df['c/c0'] = df["Lattice Parameter (c)"]/c0

temp = df["T(K)"].to_numpy()
vol, cella = df['V/V0'].to_numpy(), df['a/a0'].to_numpy()
print(df)

### Calculate parameters for volume
print(temp, vol)

fig, ax = plt.subplots(2, 2, figsize=(12, 8))

coeff_vol, Rsq_vol = fit_lreg(np.array(temp), vol)

plot_lreg(temp,vol,coeff_vol, xlabel=r'Temperature $(K)$', ylabel=r'$V/V0$', savename=f'{MOF_NAME}_Volume-Expansion.png', R_sq=Rsq_vol, fig=fig, ax=ax[0,0])
print(coeff_vol, Rsq_vol)

### Calculate parameters for lattice parameter
coeff_a, Rsq_a = fit_lreg(np.array(temp), cella)
print(coeff_a, Rsq_a)

plot_lreg(temp,cella,coeff_a, xlabel=r'Temperature $(K)$', ylabel=r'$a/a0$', savename=f'{MOF_NAME}_a-Expansion.png', R_sq=Rsq_a, fig=fig, ax=ax[0,1])
cellb = df["b/b0"].to_numpy() 
cellc = df["c/c0"].to_numpy()
coeff_b, Rsq_b = fit_lreg(np.array(temp), cellb)
coeff_c, Rsq_c = fit_lreg(np.array(temp), cellc)

plot_lreg(temp,cellb,coeff_b, xlabel=r'Temperature $(K)$', ylabel=r'$b/b0$', savename=f'{MOF_NAME}_a-Expansion.png', R_sq=Rsq_b, fig=fig, ax=ax[1,0])
plot_lreg(temp,cellc,coeff_c, xlabel=r'Temperature $(K)$', ylabel=r'$c/c0$', savename=f'{MOF_NAME}_a-Expansion.png', R_sq=Rsq_c, fig=fig, ax=ax[1,1])

fig.suptitle(f'Simulated Thermal Expansion of {MOF_NAME}', fontweight='bold')
fig.tight_layout(pad=1.0)
fig.savefig(f'{MOF_NAME}_Validation.png')

summary_name = f'{MOF_NAME}_RegressionSummary.csv' 
df.to_csv(summary_name , index=False, header=True)



summary_name = f'{MOF_NAME}_Coefficients.csv' 
df = pd.DataFrame({"Vol_Coeff": coeff_vol, "Lattice_a": coeff_a, "Lattice_b": coeff_b, "Lattice_c": coeff_c})

df.loc[len(df.index)] = [Rsq_vol, Rsq_a, Rsq_b, Rsq_c]
df.to_csv(summary_name, index=False, header=True)

if (Rsq_vol < 0.9):
  df = pd.DataFrame({"Lattice_Vol": coeff_vol})
  df.to_csv(f'{MOF_NAME}_VOL_ERROR.csv', index=False, header=True)

if (Rsq_a < 0.9):
  df = pd.DataFrame({"Lattice_a": coeff_a})
  df.to_csv(f'{MOF_NAME}_LATTICEA_ERROR.csv', index=False, header=True)
  
if (Rsq_b < 0.9):
  df = pd.DataFrame({"Lattice_b": coeff_b})
  df.to_csv(f'{MOF_NAME}_LATTICEB_ERROR.csv', index=False, header=True)

if (Rsq_c < 0.9):
  df = pd.DataFrame({"Lattice_c": coeff_c})
  df.to_csv(f'{MOF_NAME}_LATTICEC_ERROR.csv', index=False, header=True)
