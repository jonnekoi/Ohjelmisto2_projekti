import json
from flask import Flask
from db import Database
from flask_cors import CORS

db = Database()
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# ROUTES
@app.route('/airport/<icao>')
def airport(icao):
    sql = f'''SELECT name, latitude_deg, longitude_deg
              FROM airport
              WHERE ident=%s'''
    cursor = db.get_conn().cursor(dictionary=True)
    cursor.execute(sql, (icao,))
    result = cursor.fetchone()
    return json.dumps(result)

@app.route('/airport/closest/<lat>/<lon>')
def get_closest_airports(lat, lon):
    sql = f'''
        SELECT name, ident, iso_country, id, latitude_deg, longitude_deg,
            6371 * ACOS(
                COS(RADIANS(%s)) * COS(RADIANS(latitude_deg)) 
                * COS(RADIANS(%s - longitude_deg)) +
                SIN(RADIANS(%s)) * SIN(RADIANS(latitude_deg))
            ) AS Distance_KM
        FROM
            airport
        WHERE
            type = "large_airport"
        ORDER BY
            Distance_KM ASC
        LIMIT 11;
    '''
    cursor = db.get_conn().cursor(dictionary=True)
    cursor.execute(sql, (lat, lon, lat))
    result = cursor.fetchall()
    return json.dumps(result)

@app.route('/questions')
def get_questions_avatar_sql():
    sql = "SELECT * FROM questions;"
    cursor = db.get_conn().cursor(dictionary=True)
    cursor.execute(sql, ())
    result = cursor.fetchall()
    return json.dumps(result)

@app.route('/scoreboard')
def get_scoreboard():
    sql = 'SELECT * FROM scoreboard ORDER BY `co2_emissions` ASC LIMIT 5    ;'
    cursor = db.get_conn().cursor(dictionary=True)
    cursor.execute(sql, ())
    result = cursor.fetchall()
    return json.dumps(result)

@app.route('/player/setScore/<name>/<co2>/<distance>')
def set_player_score(name, co2, distance):
    sql = 'INSERT INTO scoreboard (player, co2_emissions, distance) VALUES (%s, %s, %s);' 
    cursor = db.get_conn().cursor(dictionary=True)
    cursor.execute(sql, (name, co2, distance))
    result = cursor.lastrowid
    return json.dumps(result)

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)
