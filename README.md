# MOH-CACT-data-analytics
This repo contains the package mohKPI and the main programs used in the performance analysis of the NSW MOH CACT call centre

## Main package: mohKPI.py 

The mohKPI package contains the main classes used in the NSW MOH CACT data analytics.  Initially data analytics at CACT was procedural, however, to simplify sharing of code, an object oriented programming apporach has been implemented as part of Business Continuity Planning.  Additionally, Python programs can be run with minimal visible code which simplfies entry of file pathways for users unfamiliar with coding.

mohKPI.py focuses on analysing data from the Telephony software Geneys Cloud.  

## Calls offered per half hour using mohKPI.py
This very simple looking program uses the mohKPI package to plot the number of calls offered into MOH CACT queues every half hour for each day.  It requires downloading of the Queue metrics interval report as a CSV file.
