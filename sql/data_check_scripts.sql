SELECT * FROM temp_dimPeople; -- smazat přes skript
SELECT * FROM dimPeople;

SELECT * FROM temp_dimDepartment ; -- smazat přes skript
SELECT * FROM dimDepartment dd ;

SELECT * FROM dimDate;

SELECT * FROM dimPosition dp ORDER BY id_position;

SELECT * FROM dimCompanyBranch dcb ;

SELECT * FROM factPeople;


SELECT 
	id_person ,
	start_date ,
	end_date 
FROM temp_dimPeople tdp
ORDER BY start_date  ;

-- porovnání end_type vs end_date
SELECT 
	fp.id_person,
	fp.start_date ,
	fp.end_date ,
	--fp.id_branch ,
	--fp.id_dept ,
	--fp.id_position ,
	dp.end_type ,
	dp.end_legal 
FROM factPeople fp 
LEFT JOIN dimPeople dp 
ON fp.id_person = dp.id_person 
WHERE YEAR(fp.start_date) < 2015
GROUP BY fp.id_person , fp.start_date, fp.end_date, dp.end_type , dp.end_legal
ORDER BY fp.start_date  asc;


SELECT 
	id_person ,
	start_date ,
	end_date 
FROM factPeople fp 
WHERE year_note < 2015
GROUP BY id_person, start_date, end_date ;


SELECT 
	id_person,
	nationality 
INTO test
FROM temp_dimPeople ;

SELECT * FROM test;


SELECT DISTINCT
    dp.id_person,
    dp.id_branch,
    dp.start_date,
    dp.end_date,
    dp.employment_num,
    dp.id_position,
    dd.id_dept,
    YEAR(da.date_name) AS year,
    MONTH(da.date_name) AS MONTH
FROM
    temp_dimPeople dp
LEFT JOIN
    temp_dimDepartment dd ON dp.id_position = dd.id_position AND dp.id_branch = dd.id_branch
LEFT JOIN
    dimDate da ON dp.start_date <= da.date_name AND da.date_name <= dp.end_date
ORDER BY
    year, MONTH, dp.id_person ;

