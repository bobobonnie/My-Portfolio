import pandas as pd
from mlxtend.regressor import StackingRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import lightgbm as lgb
import xgboost as xgb
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, GridSearchCV, KFold


# read csv file, datatype = Dataframe
df = pd.read_csv('taipei_city_real_estate_transaction_v2 2.csv')

categorical_col = ['district', 'transaction_type', 'urban_land_use', 'main_building_material',
                    'transaction_year', 'carpark_category','transaction_month']

numerical_col = ['land_shift_area','building_shift_total_area','num_room','num_hall','num_toilet','unit_ntd','carpark_ntd','building_age','number_of_land','number_of_building','number_of_carpark','carpark_shift_area']

# selected features
features = ['main_use','district', 'transaction_type', 'urban_land_use', 'main_building_material','transaction_year','transaction_month', 'carpark_category','building_age','number_of_building','building_shift_total_area','num_hall','num_toilet','number_of_land', 'num_room','land_shift_area']


### getting to know data ###
print(df.shape)

# checking missing values => no missing values
def MissingValue(df):
    miss_value = df.isnull().sum()
    miss_percentage = miss_value / df.shape[0]
    miss_df = pd.concat([miss_value, miss_percentage], axis=1)
    miss_df = miss_df.rename(columns={0:'MissingValue',1:'%MissingPercent'})
    miss_df = miss_df.loc[miss_df['MissingValue']!=0, :]
    miss_df = miss_df.sort_values(by='%MissingPercent', ascending = False)
    return miss_df

print(MissingValue(df))

# exploring the relationship between attributes and the target attribute
g = sns.pairplot(x_vars=['land_shift_area'], y_vars=['district'], data=df)
g.fig.set_size_inches(15,10)
plt.show()

### data pre-processing ###
# find and deal with outliers
def outlier_treatment(datacolumn):
     sorted(datacolumn)
     Q1,Q3 = np.percentile(datacolumn , [25,75])
     IQR = Q3 - Q1
     lower_range = Q1 - (1.5 * IQR)
     upper_range = Q3 + (1.5 * IQR)
     return lower_range,upper_range

lowerbound,upperbound = outlier_treatment(df.unit_ntd)
building_shift_area_lowerbound,building_shift_area_upperbound = outlier_treatment(df.building_shift_total_area)

# upper_threshold = df['unit_ntd'].quantile(0.99)
# lower_threshold = df['unit_ntd'].quantile(0.01)
# building_shift_area_upper_threshold = df['building_shift_total_area'].quantile(0.99)
# building_shift_area_lower_threshold = df['building_shift_total_area'].quantile(0.01)
# print(building_shift_area_upper_threshold,building_shift_area_lower_threshold)

# # remove outliers
df = df[(df.unit_ntd>lowerbound)&(df.unit_ntd<upperbound)]
df = df[(df.building_shift_total_area>building_shift_area_lowerbound)&(df.building_shift_total_area<building_shift_area_upperbound)]

# remove agriculture land use form data
df = df[df.urban_land_use != 'Agriculture']

# one hot encoding to the categorical attributes
categorical_feature_mask = df.dtypes==object
categorical_cols = df.columns[categorical_feature_mask].tolist()
labelencoder = LabelEncoder()
df[categorical_cols] = df[categorical_cols].apply(lambda col: labelencoder.fit_transform(col.astype(str)))
# print(df[features].head())

# correlation heatmap
plt.figure(figsize=(30,15))
sns.heatmap(df.corr(),cmap='coolwarm',annot = True)
plt.show()

# scatter plot
plt.figure(figsize=(12,6))
plt.scatter(x=df.land_shift_area, y=df.unit_ntd)
plt.xlabel("land_shift_area", fontsize=13)
plt.ylabel("total_ntd", fontsize=13)
plt.ylim(0,800000)
plt.show()

# normalization
cols_to_norm = ['land_shift_area']
df[cols_to_norm] = StandardScaler().fit_transform(df[cols_to_norm])

# change the calendar from Taiwan local calendar to Gregorian calendar
df['complete_year'] = df['complete_year'].astype(int) + 1911



def change_word(x):
    if x == 'Address':
        return 'Residence'
    elif x == 'Quotient':
        return 'Business'
    else:
        return x

df['urban_land_use'] = df['urban_land_use'].apply(lambda x: change_word(x))

# check distribution
sns.distplot(df['building_shift_total_area'])
plt.show()

# # print the unique values of each attributes
for ind, col in enumerate(categorical_col):
    print("Unique values of {}: {} \n".format(col, set(df[col])))

# bar plots
plt.figure(figsize = (20, 30))
for ind, col in enumerate(categorical_col):
    plt.subplot(3, 3, ind+1)
    df[col].value_counts().plot(kind='bar')
    plt.xlabel(col, size=10)
    plt.ylabel("counts")
    plt.tight_layout() # to avoid graph overlapping
plt.show()

# define features and target
X=df[features]
y=df['unit_ntd']

# split dataset into train and test data (7:3)
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=7)
# K-fold cross validation
def CV(model):
    folds = KFold(n_splits = 10, shuffle = True, random_state = 11)
    scores_MAE = cross_val_score(model, x_train, y_train, scoring='neg_mean_absolute_error', cv=folds)
    scores_RMSE = cross_val_score(model, x_train, y_train, scoring='neg_root_mean_squared_error', cv=folds)
    scores_R2 = cross_val_score(model, x_train, y_train, scoring='r2', cv=folds)

    score_MAE=0
    score_RMSE=0


    for i in scores_MAE:
        score_MAE=i+score_MAE

    for i in scores_RMSE:
        score_RMSE=i+score_RMSE



    print("MAE_CV:"+str(abs(score_MAE/10)))
    print("RMSE_CV:" + str(abs(score_RMSE / 10)))
    print("RMSE_R2:" + str(scores_R2))
    print("-----------------")
# #
# # ##################################################################################################
# # models
# single methods
lr = LinearRegression()
ridge = Ridge(random_state=2019)
las = Lasso()

# ensemble methods
lgb = lgb.LGBMRegressor()
xgb = xgb.XGBRegressor()
rf = RandomForestRegressor()

models = [lr, ridge, las, lgb, rf, xgb]
print('base model')
for model in models:
    model.fit(x_train, y_train)
    pred = model.predict(x_test)
    print(model)
    CV(model)


sclf = StackingRegressor(regressors=models, meta_regressor=lr)
sclf.fit(x_train, y_train)
pred = sclf.predict(x_test)

print('stacking model')
CV(sclf)


