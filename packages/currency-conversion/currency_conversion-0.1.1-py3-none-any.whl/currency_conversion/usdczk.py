# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 14:23:32 2022

@author: jenny
"""

from math import sqrt
from math import isnan

class USDCZK_return(object):
    # Variable to store the total number of instantiated objects in this class
    num = 0
    # Variable to store the running sum of the return
    run_sum = 0
    run_squared_sum = 0
    run_sum_of_std = 0
    last_price = -1
    
    # Init all the necessary variables when instantiating the class
    def __init__(self, tick_time, avg_price):
        
        # Store each column value into a variable in the class instance
        self.tick_time = tick_time
        #self.price = avg_price
        
        if USDCZK_return.last_price == -1:
            hist_return = float('NaN')
        else:
            hist_return = (avg_price - USDCZK_return.last_price) / USDCZK_return.last_price
        
        self.hist_return = hist_return
        if isnan(hist_return):
            USDCZK_return.run_sum = 0
        else:
            # Increment the counter
            if USDCZK_return.num < 5:
                USDCZK_return.num += 1            
            USDCZK_return.run_sum += hist_return
        USDCZK_return.last_price = avg_price
        
    def add_to_running_squared_sum(self,avg):
        if isnan(self.hist_return) == False:
            USDCZK_return.run_squared_sum += (self.hist_return - avg)**2
    
    def get_avg(self,pop_value):
        if isnan(self.hist_return) == False:
            USDCZK_return.run_sum -= pop_value
            avg = USDCZK_return.run_sum/(USDCZK_return.num)
            self.avg_return = avg
            return avg
    
    def get_std(self):
        if isnan(self.hist_return) == False:
            std = sqrt(USDCZK_return.run_squared_sum/(USDCZK_return.num))
            self.std_return = std
            USDCZK_return.run_sum_of_std += std
            USDCZK_return.run_squared_sum = 0
            return std
    
    def get_avg_std(self,pop_value):
        if isnan(self.hist_return) == False:
            USDCZK_return.run_sum_of_std -= pop_value
            avg_std = USDCZK_return.run_sum_of_std/(USDCZK_return.num)
            self.avg_of_std_return = avg_std 
            return avg_std