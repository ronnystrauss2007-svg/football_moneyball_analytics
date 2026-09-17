import pyodbc
import pandas as pd

# 1. התחברות ל-SQL Server
server = 'localhost'
database = 'master' 

conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
conn = pyodbc.connect(conn_str)
conn.autocommit = True
cursor = conn.cursor()

# 2. יצירת מסד הנתונים במידה ולא קיים
cursor.execute("IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'FootballMoneyball') CREATE DATABASE FootballMoneyball;")
cursor.close()
conn.close()

# 3. התחברות למסד הנתונים FootballMoneyball
conn_db_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE=FootballMoneyball;Trusted_Connection=yes;'
conn_db = pyodbc.connect(conn_db_str)
cursor_db = conn_db.cursor()

# 4. מחיקת הטבלה הישנה (אם קיימת) ויצירתה מחדש
cursor_db.execute("IF OBJECT_ID('dbo.Players_Stats', 'U') IS NOT NULL DROP TABLE dbo.Players_Stats;")

create_table_query = """
CREATE TABLE dbo.Players_Stats (
    Player_ID INT IDENTITY(1,1) PRIMARY KEY,
    Player_Name VARCHAR(100),
    Age INT,
    Nationality VARCHAR(50),
    Position VARCHAR(20),
    Club VARCHAR(50),
    League VARCHAR(50),
    Market_Value_EUR DECIMAL(15, 2),
    Contract_Expires INT,
    Matches_Played INT,
    Minutes_Played INT,
    Goals INT,
    Assists INT,
    xG FLOAT,
    xA FLOAT,
    Key_Passes INT,
    Tackles_Won INT,
    Interceptions INT
);
"""
cursor_db.execute(create_table_query)

# 5. נתונים מורחבים עבור פרויקט ה-Moneyball
data = [
    # חלוצים (ST / CF)
    ('Erling Haaland', 24, 'Norway', 'ST', 'Manchester City', 'Premier League', 180000000, 2027, 25, 2100, 22, 5, 20.4, 3.2, 28, 8, 4),
    ('Viktor Gyökeres', 26, 'Sweden', 'ST', 'Sporting CP', 'Liga Portugal', 65000000, 2028, 24, 2050, 19, 7, 17.8, 4.1, 35, 12, 6),
    ('Alexander Isak', 25, 'Sweden', 'ST', 'Newcastle United', 'Premier League', 75000000, 2028, 22, 1850, 15, 3, 13.9, 2.5, 22, 9, 5),
    ('Lautaro Martínez', 27, 'Argentina', 'ST', 'Inter Milan', 'Serie A', 110000000, 2029, 26, 2150, 18, 4, 16.5, 3.0, 31, 10, 7),
    ('Jonathan David', 25, 'Canada', 'ST', 'Lille', 'Ligue 1', 45000000, 2025, 25, 2000, 14, 4, 12.8, 2.9, 26, 7, 3),
    
    # קשרים (CAM / CM)
    ('Jude Bellingham', 21, 'England', 'CAM', 'Real Madrid', 'La Liga', 180000000, 2029, 23, 1950, 9, 8, 8.7, 6.5, 48, 22, 14),
    ('Florian Wirtz', 21, 'Germany', 'CAM', 'Bayer Leverkusen', 'Bundesliga', 130000000, 2027, 24, 1980, 10, 11, 8.2, 9.4, 62, 18, 12),
    ('Cole Palmer', 22, 'England', 'CAM', 'Chelsea', 'Premier League', 90000000, 2030, 25, 2100, 13, 8, 11.5, 7.1, 52, 15, 9),
    ('Martin Ødegaard', 25, 'Norway', 'CAM', 'Arsenal', 'Premier League', 110000000, 2028, 24, 2020, 7, 9, 6.8, 8.2, 68, 20, 11),
    
    # בלמים (CB)
    ('William Saliba', 23, 'France', 'CB', 'Arsenal', 'Premier League', 80000000, 2027, 24, 2160, 2, 1, 1.5, 0.4, 8, 42, 28),
    ('Alessandro Bastoni', 25, 'Italy', 'CB', 'Inter Milan', 'Serie A', 70000000, 2028, 23, 1920, 1, 3, 1.1, 2.1, 19, 38, 25),
    ('Nico Schlotterbeck', 25, 'Germany', 'CB', 'Borussia Dortmund', 'Bundesliga', 40000000, 2027, 22, 1890, 2, 2, 1.8, 1.2, 12, 45, 31)
]

columns = [
    'Player_Name', 'Age', 'Nationality', 'Position', 'Club', 'League',
    'Market_Value_EUR', 'Contract_Expires', 'Matches_Played', 'Minutes_Played',
    'Goals', 'Assists', 'xG', 'xA', 'Key_Passes', 'Tackles_Won', 'Interceptions'
]

df = pd.DataFrame(data, columns=columns)

# 6. הזרמת הנתונים ל-SQL Server
insert_query = """
INSERT INTO dbo.Players_Stats (
    Player_Name, Age, Nationality, Position, Club, League,
    Market_Value_EUR, Contract_Expires, Matches_Played, Minutes_Played,
    Goals, Assists, xG, xA, Key_Passes, Tackles_Won, Interceptions
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

for index, row in df.iterrows():
    cursor_db.execute(insert_query, tuple(row))

conn_db.commit()
print("הטבלה עודכנה בהצלחה! 12 שחקנים הוזרמו ל-SQL Server.")
cursor_db.close()
conn_db.close()
