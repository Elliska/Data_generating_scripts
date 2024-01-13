import subprocess
import pyodbc
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import library3 as lib

# zvážit smazání a znovuvytvoření databáze
temp_dim_dept, dim_dept, dim_pos, dim_comp, temp_dim_ppl, dim_ppl, dim_date, fact_people = lib.table_names()

server = 'localhost'
database = 'HRprojekt'
trusted_connection = 'yes' 
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};TRUSTED_CONNECTION={trusted_connection}')
cursor = conn.cursor()

tables_to_drop = [temp_dim_dept, temp_dim_ppl]
should_drop_table = False

subprocess.run(['python', 'version 3/dimPeople_test.py'])
#subprocess.run(['python','version 3/dimDepartment_test.py'])
subprocess.run(['python','version 3/dimDate_test.py']) # způsob zapisování dat do DB je pomalý, možná zkusit upravit
subprocess.run(['python','version 3/factPeople_test.py']) 

if should_drop_table:
    for table_name in tables_to_drop:
        drop_table_script = f'DROP TABLE IF EXISTS {table_name};'
        cursor.execute(drop_table_script)

if should_drop_table == True:
    result = 'smazány'
else:
    result = 'ponechány'

print(f'Pomocné tabulky {result}')


conn.commit()
conn.close()


