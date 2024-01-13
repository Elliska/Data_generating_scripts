IF OBJECT_ID('dimCalendar', 'U') IS NOT NULL
    DROP TABLE dimCalendar;

CREATE TABLE dimCalendar (
    ID_date INT PRIMARY KEY,
    date DATE,
    date_of_week NVARCHAR(20),
    quarter INT,
    holiday NVARCHAR(1),
    holiday_name NVARCHAR(50),
    season NVARCHAR(20),
    week_num INT
);

DECLARE @startDate DATE = '2000-01-01';
DECLARE @endDate DATE = '2025-12-31';
DECLARE @currentDate DATE = @startDate;

WHILE @currentDate <= @endDate
BEGIN
    INSERT INTO dimCalendar (
        ID_date,
        date,
        date_of_week,
        quarter,
        holiday,
        holiday_name,
        season,
        week_num
    )
    VALUES (
        CONVERT(INT, FORMAT(@currentDate, 'yyyyMMdd')),
        @currentDate,
        DATENAME(dw, @currentDate),
        DATEPART(q, @currentDate),
        CASE WHEN MONTH(@currentDate) = 12 AND DAY(@currentDate) = 24 THEN 'Y'  -- Vánoce
             WHEN MONTH(@currentDate) = 12 AND DAY(@currentDate) = 31 THEN 'Y'  -- Silvestr
             ELSE 'N' END,
        CASE WHEN MONTH(@currentDate) = 1 AND DAY(@currentDate) = 1 THEN 'Nový rok'
             WHEN MONTH(@currentDate) = 5 AND DAY(@currentDate) = 1 THEN 'Svátek práce'
             -- ... další české svátky
             ELSE NULL END,
        CASE WHEN MONTH(@currentDate) IN (12, 1, 2) THEN 'Zima'
             WHEN MONTH(@currentDate) IN (3, 4, 5) THEN 'Jaro'
             WHEN MONTH(@currentDate) IN (6, 7, 8) THEN 'Léto'
             WHEN MONTH(@currentDate) IN (9, 10, 11) THEN 'Podzim'
             ELSE NULL END,
        DATEPART(wk, @currentDate)
    );

    SET @currentDate = DATEADD(DAY, 1, @currentDate);
END;
