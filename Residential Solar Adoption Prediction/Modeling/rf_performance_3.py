import pandas as pd
import numpy as np
from sklearn.preprocessing import Imputer
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.utils import shuffle
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import r2_score
import csv

#load, pre-process the data

deepsolar_original = pd.read_csv('../deepsolar_tract.csv', index_col=0, encoding='ISO-8859-1')

deepsolar_curated = deepsolar_original[deepsolar_original['population'] != 0]
deepsolar_curated = deepsolar_curated[deepsolar_curated['household_count'] != 0]
deepsolar_curated = deepsolar_curated[deepsolar_curated['population'] >= 100]
deepsolar_curated = deepsolar_curated[deepsolar_curated['household_count'] >= 100]
deepsolar_curated['water_percent'] = deepsolar_curated['water_area']/deepsolar_curated['total_area']
deepsolar_curated = deepsolar_curated[deepsolar_curated['water_percent'] < 0.75]

relevant_cols=['average_household_income','county','gini_index','land_area','per_capita_income','population_density','state','total_area','water_area','education_less_than_high_school_rate','education_high_school_graduate_rate','education_college_rate','education_bachelor_rate','education_master_rate','education_professional_school_rate','education_doctoral_rate','race_white_rate','race_black_africa_rate','race_indian_alaska_rate','race_asian_rate','race_islander_rate','race_other_rate','race_two_more_rate','employ_rate','poverty_family_below_poverty_level_rate','heating_fuel_gas_rate','heating_fuel_electricity_rate','heating_fuel_fuel_oil_kerosene_rate','heating_fuel_coal_coke_rate','heating_fuel_solar_rate','heating_fuel_other_rate','heating_fuel_none_rate','median_household_income','electricity_price_residential','electricity_consume_residential','average_household_size','housing_unit_median_value','housing_unit_median_gross_rent','lat','lon','elevation','cooling_design_temperature','earth_temperature_amplitude','frost_days','relative_humidity','daily_solar_radiation','atmospheric_pressure','wind_speed','age_18_24_rate','age_25_34_rate','age_more_than_85_rate','age_75_84_rate','age_35_44_rate','age_45_54_rate','age_65_74_rate','age_55_64_rate','age_10_14_rate','age_15_17_rate','age_5_9_rate','household_type_family_rate','dropout_16_19_inschool_rate','occupation_construction_rate','occupation_public_rate','occupation_information_rate','occupation_finance_rate','occupation_education_rate','occupation_administrative_rate','occupation_manufacturing_rate','occupation_wholesale_rate','occupation_retail_rate','occupation_transportation_rate','occupation_arts_rate','occupation_agriculture_rate','occupancy_vacant_rate','occupancy_owner_rate','mortgage_with_rate','transportation_home_rate','transportation_car_alone_rate','transportation_walk_rate','transportation_carpool_rate','transportation_motorcycle_rate','transportation_bicycle_rate','transportation_public_rate','travel_time_less_than_10_rate','travel_time_10_19_rate','travel_time_20_29_rate','travel_time_30_39_rate','travel_time_40_59_rate','travel_time_60_89_rate','health_insurance_public_rate','health_insurance_none_rate','age_median','travel_time_average','voting_2016_dem_percentage','voting_2016_dem_win','voting_2012_dem_win','number_of_years_of_education','diversity','number_of_solar_system_per_household','incentive_count_residential','incentive_residential_state_level','net_metering','feedin_tariff','cooperate_tax','property_tax','sales_tax','rebate','avg_electricity_retail_rate'
]

relevant_cols.remove('land_area')
relevant_cols.remove('water_area')
relevant_cols.remove('total_area')
relevant_cols.append('water_percent')
deepsolar_curated=deepsolar_curated[relevant_cols]

for i in range(len(deepsolar_curated.dtypes)):
    if (deepsolar_curated.columns[i] == 'number_of_solar_system_per_household') | (deepsolar_curated.dtypes[i] not in ['float64','int64']):
        continue
    else:
        deepsolar_curated[deepsolar_curated.columns[i]]. \
    fillna(deepsolar_curated[deepsolar_curated.columns[i]].median(), inplace=True)
    
    
deepsolar=deepsolar_curated.copy()

# Encode string features (county and state) into numeric features
LE = preprocessing.LabelEncoder()

LE.fit(deepsolar['county'])
deepsolar['county'] = LE.transform(deepsolar['county'])

LE.fit(deepsolar['state'])
deepsolar['state'] = LE.transform(deepsolar['state'])

deepsolar['solar_flag']=deepsolar['number_of_solar_system_per_household'].apply(lambda x: int(x>0))

X = deepsolar.drop(labels=['solar_flag', 'number_of_solar_system_per_household'], axis=1).values
Y_classifier = deepsolar['solar_flag'].values
Y_regressor = deepsolar['number_of_solar_system_per_household'].values

n_estimators=[25,50,75,100]
max_depths=[None]


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
    yr_trains.append(Y_regressor[train_index])
    yc_trains.append(Y_classifier[train_index])
    yr_tests.append(Y_regressor[test_index])
    yc_tests.append(Y_classifier[test_index])


#write row headers
with open('solar_forest_grid_3.csv','wt',newline='') as f:
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
        
    with open('solar_forest_grid_3.csv','at',newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow([model_params[i][0],model_params[i][1],model_params[i][2],model_params[i][3],
                        classifier_accuracies[0],classifier_accuracies[1],classifier_accuracies[2],
                        classifier_f1s[0],classifier_f1s[1],classifier_f1s[2],
                        regressor_r2s[0],regressor_r2s[1],regressor_r2s[2],
                        overall_r2s[0],overall_r2s[1],overall_r2s[2]])
        f.close() 

