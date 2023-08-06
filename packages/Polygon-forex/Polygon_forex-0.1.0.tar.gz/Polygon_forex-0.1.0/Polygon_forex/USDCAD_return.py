# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 01:31:19 2022

@author: Huihui
"""
from numpy import isnan,sqrt
# Define the USDCAD_return class - each instance will store one row from the dataframe
class USDCAD_return(object):#last_date,avg_price
    # Variable to store the total number of instantiated objects in this class
    num = 0
    # Variable to store the running sum of the return
    run_sum = 0
    run_squared_sum = 0
    run_sum_of_std = 0
    last_price = -1
    
    # Init all the necessary variables when instantiating the class
    def __init__(self, tick_time, avg_price):#last_date,avg_price

        # Store each column value into a variable in the class instance
        self.tick_time = tick_time
        #self.price = avg_price
        
        if USDCAD_return.last_price == -1:#first time
            hist_return = float('NaN')
        else:
            hist_return = (avg_price - USDCAD_return.last_price) / USDCAD_return.last_price
        
        self.hist_return = hist_return
        if isnan(hist_return):
            USDCAD_return.run_sum = 0#counter set 0
        else:
            # Increment the counter
            if USDCAD_return.num < 5:
                USDCAD_return.num += 1
            USDCAD_return.run_sum += hist_return
        USDCAD_return.last_price = avg_price
        
    
    def get_avg(self,pop_value):
        if isnan(self.hist_return) == False:
            self.run_sum -= pop_value
            avg = self.run_sum/(self.num)
            self.avg_return = avg
            return avg