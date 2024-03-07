import pyodbc
from faker import Faker
import random
import library3 as lib 
from datetime import datetime, timedelta
import run_scripts as rs

#seed = 12345
#random.seed(seed)
#Faker.seed(seed)

random.seed()
Faker.seed()


temp_dim_dept, dim_dept, dim_pos, dim_comp, temp_dim_ppl, dim_ppl, dim_date, fact_people = lib.table_names()

# DB connection
server = 'localhost'
database = 'HRprojekt'
trusted_connection = 'yes' 
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};TRUSTED_CONNECTION={trusted_connection}')
cursor = conn.cursor()

print('Spojení s DB navázáno')

create_table_query = f'''
IF OBJECT_ID('{dim_comp}', 'U') IS NULL
BEGIN
    CREATE TABLE {dim_comp} (
        id_branch INT PRIMARY KEY IDENTITY(1,1),
        company_name NVARCHAR(255),
        company_name_legal NVARCHAR(255),
        address_street_comp NVARCHAR(255),
        address_city_comp NVARCHAR(255), 
        address_postal_comp NVARCHAR(255), 
        address_country_comp NVARCHAR(255),
        ic NVARCHAR(15),
        dic NVARCHAR(15)
    );
END
'''

cursor.execute(create_table_query)


if rs.should_rewrite_table_dimCompanyBranch == True:
    drop_table_script = f'DROP TABLE IF EXISTS {dim_comp};'
    cursor.execute(drop_table_script)
    cursor.execute(create_table_query)
    conn.commit()

if rs.should_rewrite_table_dimCompanyBranch == True:
    update_value = 'přepsaná. Data vypsaná znovu.'
else:
    update_value = 'ponechaná. Data přidaná za existující.'

print(f'Spojení s databází navázáno a tabulka {update_value}')

# Generate data for each company
ppl, branches, top_pos = lib.people_amount()
company_branch = []

# Define predefined company data
address_parts = [
    (1, 'Berget', 'CZ', 's.r.o.', 'Nové sady 996/25', 'Brno', '602 00', 'Česká republika', '50082762', 'CZ000050082762'),
    (2, 'Arevet', 'CZ', 's.r.o.', 'Holandská 2/4', 'Brno', '639 00', 'Česká republika', '46271648', 'CZ000046271648'),
    (3, 'Adari', 'CZ', 's.r.o.', 'Na Pankráci 1685/19', 'Praha 4', '140 00', 'Česká republika', '45042906', 'CZ000045042906'),
    (4, 'Hiland', 'CZ', 's.r.o.', 'Rohanské nábřeží 671/15', 'Praha', '186 00', 'Česká republika', '60071781', 'CZ000060071781'),
    (5, 'Hiland', 'AT', 'GmbH', 'Handelskai 388', 'Wien', '1020', 'Rakouská republika', '92110288', 'AT000092110288'),
    (6, 'Arevet', 'FI', 'oy', 'Albertinkatu 25', 'Helsinki', '00180', 'Finská republika', '60071781', 'FI000060071781'),
    (7, 'Hiland', 'FI', 'oy', 'Yrttipellontie 6', 'Oulu','90230', 'Finská republika', '92110288', 'FI000092110288'),
]

# Iterate through predefined company data
for company_id, company_name, company_country, legal, address_street_comp, address_city_comp, address_postal_comp, country, ic, dic in address_parts:
    company_name_legal = f'{company_name}-{company_country}, {legal}'  # Adjust as needed

    branch_data = {
        'company_name': company_name,
        'company_name_legal': company_name_legal,
        'address_street_comp': address_street_comp,
        'address_city_comp': address_city_comp,
        'address_postal_comp': address_postal_comp,
        'address_country_comp': country,
        'ic': ic,
        'dic': dic,
    }

    company_branch.append(branch_data)

# Iterate through the generated company_branch list and print each row
for branch_data in company_branch:
    print(branch_data)

# Insert data into the table
for branch_data in company_branch:
    columns = ', '.join(branch_data.keys())
    values = ', '.join([f"N'{value}'" if isinstance(value, str) else f"{value}" for value in branch_data.values()])
    insert_data_script = f'INSERT INTO {dim_comp} ({columns}) VALUES ({values});'
    print(f'Data byla vložena do tabulky {dim_comp}')
    try:
        cursor.execute(insert_data_script)
        conn.commit()
    except Exception as e:
        print(f"Chyba při vkládání dat: {e}")
        conn.rollback()

# Close the connection
conn.close()
print('Všechna data zapsaná.')
