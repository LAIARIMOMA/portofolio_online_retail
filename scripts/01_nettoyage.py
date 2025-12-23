import pandas as pd
base='..\\data\\brute\\Online_Retail.csv'
data_frame = pd.read_csv(base)
data_frame.info()
data_frame.describe()
data_frame.isnull().sum()
data_frame=data_frame.dropna(subset=['CustomerID'])
data_frame=data_frame.drop_duplicates()
data_frame.info()
commande_vendue=data_frame[(data_frame['Quantity'])>0]
commande_annule=data_frame[(data_frame['Quantity'])<0]

commande_vendue.describe()
commande_vendue.to_csv('..\\data\\nettoyer\\Online_Retail_a_analyser1.csv',index=False)

