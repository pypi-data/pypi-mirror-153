#################
# IMPORTS
#################
from ast import Add
import pandas as pd
import umbitlib.dates as mconst
import math
import numpy as np
from datetime import datetime
import calendar


#################
# FORMATTING FUNCTIONS
#################

def human_format(num):
    """
    Takes in a number and returns a truncated version with a suffix of ' ',K,M,B, or T.
    Dependent on numerical magnitude.
    """
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'), ['', 'K', 'M', 'B', 'T'][magnitude])


    
#################
# ARITHMETIC FUNCTIONS
#################

def check_nan(value):
    """
    Replaces NAN values with 0 so they can be passed into equations.
    """
    if math.isnan(value):
        return 0.0
    return value



def clean_division(dividend, divisor):
    """
    Evaluates the divisor of division equation.  
    If 0 then the result = 0 else the division is completed as normal.
    """
    try:
        if divisor == 0:
            return 0.0
        return check_nan(dividend/divisor)
    except:
        return 0.0

def up_down(value1, value2, text='up', precision='norm', decimals=0):
    """
    Evaluates two inputs to see if the first is higher or lower than the second, then returns a string accordingly
    Default text='up' but can be modified to return greater, higher, +, increase, above, or success 
    precision values = norm/round
    """
    dict = {
        'greater':'less',
        'up':'down',
        'higher':'lower',
        'increase':'decrease',
        'above':'below',
        'success':'danger',
        '+':'-'
    }

    if precision == 'round':
        value1 = round(value1, decimals)
        value2 = round(value2, decimals)

    try:
        if value1 > value2:
            return(text)                
        elif value1 < value2:
            return(dict[text])            
        elif value1 == value2:
            return("in-line with")
    except:
        return(f"Error in up_down function value1: {value1}​ value2: {value2}​")

def delta(new_value, old_value, precision='norm', decimals=0):
    """ Returns the percentage difference between new value and old value """
    if precision == 'round':
        value1 = round(new_value, decimals)
        value2 = round(old_value, decimals)
    else:
        value1 = new_value
        value2 = old_value
    a = value1
    b = value2
    x = clean_division((a - b), b)
    return x

def evaluation(valNew, valOld, comparison, precision='round', decimals=0):
    if comparison == 'diff':
        if precision =='round':
            valNew = round(valNew, decimals)
            valOld = round(valOld, decimals)
        delta = valNew - valOld
    else:
        if precision =='round':
            valNew = round(valNew, decimals)
            valOld = round(valOld, decimals)
        delta = clean_division((valNew - valOld), valOld)

    if delta == 0:
       valUp = 'in-line with'
    elif delta > 0:
       valUp = 'above'
    elif delta < 0:
       valUp = 'below'

    dictOut = {
        'valNew' : valNew,
        'valOld' : valOld,
        'valDelta' : abs(delta),
        'valUp' : valUp,
    }

    return dictOut


#################
# CLASS HELPING FUNCTIONS
#################

def trgt_month_total(object, metric, year='cur'):
    """
    Calculates the value for the target month based on desired metric and year. (prior = prior year, cur = current year)
    Default state is current year. ('cur') Pervious year = 'prev'  
    """
    if year == 'cur':
        year = 0
    elif year == 'prev':
        year = 1

    x = object[(object['cur_fy_flg'] == year) & (object['cur_fy_month_flg'] == 1)][metric].sum()
    return x


def trgt_month_total_ar(df, metric):
    """
    trgt_month_total function adapted to be used with the AR dataset
    This should be removed and replaced with the regular trgt_month_total function
    once the 'cur_fy_flg' and 'cur_fy_month_flg' have been added to the analytics_site_db_artrend table in postgres 
    """
    x =  df[df['post_period']==mconst.TARGET_PD][metric].sum() 
    return x



def fytd_total(object, metric, year='cur'):
    """
    Calculates the value for a fiscal year based on desired metric and year.
    Default state is current year. ('cur') Pervious year = 'prev'
    """
    if year == 'cur':
        year = 0
    elif year == 'prev':
        year = 1

    x = object[(object['cur_fy_flg'] == year) & (object['fytd_flg'] == 1)][metric].sum()
    return x



def twelve_month_total(object, metric):
    """
    Calculates the rolling 12 month total for the specified metric.  
    12 month rolling period is defined as the 12 months prior to the target month.
    """
    x = object[object['post_period'].isin(mconst.LST_ROLLING_DATES)][metric].sum() #refactored ver.  needs checking
    return x



def twelve_month_avg(object, metric):
    """
    Calculates the rolling 12 month avearge for the specified metric.  
    12 month rolling period is defined as the 12 months prior to the target month.
    """
    x = clean_division(object[object['post_period'].isin(mconst.LST_ROLLING_DATES)][metric].sum(), 12) #refactored ver.  needs checking
    return x



def lst_metric_postperiods(df, metric):
    """
    Calculates a monthly total for the specified metric and fills in any missing months with a 0 value.  
    24 month rolling period is defined as the 24 months prior to the target month.
    """
    if df.empty == True:
        x = df
    else:
        df = df[df['cur_fy_flg'].isin([0,1])].groupby('post_period')[metric].sum().reset_index() # Sum up the dataframe
        df['post_period'] =  df['post_period'].dt.strftime('%m/%d/%Y') # Reformat date so join will work
        # Left Join df to the date list and fill in any missing month values with 0's 
        x = pd.merge(pd.DataFrame(mconst.LST_PFY_FYTD_MONTHS, columns=['post_period']), pd.DataFrame(df, columns=['post_period',metric]), on='post_period',how = "left").fillna(0)[metric]

    return x



def cnt_unique(object, metric, col, year='cur', tmframe='trgtmon'):
    """
    Takes in a dataframe and a column.  Counts the target month unique occurences at the selected column's aggregate
    for the year specified.
    Default state is current year. ('cur') Pervious year = 'prev'
    tmframe can be set to the following: (trgtmon (default), year)
    metric = (sx_case, visit_cnt)
    """
    if year == 'cur':
        year = 0
    elif year == 'prev':
        year = 1

    if metric == 'sx_case':        
        if tmframe == 'trgtmon':
            x = object[(object['cur_fy_flg'] == year) & (
                object['cur_fy_month_flg'] == 1) & (object['surgical_case_flg'] == 1)][col].nunique()
            return x
        elif tmframe == 'year':
            x = object[(object['post_period'].isin(mconst.LST_ROLLING_DATES)) & (object['surgical_case_flg'] == 1)][col].nunique()
            return x
    elif metric == 'visit_cnt':
        if tmframe == 'trgtmon':
            x = object[(object['cur_fy_flg'] == year) & (
                object['cur_fy_month_flg'] == 1)][col].nunique()
            return x
        elif tmframe == 'year':
            x = object[(object['post_period'].isin(mconst.LST_ROLLING_DATES))][col].nunique()
            return x

###########################
# Custom Functions
##########################

def days_in_month(date):
    """
    Takes in a date period as a datetime type.  i.e. 7/1/2022
    Returns the amount of days in the specified month. Accounts for leap years.
    """
    results = calendar.monthrange(date.year, date.month)[1] 
    return results

def lst_sums_per_dttm(df, metric, date_grouper, include_dates_lst):
    """
    Dynamically sums a specified metric by a specified date grouper.  Only includes dates that are found in the include_dates_lst argument.
    metric: pass in any numerical column that you want to aggregate
    date_grouper: the date column by which the data should be grouped by
    include_dates_lst: a list of dates by which your df should be subset.  (i.e. a list of 12 months for a summing up column x by month for 12 months.)
    """
    result = df[pd.to_datetime(df[date_grouper]).isin(include_dates_lst)].groupby(date_grouper)[metric].sum().reset_index().sort_values(date_grouper, ascending = True).reset_index(drop=True).fillna(0)[metric].tolist() 
    return result


# %%
def add(a:int, b:int, c:int=0) -> int:
    """ Add two or three integers and return an integer result.

    Args:
        a (int) :            Your first number
        b (int) :            Your second number
        c (int, optional) :  Your third number

    Returns:
        int

    Raises:
        typeError: if a, b, & c aren't all integers

    Example:
        add(1, 2)        

    """
    for var in [a, b, c]:        
        if not isinstance(var, int) :
            raise TypeError('Please make sure all inputs are integers')
    
    result = a + b + c

    return result

