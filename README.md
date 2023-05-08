# House Price Prediction Model

This project is about house price prediction model with real data crawled from chotot.com website from October 2021 to April 2022. There are two parts:
- Data processing and model training.
- API and UI implementing.

## Data processing and model training

We process and train model for three times to get a model which has the best training result.

### Data processing

**Steps to process data**
```
- Use chotot.csv file to read data and remove attributes which have more than 50% NaN values.
- Use fillna() function to fill all NaN values of 'street' attribute and use KNNImputer with n_neighbors = 5 to fill all NaN values of other attributes.
- Use histogram, heatmap and boxplots to visualize the dataset.
- Use IQR to remove outliers.
- Process street data.
- Process room, toilet, floor data.
- Process size, length data.
- Process price data.
```

Because the dataset is a real data so we should check the data accuracy to ensure model training results. 

**Street data processing**
```
Because street data is an important attribute, effect directly to house price so we should process '' data. Each record has its own title and title may contain street name so we can get street name base on its title:
- Get all street names of the dataset.
- Remove some wrong street names.
- Remove street name if it's too long or too short.
- Check all street name data if its value is '' or it's too long/short, reassign street name if record's title contains a street name in our street name list.
- Remove all remain '' data.
- Use LabelEncoder to convert string data to integer data.
```

**Room, floor, toilet data processing**
```
There are some float values in three attributes data, because room, floor, toilet must be integer so we convert all float data to integer data by using int().
```

**Size, length data processing**
```
There are lots of wrong size, length, width data. Size must be a multiple of length and width, so wrong data has size - width * length > 10:
- We can reassign size, length data base on the formula and right width data.
- Remove all remain wrong data.
```

**Price data processing**
```
Prices written in words are more accurate than prices written in numbers and there lots of unreal price data in the dataset so we should process and check the accuracy of price data. Because a house cannot cost less than 500 million VND and a price more than 1000 billion VND so they may be wrong data and we need to remove them.
```

### Model training

We use ML and DL models for model training and use the best fit model for house price prediction demo. The best fit model is the one with the highest R^2 value and the lowest MSE, RMSE, MAE values.

**Model**
```
We use 7 regression models for model training so that we can get the best fit model for house price prediction:
- Neural Network (NN) model
- Long Short Term Memory (LSTM) model
- Convolutional Neural Network (CNN) model
- Linear Regression model
- Ridge Regression model
- Lasso Regression model
- Polynomial Regression model
- Bayesian Linear Regression model
```

**Model evaluation**
```
We use 4 values to evaluate models:
- MSE
- MAE
- RMSE
- R^2
```

## Demo

We use Flask for the demo
