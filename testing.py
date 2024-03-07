import pyodbc

server = 'localhost'
database = 'HRprojekt'
trusted_connection = 'yes' 
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};TRUSTED_CONNECTION={trusted_connection}')
cursor = conn.cursor()

test_table = 'test'

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
conn.commit()





