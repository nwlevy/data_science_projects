# Predicting Solar Panel Adoption
#### UC Berkeley Master of Information and Data Science Capstone Project, Spring 2019
`Team: Gabriel Hudson, Noah Levy, Laura Williams`

## Mitigating Climate Change
We were motivated toward this project by our interest in reducing carbon emissions to mitigate the impact of climate change. Distributed renewable electricity generation additionally creates more diversity and resilience in electricity production and reduces demand on electrical grids. However, distributed electricity generation is more complex to integrate into the grid than traditional centralized energy production and requires understanding of complex customer adoption trends. Our work takes a step toward this latter goal of understanding what factors drive customer adoption of distributed residential solar panel systems.

## Open Tool with Geographic and Feature Analysis
We've created an interactive visualization of our results, focussing in particular on identifying geographic areas (as census tracts) that have high values of predictive factors driving residential solar panel adoption, but instead are under-saturated relative to our predictions. We've visualized general predictions for the continental United States and several state maps allow exploration of over 100 potentially predictive factors for every census tract in that state.

Links for files used for live demo:
https://public.tableau.com/profile/gabriel.hudson#!/vizhome/fullworkbook/Dashboard1?publish=yes
https://public.tableau.com/profile/gabriel.hudson#!/vizhome/statefile_mass/Dashboard1
https://public.tableau.com/profile/gabriel.hudson#!/vizhome/statefile_fla/Dashboard1
https://public.tableau.com/profile/gabriel.hudson#!/vizhome/statefile_cal/Dashboard1

Link to full US map containing all data (workbook can be downloaded for use):
https://public.tableau.com/profile/gabriel.hudson#!/vizhome/allstates_alldata/Dashboard1?publish=yes

## Data Source
We started with a recently released dataset from Stanford's DeepSolar team, who identified 1.47 million solar panel systems in the US using satellite imagery and their convolutional neural network.  Their dataset additionally included over 150 other variables to explore relative to solar panel systems.  Their work is described in more detail here: [DeepSolar](http://web.stanford.edu/group/deepsolar/home "DeepSolar")

## Process
We trained a two-stage Random Forest model based on a model structure that worked well for the DeepSolar team.  We carried out a number of feature engineering steps on the DeepSolar dataset, and performed careful hyperparameter tuning with that model and engineered dataset.  Our final dataset, model and results are in the [_Final_](https://github.com/nwlevy/capstone_solarpanels/tree/master/Final/) directory in this repo. Notebooks with more detailed explanations, dataset explorations and model experiments are primarily in the [_EDA_](https://github.com/nwlevy/capstone_solarpanels/tree/master/EDA) and [_Modeling_](https://github.com/nwlevy/capstone_solarpanels/tree/master/Modeling) directories.

## Results and Insights
We were able to match the performance of DeepSolar's model but with fewer variables, and we also improved on their model with a modified outcome variable that we consider to be more appropriate than the one used by DeepSolar. Our model achieved a 10-fold cross-validated R squared score of 0.744.  Our outcome variable is the number of solar panel systems per owner-occupied housing, instead of per household count, which may represent multiple households per residential structure (i.e., apartment buildings).
We explored the nationally most important features in more detail, noting the particular importance of the number of incentives available in any given geographic area.  Industry experts repeatedly pointed to the value of exploring the role of incentives and solar installation company business models. Adding more detail about incentives and business models would be the highest value next step to continuing this work in predicting residential solar panel adoption.

## Final Presentation
Our final presentation contains more detail about our feature engineering, model training, results and insights. That presentation is available  [here](https://docs.google.com/presentation/d/1U8GX9-sRrAJGWGCU2tC9OklaTwZwejZwqvVgWg8AZbs/edit?usp=sharing) or as a PDF document in this repo [here](https://github.com/nwlevy/capstone_solarpanels/blob/master/FinalPresentation.pdf).
