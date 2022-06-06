# -*- coding: utf-8 -*-

import mohKPI as mh
import os
import time

# This function users the tkinter run GUI in mohKPI.  The GUI asks for user input for relevant file pathways
def get_user_input():
    # Attempt to obtain user input
    perf_pathway, stat_pathway,rost_pathway = user_inputs()
    # If the user entered file pathways exist, assign file pathways to variables and return the variables
    while True:
        if (os.path.exists(perf_pathway)==True) and (os.path.exists(stat_pathway)==True) and (os.path.exists(rost_pathway)==True):
            return perf_pathway, stat_pathway,rost_pathway
        # If the user entered file pathways don't exist, set an alert error and then request user tries again
        else:
            mh.User_error()
            perf_pathway, stat_pathway,rost_pathway = user_inputs()
        
def user_inputs():
    # Run GUI for user input
    input_obj= mh.KpiGui()
    # Assign variables to file pathways
    perf_pathway = input_obj.return_perf_path()
    stat_pathway = input_obj.return_stat_path()
    rost_pathway = input_obj.return_rost_path()
    # Return user entered pathways
    return perf_pathway, stat_pathway,rost_pathway


def main():
    try:
        # Get user to enter file pathways and assign to variables
        perf_pathway, stat_pathway,rost_pathway = get_user_input()
        
        
        #Read in, clean and merge the performance and status csv's into a df
        kpi_df = mh.KPI_DF(perf_pathway, stat_pathway).return_df()
        
        #Read in and clean up the CACT MOH roster
        roster = mh.Roster(rost_pathway, kpi_df).return_roster()
        #Identify the teams in the roster
        roster = mh.Teams(roster).return_roster()
        #Reduce the KPI_df to only include agents within MOH CACT (there can be many offsite providers)
        cact_df = mh.CACT_KPI(roster, kpi_df).return_cact_df()
        # Calculate and print out main summary statistics for the reporting period
        mh.Mean_results(cact_df).report_summary()
        # Produce plots which compare the performance of each agent within each team
        mh.Cact_plot_agents(cact_df)
        # Produce plots which compare KPI performance across each internal team
        mh.Cact_plot_teams(cact_df)
        
    # If user uploads files that aren't complete, the program will crash - indicate this to user
    except:
        print('There is something wrong with the files you have uploaded')
        print('Please try downloading all files and ensure they are for the same dates')
        print('This program will automatically terminate within 10s')
        time.sleep(10)

   
main()
