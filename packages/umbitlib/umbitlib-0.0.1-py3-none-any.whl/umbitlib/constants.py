import os

# List of Columns with categorical variables
LST_CATG_VARIABLES = ['location', 'billing_provider', 'proc_code', 'pos_type', 'pos_group']

# Database Credentials
PASS = os.environ['PG_DEV_PASS']
USER = os.environ['PG_DEV_USER']
HOST = os.environ['PG_DEV_HOST']
PORT = os.environ['PG_DEV_PORT']
DATABASE = os.environ['PG_DEV_DB']
