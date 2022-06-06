# -*- coding: utf-8 -*-
# Import packages
import mohKPI as mh
from datetime import datetime

def main():
    # Define the file pathways
    perf_pathway = r"C:\Genesys reporting\Weekly KPI reports\2022 Reports\MOH CCTT\23-05-2022\2022-05-23 Agent Performance Summary.csv"
    stat_pathway = r"C:\Genesys reporting\Weekly KPI reports\2022 Reports\MOH CCTT\23-05-2022\2022-05-23 Agent Status Summary.csv"
    rost_pathway = r"C:\Genesys reporting\Weekly KPI reports\2022 Reports\MOH CCTT\23-05-2022\CACT Roster - 2022.csv"
   
    #Clean and merge the performance and status files from Genesys  
    kpi_df = mh.KPI_DF(perf_pathway, stat_pathway).return_df()
    #Read in and clean the roster
    roster = mh.Roster(rost_pathway, kpi_df).return_roster()
    
    #Identify teams in roster
    roster = mh.Teams(roster).return_roster()
    
    #Reduce the kpi_df to only include CACT agents
    cact_df = mh.CACT_KPI(roster, kpi_df).return_cact_df()
   
    #Identify the time period of the KPI_DF to later ensure the interactions file (below) matches
    start = datetime.strptime(kpi_df['Interval Start'].iloc[4],'%d/%m/%y')
    stop = datetime.strptime(kpi_df['Interval End'].iloc[4], '%d/%m/%y')
    
    #Define interactions filepath    
    interactions_filepath = r"C:\Genesys reporting\Weekly KPI reports\2022 Reports\MOH CCTT\23-05-2022\Interactions all past 7 days.csv"
      
    #Read in and clean the interactions report
    int_df = mh.Interactions(interactions_filepath, start, stop).return_int_report_clean()
    
    #Reduce the int_df to CACT agents only
    cact_int_df =  mh.CACT_interactions(roster, int_df).return_interactions_MOH()
    
    #Calculate the standard score and append a column containing standard score for each agent to the cact_df
    cact_df = mh.Add_strandard_score_to_KPI_df(cact_int_df, cact_df).return_kpi_df_with_standard_score()
    
    #Produce plots comparing agents standard score within each CACT internal team
    mh.Cact_plot_agents_stand_score(cact_df)
    
    # Produce plots comparing each internal teams standard socre
    mh.Cact_plot_teams_stand_score(cact_df)
    
main()