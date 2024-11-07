CREATE VIEW forestation AS
SELECT 
    fa.country_code,
    fa.country_name,
    fa.year,
    fa.forest_area_sqkm,
    la.total_area_sq_mi,
    -- Convert sq miles to sq kilometers
    la.total_area_sq_mi * 2.59 as total_area_sq_km,
    r.region,
    r.income_group,
    -- Calculate forest percentage using the converted area
    (fa.forest_area_sqkm / (la.total_area_sq_mi * 2.59)) * 100 AS forest_percentage
FROM forest_area fa
JOIN land_area la 
    ON fa.country_code = la.country_code 
    AND fa.year = la.year
JOIN regions r 
    ON fa.country_code = r.country_code;


-- 1. Global Situation

-- a. What was the total forest area (in sq km) of the world in 1990? 
    -- Please keep in mind that you can use the country record denoted as “World" in the region table.
-- Answer: 41282694.9
SELECT 
    forest_area_sqkm as total_forest_area
FROM forest_area
WHERE year = 1990 and country_name = 'World'

-- b. What was the total forest area (in sq km) of the world in 2016? 
--     Please keep in mind that you can use the country record in the table is denoted as “World.”
-- Answer: 39958245.9
SELECT 
    forest_area_sqkm as total_forest_area
FROM forest_area
WHERE year = 2016 and country_name = 'World'

-- c. What was the change (in sq km) in the forest area of the world from 1990 to 2016?
-- Answer: Decrease 1324449
SELECT 
    (SELECT forest_area_sqkm 
     FROM forest_area 
     WHERE year = 1990 AND country_name = 'World')
    -
    (SELECT forest_area_sqkm 
     FROM forest_area 
     WHERE year = 2016 AND country_name = 'World') 
    as forest_area_change

-- d. What was the percent change in forest area of the world between 1990 and 2016?
-- Answer: (1,324,449 / 41,282,694.9) * 100 = 3.21%
SELECT 
    ((SELECT forest_area_sqkm 
      FROM forest_area 
      WHERE year = 1990 AND country_name = 'World')
    -
    (SELECT forest_area_sqkm 
     FROM forest_area 
     WHERE year = 2016 AND country_name = 'World'))
    /
    (SELECT forest_area_sqkm 
     FROM forest_area 
     WHERE year = 1990 AND country_name = 'World') 
    * 100 as forest_area_percent_change

-- e. If you compare the amount of forest area lost between 1990 and 2016, to which country's total area in 2016 is it closest to?
-- Answer: Peru 1279999.99
WITH forest_loss AS (
    SELECT 
        (SELECT forest_area_sqkm 
         FROM forestation 
         WHERE year = 1990 AND country_name = 'World')
        -
        (SELECT forest_area_sqkm 
         FROM forestation 
         WHERE year = 2016 AND country_name = 'World') 
        as lost_forest_area
)
SELECT 
    country_name,
    total_area_sq_km,
    ABS(total_area_sq_km - (SELECT lost_forest_area FROM forest_loss)) as difference
FROM forestation
WHERE year = 2016 
    AND country_name != 'World'
ORDER BY difference
LIMIT 5;

-- 2. Regional Outlook
-- a. What was the percent forest of the entire world in 2016? 
    -- Which region had the HIGHEST percent forest in 2016, and which had the LOWEST, to 2 decimal places?
-- Answer:
    -- Highest region in 2016: Latin America & Caribbean	46.16
    -- World's forest percentage in 2016	31.38
    -- Lowest region in 2016: Middle East & North Africa	2.07

(
    -- World's forest percentage 2016
    SELECT 
        'World''s forest percentage 2016' as category,
        ROUND(CAST(forest_percentage AS NUMERIC), 2) as percentage
    FROM forestation
    WHERE year = 2016 
        AND country_name = 'World'
)

UNION ALL

(
    -- Region with highest forest percentage 2016
    SELECT 
        'Highest region 2016: ' || region,
        ROUND(CAST((SUM(forest_area_sqkm) / SUM(total_area_sq_km)) * 100 AS NUMERIC), 2) as percentage
    FROM forestation
    WHERE year = 2016 
        AND region IS NOT NULL
    GROUP BY region
    ORDER BY percentage DESC
    LIMIT 1
)

UNION ALL

(
    -- Region with lowest forest percentage 2016
    SELECT 
        'Lowest region 2016: ' || region,
        ROUND(CAST((SUM(forest_area_sqkm) / SUM(total_area_sq_km)) * 100 AS NUMERIC), 2) as percentage
    FROM forestation
    WHERE year = 2016 
        AND region IS NOT NULL
    GROUP BY region
    ORDER BY percentage ASC
    LIMIT 1
);


-- b. What was the percent forest of the entire world in 1990? 
    -- Which region had the HIGHEST percent forest in 1990, and which had the LOWEST, to 2 decimal places?
-- Answer:
    -- World's forest percentage 1990	32.42
    -- Highest region 1990: Latin America & Caribbean	51.03
    -- Lowest region 1990: Middle East & North Africa	1.78

(
    -- World's forest percentage 1990
    SELECT 
        'World''s forest percentage 1990' as category,
        ROUND(CAST(forest_percentage AS NUMERIC), 2) as percentage
    FROM forestation
    WHERE year = 1990 
        AND country_name = 'World'
)

UNION ALL

(
    -- Region with highest forest percentage 1990
    SELECT 
        'Highest region 1990: ' || region,
        ROUND(CAST((SUM(forest_area_sqkm) / SUM(total_area_sq_km)) * 100 AS NUMERIC), 2) as percentage
    FROM forestation
    WHERE year = 1990 
        AND region IS NOT NULL
    GROUP BY region
    ORDER BY percentage DESC
    LIMIT 1
)

UNION ALL

(
    -- Region with lowest forest percentage 1990
    SELECT 
        'Lowest region 1990: ' || region,
        ROUND(CAST((SUM(forest_area_sqkm) / SUM(total_area_sq_km)) * 100 AS NUMERIC), 2) as percentage
    FROM forestation
    WHERE year = 1990 
        AND region IS NOT NULL
    GROUP BY region
    ORDER BY percentage ASC
    LIMIT 1
);

-- c. Based on the table you created, which regions of the world DECREASED in forest area from 1990 to 2016?
-- Answer:
    -- region	forest_percent_1990	forest_percent_2016	decrease_1990_2016
    -- Latin America & Caribbean	51.03	46.16	4.8679076671464045
    -- Sub-Saharan Africa	30.67	28.79	1.885957105954116
    -- World	32.42	31.38	1.0466325932594138
    -- Middle East & North Africa	1.78	2.07	-0.2930242440214885
    -- North America	35.65	36.04	-0.38818196724225373
    -- East Asia & Pacific	25.78	26.36	-0.5825811027312291
    -- Europe & Central Asia	37.28	38.04	-0.7574817468495922
    -- South Asia	16.51	17.51	-0.9950964067324257

WITH table_1 AS(
SELECT 
    a.region,
    SUM(a.forest_area_sqkm) region_forest_1990,
    SUM(a.total_area_sq_km) region_area_1990,
    SUM(b.forest_area_sqkm) region_forest_2016,
    SUM(b.total_area_sq_km) region_area_2016
FROM  forestation a, forestation b
WHERE  
    a.year = '1990' AND a.country_code != 'World' AND
    b.year = '2016' AND b.country_code != 'World'
    AND a.region = b.region
GROUP  BY a.region)
SELECT 
    table_1.region,
    ROUND(CAST((region_forest_1990/ region_area_1990) * 100 AS NUMERIC), 2) AS forest_percent_1990,
    ROUND(CAST((region_forest_2016/ region_area_2016) * 100 AS NUMERIC), 2) AS forest_percent_2016,
    (region_forest_1990 / region_area_1990) * 100  - (region_forest_2016 / region_area_2016) * 100 AS decrease_1990_2016
FROM table_1
ORDER BY decrease_1990_2016 DESC

-- 3. Country-Level Detail
-- a. Which 5 countries saw the largest amount decrease in forest area from 1990 to 2016? What was the difference in forest area for each?
-- Answer:
    -- country_name	region	forest_area_sqkm_2016	forest_area_sqkm_1990	difference
    -- Brazil	Latin America & Caribbean	4925540.00	5467050.00	-541510.00
    -- Indonesia	East Asia & Pacific	903256.02	1185450.00	-282193.98
    -- Myanmar	East Asia & Pacific	284946.00	392180.00	-107234.00
    -- Nigeria	Sub-Saharan Africa	65834.00	172340.00	-106506.00
    -- Tanzania	Sub-Saharan Africa	456880.00	559200.00	-102320.00


SELECT
    fa_current.country_name,
    fa_current.region,  -- Added region for more context
    ROUND(CAST(fa_current.forest_area_sqkm AS NUMERIC), 2) as forest_area_sqkm_2016,
    ROUND(CAST(fa_previous.forest_area_sqkm AS NUMERIC), 2) as forest_area_sqkm_1990,
    ROUND(CAST(fa_current.forest_area_sqkm - fa_previous.forest_area_sqkm AS NUMERIC), 2) as difference
FROM 
    forestation AS fa_current
JOIN 
    forestation AS fa_previous
ON 
    (fa_current.year = '2016' AND fa_previous.year = '1990'
    AND fa_current.country_name = fa_previous.country_name)
WHERE 
    fa_current.forest_area_sqkm - fa_previous.forest_area_sqkm IS NOT NULL
    AND fa_current.country_name != 'World'
ORDER BY difference ASC
LIMIT 5;

-- b. Which 5 countries saw the largest percent decrease in forest area from 1990 to 2016? What was the percent change to 2 decimal places for each?
-- Answer:
    -- country_name	region	forest_area_sqkm_2016	forest_area_sqkm_1990	pct_change
    -- Togo	Sub-Saharan Africa	1682.00	6850.00	-75.45
    -- Nigeria	Sub-Saharan Africa	65834.00	172340.00	-61.80
    -- Uganda	Sub-Saharan Africa	19418.00	47510.00	-59.13
    -- Mauritania	Sub-Saharan Africa	2210.00	4150.00	-46.75
    -- Honduras	Latin America & Caribbean	44720.00	81360.00	-45.03

SELECT
    fa_current.country_name,
    fa_current.region,
    ROUND(CAST(fa_current.forest_area_sqkm AS NUMERIC), 2) as forest_area_sqkm_2016,
    ROUND(CAST(fa_previous.forest_area_sqkm AS NUMERIC), 2) as forest_area_sqkm_1990,
    ROUND(CAST(((fa_current.forest_area_sqkm - fa_previous.forest_area_sqkm) / fa_previous.forest_area_sqkm * 100) AS NUMERIC), 2) as pct_change
FROM 
    forestation AS fa_current
JOIN 
    forestation AS fa_previous
ON 
    (fa_current.year = '2016' AND fa_previous.year = '1990'
    AND fa_current.country_name = fa_previous.country_name)
WHERE 
    fa_previous.forest_area_sqkm IS NOT NULL
    AND fa_current.forest_area_sqkm IS NOT NULL
    AND fa_current.country_name != 'World'
    AND fa_previous.forest_area_sqkm > 0  -- Avoid division by zero
ORDER BY pct_change ASC
LIMIT 5;

-- c. If countries were grouped by percent forestation in quartiles, which group had the most countries in it in 2016?
-- Answer:
    -- quartile	number_of_countries
    -- 0-25%	85
    -- 25-50%	72
    -- 50-75%	38
    -- 75-100%	9

WITH quartile_data AS (
    SELECT 
        country_name,
        region,
        forest_percentage,
        CASE
            WHEN forest_percentage <= 25 THEN '0-25%'
            WHEN forest_percentage <= 50 THEN '25-50%'
            WHEN forest_percentage <= 75 THEN '50-75%'
            ELSE '75-100%'
        END AS quartile
    FROM forestation
    WHERE year = 2016 
        AND country_name != 'World'
        AND forest_percentage IS NOT NULL
)
SELECT 
    quartile,
    COUNT(*) as number_of_countries
FROM quartile_data
GROUP BY quartile
ORDER BY quartile;


-- d. List all of the countries that were in the 4th quartile (percent forest > 75%) in 2016.
-- Answer:
    -- country_name	region	forest_percentage
    -- Suriname	Latin America & Caribbean	98.26
    -- Micronesia, Fed. Sts.	East Asia & Pacific	91.86
    -- Gabon	Sub-Saharan Africa	90.04
    -- Seychelles	Sub-Saharan Africa	88.41
    -- Palau	East Asia & Pacific	87.61
    -- American Samoa	East Asia & Pacific	87.50
    -- Guyana	Latin America & Caribbean	83.90
    -- Lao PDR	East Asia & Pacific	82.11
    -- Solomon Islands	East Asia & Pacific	77.86

SELECT 
    country_name,
    region,
    ROUND(CAST(forest_percentage AS NUMERIC), 2) as forest_percentage
FROM forestation
WHERE year = 2016 
    AND forest_percentage > 75
    AND country_name != 'World'
ORDER BY forest_percentage DESC;


-- e. How many countries had a percent forestation higher than the United States in 2016?
-- Answer: 94

SELECT COUNT(*) as countries_with_higher_percentage
FROM forestation
WHERE year = 2016
    AND country_name != 'World'
    AND country_name != 'United States'
    AND forest_percentage > (
        SELECT forest_percentage
        FROM forestation
        WHERE year = 2016 
            AND country_name = 'United States'
    );
