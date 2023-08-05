# Cassandra Demo

## Import
```
from cassandra.model.linear import *
from cassandra.model.logLinear import *
from cassandra.model.logLog import *
from cassandra.model.mlpRegressor import *
from cassandra.model.ridge import *
from cassandra.model.modelEvaluation.plot import *
from cassandra.model.nestedModel import *
from cassandra.model.modelEvaluation.evaluation import *
from cassandra.model.nevergrad.nevergrad import *
from cassandra.model.nevergrad.utils import *
from cassandra.data.dataProcessing.prophet import *
from cassandra.data.trasformations.trasformations import *
from cassandra.data.dataAnalysis.plot import *
from cassandra.data.dataProcessing.clean_and_format import *
from cassandra.data.featureSelection.ols import *
from cassandra.data.dataAnalysis.correlation import *
from cassandra.data.dataAnalysis.exploration.exploration import *
from cassandra.budgetAllocator.budget_allocator import *
from cassandra.budgetAllocator.utils import *
from cassandra.budgetAllocator.plot import *
from cassandra.utils.save import *
from cassandra.robyn.export import *
import pandas as pd 
import nevergrad as ng
import plotly.express as px
```

## Read e rename a df
```
pd.set_option("display.max_rows", 20)
pd.set_option("display.max_columns", 20)
csv_path="C:/Users/Federico/Downloads/spedire-dataset-new.csv"
csv=pd.read_csv(csv_path) #, index_col=0)
csv.rename(columns = {'o_bing':'bing_org', 'o_google':'google_org', 's_referral':'referral_org', 's_email':'email_org'}, inplace = True)
csv
```

## Create a df with prophet
```
df = prophet(csv, 'ordine_data', 'transazioni', national_holidays_abbreviation='IT', 
                     future_dataframe_periods=14, plot_prophet=True,
                        trend_seasonality=False,
                     holidays_seasonality=True, daily_seasonality=False, weekly_seasonality=True,
                        monthly_seasonality=False, yearly_seasonality=False, seasonality_mode='additive')
df
```

## Define a features
```
everything, media, organic, price, seasonality, no_media, no_organic, no_price, no_seasonality, media_google, media_fb, media_others = define_features(df, media_split=True)
```

## Create a spend df
```
spends_df = spend_to_dataset(df, media)
spends, response_get_budget = getBudget(df, 'ordine_data', 'transazioni', media)
spends_df
```

## Nevergrad
Create a dict for Hyperparameters
```
hyperparameters_dict = instrum_variables_nevergrad(media, no_media, force_coeffs=True, use_intercept=True, use_adstock=True,
                                use_saturation=True, saturation_type='hill', adstock_type='weibull')

hyperparameters_dict['bing_org'] = {'lower': 0, 'upper': None}
hyperparameters_dict['google_org'] = {'lower': 0, 'upper': None}
hyperparameters_dict['referral_org'] = {'lower': 0, 'upper': None}
hyperparameters_dict['email_org'] = {'lower': 0, 'upper': None}
hyperparameters_dict['intercept'] = {'lower': 0, 'upper': None}
hyperparameters_dict
```

Run nevergrad model
```
metrics, result, model, raccomendation_coeff, metric_array = nevergrad_model(df, hyperparameters_dict, media, no_media, 'transazioni', adstock_type='weibull', saturation_type='hill', metric_return=['rsq_test', 'rssd'], budget=5000)
```

## Show metric result of nevergrad
```
show_metric_trend(metric_array, name_metric=['rsq_test', 'rssd'])
```

## Show actual vs predicted response of nevergrad result
With 1 result of Nevergrad
```
show_prediction_vs_actual_graph_with_error(result, target_column=result['transazioni'],name_target_column='transazioni', prediction_column=result['prediction'],name_data_column='ordine_data')
```

With 2 result of Nevergrad (show all result)
```
for r in result:
    show_prediction_vs_actual_graph_with_error(r, target_column=r['transazioni'],name_target_column='transazioni', prediction_column=r['prediction'],name_data_column='ordine_data')
```

With 2 result of Nevergrad (show a specific result)
```
show_prediction_vs_actual_graph_with_error(result[3], target_column=result[3]['transazioni'],name_target_column='transazioni', prediction_column=result[3]['prediction'],name_data_column='ordine_data')
```

## Show metrics
```
metrics
```

## Adstock and Saturation
Create a df for adstock e saturation hyperparameters

```
df_adstock_saturation, result_adstock_df, result_saturation_df = adstock_saturation_to_dataset(raccomendation_coeff, use_adstock=True, adstock_type='weibull', weibull_type='pdf', 
                                   use_saturation=True, saturation_type = 'hill', graph=True)
```

Show adstock e saturation hyperparameters
```
df_adstock_saturation
```

## Response Curves
Create a coefficients dict e show them
```
coefficenti = show_coefficients(everything, model, 'Linear', graph = True)
```

Create a df for response curves e show them
```
df_response_curves = show_response_curves(df, df_adstock_saturation, coefficenti, everything, media, saturation_type = 'hill')
```

## Contribution Decomposition
```
coefs_dict = create_coefs_dict(raccomendation_coeff)

df_aggregated, df_all_decomp = decomposition_to_dataset(result, coefs_dict, media, spends_df, 'ordine_data', 'transazioni', 'prediction', df_adstock_saturation)

show_all_decomp_response(df_all_decomp, 'ordine_data', everything)
```

## Effect share vs Spend share
```
show_effect_share_vs_spend_share(df_aggregated, show_cpa = True)
```

## Budget Allocator
Create a df for budget allocator
```
lower_bounds = [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7]
upper_bounds = [1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5]

budget_allocator_df = budget_allocator(result, 'ordine_data', media, everything, 
                                       model, spends, response_get_budget, lower_bounds, upper_bounds, 
                                       df_aggregated, df_all_decomp, '2022-02-07', 200, algoritm = 'GN_ISRES')
```

show a metrics of budget_allocator_df
```
tsi, tri = show_metrics_budget_allocator(budget_allocator_df)
print(tsi)
print(tri)
```


show a df and graph of budget_allocator
```
show_budget_allocator(budget_allocator_df)
budget_allocator_df
```