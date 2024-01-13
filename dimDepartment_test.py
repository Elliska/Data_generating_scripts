################################
## pak přidat rozseknutí na dvě části SQL tabulky (celkem 3, 1 pomocná)
## pro faktovku potřebuji kombinaci ID pozice a ID oddělení
###############################

import random
import library3 as lib
import pyodbc

seed = 12345
random.seed(seed)
#lib = library

temp_dim_dept, dim_dept, dim_pos, dim_comp, temp_dim_ppl, dim_ppl, dim_date, fact_people = lib.table_names()

########### DB connection
server = 'localhost'
database = 'HRprojekt'
trusted_connection = 'yes' 
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};TRUSTED_CONNECTION={trusted_connection}')
cursor = conn.cursor()


create_table_query = f'''
IF OBJECT_ID('{temp_dim_dept}', 'U') IS NULL
BEGIN
    CREATE TABLE {temp_dim_dept} (
        id_note INT PRIMARY KEY IDENTITY(1,1),
        id_dept INT,
        dept_name NVARCHAR(255),
        dept_hierarchy_1 NVARCHAR(8),
        dept_hierarchy_2 NVARCHAR(8),
        dept_hierarchy_3 NVARCHAR(8),
        id_position INT,
        position_name NVARCHAR(255),
        seniority NVARCHAR(255),
        level_pos NVARCHAR (255),
        salary_min INT,
        salary_max INT,
        team INT,
        seasonal VARCHAR(255),
        id_branch INT
    );
END
'''

cursor.execute(create_table_query)

should_update_table = True

if should_update_table:
    drop_table_script = f'DROP TABLE IF EXISTS {temp_dim_dept};'
    cursor.execute(drop_table_script)
    print(f'Tabulka {temp_dim_dept} byla přepsaná.')
else:
    print(f'Do tabulky {temp_dim_dept} byla přidaná nová data.')

cursor.execute(create_table_query)
conn.commit()

##########
ppl, branches, top_pos, total_pos = lib.people_amount()
dept_parts = lib.department_numbers()
dept_num = []
total_rows = 0

for dept in dept_parts:
    positions_seniority = lib.generate_positions_seniority(dept[1])
    
    for position, seniorities in positions_seniority.items():
        for seniority in seniorities:
            total_rows += 1

last_code_numbers = {}

# Seznam pro uchování výsledných dat
companies = []

for company_id in range(1,branches+1):
    # Inicializace čísla pro aktuální firmu, pokud ještě není inicializováno
    if company_id not in last_code_numbers:
        last_code_numbers[company_id] = 1

    # Aktuální číslo pro firmu
    current_code_number = last_code_numbers[company_id]

    for dept in dept_parts:
        positions_seniority = lib.generate_positions_seniority(dept[1])

        for position, seniorities in positions_seniority.items():
            for seniority in seniorities:

                if 'ředitel' in position.lower():
                    pos_level = 'board'
                    seasonal = 'N'
                    salary_min = random.randint(65000, 75000)
                    salary_max = random.randint(salary_min, 95000)
                    team = random.randint(1, 2)
                elif 'vedoucí' in position.lower(): 
                    pos_level = 'top-management'
                    seasonal = 'N'
                    salary_min = random.randint(45000, 55000)
                    salary_max = random.randint(salary_min, 75000)
                    team = random.randint(1, 2)
                elif 'týmu' in position.lower(): # pokud bych ještě chtěla vedoucí týmů
                    pos_level = 'mid-management'
                    seasonal = 'N'
                    salary_min = random.randint(30000, 35000)
                    salary_max = random.randint(salary_min, 55000)
                    team = random.randint(1, 2)
                elif any(pos in position.lower() for pos in ['uklízeč','skladník', 'balič', 'pražič kávy']):
                    pos_level = 'non_management'
                    #seasonal = random.choices(['N', 'Y'], weights=[40,60])[0]
                    seasonal = 'Y'
                    salary_min = random.randint(15000, 25000)
                    salary_max = random.randint(salary_min, 30000)
                    team = random.randint(1, 2)
                else:
                    pos_level = 'non-management'
                    seasonal = 'N'
                    salary_min = random.randint(25000, 35000)
                    salary_max = random.randint(salary_min, 45000)
                    team = random.randint(10, 20)

                company_data = {
                    'id_dept': dept[0],
                    'dept_name': dept[1],
                    'dept_hierarchy_1': dept[2],
                    'dept_hierarchy_2': dept[3],
                    'dept_hierarchy_3': dept[4],
                    'id_position': current_code_number,
                    'position_name': position,
                    'seniority': seniority,
                    'level_pos': pos_level,
                    'salary_min': salary_min,
                    'salary_max': salary_max,
                    'team': team,
                    'seasonal': seasonal,
                    'id_branch': company_id,
                }
                
                companies.append(company_data)
                current_code_number += 1

    # Uložení posledního použitého čísla pro firmu
    last_code_numbers[company_id] = current_code_number

limited_combinations = companies[:10]

print(f'Data pro tabulku {temp_dim_dept} byla vygenerovaná.')


####################################

for company_data in companies:
    columns = ', '.join(company_data.keys())
    values = ', '.join([f"N'{value}'" if isinstance(value, str) else f"{value}" for value in company_data.values()])
    insert_data_script = f'INSERT INTO {temp_dim_dept} ({columns}) VALUES ({values});'
    cursor.execute(insert_data_script)

conn.commit()
conn.close()

print(f'Data pro tabulku {temp_dim_dept} byla zapsaná do databáze.')