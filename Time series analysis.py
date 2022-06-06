# -*- coding: utf-8 -*-

import mohKPI as mh
import pandas as pd
from datetime import datetime

def main():
    # Define file pathways
    rost_path = r"C:\Genesys reporting\Weekly KPI reports\2022 Reports\MOH CCTT\23-05-2022\CACT Roster - 2022.csv"
    perf_path = r"C:\Genesys reporting\Weekly KPI reports\2022 Reports\MOH CCTT\23-05-2022\2022-05-23 Agent Performance Summary.csv"
    int_path = r"C:\Genesys reporting\Weekly KPI reports\2022 Reports\MOH CCTT\23-05-2022\Interactions all past 7 days.csv"
    perf_df = pd.read_csv(perf_path)
    
    #Make date columns a datetime object
    perf_df['Interval Start'] = pd.to_datetime(perf_df['Interval Start'])
    perf_df['Interval End'] = pd.to_datetime(perf_df['Interval End'])
    
    #Get the formating for datetime columns to Australian standard
    perf_df['Interval Start'] = perf_df['Interval Start'].dt.strftime('%d/%m/%y')
    perf_df['Interval End'] = perf_df['Interval End'].dt.strftime('%d/%m/%y')
    
    # Read in and clean up the CACT roster
    roster = mh.Roster(rost_path, perf_df).return_roster()
    
    # Identify teams in roster
    teams_df = mh.Teams(roster, reduce=False).return_roster()
    
    # Identify the index location of teams within the roster
    team_index_list = mh.Team_index(teams_df, roster).return_team_index()
    
    
    # Get dates of perf_df to use below
    start = datetime.strptime(perf_df['Interval Start'].iloc[4],'%d/%m/%y')
    stop = datetime.strptime(perf_df['Interval End'].iloc[4], '%d/%m/%y')
        
    # Clean in and read the interactions df
    int_df_obj = mh.Interactions(int_path, start, stop)
    
    int_df = int_df_obj.return_int_report_clean()
    
    #Produce a df which resamples the number of calls taken in 30min increments
    time_df = int_df_obj.total_time_analysis()
        
    #Plot the percentage of time spend on handles for each team and each agent for the week every half hour
    mh.Plots_time_series(roster, team_index_list, int_df, time_df)
    
    
main()
