# -*- coding: utf-8 -*-

#Import packages
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#This function reads in the telstra data from csv, cleans the df and reformats strings of dates/times to datetime objects
def read_telstra(file_path):
    # TRead in the file
    df = pd.read_csv(file_path, header =4)
  
    #Get rid of numbers with and N - these are network landing points and do not directly reflect call volumes
    #?Possibly if we take away total calls from volume of N we may get the number of disconnections before routing to PHU or CACT
    nolike = df[df['Answer Point'].str.contains('N')]
    #Concat the two nolike dataframe and with the telstra fata, then drop duplicates with keep set to False to remove N numbers
    df = pd.concat([df, nolike]).drop_duplicates(keep=False)
    
    #Convert date columns to a datetime object
    #First get rid of the time of call (not relevant to current analysis)
    df['Date (DD/MM/YYYY HH:MM:SS)'] = df['Date (DD/MM/YYYY HH:MM:SS)'].str.split(' ', expand = False).str[0]
    # Convert date to datetime object
    df['Date (DD/MM/YYYY HH:MM:SS)'] = pd.to_datetime(df['Date (DD/MM/YYYY HH:MM:SS)'], format='%d/%m/%Y')
    # Uncomment and modify below lines to select start and fininsh dates we want to analyse if dates weren't limited in download
    # start = pd.to_datetime('15/05/2022', format='%d/%m/%Y')
    # end = pd.to_datetime('21/05/2022', format='%d/%m/%Y')
    # df = df[(df['Date (DD/MM/YYYY HH:MM:SS)'] >= start) &( df['Date (DD/MM/YYYY HH:MM:SS)']<=end)]
    
    #Remove 'MOBILE-' in locality column
    df['Locality'] = df['Locality'].str.replace('MOBILE-', '')
    #Make locality column all lower case
    df['Locality'] = df['Locality'].str.lower()
    
    
    #Get rid of suburbs with a nsw following there name
    df['Locality'] = df['Locality'].str.replace(' nsw', '')
    df['Locality'] = df['Locality'].str.replace('the ', '')
   
    
    return df


#This function creates a new columns where each calls is associated with a particular PHU   
def assign_LHD_nums(df):
    #Read in data file which contains the phone numbers and associated LHD numbers
    LHD_nums = pd.read_csv(r'C:\1300 number analysis\unchanging data\LHD numbers.csv')
    LHD_nums.dropna(inplace=True)
    #Create empty columns for PHU and LHD
    df['PHU'] = np.nan
    df['LHD'] = np.nan
    
    # Assign each answer point to a particular PHU 
    for num in LHD_nums['Terminating number']:
        PHU = (LHD_nums[LHD_nums['Terminating number']==num]['PHU'].iloc[0])
        
        LHD = (LHD_nums[LHD_nums['Terminating number']==num]['LHD'].iloc[0])
        
        df.loc[df['Answer Point']==num, ['PHU']] = PHU
        df.loc[df['Answer Point']==num, ['LHD']] = LHD

    return(df)


#This function identifies how many calls went to each PHU and the percentage of thiese calls
def unique_num_df(df):
    #Create an empty list to append the total number fof calls handled by each PHU (as a list of lists)
    total_LHD = []
    # Loop over each PHU and count the number of calls, append to empty list
    for locality in df['PHU'].unique():
        #Create emmpty list then append name of PHU and call count
        PHU = []
        PHU.append(locality)
        
        PHU.append(len(df[df['PHU']==locality]))
        if len(df[df['PHU']==locality])==0:
            pass
        else:
            #Append list containing PHU and call count to total_LHD list
            total_LHD.append(PHU)
    
    #Get info re what numbers are associated with each PHU
    LHD_nums = pd.read_csv(r'C:\1300 number analysis\unchanging data\LHD numbers.csv')
    LHD_nums.dropna(inplace=True)
    LHD_nums = LHD_nums.iloc[:18]
    
    #Create df that has the call colume to each PHU
    #First create an empty dataframe with relevant colums
    uni_df = pd.DataFrame(data=total_LHD, columns=['location that answered', 'volume'])
    #Merge the uni_df with LHD nums so that PHU and terminating number are associated
    uni_df = pd.merge(uni_df, LHD_nums, left_on='location that answered', right_on='PHU', how='left')
    #Get rid of repeating PHU colum
    uni_df.drop('PHU', axis = 1, inplace = True)
    #Add a columns that calculates percentage of calls
    uni_df['Percentage'] = uni_df['volume'] / uni_df['volume'].sum() *100
    #Sort df by volume of calls in descencing order
    uni_df.sort_values(by= 'volume', ascending=False, inplace=True)
    
    # print(uni_df)
    return uni_df


#This function is poorly names for historical resons
#This function simply reads infor about what psotcode is associated with what PHU
def clean_up_LHD_df():
    #Read in LHD matched to locality name csv file
    LHD_df = pd.read_csv(r'C:\1300 number analysis\unchanging data\postcodes suburbs LGAs PHUs and LHDs.csv')
   
    #Make column 'Postcode Name' all lower case to standardise for later data wrangling
    LHD_df['Postcode Name'] = LHD_df['Postcode Name'].str.lower()
    return LHD_df

#This function assigns each call location to a particular PHU, plots number of calls answred by CACT from each PHU and saves info in a csv
def get_vol_calls_from_each_LHD(df, LHD_df):
    
    df = pd.merge(df, LHD_df, left_on='Locality', right_on='Postcode Name', how='left')
  
    #The LHD_df has some duplication which must be eliminated.  
    #Additionally, duplication occasionally occurs due to places having two names e.g. dural - has low effect on true numbers 
    #~3.5% of all town names repeat but analysis suggests this affects the results by <1% (0.6%)
    df = df.drop_duplicates(subset='Call ID')
    
    df['LHD_y'].fillna('Out of state', inplace=True)
    
    #Create empty lists to append info to
    ori_num_calls = []
    LHD = []
    answered_CACT = []
    
    # Loop over each LHD
    for LHD_y in df['LHD_y'].unique():
        # append the relevant PHU
        LHD.append(LHD_y)
        #Append the number of calls made from within PHU
        ori_num_calls.append(len(df[df['LHD_y']==LHD_y]['LHD_y']))
        #Calculate percentage of calls answered for that PHU by CACT
        answered_CACT.append(len(df[(df['Answer Point']=='02 7209 7087') & (df['LHD_y']==LHD_y)]))
        
        
    #Plot the number of calls into CACT from within each PHU location     
    plt.bar(LHD, ori_num_calls)
    plt.xticks(rotation=90)
    plt.title('Number of calls into 1300 from each LHD')    
    plt.show()
   
    #Create a df that contains the volume of calls from each LHD/PHU, the number and percentage of those calls answered by CACT    
    call_ori_df = pd.DataFrame()
    call_ori_df['LHD']= LHD
    call_ori_df['volume of calls generated in LHD'] = ori_num_calls
    call_ori_df['Answered by CACT'] = answered_CACT
    call_ori_df['% calls answered by CACT'] = call_ori_df['Answered by CACT'] / call_ori_df['volume of calls generated in LHD'] *100
    #Save new df to a csv
    call_ori_df.to_csv('Origin af calls from each LHD.csv')
 
# This function simpply calculates the percentage of calls answered by CACT for each day in the reporting period
def perc_calls_by_CACT(df):
    # Create empty list to append to (make a list of lists later)
    volumes = []
    # loop over dates in the Telstra data
    for date in df['Date (DD/MM/YYYY HH:MM:SS)'].unique():
        temp_df = df[df['Date (DD/MM/YYYY HH:MM:SS)']==date]
        # Creat temp list which will later be appended to volumes list
        temp_list = []
        #Append relevant data to temp list
        daily_in = len(temp_df)
        CACT_vol = len(temp_df[temp_df['Answer Point']=='02 7209 7087'])
        temp_list.append(date)
        temp_list.append(daily_in)
        temp_list.append(CACT_vol)
        #Append days data to volumes list
        volumes.append(temp_list)
    #Convert data contained in volumes list to a df and save as a csv
    daily_vol = pd.DataFrame(volumes, columns=['Date', 'Total inbound volume', 'CACT inbound volume'])
    daily_vol['% 1300 to CACT'] = daily_vol['CACT inbound volume'] / daily_vol['Total inbound volume'] *100
    daily_vol.to_csv('Daily percentage of calls to CACT.csv')
        
   
def main():
    #Read in telstra data and clean it up a little
    df = read_telstra(file_path = r'extract (29).csv')
    
    start = str(df.iloc[0,0])[:-9]
    stop = str(df.iloc[-1,0])[:-9]
    
    
    # Assign LHD to each phone calls in a new column
    df = assign_LHD_nums(df)
    #Make a df that has number and percentage of calls to each PHU + save to csv
    uni_df = unique_num_df(df)
    
    file_name = 'volumes to LHDs via 1300 ' + start +' to ' + stop + '.csv'
    
    # Save file containing the percentage and number of calls handled by each PHU and CACT 
    uni_df.to_csv(file_name)
    
    # Read in df that contains postcode and associated PHU
    LHD_df = clean_up_LHD_df()
    #Find out the PHU origin of calls and how many are handled by CACT
    get_vol_calls_from_each_LHD(df, LHD_df)
    # Calculate the daily percentage of calls into 1300 number handled by CACT
    perc_calls_by_CACT(df)
    
main()
    
    
