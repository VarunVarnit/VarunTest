from azure.identity import DefaultAzureCredential
import pyodbc, struct

# Uncomment one of the two lines depending on the identity type
#credential = DefaultAzureCredential() # system-assigned identity
credential = DefaultAzureCredential(managed_identity_client_id='e6108a97-5efa-41ae-8f00-7cafebcd8c0c') # user-assigned identity

# Get token for Azure SQL Database and convert to UTF-16-LE for SQL Server driver
token = credential.get_token("https://database.windows.net/.default").token.encode("UTF-16-LE")
token_struct = struct.pack(f'<I{len(token)}s', len(token), token)

# Connect with the token
SQL_COPT_SS_ACCESS_TOKEN = 1256
connString = f"Driver={{ODBC Driver 17 for SQL Server}};SERVER=varun-database.database.windows.net;DATABASE=varun-database"
conn = pyodbc.connect(connString, attrs_before={SQL_COPT_SS_ACCESS_TOKEN: token_struct})