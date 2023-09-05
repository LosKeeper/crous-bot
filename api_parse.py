import pycurl
import certifi
from io import BytesIO

import json


def EN_to_FR(month):
    """Convert the english month to french month

    Args:
        month (str): The english month

    Returns:
        str: The french month
    """
    months = {
        "January": "janvier",
        "February": "février",
        "March": "mars",
        "April": "avril",
        "May": "mai",
        "June": "juin",
        "July": "juillet",
        "August": "août",
        "September": "septembre",
        "October": "octobre",
        "November": "novembre",
        "December": "décembre"
    }

    return months[month]


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


def print_illkirch(date, json_illkirch):
    # Get the corrsponding index of the date
    index = 0
    for i in range(len(json_illkirch)):
        if date in json_illkirch[i]["date"]:
            index = i
            break

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
    index = 0
    for i in range(len(json_cronenbourg)):
        if date in json_cronenbourg[i]["date"]:
            index = i
            break

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
    index = 0
    for i in range(len(json_paul_appell)):
        if date in json_paul_appell[i]["date"]:
            index = i
            break

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
