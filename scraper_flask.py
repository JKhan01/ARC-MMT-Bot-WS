from flask import redirect,render_template,request, session
from flask import Flask
from scraper_helper import get_flight_data
# import requests

app = Flask(__name__)

city_to_airport = {"Delhi": "DEL",
                    "Mumbai": "BOM",
                    "Pune": "PNQ",
                    "Aurangabad": "IXU",
                    "Chennai": "MAA",
                    "Kolkata": "CCU"}

@app.route("/fetch_details/<source>/<destination>/<trip>/<date>")
def api_post(source,destination,trip,date):
    for i in city_to_airport:
        if i.lower() == source.lower():
            src = city_to_airport[i]
        elif i.lower() == destination.lower():
            dest = city_to_airport[i]
        else:
            pass
    if trip == "Return":
        trip_type = "R"
        for i in city_to_airport:
            if i.lower() == source.lower():
                src_ret = dest
            elif i.lower() == destination.lower():
                dest_ret = src
            else:
                pass
    else:
        trip_type = "O"

    lang = "eng"
    country_code = "IN"
    cabin_class = "E"
    is_international = "false"
    passenger_type = f"A-1_C-0_I-0"

    travel_date= str(date.replace("-","/"))

    data = get_flight_data(source=src,destination=dest,travel_date=travel_date,journey_type="O")

    return data

@app.route("/")
def check_site():
    return "site is up"
if __name__ == "__main__":
    app.run(debug=False, port=5000, host="0.0.0.0")
