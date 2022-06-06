# -*- coding: utf-8 -*-
#Import the mohKPI program
import mohKPI as mh

#Main function controls the rest of the program  
def main():
    
    # Read in the queue metrics interval report
    df = mh.Clean_queue_metrics_int_report(r"C:\Genesys reporting\Call volumes per hour code\06-06-2022\All inbound queues half hour interval report.csv").return_clean_queue_metrics()
    # Plot the number of calls per half hour for each day of the report
    mh.Plot_half_hourly_queue_offers(df)
    
main()
