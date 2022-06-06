# MOH-CACT-data-analytics
This repo contains the package mohKPI and the main programs used in the performance analysis of the NSW MOH CACT call centre


## Main package: mohKPI.py 

The mohKPI package contains the main classes used in the NSW MOH CACT data analytics.  Initially data analytics at CACT was procedural, however, to simplify sharing of code, an object oriented programming apporach has been implemented as part of Business Continuity Planning (BCP).  Additionally, Python programs can be run with minimal visible code which simplfies entry of file pathways for users unfamiliar with coding.

mohKPI.py focuses on analysing data from the Telephony software Geneys Cloud.  

## Main KPI report with GUI and user error handling.py
This program produces summary statistics and plots KPIs of agents and teams.  Since this is the main program, a simple GUI has been built with user error handling for BCP.  Two main KPIs are analysed:
1) The number of handles per hour
2) The percentage of logged in time spend on handles


## Standard score.py
Due to the complexity and variety of work tasks within the NSW MOH CACT, a standardised score was developed to fairly compare agents doing different work tasks.  The formula for this score is mathematically derived.  This program produces plots which compare an agents standard score with agents from the same team and a plot which compares teams within MOH CACT.  


## Calls offered per half hour using mohKPI.py
This very simple looking program uses the mohKPI package to plot the number of calls offered into MOH CACT queues every half hour for each day.  It requires downloading of the Queue metrics interval report as a CSV file.
