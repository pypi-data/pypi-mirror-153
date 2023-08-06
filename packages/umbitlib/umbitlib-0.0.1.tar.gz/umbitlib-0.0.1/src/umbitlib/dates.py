from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import calendar

# DATE CONSTANTS
TODAY = datetime.today() # Uncomment this line to test different dates for all the constants + relativedelta(months=5)
TRGTMON_DATETIME = TODAY.replace(day=1) - relativedelta(months=1)
TRGTMON_TRGT_DAY_DATETIME = TODAY.replace(day=1) - relativedelta(days=1)
TRGTMON_TRGT_DAY = format(TRGTMON_TRGT_DAY_DATETIME, '%m/%d/%Y')
TRGTMON_MMDDYYYY = format(TRGTMON_DATETIME, '%m/%d/%Y')
TRGTMON_YYYYMMDD = format(TRGTMON_DATETIME, '%Y/%m/%d')
TRGTMON_NAME = format(TRGTMON_DATETIME, '%B')
TRGTMON_NAME_YEAR_NUM = format(TRGTMON_DATETIME, '%B %Y')
TRGT_FISCAL_YEAR_NUM = format(TRGTMON_DATETIME, '%Y') if int(format(TRGTMON_DATETIME, '%m'))<7 else int(format(TRGTMON_DATETIME, '%Y'))+1

PRIOR_YR_TRGTMON_DATETIME = TRGTMON_DATETIME.replace(hour=0, minute=0, second=0, microsecond=0) - relativedelta(months=12)
PRIOR_YR_TRGTMON = format(PRIOR_YR_TRGTMON_DATETIME, '%m/%d/%Y')
PRIOR_YR_TRGTMON_NAME_YEAR_NUM = format(PRIOR_YR_TRGTMON_DATETIME, '%B %Y')

TWO_YRS_PRIOR_TRGTMON_DATETIME = TRGTMON_DATETIME.replace(hour=0, minute=0, second=0, microsecond=0) - relativedelta(months=24)

# period in which the report is generated
CURRENT_PD = TODAY.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
# period for which reporting is being done.
TARGET_PD = (CURRENT_PD - relativedelta(months=1)).replace(hour=0, minute=0, second=0, microsecond=0)
# Defines the periods for the start and end of the rolling 12 months prior to the target period
ROLLING_PD_START = (CURRENT_PD - relativedelta(months=13)).replace(hour=0, minute=0, second=0, microsecond=0)
ROLLING_PD_END = (CURRENT_PD - relativedelta(months=2)).replace(hour=0, minute=0, second=0, microsecond=0)
TWENTYFOUR_MO_PD_START = (CURRENT_PD - relativedelta(months=24)).replace(hour=0, minute=0, second=0, microsecond=0)

PRIOR_FISCAL_YEAR_START = format(PRIOR_YR_TRGTMON_DATETIME, '%Y/07/01') if int(format(TRGTMON_DATETIME, '%m'))>=7 else format(TWO_YRS_PRIOR_TRGTMON_DATETIME, '%Y/07/01')

LST_ROLLING_DATES = pd.date_range(start=ROLLING_PD_START, periods=12, freq=pd.offsets.MonthBegin(1)).strftime('%m/%d/%Y').tolist()    
LST_13_MONTHS = pd.date_range(start=ROLLING_PD_START, periods=13, freq=pd.offsets.MonthBegin(1)).strftime('%m/%d/%Y').tolist()
LST_24_MONTHS = pd.date_range(start=TWENTYFOUR_MO_PD_START, periods=24, freq=pd.offsets.MonthBegin(1)).strftime('%m/%d/%Y').tolist()                                                            
LST_PFY_FYTD_MONTHS = pd.date_range(start=PRIOR_FISCAL_YEAR_START, end=TARGET_PD, freq=pd.offsets.MonthBegin(1)).strftime('%m/%d/%Y').tolist()


START_PD = ROLLING_PD_START.strftime('%Y/%m/%d')
END_PD = ROLLING_PD_END.strftime('%Y/%m/%d')

# USED IN ED CENSUS MODULE
ROLLING_DATES_DTTM = pd.date_range(start=ROLLING_PD_START, periods=13, freq=pd.offsets.MonthBegin(1)) 
DAYS_IN_MONTH_LST = [calendar.monthrange(i.year, i.month)[1] for i in ROLLING_DATES_DTTM]


# Used in AR Bot
FOUR_WKS_AGO = TODAY - relativedelta(days=28)
START_52_WK_ROLLING_PD = TODAY - relativedelta(days=392) # start of rolling 364 days prior to 4 weeks ago
END_52_WK_ROLLING_PD = TODAY - relativedelta(days=29)
