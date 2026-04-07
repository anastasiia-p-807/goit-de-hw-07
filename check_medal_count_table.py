from sqlalchemy import create_engine, text
import pandas as pd

connection_string = "mysql+pymysql://myuser:mypass123@127.0.0.1:3306/mydb"
engine = create_engine(connection_string)

with engine.connect() as connection:
    query = text(f"SELECT * FROM medal_counts;")
    result = connection.execute(query)
    
    rows = result.fetchall()

df = pd.DataFrame(rows, columns=result.keys())
print(df)