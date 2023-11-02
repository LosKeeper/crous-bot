import pycurl
import certifi
from io import BytesIO
from datetime import datetime

import json


# French months dict
month_dict = {1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin",
              7: "Juillet", 8: "Août", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"}


def format_date_to_french(date_str):
    # Convertir la date du format "YYYY-MM-DD" en un objet datetime
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")

    # Obtenir le jour, le mois et l'année
    day = date_obj.day
    month = month_dict[date_obj.month]
    year = date_obj.year

    # Formater la date en français
    formatted_date = f"{day} {month} {year}"

    return formatted_date


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


def print_illkirch(date, json_illkirch):
    # Get the corrsponding index of the date
    index = get_date_index(date, json_illkirch)

    # Make the string to return
    string = "Entrées:\n"
    for plate in json_illkirch[index]["Déjeuner"]["ENTREES"]:
        string += "\t"+plate+"\n"

    string += "\nMenu du jour:\n"
    for plate in json_illkirch[index]["Déjeuner"]["MENU DU JOUR"]:
        string += "\t"+plate+"\n"

    string += "\nMenu végétarien:\n"
    for plate in json_illkirch[index]["Déjeuner"]["MENU VEGETARIEN"]:
        string += "\t"+plate+"\n"

    string += "\nPole pates:\n"
    for plate in json_illkirch[index]["Déjeuner"]["POLE PATES"]:
        string += "\t"+plate+"\n"

    string += "\nGrill:\n"
    for plate in json_illkirch[index]["Déjeuner"]["GRILL"]:
        string += "\t"+plate+"\n"

    string += "\nDesserts:\n"
    for plate in json_illkirch[index]["Déjeuner"]["DESSERTS"]:
        string += "\t"+plate+"\n"

    return string


def print_cronenbourg(date, json_cronenbourg):
    # Get the corrsponding index of the date
    index = get_date_index(date, json_cronenbourg)

    # Make the string to return
    string = "Grillade:\n"
    for plate in json_cronenbourg[index]["Déjeuner"]["Grillade"]:
        string += "\t"+plate+"\n"

    string += "\nPlat du jour:\n"
    for plate in json_cronenbourg[index]["Déjeuner"]["Plat du jour"]:
        string += "\t"+plate+"\n"

    string += "\nVégétarien:\n"
    for plate in json_cronenbourg[index]["Déjeuner"]["Végétarien"]:
        string += "\t"+plate+"\n"

    string += "\nExtension:\n"
    for plate in json_cronenbourg[index]["Déjeuner"]["Extension"]:
        string += "\t"+plate+"\n"

    return string


def print_paul_appell(date, json_paul_appell):
    # Get the corrsponding index of the date
    index = get_date_index(date, json_paul_appell)

    # Make the string to return
    string = "Déjeuner:\n"
    string += "\n - Pôle végétal:\n"
    for plate in json_paul_appell[index]["Déjeuner"]["Pôle végétal"]:
        string += "\t"+plate+"\n"

    string += "\n - Flam and Co:\n"
    for plate in json_paul_appell[index]["Déjeuner"]["Flam and Co"]:
        string += "\t"+plate+"\n"

    string += "\n - Plat du jour:\n"
    for plate in json_paul_appell[index]["Déjeuner"]["Plat du jour"]:
        string += "\t"+plate+"\n"

    string += "\n - Annexe:\n"
    for plate in json_paul_appell[index]["Déjeuner"]["Annexe"]:
        string += "\t"+plate+"\n"

    string += "\nDîner:\n"
    string += "\n - Pôle végétal:\n"
    for plate in json_paul_appell[index]["Dîner"]["Pôle végétal"]:
        string += "\t"+plate+"\n"

    string += "\n - Flam and Co:\n"
    for plate in json_paul_appell[index]["Dîner"]["Flam and Co"]:
        string += "\t"+plate+"\n"

    string += "\n - Plat du jour:\n"
    for plate in json_paul_appell[index]["Dîner"]["Plat du jour"]:
        string += "\t"+plate+"\n"

    string += "\n - Annexe:\n"
    for plate in json_paul_appell[index]["Dîner"]["Annexe"]:
        string += "\t"+plate+"\n"

    return string
