# -*- coding: utf-8 -*-


import mohKPI as mh
import pandas as pd
from datetime import datetime


def main():
    # Create and instance of the KPI_DF class
    main_df_obj = mh.KPI_DF(r'C:/Genesys reporting/Weekly KPI reports/2022 Reports/Offsite report 2022/30-05-2022/2022-05-30 Agent Performance Summary.csv', \
                       r'C:\Genesys reporting\Weekly KPI reports\2022 Reports\Offsite report 2022\30-05-2022\2022-05-30 Agent Status Summary.csv')
   
    # Split out 247 staff by email 
    main_df_obj.split_out_email('247nursing.com.au')
    # Add status columns to the main_df
    main_df_obj.add_status_perc_main_df()
    # Get the main df which now only has 24/7 staff and has status columns
    main_df = main_df_obj.return_df()
    
    # Make a df with only status Percentage and save locally into a csv
    nurse_df = main_df[['Agent Name', 'Available %', 'Busy %', 'Away %', 'Break %', 'Meal %', 'Meeting %', 'Training %', 'On queue % accurate', 'Not Responding %']]
    nurse_df.to_csv('247 status report.csv')
    
    # Produce summary statistics for team
    mh.Mean_results(main_df).report_summary()
    
    # Identify start and stop of kpi_df to later ensure interactions report complies with dates
    start = datetime.strptime(main_df['Interval Start'].iloc[4],'%d/%m/%y')
    stop = datetime.strptime(main_df['Interval End'].iloc[4], '%d/%m/%y')
    
       
    # Define interactions report file path
    interactions_filepath = r"C:\Genesys reporting\Weekly KPI reports\2022 Reports\MOH CCTT\30-05-2022\Interactions all past 7 days.csv"
    
    # Read in and clean interactions report
    int_df = mh.Interactions(interactions_filepath, start, stop).return_int_report_clean()
    
    # Calculate and add standard score column to main_df
    main_df = mh.Add_strandard_score_to_KPI_df(int_df, main_df).return_kpi_df_with_standard_score()
    # Fill any missing standard score values with 0
    main_df['standard score'].fillna(0, inplace=True)
    
    #Rank agents by standard score
    nurse_df_rank = main_df.sort_values(by='standard score')
    # Reset the index
    nurse_df_rank = nurse_df_rank.reset_index(drop=True)
    # Reduce the columns to inly the agent names
    nurse_df_rank = nurse_df_rank[['Agent Name', 'standard score']]
    nurse_df_rank.fillna(0, inplace=True)
    # Outout agent standardised score rank to a csv
    nurse_df_rank.to_csv('247 rank agents by standardised score.csv')
main()       