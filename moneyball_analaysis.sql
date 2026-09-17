USE FootballMoneyball;

SELECT * 
FROM dbo.Players_Stats;

-- 1. דירוג שחקנים בתוך כל עמדה
SELECT 
    Player_Name,
    Position,
    Club,
    Goals,
    ROW_NUMBER() OVER (PARTITION BY Position ORDER BY Goals DESC) AS Position_Rank
FROM dbo.Players_Stats;

-- 2. השוואת שחקן מול ממוצע ה-xG בעמדה שלו
WITH PositionAvg AS (
    SELECT 
        Position,
        AVG(xG) AS Avg_xG
    FROM dbo.Players_Stats
    GROUP BY Position
)
SELECT 
    p.Player_Name,
    p.Position,
    p.xG,
    ROUND(pa.Avg_xG, 2) AS Position_Avg_xG,
    ROUND(p.xG - pa.Avg_xG, 2) AS Above_Average_xG
FROM dbo.Players_Stats p
JOIN PositionAvg pa ON p.Position = pa.Position
ORDER BY Above_Average_xG DESC;

-- 3. איתור "מציאות שוק" (שחקנים עד גיל 26, מעורבות 10+ בשערים, מחיר מתחת ל-100 מיל')
SELECT 
    Player_Name,
    Age,
    Club,
    Market_Value_EUR,
    Contract_Expires,
    (Goals + Assists) AS Total_Contributions
FROM dbo.Players_Stats
WHERE Age <= 26 
  AND (Goals + Assists) >= 10
  AND Market_Value_EUR < 100000000
ORDER BY Market_Value_EUR ASC;