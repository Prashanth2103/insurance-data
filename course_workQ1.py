#-*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from pandas import DataFrame as df
import matplotlib.pyplot as plt


data = pd.read_csv(r"C:\Users\Sneha\OneDrive\Desktop\Insurance_Data_and_Description_CW1.csv")

###  a. List all professions and products in the dataset.

prof_prod = data[['Product', 'Profession']]
print(prof_prod)

###  b. Find and describe any issues with the data. 

# 1. Duplicate values found

# prof_prod.duplicated().sum()
# Out[28]: 14804 out of 14845


# 2. Use of wrong datatype

#instead of using int(4000) they have used string(4k) 



###   c. Clean and transform the data into the correct data types

df = pd.DataFrame(data)

df["First Rate Paid"] = df["First Rate Paid"].map({"Y": True, "N": False})    # Convert "first_rate_paid" column to boolean
df["Contract sum"] = df["Contract sum"].replace("K", "000", regex=True).astype(float)   # Convert "contract_sum" column to float
df["Closing Date"] = pd.to_datetime(df["Closing Date"])      # Convert "closing_date" column to datetime
df = df.reset_index(drop=True)    # Reset index
df = df.dropna()     # Delete empty cells
print(df)
 


###  d. Add a new column “Age Group” and fill up its data according to the criteria below:
for col in ["Contract sum", "Closing Date"]:
  

    conditions = [
        (data['Age']<=16),
        (data['Age']>=17) & (data['Age']<=24),
        (data['Age']>=25) & (data['Age']<=29),
        (data['Age']>=30) & (data['Age']<=39),
        (data['Age']>=40) & (data['Age']<=49),
        (data['Age']>=50) & (data['Age']<=59),
        (data['Age']>=60) 
        ]

    values = ['AG-1','AG-2','AG-3','AG-4','AG-5','AG-6','AG-7']

data['Age Group'] = np.select(conditions, values)
data.head()
    
df.to_csv(r"C:\Users\Sneha\OneDrive\Desktop\Insurance_Data_and_Description_CW11.csv")  

###  e. Rank region by total insurance product.

from collections import defaultdict
prod_reg = data[['Product', 'Region']]
d = {}
for i,j in zip(data['Product'], data['Region']):
    d.setdefault(i, []).append(j)

d.items()

result = {k: sum(values) for k, values in d.items()}
print(result)

a = list(result.keys())
b = list(result.values())
sort = np.argsort(b)
sorted = {a[i]:b[i] for i in sort}
print(sorted)

# q = sorted(list(result.values()))

###   f. Find total insurance product by profession.

from collections import defaultdict
prof_insurance = data[['Product', 'Profession']]
pi = {}
for i,j in zip(data['Product'], data['Profession']):
    pi.setdefault(i, []).append(j)

pi.items()

prof_insurance1 = data[['Profession', 'Product']]
pi1 = {}
for i,j in zip(data['Profession'], data['Product']):
    pi1.setdefault(i, []).append(j)

pi1.items()

###  g. Find correlations between product, profession and contract sum. What are your conclusions? 

# Convert "product" and "profession" columns to numerical variables
df["Product"] = df["Product"].map({"Life": 1, "Household": 2, "Health": 3, "Car": 4, "nan": 5})
df["Profession"] = df["Profession"].map({"Employee": 1, "Farmer": 2, "Self-employed": 3, "Executive emplyee": 4,
                                         "Student":5, "nan": 6, "Worker": 7, "Pupil": 8, "Civil servant": 9})

# Calculate the correlation matrix
corr_matrix = df[["Product", "Profession", "Contract sum"]].corr()

# Display the correlation matrix
print(corr_matrix)




###  h. Calculate and visualise products against age group. Describe your findings. 

df = pd.DataFrame(data)
grouped = df.groupby(['Age Group', 'Product']).size()
grouped.plot(kind='bar',color=['blue', 'green'], rot=60)
plt.xlabel('Age Group')
plt.ylabel('Product')
plt.title('Products by Age Group and Product')
plt.legend()
plt.show()

df = df.reset_index(drop=True)
