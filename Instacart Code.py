# Import packages
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Import data
data = pd.read_excel("data.xlsx")

# Observe the data
data.head()
data.info()

## Add extra and recoded variables

# Recode 'total_time' into total hours and total minutes columns
#
# Convert the 'total_time' column to string as a new variable
data['total_time_hrs'] = data['total_time'].astype(str)

# Extract the hours and minutes from the 'time' column using .str accessor and .split() method
hours_and_minutes = data['total_time_hrs'].str.split(':')
data['hours'] = hours_and_minutes.str[0].astype(int)
data['minutes'] = hours_and_minutes.str[1].astype(int)

# Calculate the decimal hours by dividing the minutes by 60 and adding them to the hours
data['total_time_hrs'] = data['hours'] + data['minutes'] / 60
data['total_time_hrs'] = data['total_time_hrs'].round(2).map('{:.2f}'.format)

# Recode 'total_time_hrs' into minutes
data['total_time_min'] = data['hours'] * 60 + data['minutes']

# Clean up columns unnecessary columns
data = data.drop(['hours', 'minutes'], axis=1)

#---------------------------------------------------------------------------------------------#

# Creating an efficiency column/value for each row
#
# Changing 'total_time_hrs' datatype
data['total_time_hrs'] = data['total_time_hrs'].astype(float)


data['eff'] = (data['earned']/(data['total_time_hrs'] + (0.13 * data['mileage'])))

#---------------------------------------------------------------------------------------------#
 
# Create a numeric column for days of the week
#
# Define dictionary to map days of week to numbers
day_map = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}

# Apply mapping to 'd_o_w' column and create a new variable
data['d_o_wR'] = data['d_o_w'].apply(lambda x: day_map[x])

#---------------------------------------------------------------------------------------------#

# Viewing and saving original data into new dataset
data.head()
data.to_csv('dataR.csv', index=False)

#---------------------------------------------------------------------------------------------#

#### Analyses ####

# Null Hypothesis = Every day has the same average, efficiency scores.

# Importing recoded dataset
dataR = pd.read_csv("dataR.csv")
dataR.head()

# viewing correlation matrix
corr_matrix = dataR.corr()
print(corr_matrix)

# create a heatmap of the correlation matrix
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.show()

# No shocking discoveries from correlation matrix...

# Viewing distributions
#
# Days of the week worked
plt.hist(dataR['d_o_wR'], bins=7, rwidth= 0.8, alpha= 0.7)
plt.xlabel('Day of the week')
plt.ylabel('Frequency')
plt.show()

# Efficiency information

dataR['eff'].describe()
# count    78.000000
# mean      5.380682
# std       2.265840
# min       0.000000
# 25%       4.564380
# 50%       5.671490
# 75%       6.544026
# max      11.643096

plt.hist(dataR['eff'], bins=15)
plt.xlabel('Efficiency Scores')
plt.ylabel('Frequency')
plt.show()

mean_eff = dataR.groupby('d_o_w')['eff'].mean()
mean_eff = mean_eff.sort_values(ascending=False)
mean_eff

# Sun    6.173628
# Tue    6.107056
# Mon    5.751901
# Sat    5.732059
# Fri    5.016584
# Thu    4.892312
# Wed    3.982727

### Outcome ###
#
# Saturday through Tuesday has the highest efficiency scores, and are therefore the best days to shop for Instacart in Coeur d'Alene, ID.