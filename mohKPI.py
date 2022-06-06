 # -*- coding: utf-8 -*-
"""
Created on Fri May 13 07:52:34 2022

@author: 60253052
"""
import tkinter as tk
import pandas as pd
import sys
from difflib import SequenceMatcher
import numpy as np
import matplotlib.pyplot as plt
import time

#The KpiGui class provides a simple GUI for the main KPI report as part of business continuity
#Users only need to enter the relevant file pathways in order to run the report
class KpiGui:
    #Initilalise GUI class
    def __init__(self):
        #Create tkiner window
        self.win = tk.Tk()
        #Call entry function
        self.entry()
    
    #The entry funtion provides tha main code to enter the relevant file pathways for the KPI report
    def entry(self):
        #set the title of GUI
        self.win.title('MOH CACT KPI report')
        
        #Create frame to enter performance CSV and pack into window
        self.perf_frame = tk.Frame(self.win)
        self.perf_frame.pack()
        
        #Create instruction for user to enter performance file pathway
        self.perf_label = tk.Label(master=self.perf_frame, text='Please enter the complete Genesys performance summary file pathway: ')
        self.perf_label.pack(side='left')
        
        #Create entry widget for user to enter performance file pathway
        self.perf_entry = tk.Entry(master=self.perf_frame)
        self.perf_entry.pack(side='left')
        
        
        
        #Create frame to enter status CSV and pack into window
        self.stat_frame = tk.Frame(self.win)
        self.stat_frame.pack()
        
        #Create instruction for user to enter status file pathway
        self.stat_label = tk.Label(master=self.stat_frame, text='Please enter the complete Genesys status summary file pathway: ')
        self.stat_label.pack(side='left')
        
        #Create entry widget for user to enter status file pathway
        self.stat_entry = tk.Entry(master=self.stat_frame)
        self.stat_entry.pack(side='left')
        
        
        #Create frame to enter roster CSV and pack into window
        self.rost_frame = tk.Frame(self.win)
        self.rost_frame.pack()
        
        #Create instruction for user to enter roster file pathway
        self.rost_label = tk.Label(master=self.rost_frame, text='Please enter the complete roster (as a CSV) file pathway: ')
        self.rost_label.pack(side='left')
        
        #Create entry widget for user to roster file pathway
        self.rost_entry = tk.Entry(master=self.rost_frame)
        self.rost_entry.pack(side='left')
        
        
        #Create buttonb to run program
        self.button_frame = tk.Frame(self.win)
        self.button_frame.pack()
        #Button will call get_input funtion which assigns user input to relevant variable for later use        
        self.button = tk.Button(master=self.button_frame, text='Run report', command=self.get_input)
        self.button.pack()
        
        #Run infinite loop
        self.win.mainloop()
        
    
        
        
    #The get_input function assigns user input to relevant variable to be used in KPI program  
    def get_input(self):
        #Get the performance file pathway
        self.perf_path = self.perf_entry.get()
        
        #Get the staus file pathway
        self.stat_path = self.stat_entry.get()
        
        # Get the roster file pathway
        self.rost_path = self.rost_entry.get()
        
        #Clsoe the GUI window
        self.win.destroy()
        
       
    #Use to return the data attribute self.perf_path     
    def return_perf_path(self):
        #Clean up the user input string
        self.perf_path = self.perf_path.strip().strip('"')
        return self.perf_path
    
    
    #Use to return the data attribute self.stat_path  
    def return_stat_path(self):
        #Clean up the user input string
        self.stat_path = self.stat_path.strip().strip('"')
        return self.stat_path
    
    
    #Use to return the data attribute self.rost_path  
    def return_rost_path(self):
        #Clean up the user input string
        self.rost_path = self.rost_path.strip().strip('"')
        return self.rost_path

#The user_error class provides a simple GUI where a user is informed there is an issue with the file pr pathways they have entered
class User_error:
    def __init__(self):
        #Create window and pack a frame into tkinter window
        self.err_win = tk.Tk()
        self.error_frame = tk.Frame(self.err_win)
        self.error_frame.pack()
        
        #Create error message and pack into frame
        self.error_label = tk.Label(master=self.error_frame, text='There is an error in your file and/or pathways, please try again')
        self.error_label.pack()
        
        #Create 'OK' button which closes the error message
        self.ok_error_button_frame = tk.Frame(self.err_win)
        self.ok_error_button_frame.pack()
        self.ok_error_button = tk.Button(master=self.ok_error_button_frame, text='OK', command=self.err_win.destroy)
        self.ok_error_button.pack()
        self.err_win.mainloop()
            
      


#This class is used to wrangle and clean the two main CSV files need from Genesys into one convenient df, 'main_df'
#This class also has the ability to add extra columns regarding agent status and split the email column which is needed to seperate
#different providers using the same instance of Genesys
#To be able to run this class, in the performance file the 'Handle' and 'Email' columns must be present and the status file must have
# the following columns added: Available, Busy, Away, Break, Meal, Meeting, Training, On Queue, Logged In
class KPI_DF:
    #To initialise class, a string of the Genesy performance file and status file pathways must be passed
    def __init__(self, perf_path, status_path):
        self.main_df = self.clean_and_wrangle(perf_path, status_path)
#This function reads in the perfoirmance and status file summaries, checks they are for the same time period and wrangles them together
        
    def clean_and_wrangle(self, performance_path, status_path):
        #Read in performance file ads a df and assign to variable performance_df
                   
        performance_df = pd.read_csv(performance_path)
    
        #Read in status file as a df and assign to variable status_df
        status_df = pd.read_csv(status_path)
    
        #Identify start and end dates of both files
        perf_int_start = performance_df.iloc[1][0]
        perf_int_end = performance_df.iloc[1][1]
    
        status_int_start = status_df.iloc[1][0]
        status_int_end = status_df.iloc[1][1]
    
       #Check file dates match - if they don't there is an error message and the program is terminated in 3s
        if perf_int_start != status_int_start:
            print('Program terminated: The start dates of the performamce and status files do not match.')
            time.sleep(3)
            sys.exit()
        elif perf_int_end != status_int_end:
            print('Program terminated: The end dates of the performance and status files do not match.')
            time.sleep(3)
            sys.exit()
        else:
             pass
        
        
    
        
    
        #Identify unique coolumns in status df (compared to performance df)
        unique_cols = status_df.columns.difference(performance_df.columns)
    
        #Make new df which only has unique columns
        status_df_unique = status_df[unique_cols]
    
  
        status_df_unique = status_df_unique.merge(status_df['Agent Id'],left_index=True, right_index=True, how = 'inner')
        # main_df = pd.merge(performance_df, status_df_unique, left_index=True, right_index=True, how = 'inner')
    
    
        #Merge df - use left and right index to merge on as these are the same between df's
        main_df = pd.merge(performance_df, status_df_unique, left_on = 'Agent Id', right_on='Agent Id', how = 'left')
    
        #Make date columns a datetime object
        main_df['Interval Start'] = pd.to_datetime(main_df['Interval Start'])
        main_df['Interval End'] = pd.to_datetime(main_df['Interval End'])
        
        #Get the formating for datetime columns to Australian standard
        main_df['Interval Start'] = main_df['Interval Start'].dt.strftime('%d/%m/%y')
        main_df['Interval End'] = main_df['Interval End'].dt.strftime('%d/%m/%y')
    
        #Discard users without any calls in the last 30 days
        main_df.dropna(subset = ["Logged In"], inplace=True)
    
        main_df["Handle"].fillna(0, inplace = True)
        
   
    
   
        #Split email addresses to better identify offsite providers
        main_df[['email start', 'email tail']] = main_df['Email'].str.split('@', expand = True)
        return main_df  
    
    #This method adds columns to the main_df re the percentage of time an agent spends in each status
    def add_status_perc_main_df(self): 
        self.main_df['Available %'] = self.main_df['Available']/self.main_df['Logged In']*100
        self.main_df['Busy %'] = self.main_df['Busy']/self.main_df['Logged In']*100
        self.main_df['Away %'] = self.main_df['Away']/self.main_df['Logged In']*100
        self.main_df['Break %'] = self.main_df['Break']/self.main_df['Logged In']*100
        self.main_df['Meal %']= self.main_df['Meal']/self.main_df['Logged In']*100
        self.main_df['Meeting %'] =self.main_df['Meeting']/self.main_df['Logged In']*100
        self.main_df['Training %'] = self.main_df['Training']/self.main_df['Logged In']*100
        self.main_df['On queue % accurate'] = self.main_df['On Queue']/self.main_df['Logged In']*100
        
        

    
    #This method reduces the main_df to only contain emails with a certain tail
    #This has been used to split out agents from different providers on the same instance of Genesys
    def split_out_email(self, email):
        self.main_df = self.main_df[self.main_df['email tail']==email]
      
    
    
    #This method is used to return the data attribut main_df
    def return_df(self):
        return self.main_df
    
    
    
    

# The Roster class imports the MOH CACT roster and cleans it to a more usable format
# The agent names in the roster and Gensys generally do not match and there is no set identifier between them, hence a function has been 
# included which finds the best match between the roster and Genesys and replaces the roster names with those of Genesys.  This is an imperfect 
# solution however, due to business decisions out of data analytic control, this was the best option and has a very low error rate
class Roster:
    #Initialise the class.  This class requires a roster path and a csv output from Genesys with all the agent names in the system 
    def __init__(self, roster_path, kpi_df):
        #Create the data attribute self.roster as a csv
        self.roster = self.roster_clean(kpi_df, roster_path)
        
   #Import the roster and clean  
    def roster_clean(self, kpi_df, roster_path):
        #Read in roster as a dataframe
        roster_df = pd.read_csv(roster_path)
        #Identify header 
        header_loc = roster_df.loc[roster_df.isin(['Staff Name']).any(axis=1)].index.tolist()
        #set header
        header = roster_df.iloc[header_loc[0]]
        #reset index of header
        header = header.reset_index(drop=True)
        #get the data below the header
        data_below_header = header_loc[0]+1
        roster_df = roster_df.iloc[data_below_header:]
        
        #name columns with header
        roster_df.columns = header
        #Get rid of empty cells
        roster_df.dropna(subset = ["Staff Name"], inplace=True)
        #Reset df index
        roster_df = roster_df.reset_index(drop=True)
        
        #Match the names in the roster with those in Genesys - replace Staff Names in roster with those in Genesys
        roster_df = self.match_roster_names_with_genesys(kpi_df, roster_df)
        return roster_df



    #This function matches inconsistent names across Genesys and the roster and ensures the names in the roster match those in Genesys.
    #Roster staff names are replaced with those in Genesys
    def match_roster_names_with_genesys(self, kpi_df, roster_df):
        #Identify column containing staff name and convert to panda series
        list_of_staff = roster_df["Staff Name"]
        #Convert panda setries to a list
        list_of_staff = list_of_staff.tolist()
        
        #Iterate over every name in the rostr and every name in Genesys
        for name in roster_df["Staff Name"]:
            for agent in kpi_df["Agent Name"]:
                name_match = SequenceMatcher(None, name.lower(), agent.lower()).ratio()
                #Replace name in roster with on in Genesys
                if name_match >= 0.89:
                    roster_df[roster_df["Staff Name"]==name]=agent
                    list_of_staff.remove(name)
                    
                                    
        #defrag roster_df
        roster_df = roster_df.copy()     
                   
        return roster_df
    
    #Mehtod to return self.roster data attribuet as a df
    def return_roster(self):
        return self.roster
    
    
     
    
#The CACT_KPI class merges the main_df from the class KPI_DF with the MOH CACT roster
    
class CACT_KPI:
    #Two csv files must be passed - a roster containing Staff names and a main_df which has the performance or status files
    #downloaded from Genesys.  Often the main_df is a df made from the merging of the performance and status files
    #The option reduce, when default True reduces the main_df to only CACT staff.  When False, the main_df will contain all users
    #however there is a column which has the relavent team name for each MOH CACT agent
    def __init__(self, roster, main_df, reduce=True):
        #Performen pandas puter merge roster and main_df on Staff Name
        self.cact_df = pd.merge(roster, main_df, left_on='Staff Name', right_on='Agent Name', how = 'outer')
        #Get rid of agents who never logged into Genesys
        self.cact_df.dropna(subset=['Logged In'], inplace=True)
        #Reduce main_df to only contain MOH CACT agents
        if reduce==True:
            self.cact_df = self.cact_df.dropna(subset=['Team'])
       #Keep main_df with all users of instance of Genesys
        else:
            pass
    #Method to return self.cact_df data attribute
    def return_cact_df(self):
        return self.cact_df
    
    
    
    
    
    
#This class essentially appends a column to the roster which has which team an agent belongs too
class Teams:
    #To innitialise the class, a roster must be passed.  An option 'reduce' is included and is default to True.
    #If reduces is True, then a df which contains a a column with staff names and a second columnn that contains the team is created
    #If redcuce is False, the df is returned with only rows which importantly have the names and index of the teams in the roster
    #but a whole 40 columns are still maintained
    def __init__(self, roster, reduce=True):
        self.reduce = reduce
        self.roster = self.identify_teams(roster)
        
    #Thsi function identifies the team names
    def identify_teams(self, roster):
        #Team names ocur when the Staff ID is empty - boolena mask for these
        boolean_mask_for_team_name = pd.isnull(roster["Staff ID"])
        #Make a df which contains the team name and no agents
        teams_df = (roster[boolean_mask_for_team_name])
        #Create df containing only two columns - staff name and agents team.  Calls class method pull_out_team_agents
        if self.reduce==True:
            reduced_teams_df = self.pull_out_team_agents(teams_df, roster)
            
        #Return df containing only the name and indexes of teams as well and all 40 columns from merge
        else:
            return teams_df
        return reduced_teams_df

    # This function matches agents with their respective teams and returns a DF with team name and agents in each column   
    def pull_out_team_agents(self, teams_df, roster):
        #Create empty list to append location of teams by index in roster_df
        team_indexes = []
        
        #Using teams_df, find the location of the teams within the roster_df and append values to team_indexes
        for team_name in teams_df["Staff Name"]:
            index_array = (roster[roster["Staff Name"] == team_name].index.values)
            team_indexes.append(index_array[0])
            
        #Find location of end of roster_df
        last_CCTT_member = len(roster) +1
        
        #Convert list of team_indexes to a numpy array
        team_indexes = np.array(team_indexes)
        
        #Convert last index of roster_df to and numpy array and append to team indexes
        last_CCTT_member = len(roster) +1
        
        team_indexes = np.append(team_indexes, last_CCTT_member)
        
        #Find lenght of team_indexes to be able to loop over and extract indices
        length_team_indexes = len(team_indexes)
        
        #Add team column to roster
        roster['Team'] = ''
        
        
         
        # Start counter to control finding locality of team in teams_df
        team_counter = 0
        # loop over numpy array of team indexes
        for i in range(length_team_indexes-1):
            # Extract rows in roster than contain the names of agents in each team
            roster.loc[team_indexes[i]:team_indexes[i+1], "Team"] = teams_df.iloc[team_counter]['Staff Name']
            team_counter+=1
         
        #Get rid of rows without agents
        roster.dropna(subset=['Staff ID'], inplace=True)
        # reset index
        roster.reset_index(drop=True, inplace=True)
        # Reduce roster to just the staff name and associated team
        roster = roster[['Staff Name', 'Team']]
        
        
        return roster
        

  
    #Method to return data attribute self.roster  
    def return_roster(self):
        return self.roster

#This class is used to determine the index location of teams within the roster. A teams_df made using the class Teams with reduce set to False must ve passed
#along with a clean roster df which has been cleaned through Roster.  A list of lists containing start and stop indexes of teams locations in rosters is returned
class Team_index:
    # Initialise the self.team_index_list attribute to create list of list of index locations of teams within roster df
    def __init__(self, teams_df, rost_df):
        self.team_index_list = self.make_team_list(teams_df, rost_df)
        
    # This method makes the list of lists of team index locations in roster
    def make_team_list(self, teams_df, rost_df):
        #Reduce roster to a series with only staff name column
        rost_df = rost_df['Staff Name']
        #Get index location of team names in roster as a list and assign to team_index
        team_index =teams_df.index.tolist()
        ##Get the last index in the roster df
        team_index.append(rost_df.index[-1]+1)
        
        #Create list to append where a team start index is in roster
        start_list = []
        # Loop through team index list and append start of teams index
        for i in team_index[0:-1]:
            start_list.append(i)
        
        # Create list to append where a team index ends in roster, then loop through index list and append end of teams index
        stop_list = []
        
        for i in team_index[1:]:
            stop_list.append(i-1)
        
        #create a list of lists which contains the start and stop index of teams within CACT rsoter
        team_index_list = []
        counter = 0
        for i in start_list:
            temp_list = []
            temp_list.append(i)
            temp_list.append(stop_list[counter])
            counter +=1 
            
            team_index_list.append(temp_list)
        #Return list of list of team index locations in roster
        return team_index_list
    
    #Method to return data attribute self.team_index_list
    def return_team_index(self):
        return self.team_index_list


#This class is used to provide summary statistics.
#The main_df created by KPI_DF must be passed in
class Mean_results:
    #Initialise class and create data attributes - NB: Genesys output stores time in ms so must be converted to more meaningful units
    def __init__(self, main_df):
        self.active_agents = len(main_df)
        self.handle_perc = main_df["Total Handle"].mean()/main_df["Logged In"].mean()*100
        self.handle_rate = main_df["Handle"].mean()/(main_df["Logged In"].mean()/60000/60)
        self.outbound = main_df['Outbound'].sum()
        self.inbound = main_df["Handle"].sum() - main_df["Outbound"].sum()
        self.avg_handle = main_df["Avg Handle"].mean()/60000
        self.avg_ACW = main_df["Avg ACW"].mean()/60000
        self.avg_handle_tot = main_df['Handle'].mean()
        self.report_start_date = main_df.iloc[1]['Interval Start']
        self.report_end_date = main_df.iloc[1]['Interval End']
        
        
    #Method report summary is used to print summary stats for KPI reports   
    def report_summary(self):
        print('This report is for the reporting period: ', self.report_start_date, 'to', self.report_end_date)
        print()
        print("The total number of outbound calls was:", "{:.0f}".format(self.outbound))
        print("The total number of inbound calls was:", "{:.0f}".format(self.inbound))
        print()
        print("There were", self.active_agents, "agent/s active in the time period")
        print('The average handle percentage was:', "{:.1f}".format(self.handle_perc), '%')
        print('The average handle rate was:', "{:.1f}".format(self.handle_rate), 'handles per hr')
        print('The average handle time was:', "{:.1f}".format(self.avg_handle), 'mins')
        print()
        
        
# Mean_results_stand_score is an inheritance class of Mean_results.  It has the additional data attribute self.mean_stand_score which is used for
#reporting standard score results
class Mean_results_stand_score(Mean_results):
    def __init__(self, main_df):
        Mean_results.__init__(self, main_df)
        self.mean_stand_score = main_df['standard score'].mean()
        
    def return_mean_stand_score(self):
        return self.mean_stand_score
        
# Cact_plots is an inheritance class of mean_results whose data attributes are important in the plots here
#It is used to plot the standard KPI scores of each agent, divided up into each call team at MOH CACT
#A main_df which has been reduced to CACT MOH staff and has a column 'Team'
class Cact_plot_agents(Mean_results):
    def __init__(self,cact_df):
        #initialise as an inheritance class of Mean_results
        Mean_results.__init__(self, cact_df)
        self.cact_df = cact_df
        # Do the plots
        self.plot_agents()
        
        
        
    def plot_agents(self):
        # Lopp over each team and do two plots - one for handles per hours and the other for handle %
        for team in self.cact_df['Team'].unique():
            team_df = self.cact_df[self.cact_df['Team']==team]
            
            fig, (ax1, ax2) = plt.subplots(2, 1)
            fig.set_figheight(8)
            fig.set_figwidth(8)
            
            ax1.barh(team_df['Agent Name'], team_df['Handle']/(team_df["Logged In"]/3600000))
            ax1.set_xlabel("Number of handles per hour logged in")
            
            #Uncomment line below to hide names
            #plt.yticks(color="white")
            title = 'Number of handles per hour for ' + str(team)
            ax1.axvline(x=3, color ='r', linestyle = '-')
            ax1.axvline(x=self.handle_rate, color = 'g', linestyle = '-')
            ax1.set_title(title)
           
           
            #Plot % of time spent on handles
            ax2.barh(team_df['Agent Name'], team_df['Total Handle']/team_df["Logged In"]*100)
            ax2.set_xlabel("%")
            # plt.xticks(rotation=90)
            title = 'Handle time as a percentage of time logged in for '+ str(team)
            ax2.axvline(x=40, color ='r', linestyle = '-')
            ax2.axvline(x=self.handle_perc, color = 'g', linestyle = '-')
            ax2.set_title(title)
            
            
            plt.tight_layout()
            plt.show()
     
            

# Cact_plot_agents_stand_score is an inheritance class of Mean_results whose data attributes are used in the plots
#This class is used to automatically plot each agent's standard score, grouped into a team plot
#the cact_df containing only CACT agents from the peformance and status files merged
class Cact_plot_agents_stand_score(Mean_results_stand_score):
    def __init__(self, cact_df):
        # Initialise inheritance class
        Mean_results_stand_score.__init__(self, cact_df)
        self.cact_df = cact_df
        #Do the plots of each agents standardised score grouped as a team
        self.plot_agents()
        
        
        
    def plot_agents(self):
        for team in self.cact_df['Team'].unique():
            team_df = self.cact_df[self.cact_df['Team']==team]
            
            fig, ax1 = plt.subplots(1, 1)
            # fig.set_figheight(8)
            fig.set_figwidth(10)
            
            ax1.barh(team_df['Agent Name'], team_df['standard score'])
            ax1.set_xlabel("'Standardised score'")
            
            #Uncomment line below to hide names
            #plt.yticks(color="white")
            title = 'Standardised scores for ' +  str(team)
           
            ax1.axvline(x=self.mean_stand_score, color = 'g', linestyle = '-')
            ax1.set_title(title)
            ax1.set_xlim([0, 1.4])
            plt.show()
           
   

# Cact_plot_teams class is an inheritance class of Mean results.  This calls is used to plot teams KPI performance against
# each other.  Two subplots are produced - one for handle rate and one for handle %
class Cact_plot_teams(Mean_results):
    def __init__(self,cact_df):
        # Initialise the inheritance class
        Mean_results.__init__(self, cact_df)
        self.cact_df = cact_df
        
       # Plot all of the teams against each other
        self.plot_teams()
    
    def plot_teams(self):
        # Create lists and append team names and KPI performance to the to easily plot
        team_names = []
        team_handle_rate = []
        team_handle_perc = []
        for team in self.cact_df['Team'].unique():
            team_names.append(team)
            
            team_df = self.cact_df[self.cact_df['Team']==team]
            team_handle_rate.append(team_df["Handle"].mean()/(team_df["Logged In"].mean()/60000/60))
            team_handle_perc.append(team_df["Total Handle"].mean()/team_df["Logged In"].mean()*100)
            
        fig, (ax1, ax2) = plt.subplots(1,2)
       
        
        fig.set_figheight(7)
        fig.set_figwidth(11.5)
        ax1.bar(team_names, team_handle_rate)
        ax1.set_ylabel("Number of handles per hour logged in")
        ax1.tick_params(axis = 'x', rotation = 90)
        #Uncomment line below to hide names
        #plt.yticks(color="white")
        title = 'Number of handles per hour for each team in the CCTT'
        ax1.axhline(y=3, color ='r', linestyle = '-')
        ax1.axhline(y=self.handle_rate, color = 'g', linestyle = '-')
        ax1.set_title(title)
        
        
       
        
        #Plot % of time spent on handles
        ax2.bar(team_names, team_handle_perc)
        ax2.set_ylabel("%")
        ax2.tick_params(axis = 'x', rotation = 90)
        
        title = 'Handle time as a percentage time logged in for each team in the CCTT'
        ax2.axhline(y=40, color ='r', linestyle = '-')
        ax2.axhline(y=self.handle_perc, color= 'g', linestyle = '-')
        ax2.set_title(title)
        plt.tight_layout()
        plt.show()
            


# Cact_plot_teams_stand_score is an inheritiance class of Mean_results_stand_score which is itself an inheritance class of 
# Mean_results.  This class simply plots the performance of each team against each other in terms of standard score
class Cact_plot_teams_stand_score(Mean_results_stand_score):
    def __init__(self,cact_df):
        # Initialize the inheritance class
        Mean_results_stand_score.__init__(self, cact_df)
        self.cact_df = cact_df
        # Do the plots
        self.plot_teams()
    
    def plot_teams(self):
        # Create lists, loop over teams and append team name and performance to lists
        team_names = []
        team_stand_score = []
        for team in self.cact_df['Team'].unique():
            team_names.append(team)
            
            team_df = self.cact_df[self.cact_df['Team']==team]
            team_stand_score.append(team_df['standard score'].mean())
        
        # Do the plot
        fig, ax1 = plt.subplots(1,1)
        fig.set_figheight(7)
        fig.set_figwidth(11.5)
        ax1.bar(team_names, team_stand_score)
        ax1.set_ylabel("Standard Score")
        ax1.tick_params(axis = 'x', rotation = 90)
        #Uncomment line below to hide names
        #plt.yticks(color="white")
        title = 'Standard score across each team'
        
        ax1.axhline(y=self.mean_stand_score, color = 'g', linestyle = '-')
        ax1.set_title(title)
        
        plt.show()

# The interactions class is used to read in the Interaction Details Report which is downloaded from Genesys
# The columns with time are converted to timedelta's and the date column is converted to a datetime object
# A file pathways and when the dates that should be included in the df need to be passed (obtain from performance or status downloads in Genesys)
class Interactions:
    def __init__(self, file_path, start, stop):
        # Initialise the class
        self.int_report_clean = self.read_in_interactions_report(file_path, start, stop)       
        
    def read_in_interactions_report(self, file_path, start, stop):
        #read in interactions csv file
        df = pd.read_csv(file_path)
        
        # Get the location of the header
        header_loc = df.loc[df.isin(['User']).any(axis=1)].index.tolist()
        # Select row with actual column headings - Genesys output has many useless rows 
        header = df.iloc[header_loc[0]]
        
        # Get the actual data below the header
        data_below_header = header_loc[0]+1
        #Select rows below the header - delete last irrelevant row
        df = df[data_below_header:-1]
        # Append the heading to the columns - we now have a nice, clean simple csv file with appropriate headings
        df.columns = header
        
        #Make Duration columns a time
        time = pd.to_timedelta(df["Duration"])
        df["Duration time"] = time
        
       
        #Fill nan lines in Queue with 0 to allow changes to timedelta
        df["Queue Wait (secs)"]=df["Queue Wait (secs)"].fillna(0)
        #Change Queue wait (secs) volumn entries to a string - required to perform next step
        df["Queue Wait (secs)"] = df["Queue Wait (secs)"].astype(str)
        #Deal with inboun/outbound wait times which are seperated by a ','
        # df["Queue Wait (secs)"]= df["Queue Wait (secs)"].replace(np.nan,0)
        df["Queue Wait (secs)"] = df["Queue Wait (secs)"].apply(lambda x: sum(map(int, x.split(', '))))
        #Change Queue wait (secs) columns to numeric type so we can perform mathematical functions on column
        df["Queue Wait (secs)"] = pd.to_numeric(df["Queue Wait (secs)"])
        #Convert Queue Wait (secs) columns to a timedelta and assign to new column "wait time as a time delta"
        wait = pd.to_timedelta(df["Queue Wait (secs)"], unit='S')
        df["wait time as a time delta"]= wait
        #make a new column which has the calculated wait time
        df["Handle time"] = df["Duration time"] - df["wait time as a time delta"]
        
        # Convert Date/Time columns to a Pandas datetime object
        df['Date/Time'] = pd.to_datetime(df['Date/Time'])
        # Limit dates to match those in the performance and status files (often Genesys can be a little liberal with restricting date output)
        df = df[df['Date/Time']<=stop]
        df = df[df['Date/Time']>=start]  
       # Get rid of any handles which are open for more than and hour as they are almost definetely due a call being left open by an agent by error
        df = df[df['Handle time']<=pd.Timedelta(value=1, unit='hours')]
        
        return df

    

    # Method to return interactions DF
    def return_int_report_clean(self):
        return self.int_report_clean
    
    # This function creates the 'time_df' which is a resmapling of the interactions DF counting othe number of calls in 30min intervals 
    def total_time_analysis(self):
        df = self.int_report_clean
        # Convert Date/Time column to a string to be able to split column into both date and time
        df['Date/Time'] = df['Date/Time'].astype(str)
        # Split Date/Time column to make two columns Date and Time
        df[['Date', 'Time']] = df['Date/Time'].str.split(' ', expand=True, n=1)
        # Make Date and time column pd datetime ojects
        df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d')
        df['Time'] = pd.to_datetime(df['Time'], format ='%H:%M:%S')#.dt.time
        #Add call volume number of 1 - so can be added later - to each call in interactions df
        df['call number'] = 1
        #Make a new df - called time_df - from copying df
        time_df = df
        #define na as time delta of 0s
        na = pd.to_timedelta(0)
        #Fill nan with timedelta of 0s for handle time
        time_df.loc[:, 'Handle time'] = time_df['Handle time'].fillna(na)
        #Extract handle times in seconds for easier processing
        time_df['Handle time (s)'] = time_df['Handle time'].dt.total_seconds()
        
        #Resample the time_df in 30min time intervals        
        time_df = time_df.resample('30T', on='Time').sum()
        # Make the time column the index of the time_df
        time_df['Time'] = time_df.index
        
        #Convert handle time to hrs column
        time_df['Handle time (hrs)'] = time_df['Handle time (s)']/3600
        #Convers queue wait to hrs column
        time_df['Queue Wait (hrs)'] = time_df['Queue Wait (secs)']/3600
        
        #Get rid of times where no calls are made
        time_df = time_df[time_df['Queue Wait (secs)']!=0]
        #Convert time columns to a pd datetime
        time_df.loc[:, 'Time'] = time_df['Time'].dt.time
        #Convert time column to a string
        time_df.loc[:, 'Time'] = time_df['Time'].astype(str)
        
        
        time_df['time'] = time_df['Time']
        
        # df = df[df['Handle time']<=pd.Timedelta(value=1, unit='hours')]
        return time_df

# Plots_time_series class plots the wait accumulative wait times sampled every 30min during the week and plots the percentage of time each team and 
# agent spends on handles at each hald hour interval in the day.  
# The roster, team_index_list, an interactions_df and a time_df must all be passed and are made from other classes in the mohKPI package
# There are underlying assumptions in the amount of work down by each agent, thus the plots produced here are only intended to be indicative 
# of when teams and agents are most active
class Plots_time_series():
    def __init__(self, rost_df, team_index_list, int_df, time_df):
        # Initialize class, assign data attributes and call the internal metho control plots to make plots
        self.rost_df = rost_df
        self.team_index_list = team_index_list
        self.int_df = int_df
        self.time_df = time_df
        
        self.control_plots()
    # This function controls the order that plots are produced by looping over the team index list (which contains index location of teams in the roster)
    def control_plots(self):   
        # Loop over team names and plot each Teams half hourly time percentage on handles and plot individual agents after each team
        for i in self.team_index_list:
            # Find start and stop of team of team in roster
            start = i[0]
            stop = i[1]
            # Pull out the team from the roster
            team = self.rost_df.loc[start:stop]
            # Convert team to a list
            team = team['Staff Name'].tolist()
            # Plot the percentage of time spend on handles for the whole team
            self.plot_team(team)
            # Plot the percentage of time spent on handles for each agent in the team
            self.plot_agent(team)
            
    def plot_team(self, team):
        # Get the header from the interactions df and then use those headings to start building a teams interaction_df
        header = self.int_df.columns
        team_df = pd.DataFrame(columns=header)
        # Identify the team name
        team_name = team[0]
        # Identify the actual team agents (listed after the team name)
        team = team[1:]
        counter = 0
        # Loop over team list and concat each agents rows of data from the intereractions df to the team df
        for i in team:
            
            counter+=1
            temp_df = self.int_df[self.int_df['User']==i]
            team_df = pd.concat([team_df,temp_df])
       
        # Reset the index of the team_df
        team_df.reset_index(drop=True, inplace=True)
        #Following line stops copy warning which is being raised incorrectly by Pandas
        team_df = team_df.copy()
        # Create a variable na which holds the pandas timedelta of 0s
        na = pd.to_timedelta(0)
        # Don't plot a team if it hasn't got any data
        if team_df.empty:
            pass
        # Plot team if it has data
        else:
            # Fill in any missing handle time data with pandas timedelta of 0s
            team_df.loc[:, 'Handle time'] = team_df['Handle time'].fillna(na)
            # Get teams total amount of seconds spent on handles
            team_df.loc[:, 'Handle time'] = team_df['Handle time'].dt.total_seconds()
            # Resample team data every 30min for the amount of time spent on a call every 
            team_df = team_df.resample('30T', on='Time').sum()
            # Assign the Time column as the team_df index
            team_df['Time'] = team_df.index
            # Convert Time colimn to a date time object
            team_df.loc[:, 'Time'] = team_df['Time'].dt.time
            # Convert Time to a string
            team_df.loc[:, 'Time'] = team_df['Time'].astype(str)
            # Calaculate % of time spent on handles assuming every agent worked 4 * 7.5hr days - this is a business decision since actual worked 
            # hrs is difficult to obtain within wanted time frames for reporting
            team_df['% handle'] = team_df['Handle time']/(1800*4)*100/len(team)
                       
            # Assign same columns to both df to allow merging
            team_df['time'] = team_df['Time']
            team_df['Time'] = team_df['time']
            # Merge the team_df with time_df
            team_df = pd.merge(self.time_df['time'], team_df, left_on='time', right_on='time', how = 'left')
            team_df['Time'] = team_df['time']
            # Fill any na values with 0 to allow numerical calculations
            team_df.fillna(0, inplace=True)
            
            # Plot the percentage of time the teams spends on handles every half hour of the day
            plt.bar(team_df['Time'], team_df['% handle'])
            plt.title(team_name)
            plt.ylabel('%')
            plt.ylim(top=100)
            plt.xticks(rotation=90)
            plt.show()

            
    # Plost the percentage of time each agent spends on handles every half hour
    def plot_agent(self, team):
        # Loop over agents witin team
        for i in team[1:]:
            agent_name = i
            # Convert Date/Time object in interactions_df to a pd datetime object
            self.int_df['Date/Time'] = pd.to_datetime(self.int_df['Date/Time'])
            # Make and agent interactions df from total interactions df
            agent_df = self.int_df[self.int_df['User']==agent_name]
            # Reset the index
            agent_df.reset_index(drop=True, inplace=True)
            #Followong line stops copy warning which is being raised incorrectly by Pandas
            agent_df = agent_df.copy()
            # Get total agent time spent on handles
            agent_df.loc[:, 'Handle time'] = agent_df['Handle time'].dt.total_seconds()
            
            # Name andy agents that had no data
            if agent_df.empty:
                print(agent_name, ' was inactive')
            
            # Plot agents that are active
            else:
                # Reample agent_df so that the amount of time the agent spent on handles each half hour is recorded
                agent_df = agent_df.resample('30T', on='Time').sum()
                # Re-assign Time column to df index
                agent_df['Time'] = agent_df.index
                # Convert Time column to a datetime object
                agent_df.loc[:, 'Time'] = agent_df['Time'].dt.time
                # Convert Time column to a string
                agent_df.loc[:, 'Time'] = agent_df['Time'].astype(str)
                # Calculate % of time spend on handles assuming a 4 day 7.5 hr work week
                agent_df['% handle'] = agent_df['Handle time']/(1800*4)*100
                # Fill nan values with 0 to alloow numerical calculations
                agent_df['% handle'].fillna(0, inplace = True)
                # Assign same columns to both df to allow merging
                agent_df['time'] = agent_df['Time']
                agent_df['Time'] = agent_df['time']
                # Merge agent df with time df
                agent_df = pd.merge(self.time_df['time'], agent_df, left_on='time', right_on='time', how = 'left')
                agent_df['Time'] = agent_df['time']
                agent_df.fillna(0, inplace=True)
                # Do the pleots
                heading = 'Handle % ' + agent_name
                fig, ax = plt.subplots()
                ax.bar(agent_df['time'], agent_df['% handle'])
                ax.set(title=heading, ylabel='%')
                ax.tick_params(axis='x', rotation=90)
                ax.set(ylim=[0,100])
               
                plt.show()
        
       


    
# The CACT_interactions class simply returns an interactions df which is reduced to only those names contained in the MOH CACT roster
class CACT_interactions:
    def __init__(self, rost_df, int_df):
        # Initialise the class and assign the main data attribute
        self.cact_int_df = self.interactions_MOH(rost_df, int_df)
        
    # Restrict interactions df to only CACT MOH agents 
    def interactions_MOH(self, roster_df, int_df):
        # Identify columns from Interactions df, use columns to make an empty dataframe to concat agent interactions too
        header = int_df.columns
        interactions_df = pd.DataFrame(columns = header)
        # Loop over names in roster and concat any interactions to the CACT_interactions df
        for name in roster_df['Staff Name']:
            temp_df = int_df[int_df['User']==name]
            
            if temp_df.empty:
                pass
            else:
                interactions_df = pd.concat([interactions_df, temp_df], ignore_index=True)
        
        # Return interactions_df with only CACT MOH agents
        return interactions_df

    # Method to return interactions_df with only MOH CACT agents
    def return_interactions_MOH(self):
        return self.cact_int_df
    
    
# The Add_strandard_score_to_KPI_df calculates and agents standard score and appends it to the main_df (or the KPI df made from merging of 
# performance and status files from Genesys).
# The interactions_df and the main_df or KPI_df must be passed to initialize the class
class Add_strandard_score_to_KPI_df:
    def __init__(self, int_df, kpi_df):
        self.kpi_df_with_stand_score = self.add_avg_out_column(int_df, kpi_df)
            
    # Add avg out column prepares KPI_df for appending of standard score by counting the number of outbound calls in the interactions df,
    # filling nan values with 0 for numerical calculations and calculating the time of an average outbound call.  It then calls the 
    # calculate standard score function to append the standard score column to the kpi_df
    def add_avg_out_column(self, int_df, kpi_df):
        out_counts_list = []
        duration_out_list = []
        # For each agent, count the number of outbound calls
        for name in kpi_df['Agent Name']:
            # Count number of outbound calls
            outbound_count = len(int_df[(int_df['User']==name) & (int_df['Direction']=='Outbound')])
            # Append number of outbound calls for agent to list
            out_counts_list.append(outbound_count)
            # Calculate the avergae duration of an outbound calls
            average_outbound = (int_df[(int_df['User']==name) & (int_df['Direction']=='Outbound')]['Handle time'].mean())
            # Append average call duration to a list
            duration_out_list.append(average_outbound)
        # Add colum to KPI_df which has the the number of outbound calls 
        kpi_df['Outbound call volume'] = out_counts_list
        # Fill any nan vakues with 0 to allow numerical calculations
        kpi_df['Outbound call volume'].fillna(pd.to_timedelta(0), inplace=True)
        # Add average outbound call duration columns to KPI df and fill nan values with 0 for numercial calculations
        kpi_df['Outbound call duration'] = duration_out_list
        kpi_df['Outbound call duration'].fillna(pd.to_timedelta(0), inplace=True)
        # Add the standard score as a column to the kpi df
        kpi_df = self.calculate_standard_score(kpi_df)
        return kpi_df
            
    # This function calculates the standard score and returns the kpi df with the standard score column appended
    def calculate_standard_score(self, kpi_df):
        # Assign variables for standard score calculation
        h = kpi_df['Outbound call volume']
        a = kpi_df['Outbound call duration']#.astype('timedelta64[s]')*1e3 ####Need a standard outbiound call length########################################################################
        T = pd.to_timedelta(kpi_df['Logged In'], unit = 'ms')
        q = kpi_df['On Queue %']
        # Set the undustry benchmarks for standard score calculation
        industry_outbound_handle_perc = 0.6
        industry_on_queue_perc = 0.85
        # Calculate standard score and append column to KPI df
        kpi_df['standard score'] = h*a/(industry_outbound_handle_perc*T)+q/industry_on_queue_perc
        return kpi_df
    
    # Function to return KPI_df with standard score column appended
    def return_kpi_df_with_standard_score(self):
        return self.kpi_df_with_stand_score
    
   
    
# This class reads in the queue metrics interval report from Genesys and cleans it up as Genesys output is often in a very non-user friendly format
class Clean_queue_metrics_int_report:
    def __init__(self, queue_metrics_report_pathway):
        # Read in the queue metrics report and assign to data attribute df
        self.df = pd.read_csv(queue_metrics_report_pathway)
        # Clean the df
        self.clean_queue_metrics = self.clean_df()
        
    def clean_df(self):
        df = self.df
        #Identify where the df info starts - first 5 lines are irrelevant
        df = df[5:]
        #The end of the df has an irrelevant line - delete it
        df= df[:-1]
        #Identify the column names
        header = df.iloc[1]
        #Set the column names
        
        df.columns = header
        #Make two empty columns to enter info in
        df['Queue'] = ''
        df['Date'] = ''
        #Drop where-ever the df column 'interval' has no entries - gets rid of irrelevant rows in df
        df.dropna(subset = ['Interval'], inplace=True)
        
        #Create a sub df that only contains rows where offered is empty and then get rid of the rows
        #where the column interval is empty to identify dates over which report has been run
        sub_df = df[df['Offered'].isna()]
        sub_df = sub_df.dropna(subset=['Interval'])
        #Split the 'interval into two colums- interval contains queue, offered contains dates
        sub_df[['Interval', 'Offered']] = sub_df['Interval'].str.rsplit(pat='-',n=1, expand=True)
        #Get rid of leading and trailing whitespaces
        sub_df.loc[:, 'Interval'] = sub_df['Interval'].str.strip()
        sub_df.loc[:, 'Offered'] = sub_df['Offered'].str.strip()
        
        #Loop over queues and assign each row to a queue
        for queue in sub_df['Interval'].unique():
            #Get indices of queus
            indices = df[df['Interval'].str.contains(queue)].index.tolist()
            #There are 49 rows below wach queue for each day in the df
            #Create a column 'Queue' that has what queue each row is associated with
            for i in indices:
                start = i
                stop = i+49
                df.loc[start:stop, 'Queue'] = queue
        
        #Loop over unqiue dates in df and assign each row a relevant date
        for date in sub_df['Offered'].unique():
            #Ignore empty dates
            if str(date) == '':
                pass
            #identify indices where dates start and stop and assign each row to a date under
            #new column 'Date'
            else:
                indices = df[df['Interval'].str.contains(date)].index.tolist()
                for i in indices:
                    start = i
                    stop = i +49
                    df.loc[start:stop, 'Date'] = date
                
        
        #get rid of rows containing nan values for calls (these rows have queue and date data a/a)
        df.dropna(subset=['Offered'], inplace=True)
        df.dropna(subset=['Queue'], inplace=True)
        
        #Get rid of rows with suammry stats
        df = df[df['Interval']!='Day Total']
        #Get rid of rows where the interval is not a time
        df = df[df['Interval']!= 'Interval']
        df.reset_index(drop=True, inplace=True)
        
        #Convert all counts to integer type for later processing
        df['Offered'] = df['Offered'].astype(int)
        df['Answered'] = df['Answered'].astype(int)
        df['Abandoned'] = df['Abandoned'].astype(int)
        
        return df
    
    # Method to return clean queue metrics report as a pandas df
    def return_clean_queue_metrics(self):
        return self.clean_queue_metrics


# This class takes the clean queue metric interval report as a df and then plots the volume of calls offered per half hour
class Plot_half_hourly_queue_offers:
    def __init__(self, queue_metric_df):
        # Assign data attribute
        self.df = queue_metric_df
        # Do the plots
        self.plots()
    
    
    
    def plots(self):
        df = self.df
        #Identify the half hour intervals stored in the df
        times = df['Interval'].unique()
        # Gte rid of times well ourside hours of operation
        times = times[16:]
        times = times[:-10]
        
        # Find the maximum call volume in a half hour interval duriung week - sued to assign max y value in plots
        offered_per_half_hour = []
        for date in df['Date'].unique():
            sub_df = df[df['Date']==date]
            for i in times:
                offered_per_half_hour.append(sub_df[sub_df['Interval']== i]['Offered'].sum())
        ylim = max(offered_per_half_hour)
        
        
        
        # Loop over each day and plot the number of offered calls
        for date in df['Date'].unique():
            #Pass over nan date values
            if date =='':
                pass
            #Create a sub_df which only has the day of intererest
            else:
                sub_df = df[df['Date']==date]
                # Create an empty list to append the calls counts to
                offered = []
                #Append the nummber of calls offered per half hour to the empty list
                for i in times:
                    offered.append(sub_df[sub_df['Interval']== i]['Offered'].sum())
                
                title = 'Total calls offered ' + date
                fig, ax = plt.subplots(1,1)
                fig.set_figwidth(10)
                fig.set_figheight(8)
                ax.bar(times, offered)
                ax.set_title(title)
                ax.tick_params('x', rotation=90)
                ax.set_ylim([0, ylim+1])
                # ax.tick_
                plt.show()
            