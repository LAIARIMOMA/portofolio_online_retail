import pandas as pd
base_2010 ='..\\data\\brute\\online_retail_2010.csv'
base_2011 = '..\\data\\brute\\online_retail_2011.csv'
data_2010 = pd.read_csv(base_2010,sep= ';',parse_dates=['InvoiceDate'],dayfirst=True)
data_2011 = pd.read_csv(base_2011,sep= ';',parse_dates=['InvoiceDate'],dayfirst=True)
 
data_total = pd.concat([data_2010, data_2011], ignore_index=True)

data_total.isnull().sum()
data_total=data_total.dropna(subset=['Customer ID'])


data_total=data_total[data_total['InvoiceDate']>='01/01/2010 00:00']
data_total=data_total.drop_duplicates()

print('comande_sans_DOUBLONS')
print(data_total.describe())
print(data_total.info())
data_total['mois']=data_total['InvoiceDate'].dt.month
data_total['anne']=data_total['InvoiceDate'].dt.year

commande_vendue=data_total[(data_total['Quantity'])>0]
commande_annule=data_total[(data_total['Quantity'])<0]
commande_vendue['Revenue']=commande_vendue['Price']*commande_vendue['Quantity']
print('comande_sansa_VENDUES')
print(commande_vendue.info())
print(commande_vendue.describe())
commande_vendue.to_csv('..\\data\\nettoyer\\Online_Retail_a_analyser.csv',index=False)