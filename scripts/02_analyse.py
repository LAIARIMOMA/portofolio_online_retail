import os 
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import datetime
base='..\\data\\nettoyer\\Online_Retail_a_analyser.csv'
df_a_analyser= pd.read_csv(base,parse_dates=['InvoiceDate'])
df_a_analyser['Revenue']=df_a_analyser['UnitPrice']*df_a_analyser['Quantity']
df_a_analyser['mois']=df_a_analyser['InvoiceDate'].dt.month
df_a_analyser['anne']=df_a_analyser['InvoiceDate'].dt.year
df_a_analyser.head()
df_a_analyser.groupby('CustomerID')['Revenue'].sum()
print('Nombre de transactions :',df_a_analyser['InvoiceNo'].nunique())
print('Nombre de clients :', df_a_analyser['CustomerID'].nunique())
print('Nombre de produits :', df_a_analyser['StockCode'].nunique())
top_products = df_a_analyser.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
top_products.to_excel('..\\repports\\top10_produit.xlsx')
plt.figure(figsize=(12,6))

sns.barplot(x=top_products.values, y=top_products.index)
plt.title('Top 10 produits les plus vendus')
top_revenue_products = df_a_analyser.groupby('Description')['Revenue'].sum().sort_values(ascending=False).head(10)
top_revenue_products.to_excel('..\\repports\\top10_revenue_produit.xlsx')
plt.figure(figsize=(12,6))
sns.barplot(x=top_revenue_products.values, y=top_revenue_products.index)
plt.title("Top 10 produits par Revenue(CA)")

top_revenue_par_anne = df_a_analyser.groupby(['anne','mois'])['Revenue'].sum().sort_index(ascending=True)
df_revenu=top_revenue_par_anne.to_frame(name='revenue')
df_revenu['pourcentage']=(df_revenu['revenue']/df_revenu.groupby(level=0)['revenue'].transform('sum'))*100   #anne premier index(0)
print(df_revenu)
plt.show()