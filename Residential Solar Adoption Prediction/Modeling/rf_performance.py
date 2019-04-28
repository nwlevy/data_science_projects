import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import Imputer
from sklearn.utils import shuffle
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import r2_score
import csv

#read the data
solar=pd.read_csv('../deepsolar_tract.csv',encoding = "ISO-8859-1")
solar.head()
solar_fields=pd.read_csv('../deepsolar fields.csv')
solar_fields.head()

#######pre-process the data
########
#define relevant features and dependent variable


features=solar_fields.loc[(solar_fields['Mentioned in Supplemental Info']==1)]['Field'].tolist()
all_variables=features+['number_of_solar_system_per_household']

#all_variables=features+['number_of_solar_system_per_household']+['incentive_count_residential']+['incentive_residential_state_level']

solar2=solar[all_variables]

#Create binary version of number_of_solar_system_per_household for RF classifier

solar2['solar_flag']=solar2['number_of_solar_system_per_household'].apply(lambda x: int(x>0))
solar2=solar2.loc[np.isfinite(solar2['number_of_solar_system_per_household'])]

#designate independent variable frame
independent_vars=solar2.loc[:,~solar2.columns.isin(['number_of_solar_system_per_household','solar_flag'])]
X=independent_vars.values
yc=solar2['solar_flag'].values
yr=solar2['number_of_solar_system_per_household'].values

#impute missing values
missing_val_imputer=Imputer(strategy='median')
X=missing_val_imputer.fit_transform(X)

#loop through different max depths and numbers of estimators

#max_depths=[15, 20, 30, None]
#n_estimators=[100,150,200,300]

n_estimators=[100,150,200]
max_depths=[15, 30, None]


model_params=[(x,y,a,b) for x in max_depths for y in n_estimators for a in max_depths for b in n_estimators]

# split the data 3 times into train/test folds

X_trains=[]
X_tests=[]
yr_trains=[]
yr_tests=[]
yc_trains=[]
yc_tests=[]

folds=KFold(n_splits=3, random_state=None, shuffle=True)
for train_index, test_index in folds.split(X):

    X_trains.append(X[train_index])
    X_tests.append(X[test_index])
    yr_trains.append(yr[train_index])
    yc_trains.append(yc[train_index])
    yr_tests.append(yr[test_index])
    yc_tests.append(yc[test_index])


#write row headers
with open('solar_forest_grid.csv','wt',newline='') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['max_depth_c','n_est_c','max_depth_r','n_est_r','test_acc_1','test_acc_2','test_acc_3',
                     'test_f1_1','test_f1_2','test_f1_3','test_r2_1','test_r2_2','test_r2_3','overall_r2_1',
                     'overall_r2_2','overall_r2_3'])
    
    f.close()      
    

#train model with each permutation of hyperparameters, write results to file
for i in range(0,len(model_params)):
    classifier_accuracies=[]
    classifier_f1s=[]
    regressor_r2s=[]
    overall_r2s=[]
    
    for j in range(0,len(X_trains)):
        classifier=RandomForestClassifier(max_depth=model_params[i][0],n_estimators=model_params[i][1], n_jobs=-1)
        classifier.fit(X_trains[j],yc_trains[j])
        classifier_preds=classifier.predict(X_tests[j])
        classifier_accuracies.append(accuracy_score(yc_tests[j],classifier_preds))
        classifier_f1s.append(f1_score(yc_tests[j],classifier_preds))
        
        regressor=RandomForestRegressor(max_depth=model_params[i][2],n_estimators=model_params[i][3], n_jobs=-1)
        regressor.fit(X_trains[j],yr_trains[j])
        regressor_preds=regressor.predict(X_tests[j])
        regressor_r2s.append(r2_score(yr_tests[j],regressor_preds))
        
        final_preds=classifier_preds*regressor_preds
        
        overall_r2s.append(r2_score(yr_tests[j],final_preds))
        
    with open('solar_forest_grid.csv','at',newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow([model_params[i][0],model_params[i][1],model_params[i][2],model_params[i][3],
                        classifier_accuracies[0],classifier_accuracies[1],classifier_accuracies[2],
                        classifier_f1s[0],classifier_f1s[1],classifier_f1s[2],
                        regressor_r2s[0],regressor_r2s[1],regressor_r2s[2],
                        overall_r2s[0],overall_r2s[1],overall_r2s[2]])
        f.close() 
        
        
                                     





