import os 
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import datetime
base='..\\data\\nettoyer\\Online_Retail_a_analyser.csv'
df_a_analyser= pd.read_csv(base,parse_dates=['InvoiceDate'])
df_a_analyser['Revenue']=df_a_analyser['UnitPrice']*df_a_analyser['Quantity']
date_max= df_a_analyser['InvoiceDate'].max() +pd.Timedelta(days=1)
rfm = df_a_analyser.groupby('CustomerID').agg({
'InvoiceDate': lambda x: (date_max- x.max()).days,
'InvoiceNo': 'nunique',
'Revenue': 'sum'
}).reset_index()         
rfm.rename(columns={'InvoiceDate':'Recency','InvoiceNo':'Frequency','Revenue':'Monetary'}, inplace=True)
print(rfm.head())
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1], duplicates='drop')  


rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5], duplicates='drop')
rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5], duplicates='drop')
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + \
                      rfm['F_Score'].astype(str) + \
                      rfm['M_Score'].astype(str)

print(rfm[['CustomerID','RFM_Score']].head().to_string(index=False))
rfm['R_Score']=rfm['R_Score'].astype(str)
rfm['F_Score']=rfm['F_Score'].astype(str)
rfm['M_Score']=rfm['M_Score'].astype(str)
conditions = [
    # Champions : Récence élevée (4 ou 5) ET Fréquence/Montant élevés (4 ou 5)
    (rfm['R_Score'].isin(['4', '5'])) & (rfm['F_Score'].isin(['4', '5'])) & (rfm['M_Score'].isin(['4', '5'])),
    # Clients Fidèles : Récence moyenne (2 ou 3) ET Fréquence/Montant élevés (4 ou 5)
    (rfm['R_Score'].isin(['2', '3','4'])) & (rfm['F_Score'].isin(['3','4', '5'])),
    # Clients En Danger : Récence faible (1 ou 2) mais historiquement bons (F & M élevés)
    (rfm['R_Score'].isin(['1', '2'])) & (rfm['F_Score'].isin(['4', '5'])),
    # Clients Perdus : Tout est faible
    (rfm['R_Score'].isin(['1', '2'])) & (rfm['F_Score'].isin(['1', '2'])),
    (rfm['R_Score'].isin(['4', '5'])) & (rfm['F_Score'].isin(['1']))
]

choix_segments = [
    'Meilleurs Clients (Champions)',
    'Clients Fidèles',
    'Clients En Danger',
    'Clients Perdus',
    'Nouveau client'
]
# 6. Application des règles (le reste est classé 'Autres')
rfm['Segment'] = np.select(conditions, choix_segments, default='Autres')
pourcentage=rfm.groupby(['Segment']).size().reset_index(name='nombre')
somme=pourcentage['nombre'].sum()
pourcentage['pourcent']=((pourcentage['nombre']/somme)*100 ).map('{:.2f}%'.format)  # afficher deux chiffres apres
pourcentage_rev=rfm.groupby('Segment')['Monetary'].sum().reset_index(name='total_revenue')
somme_rev=pourcentage_rev['total_revenue'].sum()
pourcentage_rev['pourcent']=((pourcentage_rev['total_revenue']/somme_rev)*100 ).map('{:.2f}%'.format)
print('pourcentage  par nombre de segment')
print(pourcentage)
print("pourcentage  par segment par Chiffre d'Affaie")
print(pourcentage_rev)
