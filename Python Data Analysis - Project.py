#Python Data Analysis - Project


# Importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#TASK 1 - CREATE A DATASET
# Set random seed for reproducibility
np.random.seed(0)

# Number of samples
n_samples = 1000

# Generate car make data
car_makes = np.random.choice(['Toyota', 'Honda', 'Ford', 'Chevrolet', 'BMW'], size=n_samples)

# Generate car types data
car_types = np.random.choice(['SUV', 'Saloon', 'Van'], size=n_samples)

# Generate car years data
car_years = np.random.randint(2000, 2023, size=n_samples)

# Generate car mileages data
car_mileages = np.random.randint(1000, 100000, size=n_samples)

# Generate car prices data
car_prices = np.random.randint(5000, 50000, size=n_samples)

# Create DataFrame
car_sales_data = pd.DataFrame({
    'Make': car_makes,
    'Type': car_types,
    'Year': car_years,
    'Mileage': car_mileages,
    'Price': car_prices
})

# Save the generated dataset to a CSV file
car_sales_data.to_csv('car_sales_data.csv', index=False)



# TASK 2 - STATISTICAL ANALYSIS
# Load the dataset
car_sales_data = pd.read_csv('car_sales_data.csv')

# Display the first few rows of the dataset
print(car_sales_data.head())

# Summary statistics of numerical columns
print(car_sales_data.describe())

# Check for missing values
print(car_sales_data.isnull().sum())

# Check the data type of the 'Price' column
print(car_sales_data['Price'].dtype)

# Sampling
sample_size = 100  # Define sample size
sample_data = car_sales_data.sample(sample_size, random_state=0)  # Randomly sample data
print("Sample Data:")
print(sample_data.head())

# Variables
variables = car_sales_data.columns
print("Variables in the dataset:")
print(variables)

# Frequency distributions
for column in ['Make', 'Type']:
    print(f"\nFrequency distribution of {column}:")
    print(car_sales_data[column].value_counts())

# Weighted Mean of Prices
weighted_mean_price = np.average(car_sales_data['Price'], weights=car_sales_data['Mileage'])
print("\nWeighted Mean of Prices based on Mileage:", weighted_mean_price)

# Measures of Variability (Standard Deviation)
std_deviation_price = np.std(car_sales_data['Price'])
print("\nStandard Deviation of Prices:", std_deviation_price)

# Z-Scores
mean_price = np.mean(car_sales_data['Price'])
std_price = np.std(car_sales_data['Price'])
car_sales_data['Price_Z_Score'] = (car_sales_data['Price'] - mean_price) / std_price
print("\nZ-Scores of Prices:")
print(car_sales_data[['Price', 'Price_Z_Score']].head())



#TASK 3 - DATA VISUALISATION 
# Distribution of Car Prices
plt.figure(figsize=(10, 6))
car_sales_data['Price'].hist(bins=20, color='skyblue', edgecolor='black')
plt.title('Distribution of Car Prices')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.grid(False)
plt.show()

# Scatter plot between Price and Mileage
plt.figure(figsize=(8, 6))
plt.scatter(x=car_sales_data['Mileage'], y=car_sales_data['Price'], alpha=0.5)
plt.title('Scatter plot of Price vs Mileage')
plt.xlabel('Mileage')
plt.ylabel('Price')
plt.grid(True)
plt.show()

# Box plot of Price by Car Type
plt.figure(figsize=(10, 6))
sns.boxplot(x='Type', y='Price', data=car_sales_data, palette='Set3')
plt.title('Box plot of Price by Car Type')
plt.xlabel('Car Type')
plt.ylabel('Price')
plt.show()

# Column Chart of Car Make Counts
plt.figure(figsize=(12, 6))
car_sales_data['Make'].value_counts().plot(kind='bar', color='salmon')
plt.title('Column Chart of Car Make Counts')
plt.xlabel('Car Make')
plt.ylabel('Count')
plt.show()