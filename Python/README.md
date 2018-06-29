This Python code was made for Leonieke van den Bulk's internship at the Nederlandse Spoorwegen.
The goal of the internship was to predict short-term delays on the Dutch rail network.
Two machine learning models were applied: XGBoost and Neural Networks.

A small description of how to use this code is given below:

-	For this code to work properly, you will need three datasets created from realization data from the period 4 September 2017 - 8 December 2017. A train dataset, a validation dataset
 	and a test dataset which contains the last four Tuesdays of the realization data.
	
- 	To be able to create the feature sets properly, six more files are needed: a file containing a timetable for one week which is repeated throughout the realization data,
	a file containing the rolling stock connections, a file containing when which trains changes composition, a file containing when which trains switches from driver,
	a file containing which train series pass through which location and a file containing the most common route per train series.
	These last two files can be made with the python files "find_locations_per_trainseries.py" and "find_route_per_series.py" respectively. The rest has to be available from the NS.

-	The first step is to create the feature sets with the files above using the python file "create_featuresets.py". Here you can set the type of feature set you want to create.
	The train/validation feature sets are created by different functions than the test feature sets. Be sure to set which one you want to create in the main().
	
-	The second step in to use the create feature sets to train models. Neural networks can be trained in the python file "neural_network_model.py" and XGBoost can be trained in the
	python file "xgboost_model.py". All important settings can be found in their main().
	
- 	After a model has been trained, test set predictions can be made using the same python files by setting test=True in the main() and by giving the path to your trained model. 
	These predictions can be tested against the ground truth in the python file "compare_predictions_to_groundtruth_and_baselines.py". This python file will output the final 
	performance scores for your model and two baselines.





