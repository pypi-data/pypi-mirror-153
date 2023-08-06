import psycopg2
import pandas as pd
import time
from umbitlib.constants import HOST, DATABASE, PORT, USER, PASS, LST_CATG_VARIABLES
from umbitlib.dates import TRGTMON_YYYYMMDD
def query(sql):
    connection = psycopg2.connect(user=USER,
                                  password=PASS,
                                  host=HOST,
                                  port=PORT,
                                  database=DATABASE)
    tic = time.perf_counter()                            
    df = pd.read_sql_query(sql, connection, parse_dates='post_period')
    connection.close()
    toc = time.perf_counter() 
    print(f"Query finished in {toc - tic:0.4f} seconds")
    df.drop('id', axis = 1, inplace = True) 
    return df

def mk_table_df(strTableName):
    """ Creates a query for any table in the umbdb schema  
        strTableName: Takes a string with the '[app_name]_[model_name]' 
                                         i.e. 'month_end_mefs_menu'
    """
    print(f"Setting up and Running {strTableName} SQL Query...")
    strSQL = f"""
                select *
                from public.{strTableName}
             """ 
    df = query(strSQL)
    return df

def mk_menu_df():
    """ Creates SQL query for entire month_end_mefs_menu table """
    print('Setting up and Running Menu SQL Query...')
    strSQL = """select * from public.month_end_mefs_menu"""
    df = query(strSQL)
    df = df.sort_values(by='tab_order', ascending=True)
    df.rename(columns={'billing_prov_dwid': 'billing_provider_dwid'}, inplace=True)
    return df
    
def mk_fin_df():
    """ Creates a query for analytics_site_db_financialmetrics table 
        strDwid: Takes a string of comma-seperated billing_group_dwids
    """
    print('Setting up and Running Financials SQL Query...')    
    strSQL = """
                 select * from analytics_site_db_financialmetrics
             """ 
    df = query(strSQL)

    # Setting Categorical variable columns to default to Other/Collection Fee (Not populated for bad debt payments)
    df[LST_CATG_VARIABLES] = df[LST_CATG_VARIABLES].fillna(value='OTHER/COLLECTION FEE') # This will remain here because its simpler than a ton of NVL()s in the SQL
    return df


def mk_fin_df_grp(strDwid):
    """ Creates a query for analytics_site_db_financialmetrics table for one or more given billing_group_dwid's 
        strDwid: Takes a string of comma-seperated billing_group_dwids
    """
    print('Setting up and Running Financials SQL Query...')    
    strSQL = """
                 select * from analytics_site_db_financialmetrics
                 where billing_group_dwid in (""" + str(strDwid) + """)
             """ 
    df = query(strSQL)

    # Setting Categorical variable columns to default to Other/Collection Fee (Not populated for bad debt payments)
    df[LST_CATG_VARIABLES] = df[LST_CATG_VARIABLES].fillna(value='OTHER/COLLECTION FEE') # This will remain here because its simpler than a ton of NVL()s in the SQL
    return df

def mk_gencnt_df():
    """ Creates a query for analytics_site_db_generalcounts table 
    """
    print('Setting up and Running General Counts SQL Query...')
    strSQL = """
                 select * from analytics_site_db_generalcounts
             """ 
    df = query(strSQL)
    return df

def mk_gencnt_df_grp(strDwid):
    """ Creates a query for analytics_site_db_generalcounts table for one or more given billing_group_dwid's 
        strDwid: Takes a string of comma-seperated billing_group_dwids
    """
    print('Setting up and Running General Counts SQL Query...')
    strSQL = """
                 select * from analytics_site_db_generalcounts
                 where billing_group_dwid in (""" + str(strDwid) + """)
             """ 
    df = query(strSQL)
    return df

def mk_ar_df():
    """ Creates a query for analytics_site_db_artrendreport table 
    """
    print('Setting up and Running AR SQL Query...')
    strSQL = """
                 select * from analytics_site_db_artrendreport
             """ 
    df = query(strSQL)
    # Truncing the post_period dates (3rd of the month etc.) to show only the first of the month
    df = df[df['post_period'] <= TRGTMON_YYYYMMDD] # Removing Current Month AR Numbers
    df = df[(df['current_financial_class_dwid'] != 883153)] # Removing null Financial classes and payor not found # DELETE - Shuktika is adding to dataset 
    # Combining any additional buckets
    df.loc[df['aging_bucket']=='121-150 DAYS', 'aging_bucket'] = '121-180 DAYS'
    df.loc[df['aging_bucket']=='151-180 DAYS', 'aging_bucket'] = '121-180 DAYS'
    return df

def mk_ar_df_grp(strDwid):
    """ Creates a query for analytics_site_db_artrendreport table for one or more given billing_group_dwid's 
        strDwid: Takes a string of comma-seperated billing_group_dwids
    """
    print('Setting up and Running AR SQL Query...')
    strSQL = """
                 select * from analytics_site_db_artrendreport
                 where billing_group_dwid in (""" + str(strDwid) + """)
             """ 
    df = query(strSQL)
    # Truncing the post_period dates (3rd of the month etc.) to show only the first of the month
    df = df[df['post_period'] <= TRGTMON_YYYYMMDD] # Removing Current Month AR Numbers
    df = df[(df['current_financial_class_dwid'] != 883153)] # Removing null Financial classes and payor not found # DELETE - Shuktika is adding to dataset 
    # Combining any additional buckets
    df.loc[df['aging_bucket']=='121-150 DAYS', 'aging_bucket'] = '121-180 DAYS'
    df.loc[df['aging_bucket']=='151-180 DAYS', 'aging_bucket'] = '121-180 DAYS'
    return df

def mk_lag_df():
    """ Creates a query for analytics_site_db_postlagmetrics table 
    """
    print('Setting up and Running Lag SQL Query...')
    strSQL = """
                 select * from analytics_site_db_postlagmetrics
             """ 
    df = query(strSQL)
    return df

def mk_lag_df_grp(strDwid):
    """ Creates a query for analytics_site_db_postlagmetrics table for one or more given billing_group_dwid's 
        strDwid: Takes a string of comma-seperated billing_group_dwids
    """
    print('Setting up and Running Lag SQL Query...')
    strSQL = """
                 select * from analytics_site_db_postlagmetrics
                 where billing_group_dwid in (""" + str(strDwid) + """)
             """ 
    df = query(strSQL)
    return df

def mk_asa_df():
    """ Creates a query for analytics_site_db_asaunits table 
    """
    print('Setting up and Running Asa SQL Query...')
    strSQL = """
                 select * from analytics_site_db_asaunits
             """ 
    df = query(strSQL)
    return df

def mk_asa_df_grp(strDwid):
    """ Creates a query for analytics_site_db_asaunits table for one or more given billing_group_dwid's 
        strDwid: Takes a string of comma-seperated billing_group_dwids
    """
    print('Setting up and Running Asa SQL Query...')
    strSQL = """
                 select * from analytics_site_db_asaunits
                 where billing_group_dwid in (""" + str(strDwid) + """)
             """ 
    df = query(strSQL)
    return df

def mk_dist_df():
    """ Creates a query for analytics_site_db_distributions table 
    """
    print('Setting up and Running Distributions SQL Query...')
    strSQL = """
                 select * from analytics_site_db_distributions
             """ 
    df = query(strSQL)
    return df

def mk_dist_df_grp(strDwid):
    """ Creates a query for analytics_site_db_distributions table for one or more given billing_group_dwid's 
        strDwid: Takes a string of comma-seperated billing_group_dwids
    """
    print('Setting up and Running Distributions SQL Query...')
    strSQL = """
                 select * from analytics_site_db_distributions
                 where billing_group_dwid in (""" + str(strDwid) + """)
             """ 
    df = query(strSQL)
    return df

def mk_edcensus_df():
    """ Creates a query for analytics_site_db_edcensus table 
    """
    print('Setting up and Running edcensus SQL Query...')
    strSQL = """
                 select * from analytics_site_db_edcensus
             """ 
    df = query(strSQL)
    return df

def mk_edcensus_df_grp(strDwid):
    """ Creates a query for analytics_site_db_edcensus table for one or more given billing_group_dwid's 
        strDwid: Takes a string of comma-seperated billing_group_dwids
    """
    print('Setting up and Running edcensus SQL Query...')
    strSQL = """
                 select * from analytics_site_db_edcensus
                 where billing_group_dwid in (""" + str(strDwid) + """)
             """ 
    df = query(strSQL)
    return df

def mk_arbotartrend_df():
    """ Creates a query for analytics_site_db_arbotartrend table 
    """
    print('Setting up and Running arTrend SQL Query...')
    strSQL = """
                select *
                from public.analytics_site_db_arbotartrend ar
                where ar.aging_bucket in ('180+ DAYS','91-120 DAYS', '121-150 DAYS', '151-180 DAYS')
             """ 
    df = query(strSQL)
    return df

def mk_arbotdenialtrend_df():
    """ Creates a query for analytics_site_db_artrend table 
    """
    print('Setting up and Running arTrend SQL Query...')
    strSQL = """
                select *
                from public.analytics_site_db_arbotdenialtrend 
             """ 
    df = query(strSQL)
    return df

def mk_arbotfinancialmetrics_df():
    """ Creates a query for analytics_site_db_arbotfinancialmetrics table 
    """
    print('Setting up and Running arTrend SQL Query...')
    strSQL = """
                select *
                from public.analytics_site_db_arbotfinancialmetrics
             """ 
    df = query(strSQL)
    return df

def mk_arbothundredpercentadjustments_df():
    """ Creates a query for analytics_site_db_arbothundredpercentadjustments table 
    """
    print('Setting up and Running arTrend SQL Query...')
    strSQL = """
                select *
                from public.analytics_site_db_arbothundredpercentadjustments
             """ 
    df = query(strSQL)
    return df


