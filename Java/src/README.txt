This code is an adaptation of John Brouwers code (originally made for delay prediction) by Leonieke
van den Bulk in order to apply it to the data of the RAS competition.

A small description of how to use this code is explained below:

-	For this code to work properly, you will need two datasets. A realisation dataset
 	and a test dataset.

-	The first step that needs to be done is to convert these two dataset to the right 
	format to work with John's code, this can be done with the class 'DataTransformer.java'. 
	Make sure to change the paths at the top of the main() according to your system.

-	The second step is to use the class 'CreateTestsetInputFromTestSet.java', this will 
	filter the entries from the test dataset (NOT the converted one) that need to be predicted 
	(in this case around 08:20, 12:20 and 16:20). Make sure to change the paths at the top of 
	the main() according to your system.

-	The third step is to use the class that actually calculates the delay: 
	'CalcPerformance.java'. The paths you need to change are located at the top of the function
	'catPerformance', make sure to put the files in you created using steps one and two.
	The code will produce a .txt file with the prediction for the test inputs using the 
	following columns:
	'Trainnumber,Current_location,Future_location,Current_time,Future_time,Actual_delay,
	Trimean_prediction,ARNU_prediction,Stays_the_same_prediction'.
