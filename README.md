# anomaly-labeling
This code develops a dash app for traffic anomalous data labeling

The app is created using dash from Plotly. Traffic data (volume, density) of a six-month period from a specific location is presented to the users. They can select the abnormal (anomalous) points that they are seeing in each plot by clicking on them. A csv file will be automatically downloaded on the user system in the end and it includes the indices of the selected points by the user. 

All data related to any specific time interval (e.g. 10:00: AM) is shown to the user so they can judge the abnormality of a point by comparing it to its counterparts.

The points with more distances to their counterparts will be more selected by the users so we can make sure that they have a higher probability to be anomalous.

A deployed version of this code with 7 tasks (each task include data of three different locations) is available at http://labeling-version1.herokuapp.com/

![image](https://user-images.githubusercontent.com/112522995/187570834-9fa99a1d-0e84-483f-bbf9-d96c28475419.png)
