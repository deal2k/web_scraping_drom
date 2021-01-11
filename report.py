import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# create folder for pages (if not exists)
if not os.path.exists('report'):
    os.mkdir('report')

# load data from CSV file to DataFrame
df = pd.read_csv('cars.csv')

# clean data
df = df[df['mileage'].notna()]
df = df[df['volume'] != 1.8]  # wrong input from user

# price histogram
sns.set_style('white')
sns.histplot(df['price'], bins=20, alpha=0.5, kde=True)
sns.despine(left=True)
plt.savefig('report/price_hist.png')
plt.close()

# type of fuel
sns.set_style('white')
sns.countplot(x=df['fuel'], alpha=0.5)
sns.despine(left=True)
plt.savefig('report/fuel.png')
plt.close()

# type of drive
sns.set_style('white')
sns.countplot(x=df['drive'], alpha=0.5)
sns.despine(left=True)
plt.savefig('report/drive.png')
plt.close()

# price change vs mileage
sns.set_style('darkgrid')
sns.lmplot(data=df, x='mileage', y='price', order=3, 
           hue='volume', ci=None)
sns.despine(left=True)
plt.savefig('report/price_mileage.png')
plt.close()

# price change per year
sns.set_style('darkgrid')
sns.regplot(data=df, x='year', y='price', order=4,
            x_estimator=np.mean)
sns.despine(left=True)
plt.savefig('report/price_year.png')
plt.close()