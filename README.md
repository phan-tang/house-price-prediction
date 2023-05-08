# House Price Prediction Model

This project is about house price prediction model with real data crawled from chotot.com website from October 2021 to April 2022. There are two parts:
- Data processing and model training.
- API and UI implementing.

### Data processing and model training

We process and train model for three times to get a model which has the best training result.

```
Data processing

First, we use chotot.csv file to read data and remove attributes which have more than 50% NaN values. After that, we use fillna() function to fill all NaN values of 'street' attribute and use KNNImputer with n_neighbors = 5 to fill all NaN values of other attributes, use histogram, heatmap and boxplots to visualize the dataset.
```

```
Model training
```