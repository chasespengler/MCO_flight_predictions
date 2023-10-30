# MCO Flight Delay Prediction

This project initially started as a mock consulting project for Orlando International Airport (MCO) while studying Industrial and Systems Engineering at the University of Florida wher my part of the project was to perform the statistical analysis of the data and determine what flights would be late. Since then, I have decided to modernize the approach using TensorFlow. You will notice three primary directories within the project, NaiveBayesOriginal, UpdatedTFPredictions, and UpdatedTFTrees.

#### Naive Bayes

 The former contains code and frequency tables used to analyze and then describe the data we collected for the project. This was done by basic classification and then using the frequency tables to determine how likely a flight was to be late. I decided to take the project a step further by fitting each type of flight data to a distribution to try to get a better picture of not only how likely a flight is to be delayed but also by how much. You'll notice that in the second frequency table, each flight type also include the distribution type and the respective parameters.

#### UpdatedTFPredictions

The latter contains the files and models built using the same data while leveraging TensorFlow's BoostedTreesRegressor to make the predictions.
NOTE: This is now deprecated. Please refer to the following Folder for updated TensorFlow usage.

#### UpdatedTFTrees

This is the most up do date prediction model using supported TensorFlow modules.