import json
from flask import Flask
from db import Database
from flask_cors import CORS
import requests

db = Database()
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


# @app.route('/continents')
# def continents():
#     sql = f'''SELECT DISTINCT continent
#               FROM country'''
#     cursor = db.get_conn().cursor(dictionary=True)
#     cursor.execute(sql)
#     result = cursor.fetchall()
#     return json.dumps(result)


# @app.route('/countries/<continent>')    
# def countries_by_continent(continent):
#     sql = f'''SELECT iso_country, name
#               FROM country
#               WHERE continent = %s'''
#     cursor = db.get_conn().cursor(dictionary=True)
#     cursor.execute(sql, (continent,))
#     result = cursor.fetchall()
#     return json.dumps(result)


# @app.route('/airports/<country>')
# def airports_by_country(country):
#     sql = f'''SELECT ident, name, latitude_deg, longitude_deg
#               FROM airport
#               WHERE iso_country = %s'''
#     cursor = db.get_conn().cursor(dictionary=True)
#     cursor.execute(sql, (country,))
#     result = cursor.fetchall()
#     return json.dumps(result)


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
    sql = "SELECT * FROM questions limit 5;"

    cursor = db.get_conn().cursor(dictionary=True)
    cursor.execute(sql, ())
    result = cursor.fetchall()
    return json.dumps(result)


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)

# inputs and prints are moved to web page