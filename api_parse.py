import pycurl
import certifi
from io import BytesIO
from datetime import datetime, timedelta

import json


# French months dict
month_dict = {1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin",
              7: "Juillet", 8: "Août", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"}


def format_date_to_french(date_str):
    """Format a date string to french

    Need month_dict to be defined

    Args:
        date_str (str): The date string in YYYY-MM-DD format

    Returns:
        str: The date string in french
    """
    # Convert the date string to a datetime object
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    day = date_obj.day
    month = month_dict[date_obj.month]
    year = date_obj.year

    # Format the date
    formatted_date = f"{day} {month} {year}"

    return formatted_date


def get_date():
    """Get the date in YYYY-MM-DD format, if the time is after 14h, add a day to the date

    Returns:
        str: The date in YYYY-MM-DD format
    """
    # Get the date
    current_date = datetime.now()

    # If the time is after 14h, add a day to the date
    if current_date.hour >= 14:
        current_date += timedelta(days=1)

    # Format the date to YYYY-MM-DD
    current_date_str = current_date.strftime("%Y-%m-%d")

    return current_date_str


def get_html(URL):
    """Get the html code of the menu webpage

    Returns:
        str: The html code
    """

    # Create a buffer to store the response
    buffer = BytesIO()

    # Create a pycurl object
    c = pycurl.Curl()

    # Set URL value
    c.setopt(c.URL, URL)

    # Write bytes that are utf-8 encoded
    c.setopt(c.WRITEDATA, buffer)

    # Set the User-Agent
    c.setopt(c.USERAGENT, 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')

    # Use certifi to verify the certificate
    c.setopt(c.CAINFO, certifi.where())

    # Perform a file transfer
    c.perform()

    # End curl session
    c.close()

    # Decode the buffer
    body = buffer.getvalue().decode('utf-8')

    return body


def json_to_dict(string):
    """Convert a json string to a dict

    Args:
        string (str): The json string

    Returns:
        dict: The dict
    """
    return json.loads(string)


def get_date_index(date, json):
    """Get the index of the date in the json

    Args:
        date (str): The date in YYYY-MM-DD format
        json (dict): The json

    Returns:
        int: The index
    """
    index = 0
    for i in range(len(json)):
        if date == json[i]["date"]:
            index = i
            break

    return index


def print_lunch_diner(date, json_data):
    """Print the menu of the RU for lunch and diner

    Args:
        date (str): The date in YYYY-MM-DD format
        json_cronenbourg (JSON): The json of the RU

    Returns:
        str: The string to print
    """

    # Get the corrsponding index of the date
    index = get_date_index(date, json_data)

    # Get the categories from the json
    categories = json_data[index]["Déjeuner"].keys()
    meals = ["Déjeuner"]
    if "Dîner" in json_data[index].keys():
        meals.append("Dîner")

    # Make the string to return
    string = ""
    for meal in meals:
        string += f"\n{meal.capitalize().replace('é','e').replace('î','i')}:\n"
        for category in categories:
            string += f"\n - {category.capitalize().replace('é','e')}:\n"
            for plate in json_data[index][meal][category]:
                string += f"\t{plate}\n"

    return string
