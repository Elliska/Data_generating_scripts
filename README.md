# About this project

## Imaginary Company

This is a set of scripts for creating dummy data. Any similarity to real people is purely coincidental. Essentially, it represents an imaginary company with branches in several countries that roasts and trades coffee. People belong to various nationalities (Czech, Slovak, Austrian, and Finnish).

The code takes into consideration intersex individuals, gender, and nonconformity to assigned biological sex.

The majority of the generated data is derived from nationality. Each company has people of different ages, and additional data such as email addresses are included.

The code accounts for people leaving and joining the imaginary company. Individuals who leave during the probationary period should not remain in the company for more than 3 months. The code tries to portray a serious issue in company: an increased number of terminations for individuals unfit to perform their job due to health reasons and those with health limitations.

While job positions are assigned somewhat randomly, company leadership is generated fixedly. There is a specific number of managerial positions, each filled exactly once in each company. The termination of people's careers is more or less random, but their start date is not. The date is determined by whether individuals are currently active in a company or not. 

## About Code and Data Integrity
There are errors and possibly nonsense in the data. All errors and nonsense discovered during exploratory SQL queries and Power BI exploratory analysis have been corrected. The Python code is very beginner-like and organically created as my skills increased.

This is the first attempt at code. Although I had encountered Python in the past, at the time of deciding to write these scripts, I couldn't independently write any code (let alone a library).

## About the Database
The database is used to connect to Power BI as demo data. Connection is made to an MS SQL server (T-SQL). The database has a classic star schema with a fact table in the middle.

## Data Creation and Transformation
All data are created in two main tables, which can be deleted by script, and two final tables (data, company information). Temporary tables are denormalized to easily use all IDs for the fact table.

Temporary tables are then modified with the help of data transformation (SQL scripts in Python) and divided into final tables. Temporary tables can be easily deleted directly in the script.

Consistency and data quality were verified throughout using SQL scripts and Power BI. Discovered errors were promptly fixed.

## About Helpers
ChatGPT 3.5 was used, occasionally Bard was tried as GPT was often unavailable during the writing. 

The initial writing was entirely based on AI-suggested code, and later, I was able to write the code on my own.

Assistance was also provided by the Junior Guru community.

Towards the end of code writing, I no longer needed generative AI, as I gained a decent understanding of the libraries used and ways to achieve what I wanted.

Later, I only had unfamiliar things explained and checked the code. Subsequently, I created a library and a summary script to run all others on my own.

# What did I use?

### Libraries

* Main
    * faker and mimesis for random data
    * pyodbc for connecting to MS SQL server
    * random
    * datetime
* Others
    * unidecode
    * custom library

### Programs

* Visual Studio Code
* Power BI
* DBeaver
* Git
    * Git Bash (only tried)
    * GitHub Desktop GUI
    * Git through VS Code

### Assistance

* GPT 3.5
* Bard
* Junior Guru

### Version
* it took 3 working versions to get to this point (so this one is 3rd)