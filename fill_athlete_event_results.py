from sqlalchemy import create_engine, text
 
connection_string = "mysql+pymysql://myuser:mypass123@127.0.0.1:3306/mydb"
 
def main() -> None:
    engine = create_engine(connection_string)
 
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS athlete_event_results (
        id INT AUTO_INCREMENT PRIMARY KEY,
        athlete_name VARCHAR(100) NOT NULL,
        country VARCHAR(100) NOT NULL,
        sport VARCHAR(100) NOT NULL,
        event_name VARCHAR(150) NOT NULL,
        medal VARCHAR(20) NOT NULL,
        event_date DATE NOT NULL
    );
    """
 
    delete_sql = "DELETE FROM athlete_event_results;"
 
    insert_sql = """
    INSERT INTO athlete_event_results
        (athlete_name, country, sport, event_name, medal, event_date)
    VALUES
        (:athlete_name, :country, :sport, :event_name, :medal, :event_date)
    """
 
    rows = [
        {"athlete_name": "Athlete 1", "country": "USA", "sport": "Athletics", "event_name": "100m", "medal": "Gold", "event_date": "2024-07-01"},
        {"athlete_name": "Athlete 2", "country": "Canada", "sport": "Swimming", "event_name": "200m Freestyle", "medal": "Silver", "event_date": "2024-07-02"},
        {"athlete_name": "Athlete 3", "country": "Germany", "sport": "Cycling", "event_name": "Road Race", "medal": "Bronze", "event_date": "2024-07-03"},
        {"athlete_name": "Athlete 4", "country": "France", "sport": "Judo", "event_name": "60kg", "medal": "Gold", "event_date": "2024-07-04"},
        {"athlete_name": "Athlete 5", "country": "Italy", "sport": "Fencing", "event_name": "Foil", "medal": "Silver", "event_date": "2024-07-05"},
        {"athlete_name": "Athlete 6", "country": "Spain", "sport": "Rowing", "event_name": "Single Sculls", "medal": "Bronze", "event_date": "2024-07-06"},
        {"athlete_name": "Athlete 7", "country": "Japan", "sport": "Gymnastics", "event_name": "All-Around", "medal": "Gold", "event_date": "2024-07-07"},
        {"athlete_name": "Athlete 8", "country": "China", "sport": "Diving", "event_name": "10m Platform", "medal": "Silver", "event_date": "2024-07-08"},
        {"athlete_name": "Athlete 9", "country": "Brazil", "sport": "Volleyball", "event_name": "Indoor Finals", "medal": "Bronze", "event_date": "2024-07-09"},
        {"athlete_name": "Athlete 10", "country": "Australia", "sport": "Surfing", "event_name": "Shortboard", "medal": "Gold", "event_date": "2024-07-10"},
        {"athlete_name": "Athlete 11", "country": "USA", "sport": "Athletics", "event_name": "200m", "medal": "Silver", "event_date": "2024-07-11"},
        {"athlete_name": "Athlete 12", "country": "Canada", "sport": "Swimming", "event_name": "100m Butterfly", "medal": "Bronze", "event_date": "2024-07-12"},
        {"athlete_name": "Athlete 13", "country": "Germany", "sport": "Cycling", "event_name": "Time Trial", "medal": "Gold", "event_date": "2024-07-13"},
        {"athlete_name": "Athlete 14", "country": "France", "sport": "Judo", "event_name": "73kg", "medal": "Silver", "event_date": "2024-07-14"},
        {"athlete_name": "Athlete 15", "country": "Italy", "sport": "Fencing", "event_name": "Sabre", "medal": "Bronze", "event_date": "2024-07-15"},
        {"athlete_name": "Athlete 16", "country": "Spain", "sport": "Rowing", "event_name": "Double Sculls", "medal": "Gold", "event_date": "2024-07-16"},
        {"athlete_name": "Athlete 17", "country": "Japan", "sport": "Gymnastics", "event_name": "Rings", "medal": "Silver", "event_date": "2024-07-17"},
        {"athlete_name": "Athlete 18", "country": "China", "sport": "Diving", "event_name": "3m Springboard", "medal": "Bronze", "event_date": "2024-07-18"},
        {"athlete_name": "Athlete 19", "country": "Brazil", "sport": "Volleyball", "event_name": "Beach Finals", "medal": "Gold", "event_date": "2024-07-19"},
        {"athlete_name": "Athlete 20", "country": "Australia", "sport": "Surfing", "event_name": "Longboard", "medal": "Silver", "event_date": "2024-07-20"},
        {"athlete_name": "Athlete 21", "country": "USA", "sport": "Athletics", "event_name": "400m", "medal": "Bronze", "event_date": "2024-07-21"},
        {"athlete_name": "Athlete 22", "country": "Canada", "sport": "Swimming", "event_name": "400m Medley", "medal": "Gold", "event_date": "2024-07-22"},
        {"athlete_name": "Athlete 23", "country": "Germany", "sport": "Cycling", "event_name": "Sprint", "medal": "Silver", "event_date": "2024-07-23"},
        {"athlete_name": "Athlete 24", "country": "France", "sport": "Judo", "event_name": "81kg", "medal": "Bronze", "event_date": "2024-07-24"},
        {"athlete_name": "Athlete 25", "country": "Italy", "sport": "Fencing", "event_name": "Epee", "medal": "Gold", "event_date": "2024-07-25"},
        {"athlete_name": "Athlete 26", "country": "Spain", "sport": "Rowing", "event_name": "Quadruple Sculls", "medal": "Silver", "event_date": "2024-07-26"},
        {"athlete_name": "Athlete 27", "country": "Japan", "sport": "Gymnastics", "event_name": "Vault", "medal": "Bronze", "event_date": "2024-07-27"},
        {"athlete_name": "Athlete 28", "country": "China", "sport": "Diving", "event_name": "Synchronised 10m", "medal": "Gold", "event_date": "2024-07-28"},
        {"athlete_name": "Athlete 29", "country": "Brazil", "sport": "Volleyball", "event_name": "Indoor Semis", "medal": "Silver", "event_date": "2024-07-29"},
        {"athlete_name": "Athlete 30", "country": "Australia", "sport": "Surfing", "event_name": "Mixed Relay", "medal": "Bronze", "event_date": "2024-07-30"},
        {"athlete_name": "Athlete 31", "country": "USA", "sport": "Athletics", "event_name": "800m", "medal": "Gold", "event_date": "2024-08-01"},
        {"athlete_name": "Athlete 32", "country": "Canada", "sport": "Swimming", "event_name": "50m Freestyle", "medal": "Silver", "event_date": "2024-08-02"},
        {"athlete_name": "Athlete 33", "country": "Germany", "sport": "Cycling", "event_name": "Keirin", "medal": "Bronze", "event_date": "2024-08-03"},
        {"athlete_name": "Athlete 34", "country": "France", "sport": "Judo", "event_name": "90kg", "medal": "Gold", "event_date": "2024-08-04"},
        {"athlete_name": "Athlete 35", "country": "Italy", "sport": "Fencing", "event_name": "Team Foil", "medal": "Silver", "event_date": "2024-08-05"},
        {"athlete_name": "Athlete 36", "country": "Spain", "sport": "Rowing", "event_name": "Coxless Pair", "medal": "Bronze", "event_date": "2024-08-06"},
        {"athlete_name": "Athlete 37", "country": "Japan", "sport": "Gymnastics", "event_name": "Parallel Bars", "medal": "Gold", "event_date": "2024-08-07"},
        {"athlete_name": "Athlete 38", "country": "China", "sport": "Diving", "event_name": "Synchronised 3m", "medal": "Silver", "event_date": "2024-08-08"},
        {"athlete_name": "Athlete 39", "country": "Brazil", "sport": "Volleyball", "event_name": "Beach Semis", "medal": "Bronze", "event_date": "2024-08-09"},
        {"athlete_name": "Athlete 40", "country": "Australia", "sport": "Surfing", "event_name": "Team Event", "medal": "Gold", "event_date": "2024-08-10"},
        {"athlete_name": "Athlete 41", "country": "USA", "sport": "Athletics", "event_name": "1500m", "medal": "Silver", "event_date": "2024-08-11"},
        {"athlete_name": "Athlete 42", "country": "Canada", "sport": "Swimming", "event_name": "200m Backstroke", "medal": "Bronze", "event_date": "2024-08-12"},
        {"athlete_name": "Athlete 43", "country": "Germany", "sport": "Cycling", "event_name": "Madison", "medal": "Gold", "event_date": "2024-08-13"},
        {"athlete_name": "Athlete 44", "country": "France", "sport": "Judo", "event_name": "100kg", "medal": "Silver", "event_date": "2024-08-14"},
        {"athlete_name": "Athlete 45", "country": "Italy", "sport": "Fencing", "event_name": "Team Epee", "medal": "Bronze", "event_date": "2024-08-15"},
        {"athlete_name": "Athlete 46", "country": "Spain", "sport": "Rowing", "event_name": "Eight", "medal": "Gold", "event_date": "2024-08-16"},
        {"athlete_name": "Athlete 47", "country": "Japan", "sport": "Gymnastics", "event_name": "Pommel Horse", "medal": "Silver", "event_date": "2024-08-17"},
        {"athlete_name": "Athlete 48", "country": "China", "sport": "Diving", "event_name": "Mixed Team", "medal": "Bronze", "event_date": "2024-08-18"},
        {"athlete_name": "Athlete 49", "country": "Brazil", "sport": "Volleyball", "event_name": "Indoor Bronze Match", "medal": "Gold", "event_date": "2024-08-19"},
        {"athlete_name": "Athlete 50", "country": "Australia", "sport": "Surfing", "event_name": "Open Final", "medal": "Silver", "event_date": "2024-08-20"},
    ]
 
    with engine.begin() as connection:
        connection.execute(text(create_table_sql))
        connection.execute(text(delete_sql))
        connection.execute(text(insert_sql), rows)
 
    print("Таблица athlete_event_results заполнена 50 записями.")


if __name__ == "__main__":
    main()