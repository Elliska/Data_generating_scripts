import pyodbc
#from datetime import datetime, timedelta
#from dateutil.relativedelta import relativedelta
import library3 as lib



temp_dim_dept, dim_dept, dim_pos, dim_comp, temp_dim_ppl, dim_ppl, dim_date, fact_people = lib.table_names()
print(f'Skript {fact_people} inicializován')

# Připojení k databázi
server = 'localhost'
database = 'HRprojekt'
trusted_connection = 'yes' 
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};TRUSTED_CONNECTION={trusted_connection}')
cursor = conn.cursor()

print('Spojení s DB navázáno')

tables_to_drop = [temp_dim_dept, temp_dim_ppl]
should_drop_table = False

should_drop_and_create_table = True
tables_to_update = [fact_people, dim_ppl]

if should_drop_and_create_table:
    for table_name in tables_to_update:
        drop_table_script = f'DROP TABLE IF EXISTS {table_name};'
        cursor.execute(drop_table_script)
        update_status = 'přepsány'
else:
    update_status = 'ponechány'

if should_drop_table == True:
    update_status2 = 'přepsány'
else:
    update_status2 = 'ponechány'

print(f'Tabulky {tables_to_update} budou {update_status}.')
print(f'Tabulky {tables_to_drop} budou {update_status2}.')

fact_table_script = f'''
IF OBJECT_ID('{fact_people}', 'U') IS NULL
BEGIN
    SELECT DISTINCT
        dp.id_person,
        dp.id_branch,
        dp.start_date,
        dp.end_date,
        dp.employment_num,
        dp.id_position,
        dd.id_dept,
        YEAR(da.date_name) AS year_note,
        MONTH(da.date_name) AS month_note
    INTO {fact_people}
    FROM
        {temp_dim_ppl} dp
    LEFT JOIN
        {temp_dim_dept} dd ON dp.id_position = dd.id_position AND dp.id_branch = dd.id_branch
    LEFT JOIN
        dimDate da ON dp.start_date <= da.date_name AND da.date_name <= dp.end_date
END
'''
cursor.execute(fact_table_script)
print(f'{fact_people} tabulka vytvořena.')

dim_ppl_script = f'''
IF OBJECT_ID('{dim_ppl}', 'U') IS NULL
BEGIN
    SELECT 
        id_person,
        first_name,
        last_name,
        date_of_birth,
        age,
        title,
        education,
        email,
        sex,
        gender,
        address_street,
        address_city,
        address_psc,
        address_state,
        health_limit,
        health_limit_spec,
        nationality,
        language_primary,
        language_secondary,
        end_legal,
        end_type,
        employment_type
    INTO {dim_ppl}
    FROM
        {temp_dim_ppl} dp
END
'''
cursor.execute(dim_ppl_script)
print(f'{dim_ppl} byla vytvořena')

dim_dept_script = f'''
IF OBJECT_ID('{dim_dept}', 'U') IS NULL
BEGIN
    SELECT distinct
        id_dept,
        dept_name,
        dept_hierarchy_1,
        dept_hierarchy_2,
        dept_hierarchy_3
    INTO {dim_dept}
    FROM
        {temp_dim_dept} dp
END
'''
cursor.execute(dim_dept_script)
print(f'{dim_dept} tabulka vytvořena.')

dim_pos_script = f'''
IF OBJECT_ID('{dim_pos}', 'U') IS NULL
BEGIN
    SELECT --distinct
        min(id_position) AS id_position,
        position_name,
        seniority,
        level_pos,
        min(salary_min) AS salary_min,
        max(salary_max) AS salary_max,
        min(team) AS team,
        seasonal
    INTO {dim_pos}
    FROM
        {temp_dim_dept} dp
    GROUP BY position_name, seniority, level_pos, seasonal
END
'''
cursor.execute(dim_pos_script)
print(f'{dim_pos} tabulka vytvořena.')



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

print(f'Skript {fact_people} ukončen.')

