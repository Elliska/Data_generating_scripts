###########
## na základě národnosti je vygenerované prakticky všechno
###########

import pyodbc
from faker import Faker
import random
#import uuid
import library3 as lib 
#from datetime import datetime, timedelta
import run_scripts as rs

#seed = 12345
#random.seed(seed)
#Faker.seed(seed)

random.seed()
Faker.seed()

temp_dim_dept, dim_dept, dim_pos, dim_comp, temp_dim_ppl, dim_ppl, dim_date, fact_people = lib.table_names()
########### DB connection
server = 'localhost'
database = 'HRprojekt'
trusted_connection = 'yes' 
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};TRUSTED_CONNECTION={trusted_connection}')
cursor = conn.cursor()

print('Spojení s DB navázáno')


#should_rewrite_tables_dimPeople = True

if rs.should_rewrite_tables_dimPeople == True:
    drop_table_script = f'DROP TABLE IF EXISTS {temp_dim_ppl};'
    cursor.execute(drop_table_script)

if rs.should_rewrite_tables_dimPeople == True:
    update_value = 'přepsaná. Data vypsaná znovu.'
else:
    update_value = 'ponechaná. Data přidaná za existující.'

print(f'Spojení s databází navázáno a tabulka {update_value}')

create_table_query = f'''
IF OBJECT_ID('{temp_dim_ppl}', 'U') IS NULL
BEGIN
    CREATE TABLE {temp_dim_ppl} (
        id_person INT PRIMARY KEY IDENTITY(1,1),
        first_name NVARCHAR(255),
        last_name NVARCHAR(255),
        date_of_birth DATE,
        age INT,
        title NVARCHAR(50),
        education NVARCHAR(50),
        -- phone NVARCHAR(255),
        email NVARCHAR(255),
        sex NVARCHAR(1),
        gender NVARCHAR(10),
        address_street NVARCHAR(255),
        address_city NVARCHAR(255),
        address_psc NVARCHAR(20),
        address_state NVARCHAR(255),
        health_limit NVARCHAR(1),
        health_limit_spec NVARCHAR(255),
        nationality NVARCHAR(50),
        language_primary NVARCHAR(50),
        language_secondary NVARCHAR(50),
        -- employment NVARCHAR(50),
        end_legal NVARCHAR(50),
        end_type NVARCHAR(50),
        employment_type NVARCHAR(255),
        -- informace o firmě,
        id_branch INT,
        -- company_name NVARCHAR(255),
        -- company_name_legal NVARCHAR(255),
        -- address_street_comp NVARCHAR(255),
        -- address_city_comp NVARCHAR(255), 
        -- address_postal_comp NVARCHAR(255), 
        -- address_country_comp NVARCHAR(255),
        -- ic NVARCHAR(15),
        -- dic NVARCHAR(15),
        -- informace do faktové tabulky,
        start_date DATE,
        end_date DATE,
        employment_num FLOAT,
        id_position NVARCHAR(255)
    );
END
'''
cursor.execute(create_table_query)
conn.commit()

print(f'{temp_dim_ppl} tabulka vytvořena.')


##########

ppl, branches, top_pos, total_pos = lib.people_amount()

people_person = []

for i in range(ppl):
    #person_id = str(uuid.uuid4())
    nationality, first_language, second_language, first_name, last_name, gender, sex, email, company_id, company_name, ctr, legal, address_street_comp, address_city_comp, address_postal_comp, country, ic, dic, street_number, address_street, address_city, address_psc, phone, address_state, birthdate,age = lib.generate_nationality()

    company_name_legal = f'{company_name}-{ctr}, {legal}' 
    #birthdate, age = lib.generate_age()
    health_limit_spec, health_limit, voluntary, legal, start_date, end_date, start_date2, end_date2 = lib.generate_health_and_date()

    title, education = lib.generate_title_and_hierarchy()
    employment_type, employment_num = lib.generate_employment_type()

    #today = datetime.now()

    start_date = start_date.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')

    id_position = random.randint(top_pos+1,total_pos)

    person_data = {
        #'ID_person': person_id ,
        'first_name': first_name,
        'last_name': last_name,
        'date_of_birth': birthdate,
        'age': age,
        'title': title,
        'education': education,
        #'phone': phone, #potřebuje sjednotit formát čísla, nechce mi to DB schroupat (a mne se s tím nechce dělat)
        'email': email,
        'sex': sex,
        'gender': gender,
        'address_street': address_street,
        'address_city': address_city,
        'address_psc': address_psc,
        'address_state': address_state,
        'health_limit': health_limit,
        'health_limit_spec': health_limit_spec,
        'nationality': nationality,
        'language_primary': first_language,
        'language_secondary': second_language,
        #'employment': '1', #asi doplnit až podle pozice
        'end_legal': legal,
        'end_type': voluntary,
        'employment_type': employment_type,
        # informace o firmě:
        'id_branch': company_id, # id
        #'company_name': company_name,
        #'company_name_legal': company_name_legal,
        #'address_street_comp': address_street_comp,
        #'address_city_comp': address_city_comp, 
        #'address_postal_comp': address_postal_comp, 
        #'address_country_comp': country,
        #'ic': ic,
        #'dic': dic,
        # informace do faktové tabulky:
        'start_date': start_date,
        'end_date': end_date,
        'employment_num': employment_num,
        'id_position': id_position,
    }

    people_person.append(person_data)

#print('První sekce vygenerovaná}')

###################################
people_board = []

last_code_numbers = {}

for spec_company_id in range(1,branches+1):
    if spec_company_id not in last_code_numbers:
        last_code_numbers[spec_company_id] = 1


    current_company_number = 1

    for j in range(1,top_pos+1):
        current_code_number = last_code_numbers[spec_company_id]

        for i in range(1):
            nationality, first_language, second_language, first_name, last_name, gender, sex, email, company_id, company_name, ctr, legal, address_street_comp, address_city_comp, address_postal_comp, country, ic, dic, street_number, address_street, address_city, address_psc, phone, address_state, birthdate, age = lib.generate_nationality()

            company_name_legal = f'{company_name}-{ctr}, {legal}' 
            #birthdate, age = lib.generate_age()
            health_limit_spec, health_limit, voluntary, legal, start_date, end_date, start_date2, end_date2 = lib.generate_health_and_date()

            title, education = lib.generate_title_and_hierarchy()
            """"
            today = datetime.now()

            start_date2 = datetime(2015, 1, 1) + timedelta(days=random.randint(1, 3000))
            end_date2 = datetime.now() + timedelta(days=random.randint(365, 730))  # den ukončení bude 365 dní v budoucnosti
            end_date2 = max(end_date2, start_date2 + timedelta(days=30))
            """

            start_date2 = start_date2.strftime('%Y-%m-%d')
            end_date2 = end_date2.strftime('%Y-%m-%d')
            

            last_code_numbers[spec_company_id] += 1

            # muselo by být ještě spolu se jménem (zbytečné komplikace, lze přidat radši do knihovny)
            sex2 = random.choices(['M', 'F','I'], weights=[30,68,2])[0]
            if sex2 == 'M':
                gender2 = random.choices(['male','female', 'other'], weights = [70,25,5])[0]
            elif sex2 == 'F':
                gender2 = random.choices(['male','female', 'other'], weights = [25,70,5])[0]
            else:
                gender2 = random.choice(['male','female', 'other'])

            board_data = {
                #'ID_person': person_id ,
                'first_name': first_name,
                'last_name': last_name,
                'date_of_birth': birthdate,
                'age': age,
                'title': title,
                'education': education,
                #'phone': phone, #potřebuje sjednotit formát čísla, nechce mi to DB schroupat (a mne se s tím nechce dělat)
                'email': email,
                'sex': sex,
                'gender': gender,
                'address_street': address_street,
                'address_city': address_city,
                'address_psc': address_psc,
                'address_state': address_state,
                'health_limit': 'A',
                'health_limit_spec': '',
                'nationality': nationality,
                'language_primary': first_language,
                'language_secondary': second_language,
                #'employment': '1', #asi doplnit až podle pozice
                'end_legal': '',
                'end_type': 'aktivní',
                'employment_type': 'HPP',
                # informace o firmě:
                'id_branch': spec_company_id, # id
                #'company_name': company_name,
                #'company_name_legal': company_name_legal,
                #'address_street_comp': address_street_comp,
                #'address_city_comp': address_city_comp, 
                #'address_postal_comp': address_postal_comp, 
                #'address_country_comp': country,
                #'ic': ic,
                #'dic': dic,
                # informace do faktové tabulky:
                'start_date': start_date2,
                'end_date': end_date2,
                'employment_num': 1,
                'id_position': current_code_number, #id
            }


            people_board.append(board_data)

#print('Druhá sekce vygenerovaná}')


#################################
tables_and_data = [
    (temp_dim_ppl, people_person),
    (temp_dim_ppl, people_board),
    ]


which_piece_choices = ['first', 'second', 'both']
which_piece = 'both'


if which_piece == 'first':
    for person_data in people_person:
        columns = ', '.join(person_data.keys())
        values = ', '.join([f"N'{value}'" if isinstance(value, str) else f"{value}" for value in person_data.values()])
        insert_data_script = f'INSERT INTO {temp_dim_ppl} ({columns}) VALUES ({values});'
        print('První sekce lidí zapsaná do tabulky.')
        try:
            cursor.execute(insert_data_script)
            conn.commit()
        except Exception as e:
            print(f"Chyba při vkládání dat: {e}")
        conn.rollback()
elif which_piece == 'second':
    for board_data in people_board:
        columns = ', '.join(board_data.keys())
        values = ', '.join([f"N'{value}'" if isinstance(value, str) else f"{value}" for value in board_data.values()])
        insert_data_script = f'INSERT INTO {temp_dim_ppl} ({columns}) VALUES ({values});'
        print('Druhá sekce lidí zapsaná do tabulky.')
        try:
            cursor.execute(insert_data_script)
            conn.commit()
        except Exception as e:
            print(f"Chyba při vkládání dat: {e}")
        conn.rollback()
elif which_piece == 'both': # při pokusu je dát dohromady nefungovalo
    for person_data in people_person:
        columns = ', '.join(person_data.keys())
        values = ', '.join([f"N'{value}'" if isinstance(value, str) else f"{value}" for value in person_data.values()])
        insert_data_script = f'INSERT INTO {temp_dim_ppl} ({columns}) VALUES ({values});'
        print('První sekce lidí zapsaná do tabulky.')
        try:
            cursor.execute(insert_data_script)
            conn.commit()
        except Exception as e:
            print(f"Chyba při vkládání dat: {e}")
        conn.rollback()

    for board_data in people_board:
        columns = ', '.join(board_data.keys())
        values = ', '.join([f"N'{value}'" if isinstance(value, str) else f"{value}" for value in board_data.values()])
        insert_data_script = f'INSERT INTO {temp_dim_ppl} ({columns}) VALUES ({values});'
        print('Druhá sekce lidí zapsaná do tabulky.')
        try:
            cursor.execute(insert_data_script)
            conn.commit()
        except Exception as e:
            print(f"Chyba při vkládání dat: {e}")
        conn.rollback()
else:
    print('Nothing selected')

print(f'Data pro tabulku {temp_dim_ppl} byla vytvořena a zapsaná.')