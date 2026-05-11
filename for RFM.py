# -*- coding: utf-8 -*-
"""
Created on Tue Jan  6 15:50:54 2026

@author: savin
"""
"""
Pseudo code
1) import data
2) convert InvoiceDate to pandas date time 
3) find the max invoice date from the entire data
4) find reference date by adding 1 day to the max of InvoiceDate
5) filter for 1 customer id
6) find max of invoice date for that customer
7) find recency: recency = reference date - max of invoice date for that customer (recency is the number of days since last purchase)
8) find frequency: frequency = number of unique invoices (how often the customer purchased)
9) find monetary: monetary = sum of (quantity * unit price)  (how much the customer spent)
10) create customer_id list
11) create recency list
12) create frequency list
13) create monetary list
14) loop through each customer id
15) add recency to recency list
16) add frequency to frequency list
17) add monetary to monetary list
16) zip customer_id list and recency, frequency and monetary lists into output variable
17) convert ouput to csv
"""

import pandas as pd
import numpy as np

data = pd.read_csv("C:/Users/savin/OneDrive/Desktop/Spyder projects/for RFM customer segmentation/data.csv", encoding="latin1")



data["InvoiceDate"] = pd.to_datetime(data["InvoiceDate"],errors="coerce",infer_datetime_format=True)


max_invoice_date = data["InvoiceDate"].max()
reference_date = max_invoice_date + pd.Timedelta(days=1)

#start of base code
data_cust_id1 = data[data["CustomerID"]==17850]

max_of_invoice_date_cust_id_1 = data_cust_id1["InvoiceDate"].max()

recency = reference_date - max_of_invoice_date_cust_id_1

frequency = data_cust_id1["InvoiceNo"].nunique()

monetary = sum(data_cust_id1["Quantity"]*data_cust_id1["UnitPrice"])

#end of base code

customer_id_list = data["CustomerID"].unique().tolist()

recency_list = []
frequency_list = []
monetary_list = []

for i in customer_id_list:
    
    data_cust_id1 = data[data["CustomerID"]==i]

    max_of_invoice_date_cust_id_1 = data_cust_id1["InvoiceDate"].max()

    recency = reference_date - max_of_invoice_date_cust_id_1

    frequency = data_cust_id1["InvoiceNo"].nunique()

    monetary = sum(data_cust_id1["Quantity"]*data_cust_id1["UnitPrice"])
    
    recency_list.append(recency)
    frequency_list.append(frequency)
    monetary_list.append(monetary)
    
output = pd.DataFrame(list(zip(customer_id_list,recency_list,frequency_list,monetary_list)),columns = ["Customer_id","Recency","Frequency","Monetary"])
    
    
output["Recency"] = pd.to_timedelta(output["Recency"]).dt.days    

quartile_cuts = [25,50,75]

recency_per_cut = []
frequency_per_cut = []
monetary_per_cut = []

for i in quartile_cuts:
    
    q1 = np.nanpercentile(output["Recency"],i)    
    recency_per_cut.append(q1)
    
    q1 = np.nanpercentile(output["Frequency"],i)    
    frequency_per_cut.append(q1)
    
    q1 = np.nanpercentile(output["Monetary"],i)    
    monetary_per_cut.append(q1)
    
recency_bands = []
recency_score_bands = []

frequency_bands = []
frequency_score_bands = []

monetary_bands = []
monetary_score_bands = []

for i in output["Recency"]:
    
    if pd.isna(i):
        y = "1. missing value"
        score = 0
    elif i < recency_per_cut[0]:
        y = f"2. <{recency_per_cut[0]}"
        score = 10
    elif i < recency_per_cut[1]:
        y = f"3. {recency_per_cut[0]} to {recency_per_cut[1]}"
        score = 7.5
    elif i < recency_per_cut[2]:
        y = f"4. {recency_per_cut[1]} to {recency_per_cut[2]}"
        score = 5
    else:
        y = f"5. {recency_per_cut[2]}+"
        score = 2.5
    
    recency_bands.append(y)
    recency_score_bands.append(score)

for i in output["Frequency"]:
    
    if pd.isna(i):
        y = "1. missing value"
        score = 0
    elif i < frequency_per_cut[0]:
        y = f"2. <{frequency_per_cut[0]}"
        score = 2.5
    elif i < frequency_per_cut[1]:
        y = f"3. {frequency_per_cut[0]} to {frequency_per_cut[1]}"
        score = 5
    elif i < frequency_per_cut[2]:
        y = f"4. {frequency_per_cut[1]} to {frequency_per_cut[2]}"
        score =  7.5
    else:
        y = f"5. {frequency_per_cut[2]}+"
        score = 10
    
    frequency_bands.append(y)
    frequency_score_bands.append(score)

for i in output["Monetary"]:
    
    if pd.isna(i):
        y = "1. missing value"
        score = 0
    elif i < monetary_per_cut[0]:
        y = f"2. <{monetary_per_cut[0]}"
        score = 2.5
    elif i < monetary_per_cut[1]:
        y = f"3. {monetary_per_cut[0]} to {monetary_per_cut[1]}"
        score = 5
    elif i < monetary_per_cut[2]:
        y = f"4. {monetary_per_cut[1]} to {monetary_per_cut[2]}"
        score = 7.5
    else:
        y = f"5. {monetary_per_cut[2]}+"
        score = 10
    
    monetary_bands.append(y)
    monetary_score_bands.append(score)

output2 = pd.DataFrame(list(zip(customer_id_list,recency_list,recency_bands,recency_score_bands,frequency_list,frequency_bands,frequency_score_bands,monetary_list,monetary_bands,monetary_score_bands)),columns=["customer_id","recency","recency_bands","recency_score","frequency","frequency_bands","frequency_score","monetary","monetary_bands","monetary_score"])
    

output2["total_score"] = output2[["recency_score","frequency_score","monetary_score"]].sum(axis=1)


#output2.to_csv("C:/Users/savin/OneDrive/Desktop/Spyder projects/for RFM customer segmentation/output.csv")    
   





