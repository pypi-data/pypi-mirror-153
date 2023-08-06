# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 01:29:15 2022

@author: Huihui
"""
# The following 10 blocks of code define the classes for storing the the return data, for each
# currency pair.
from numpy import isnan

# The following 10 blocks of code define the classes for storing the the return data, for each
# currency pair.
        
# Define the AUDUSD_return class - each instance will store one row from the dataframe
class AUDUSD_return(object):
    # Variable to store the total number of instantiated objects in this class
    num = 0
    # Variable to store the running sum of the return
    run_sum = 0.0
    run_squared_sum = 0
    run_sum_of_std = 0
    last_price = -1
    
    # Init all the necessary variables when instantiating the class
    def __init__(self, tick_time, avg_price):
        
        # Store each column value into a variable in the class instance
        self.tick_time = tick_time
        #self.price = avg_price
        
        if AUDUSD_return.last_price == -1:
            hist_return = float('NaN')
        else:
            hist_return = (avg_price - AUDUSD_return.last_price) / AUDUSD_return.last_price
        
        self.hist_return = hist_return
        if isnan(hist_return):
            AUDUSD_return.run_sum = 0
        else:
            # Increment the counter
            if AUDUSD_return.num < 5:
                AUDUSD_return.num += 1
            AUDUSD_return.run_sum += hist_return
        AUDUSD_return.last_price = avg_price
        

    def get_avg(self,pop_value):
        if isnan(self.hist_return) == False:
            self.run_sum -= pop_value
            avg = self.run_sum/(self.num)
            self.avg_return = avg
            return avg
    
   