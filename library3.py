from mimesis import Address
from mimesis.locales import Locale
import pyodbc
import faker
from faker import Faker
from faker.providers import address
from datetime import datetime, timedelta
import random
from unidecode import unidecode
import uuid

fake_cz = faker.Faker(['cs_CZ'])
fake_sk = faker.Faker(['sk_SK'])
fake_at = faker.Faker(['de_AT'])
fake_fi = faker.Faker(['fi_FI'])
mime_cz = Address(locale=Locale.CS)
mime_sk = Address(locale=Locale.SK)
mime_at = Address(locale=Locale.DE_AT)
mime_fi = Address(locale=Locale.FI)

dept_lead = 'Vedení společnosti'
# nezbytná oddělení pro asi každou společnost
dept_fin = 'Finance a účetnictví'
dept_it = 'IT oddělení'
dept_legal = 'Právní oddělení'
dept_hr = 'HR a vztahy s veřejností'
dept_tech = 'Technické oddělení a správa budov'

# samotná výroba a naskladňování
dept_log = 'Zásobování, logistika a distribuce'
dept_sale = 'Obchodní a marketingové oddělení'
dept_manuf = 'Výroba a produkce'

dept_names = [dept_lead, dept_fin, dept_it, dept_legal, dept_hr, dept_tech, dept_log, dept_sale, dept_manuf]
nr = 1
nr_form = f'{nr:02d}'

#nationality = random.choices(['česká', 'slovenská', 'rakouská', 'finská'],weights=[40,15,15,30])[0]
sex_choice = ['M', 'F', 'I']

def table_names():
    temp_dim_dept = 'temp_dimDepartment'
    dim_dept = 'dimDepartment'
    dim_pos = 'dimPosition'
    dim_comp = 'dimCompanyBranch'
    temp_dim_ppl = 'temp_dimPeople'
    dim_ppl = 'dimPeople'
    dim_date = 'dimDate'
    fact_people = 'factPeople'

    return temp_dim_dept, dim_dept, dim_pos, dim_comp, temp_dim_ppl, dim_ppl, dim_date, fact_people

def people_amount():
    ppl = 1965
    branches = 7
    top_pos = 5
    total_pos = 136
    return ppl, branches, top_pos, total_pos

def department_numbers():
    dept_parts = []

    for i, dept_name in enumerate(dept_names, start=1):
        dept_parts.append((
            str(i), 
            dept_name, 
            f'{int(nr) + i - 1:02d}', 
            f'{int(nr) + i - 1:02d}.{int(nr) + i - 1:02d}', 
            f'{int(nr) + i - 1:02d}.{int(nr) + i - 1:02d}.{int(nr) + i - 1:02d}'
        ))

    return dept_parts

def generate_positions_seniority(dept_name):
    position_mapping = {
        dept_lead: {
            'Generální ředitel (CEO)': ['medior'],
            'Obchodní ředitel (CSO)': ['medior'],
            'Provozní ředitel (COO)': ['medior'],
            'Finační ředitel (CFO)': ['medior'],
            'Výrobní ředitel (CTO)': ['medior'],
        },
        dept_fin: {
            'Vedoucí finančního oddělení': ['medior', 'senior'],
            'Účetní': ['junior', 'medior', 'senior'],
            'Ekonom': ['junior', 'medior', 'senior'],
            'Daňový poradce': ['junior', 'medior', 'senior'],
            'Investice a pojištění': ['junior','medior','senior'],
            'Finanční analytik': ['junior', 'medior', 'senior'],
        },
        dept_it: {
            'Vedoucí IT oddělení': ['medior', 'senior'],
            'Systémový analytik': ['junior', 'medior', 'senior'],
            'Bezpečnostní specialista': ['junior', 'medior', 'senior'],
            'Správce sítě': ['junior', 'medior', 'senior'],
            'IT podpora': ['junior', 'medior', 'senior'],
            'IT technik': ['junior', 'medior', 'senior'],
        },
        dept_legal: {
            'Vedoucí právního oddělení': ['medior', 'senior'],
            'Právník': ['junior', 'medior', 'senior'],
            'Asistent': ['trainee', 'junior', 'medior', 'senior'],
            'Mediátor': ['junior', 'medior', 'senior'],
        },
        dept_hr: {
            'Vedoucí HR oddělení': ['medior', 'senior'],
            'Vedoucí PR oddělení': ['medior', 'senior'],
            'Personalista': ['junior', 'medior', 'senior'],
            'Náborář': ['junior', 'medior', 'senior'],
            'HR asistent': ['trainee', 'junior', 'medior', 'senior'],
            'Tiskový mluvčí': ['junior', 'medior', 'senior'],
            'Marketing': ['junior', 'medior', 'senior'],
            'Designer': ['junior', 'medior', 'senior'],
            'Copywriter': ['junior', 'medior', 'senior'],

        },
        dept_log: {
            'Vedoucí logistického oddělení': ['medior', 'senior'],
            'Vedoucí skladu': ['junior', 'medior', 'senior'],
            'Skladník': ['junior', 'medior', 'senior'],
            'Nákupčí': ['junior', 'medior', 'senior'],
            'Správce distribuce': ['junior', 'medior', 'senior'],
            'Zajišťovatel transportu zboží': ['junior', 'medior', 'senior'],
            'Koordinátor': ['junior', 'medior', 'senior'],
        },
        dept_sale: {
            'Vedoucí obchodního oddělení': ['medior', 'denior'],
            'Obchodník pro severní Evropu': ['junior', 'medior', 'senior'],
            'Obchodník pro západní Evropu': ['junior', 'medior', 'senior'],
            'Obchodník pro východní Evropu': ['junior', 'medior', 'senior'],
            'Obchodník pro střední Evropu': ['junior', 'medior', 'senior'],
            'Obchodník pro jižní Evropu': ['junior', 'medior', 'senior'],
        },
        dept_manuf: {
            'Vedoucí výrobního oddělení': ['medior', 'senior'],
            'BOZP technik': ['junior', 'medior', 'senior'],
            'Pražič kávy' : ['trainee', 'junior', 'medior','senior'],
            'Balič': ['junior', 'medior', 'senior'],
        },
        dept_tech: {
            'Vedoucí technického oddělení': ['medior', 'senior'],
            'Technik': ['trainee','junior', 'medior', 'senior'],
            'Uklízeč': ['trainee', 'junior','medior', 'senior'],
        },
    }

    return position_mapping.get(dept_name, {})

def generate_employment_type():
    employment_type = random.choices(['HPP', 'IČO', 'DPP', 'DPČ'], weights=[50,20,20,10])[0]
    employment_num = random.choices([0.25, 0.5, 0.75, 1], weights=[5,10,15,70])[0]
    
    return employment_type, employment_num

def generate_age():
    # věk a vzdělání

    #unused, moved
    max_birthdate = datetime.now() - timedelta(days=(25 * 365))  # 25 let zpětně
    birthdate = fake_cz.date_time_between(start_date="-60y", end_date=max_birthdate)
    age = (datetime.now() - birthdate).days // 365
    birthdate = birthdate.strftime('%Y-%m-%d')

    return birthdate, age

def generate_health_and_date():
    # zdravotní stav
    voluntary = random.choices(['aktivní', 'odešel', 'odejit'], weights = [40,20,20])[0]
    health_limit = random.choices(['A', 'B', 'C', 'D'], weights=[60,20,10,10])[0] # schopen, schopen s výhradou, schopen s omezením, neschopen
    health = fake_cz.random_element(health_limit)
    map_health_spec = {
    'D': ['neschopen práce'],
    'C': ['potřebuje bezbariérový vstup', 'vyžaduje asistenta', 'potřebuje tlumočníka do znakového jazyka'],
    'B': ['nesmí zvedat břemena nad 25 kg', 'nemůže obsluhovat motorové stroje', 'potřebuje časté a delší pauzy'],
    'A': ['bez omezení'],
    }
    health_limit_spec = fake_cz.random_element(map_health_spec.get(health, ['']))

    
    if voluntary == 'odešel':
        legal = fake_cz.random.choices(['dohodou', 'skončením smlouvy','výpovědí', 've zkušební době'], weights=[35,30,25,10])[0]
        health_limit = random.choice(['A', 'B', 'C', 'D'])
    elif voluntary == 'odejit':
        legal = fake_cz.random_element(['dohodou', 'skončením smlouvy','výpovědí', 've zkušební době', 'okamžitým zrušením'])
        health_limit = random.choices(['A', 'B', 'C', 'D'], weights=[10,10,20,60])[0]
    else:
        legal = fake_cz.random_element([''])
        health_limit = random.choices(['A', 'B'], weights=[70, 30])[0]
    
    # odešel/odejit a aktivní je zcela zástupná hodnota, pouze ke sledování způsobu ukončení, ale nemusí správně reflektovat datum ukončení ke konkrétnímu datu
    # = nedochází k její aktualizaci
    # lidi co mají status aktivní, nemusí být reálně k dnešnímu datu ve firmě stále zaměstnáni

    # start a end date pracovního úvazku
    if voluntary in ['odešel', 'odejit'] and legal != 've zkušební době':
        start_date = datetime(2015, 1, 1) + timedelta(days=random.randint(1, 1800))
        # Minimální délka zaměstnání je X měsíce
        min_days_of_employment = 365
        # Náhodně určit délku zaměstnání mezi minimální a maximální
        employment_duration = random.randint(min_days_of_employment, 1095)
        # Určit end_date tak, aby bylo alespoň 2 měsíce před dnešním dnem
        end_date = datetime(2020, 12, 31) - timedelta(days=min_days_of_employment + random.randint(0, 60))
        # Přiřadit hodnotu employment_duration k end_date
        end_date = start_date + timedelta(days=employment_duration)
        # Zajistit, aby end_date nebylo před start_date
        end_date = max(end_date, start_date + timedelta(days=60))
    elif voluntary in ['odešel', 'odejit'] and legal == 've zkušební době':
        start_date = datetime(2014, 1, 1) + timedelta(days=random.randint(1, 2555))
        min_days_of_employment = 1
        employment_duration = random.randint(min_days_of_employment, 89)
        end_date = datetime(2023, 12, 31) - timedelta(days=min_days_of_employment + random.randint(0, 1))
        end_date = start_date + timedelta(days=employment_duration)
        end_date = max(end_date, start_date + timedelta(days=7))
    else:
        start_date = datetime(2013, 1, 1) + timedelta(days=random.randint(1, 4015))
        min_days_of_employment = 365
        employment_duration = random.randint(min_days_of_employment, 1095)
        end_date = datetime.now() + timedelta(days=random.randint(60, 365))
        end_date = max(end_date, start_date + timedelta(days=60))
        """
    else:
        end_date = datetime.now() + timedelta(days=random.randint(60, 365))
        min_days_of_employment = 365
        employment_duration = random.randint(min_days_of_employment, 2000)
        start_date = end_date - timedelta(days=employment_duration)
        """

    start_date2 = datetime(2014, 1, 1) + timedelta(days=random.randint(1, 365))
    end_date2 = datetime.now() + timedelta(days=random.randint(60, 365))

    return health_limit_spec, health_limit, voluntary, legal, start_date, end_date, start_date2, end_date2

def generate_nationality():
    address_parts = random.choice([
        #Brno
        #0      1       2       3           4           5        6               7             8            9
        (1, 'Berget', 'CZ', 's.r.o.', 'Nové sady 996/25', 'Brno', '602 00', 'Česká republika', '50082762', 'CZ000050082762'),
        (2, 'Arevet', 'CZ', 's.r.o.', 'Holandská 2/4', 'Brno', '639 00', 'Česká republika', '46271648', 'CZ000046271648'),
        #Praha
        (3, 'Adari', 'CZ', 's.r.o.', 'Na Pankráci 1685/19', 'Praha 4', '140 00', 'Česká republika', '45042906', 'CZ000045042906'),
        (4, 'Hiland', 'CZ', 's.r.o.', 'Rohanské nábřeží 671/15', 'Praha', '186 00', 'Česká republika', '60071781',	'CZ000060071781'),
        # Rakousko
        (5, 'Hiland', 'AT', 'GmbH', 'Handelskai 388', 'Wien', '1020', 'Rakouská republika', '92110288', 'AT000092110288'),
        # Finsko
        (6, 'Arevet', 'FI', 'oy', 'Albertinkatu 25', 'Helsinki', '00180', 'Finská republika', '60071781', 'FI000060071781'),
        (7, 'Hiland', 'FI', 'oy', 'Yrttipellontie 6', 'Oulu','90230', 'Finská republika', '92110288', 'FI000092110288'),
        ])

    # Národnost a jazyk
    nationality = random.choices(['česká', 'slovenská', 'rakouská', 'finská'],weights=[40,10,20,20])[0]
    

    map_language_var = {
    'česká': random.choices(['čeština'], weights=[100])[0],
    'slovenská': random.choices(['čeština', 'slovenština'], weights=[30, 70])[0],
    'rakouská': random.choices(['němčina', 'slovenština', 'angličtina'], weights=[70, 10, 20])[0],
    'finská': random.choices(['finština', 'švédština', 'sámi'], weights=[80, 15, 5])[0],
    }
    first_language = map_language_var.get(nationality, '')

    #language secondary
    if nationality in ['česká', 'slovenská']:
        second_language = random.choices(['angličtina', 'němčina', 'francouzština'], weights=[80, 10, 10])[0]
        max_birthdate = datetime.now() - timedelta(days=(21 * 365))  # 25 let zpětně
        birthdate = fake_cz.date_time_between(start_date="-65y", end_date=max_birthdate)
        age = (datetime.now() - birthdate).days // 365
        birthdate = birthdate.strftime('%Y-%m-%d')
    elif nationality == 'rakouská':
        second_language = random.choices(['angličtina', 'španělština', 'francouzština'], weights=[80, 10, 10])[0]
        max_birthdate = datetime.now() - timedelta(days=(25 * 365))  # 25 let zpětně
        birthdate = fake_cz.date_time_between(start_date="-60y", end_date=max_birthdate)
        age = (datetime.now() - birthdate).days // 365
        birthdate = birthdate.strftime('%Y-%m-%d')
    elif nationality == 'finská' and not first_language == 'švédština':
        second_language = random.choices(['angličtina', 'švédština'], weights=[80, 20])[0]
        max_birthdate = datetime.now() - timedelta(days=(26 * 365))  # 25 let zpětně
        birthdate = fake_cz.date_time_between(start_date="-55y", end_date=max_birthdate)
        age = (datetime.now() - birthdate).days // 365
        birthdate = birthdate.strftime('%Y-%m-%d')
    else: # všichni fini s prvním jazykem švédštinou
        second_language = random.choices(['angličtina'])[0]
        max_birthdate = datetime.now() - timedelta(days=(26 * 365))  # 25 let zpětně
        birthdate = fake_cz.date_time_between(start_date="-55y", end_date=max_birthdate)
        age = (datetime.now() - birthdate).days // 365
        birthdate = birthdate.strftime('%Y-%m-%d')
    ###
    #sex = random.choices(['M', 'F', 'I'], weights=[49, 49, 2])[0]
    sex = random.choices(sex_choice, weights=[49, 49, 2])[0]   

    if sex == 'M':   
        gender = random.choices(['male', 'female', 'other'], weights=[80,10,10])[0]
    elif sex == 'F':
        gender = random.choices(['male', 'female', 'other'], weights=[10,80,10])[0]
    else:
        gender = random.choices(['male', 'female', 'other'], weights=[45,45,10])[0]
    

    ## Křestní jméno dle národnosti
    if nationality == 'česká' and gender in ['female', 'other']:
        first_name = fake_cz.first_name_female()
        last_name = fake_cz.last_name_female()
    elif nationality == 'slovenská' and gender in ['female', 'other']:
        first_name = fake_cz.first_name_female()
        last_name = fake_cz.last_name_female()
    elif nationality == 'rakouská' and gender in ['female', 'other']:
        first_name = fake_at.first_name_female()
        last_name = fake_at.last_name_female()
    elif nationality == 'finská' and gender in ['female', 'other']:
        first_name = fake_fi.first_name_female()
        last_name = fake_fi.last_name_female()
    if nationality == 'česká' and gender in ['male', 'other']:
        first_name = fake_cz.first_name_male()
        last_name = fake_cz.last_name_male()
    elif nationality == 'slovenská' and gender in ['male', 'other']:
        first_name = fake_cz.first_name_male()
        last_name = fake_cz.last_name_male()
    elif nationality == 'rakouská' and gender in ['male', 'other']:
        first_name = fake_at.first_name_male()
        last_name = fake_at.last_name_male()
    elif nationality == 'finská' and gender in ['male', 'other']:
        first_name = fake_fi.first_name_male()
        last_name = fake_fi.last_name_male()
    else:
        first_name = fake_sk.first_name_female()
        last_name = fake_sk.last_name_female()

    # email, phone, address
    street_number = f'{random.randint(1, 999)}/{random.randint(1, 99)}' 
    if nationality == 'česká':
        email = f'{unidecode(last_name.lower())}.{unidecode(first_name.lower())}@{unidecode(address_parts[1].lower())}.cz'
        phone = fake_cz.phone_number()
        address_city = mime_cz.city()
        address_psc = fake_cz.postcode()
        address_street = f'{fake_cz.street_name()} {street_number}'
        address_state = 'Česká republika'
        company_id = random.choices([1,2,3,4,5,6,7], weights=[20,20,20,20,5,3,2])[0]
    elif nationality == 'slovenská':
        email = f'{unidecode(last_name.lower())}.{unidecode(first_name.lower())}@{unidecode(address_parts[1].lower())}.sk'
        phone = fake_sk.phone_number()
        address_city = mime_sk.city()
        address_psc = fake_sk.postcode()
        address_street = f'{fake_sk.street_name()} {street_number}'
        address_state = 'Slovenská republika'
        company_id = random.choices([1,2,5], weights=[25,25,50])[0]
    elif nationality == 'rakouská':
        email = f'{unidecode(last_name.lower())}.{unidecode(first_name.lower())}@{unidecode(address_parts[1].lower())}.at'
        phone = fake_at.phone_number()
        address_city = mime_at.city()
        address_psc = fake_at.postcode()
        address_street = f'{fake_at.street_name()} {street_number}'
        address_state = 'Rakouská republika'
        company_id = random.choices([1,2,5,6], weights=[15,10,70,5])[0]
    elif nationality == 'finská':
        email = f'{unidecode(last_name.lower())}.{unidecode(first_name.lower())}@{unidecode(address_parts[1].lower())}.fi'
        phone = fake_fi.phone_number()
        address_city = mime_fi.city()
        address_psc = fake_fi.postcode()
        address_street = f'{fake_fi.street_name()} {street_number}'
        address_state = 'Finská republika'
        company_id = random.choices([1,5,6,7], weights=[5,5,60,30])[0]
    else:
        email = ''
        phone = ''
        address_city = random.choice('Londýn', 'Birmingham', 'Durham')
        address_psc = ''
        address_street = ''
        address_state = 'Velká británie'
        company_id = random.choice(1,2,3,4,5,6,7)


    return nationality, first_language, second_language, first_name, last_name, gender, sex, email, company_id, address_parts[1], address_parts[2], address_parts[3], address_parts[4], address_parts[5], address_parts[6], address_parts[7], address_parts[8], address_parts[9], street_number, address_street, address_city, address_psc, phone, address_state, birthdate, age

def generate_title_and_hierarchy():
    education_options = ['základní', 'středoškolské s výučním listem', 'středoškolské odborné', 'středoškolské všeobecné', 'středoškolské s maturitou', 
                         'vyšší odborné vzdělání', 'vysokoškolské bakalářské', 'vysokoškolské navazující', 'vysokoškolské doktorské']
    education = fake_cz.random_element(education_options)
    
    mapping = {
        'vyšší%': ['DiS.'],
        'vysokoškolské bakalářské': ['Bc.', 'BcA.'],
        'vysokoškolské navazující': ['Ing.', 'Ing. arch', 'Mgr.', 'MgA.'],
        'vysokoškolské doktorské': ['PhD.','JUDr.', 'PhDr.', 'RNDr.'],
    }
    title = fake_cz.random_element(mapping.get(education, ['']))

    return title, education

#vvv