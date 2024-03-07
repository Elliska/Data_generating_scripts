import pyodbc
import run_scripts as rs

server = 'localhost'
database = 'HRprojekt'
trusted_connection = 'yes' 
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};TRUSTED_CONNECTION={trusted_connection}')
cursor = conn.cursor()

test_table = 'test'

if rs.should_rewrite_test == True:
    drop_table_script = f'DROP TABLE IF EXISTS {test_table};'
    cursor.execute(drop_table_script)


create_table_query = f'''
IF OBJECT_ID('{test_table}', 'U') IS NULL
BEGIN
    CREATE TABLE {test_table} (
        id_person INT PRIMARY KEY IDENTITY(1,1),
        first_name NVARCHAR(255),
        last_name NVARCHAR(255),
    );
END
'''
cursor.execute(create_table_query)

data = {'first_name': 'someone',
        'last_name': 'someone else'}

columns = ', '.join(data.keys())
values = ', '.join([f"N'{value}'" if isinstance(value, str) else f"{value}" for value in data.values()])
insert_data_script = f'INSERT INTO {test_table} ({columns}) VALUES ({values});'
cursor.execute(insert_data_script)

conn.commit()






