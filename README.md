# CS677 - Final Project

## Summary

This project analyses sales data for a BBQ restaurant, builds a multivariate multiple regression model and is used to forcast the sales of categories of items in the future. 

## Data Set

Historical data of sales is publicly available on the internet and includes items sold between May 01 to Dec 07 of 2023.

The data set can be downloaded from this URL: https://agsc-cs677-final-project.s3.us-east-2.amazonaws.com/items.csv

### Analysis

The following analysis and development was conducted on the original data:

- Determine which columns were useful as features, predictors and not required
- Design an intermediate data frame that combined items and modifiers
- Identify and categorize items by product type (with a targeted approach on meets)
- Organize original data set into 3 main cases and 7 special cases in comparison of the items, modifiers and prices
- Partition 28 subsets of data from the original data set, categorized by case
- Modularize Python code to enable sharing of all previously realized values as global variables throughout project
- Develop Python function to determine which case a line item belonged to and return item and price data
- Identify other features not part of the original data set that may influence the predictors

### Pre-Processing

The following processes were performed against the original data set in order to create an intermediate data frame:

- Drop columns form original data set that were not required
- Mutate price columns to correct float values and replacing null values
- Mutate the modifiers column by extracting text using regex and merging into the items and prices column
- Modify prices for modifiers depending on the type of items and expected portion size
- Generate datetime index and creating date, day, and time columns by parsing the original timestamp values

### Post-Processing

The final stage of generating the final data frame used for analysis required the following:

- converting day columns to binary variables and dropping other datetime columns besides index
- add additional feature columns as described in the features section below
- generate predictor columns from items and cost columns in intermediate data frame

### Features

The following features are used in the final data frame:

| Feature | Data Type | Description                               |
|---------|-----------|-------------------------------------------|
| D01     | Binary    | Day of week is Sunday                     |
| D02     | Binary    | Day of week is Monday                     |
| D03     | Binary    | Day of week is Tuesday                    |
| D04     | Binary    | Day of week is Wednesday                  |
| D05     | Binary    | Day of week is Thursday                   |
| D06     | Binary    | Day of week is Friday                     |
| D07     | Binary    | Day of week is Saturday                   |
| D08     | Binary    | If the day is a holiday                   |
| T01     | Binary    | Time of day is morning hours              |
| T02     | Binary    | Time of day is noon hours                 |
| T03     | Binary    | Time of day is afternoon hours            |
| T04     | Binary    | Time of day is later afternoon hours      |
| V01     | Binary    | Expected sales is higher than normal      |
| V02     | Binary    | Expected sales is less than normal        |
| W01     | Float     | Weather forcast for precipitation         |
| S07     | Float     | Total sales lag from the previous 7 days  |
| S14     | Float     | Total sales lag from the previous 14 days |
| S21     | Float     | Total sales lag from the previous 21 days |
| S28     | Float     | Total sales lag from the previous 28 days |
| S35     | Float     | Total sales lag from the previous 35 days |
| S42     | Float     | Total sales lag from the previous 42 days |

### Predictors

The following predictors are all 

| Predictor | Data Type | Description                              |
|-----------|-----------|------------------------------------------|
| M01       | Float     | Sales of brisket                         |
| M02       | Float     | Sales of pork                            |
| M03       | Float     | Sales of chicken                         |
| M04       | Float     | Sales of ribs                            |
| M05       | Float     | Sales of sausage                         |
| M06       | Float     | Sales of turkey                          |
| M07       | Float     | Sales of meet of unknown portion or type |
| O01       | Float     | Sales of all other items not meet        |

## Machine Learning Model

A variety of regression types were used to build the multivariate multiple regression model using randomized 20% of the final data frame as training data. Each model was then tested using the later 80% of data. For each model, error diagnostics were performed and performance metrics were measured. The final model selected for real-world use is based on a balance between the least error and best performance. The results follow.

### Model Coefficients

Linear Regression
Lasso regression
Ridge Regression
SVM Regression

### Error Diagnostic


### Performance Metrics


### Results


## Python

### Requirements

Before running this Python package and any of the child packages/modules, all packages listed in the requirements.txt should be installed into the Python interpreter environment used to run the code.

### Packages

The python code for this project is organized into multiple packages, with the top-level package only containing a main module which will execute all child packages and modules, and can be run by simply executing Python against a compressed version of this project. 

#### Top-Level

The top-level package's main module executes the child packages and modules in the order and manner required to download the original data set, perform the pre- and post-processing of the data to create the final data frame. Additionally, builds the models, performs the regression analysis, outputs the graphs and final results at the end. 

### Modules

The child packages are developed into the programs components which further contain the code into respective modules. The first component is the configurations package, namely, the config package, which contains only the init module. Within this module, all global variables and parameters are saved and referenced here throughout every other package/module.

For detailed information about each additional package, please reference the top-level package's main module for execution order. Likewise, see the doc string included in the modules for each additional package.
