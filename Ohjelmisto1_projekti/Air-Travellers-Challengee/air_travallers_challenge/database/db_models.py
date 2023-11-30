from geopy.distance import geodesic
from database import db_connection

connection = db_connection.connect_to_database()

# GAME CLASS SQL QUERIES
# SOURCE: FROM CHATGPT
def get_closest_airports(current_airport):

    # fetch coordinates for current airport
    sql = 'SELECT latitude_deg, longitude_deg FROM airport WHERE ident = %s ;'
    lat, lon = coords = db_connection.fetch_one(connection, sql, current_airport)

    closest_airports_sql = f'''
    SELECT name, ident, iso_country, id, latitude_deg, longitude_deg,
            6371 * ACOS(
                COS(RADIANS({lat})) * COS(RADIANS(latitude_deg)) 
                * COS(RADIANS({lon} - longitude_deg)) +
                SIN(RADIANS({lat})) * SIN(RADIANS(latitude_deg))
            ) AS Distance_KM
        FROM
            airport
        WHERE
            type = "large_airport"
        ORDER BY
            Distance_KM ASC
        LIMIT 11;
    '''

    closest_airports_list = db_connection.fetch_data(connection, closest_airports_sql, ())
    return closest_airports_list

# PLAYER CLASS SQL QUERIES

def get_airports_iso_sql(iso):
    get_airports_iso_sql = 'SELECT * FROM airport WHERE iso_country = %s and type = "large_airport" LIMIT 10; '

    airports = db_connection.fetch_data(connection, get_airports_iso_sql, iso)

    return airports

def insert_player_sql(params):
    insert_player_sql = "INSERT INTO player (name, avatar_id, budget, distance_traveled, current_airport, co2_consumed) VALUES (%s, %s, %s, %s, %s, %s); "

    db_connection.execute_query(connection, insert_player_sql, (params))

    connection.commit()
    cursor = connection.cursor()

    cursor.execute("SELECT LAST_INSERT_ID()")
    row = cursor.fetchone()
    last_inserted_id = row[0]
    

    return last_inserted_id
    print('Added new player to database')

# QUESTION CLASS SQL QUERIES

def get_questions_avatar_sql(avatar_id):
    get_questions_sql = "SELECT * FROM questions WHERE avatar_id = %s;"

    questions = db_connection.fetch_data(connection, get_questions_sql, avatar_id)

    return questions

def update_points():
    update_points = "UPDATE game SET points = points + 100 WHERE name = %s; "
    cursor = connection.cursor
    cursor.execute(update_points)

def calculate_co2_used(old, new):
    coords_sql = "SELECT latitude_deg, longitude_deg FROM airport WHERE ident = %s;"

    
    cursor = connection.cursor()
    cursor.execute(coords_sql, (old,))
    coords1 = cursor.fetchone()

    cursor.execute(coords_sql, (new,))
    coords2 = cursor.fetchone()

    distance = geodesic(coords1, coords2).kilometers

    co2_calculation = (distance/40)

    return co2_calculation, distance


