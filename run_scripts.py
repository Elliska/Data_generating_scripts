import subprocess, sys
import pyodbc
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import library3 as lib
'''
import os

path = "C:/Users/michaela.maleckova/OneDrive - Seyfor/Projekt/Data_generating_scripts"
os.chdir(path)
'''
# zvážit smazání a znovuvytvoření databáze
temp_dim_dept, dim_dept, dim_pos, dim_comp, temp_dim_ppl, dim_ppl, dim_date, fact_people = lib.table_names()

server = 'localhost'
database = 'HRprojekt'
trusted_connection = 'yes' 
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};TRUSTED_CONNECTION={trusted_connection}')
cursor = conn.cursor()

tables_to_drop = [temp_dim_dept, temp_dim_ppl]
should_drop_table = False


should_rewrite_tables_dimPeople = True
should_rewrite_table_dimDepartment = True
should_rewrite_table_dimCompanyBranch = True

should_rewrite_test = True

#subprocess.run(['python', 'dimPeople_test.py'])
#subprocess.run(['python','dimDepartment_test.py'])
#subprocess.run(['python','dimDate_test.py'])
#subprocess.run(['python','factPeople_test.py']) 
#subprocess.run([sys.executable,'C:/Users/michaela.maleckova/OneDrive - Seyfor/Projekt/Data_generating_scripts/dimPeople_test.py'], check=True, cwd='C:/Users/michaela.maleckova/OneDrive - Seyfor/Projekt')
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


