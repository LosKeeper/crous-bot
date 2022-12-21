import pycurl
import certifi
from io import BytesIO
from datetime import datetime
import pytz

from config import URL_PAUL_APPELL
# Use to convert the time
delta_time = 1


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


def parse_html(buffer):
    """Parse the html code to get the menu

    Args:
        buffer (str): The html code

    Returns:
        str: The menu formatted from the current day
    """

    # Get the date
    day = datetime.now(pytz.timezone('Europe/Paris')).strftime("%d")

    if day[0] == "0":
        day = day[1]

    month = datetime.now(pytz.timezone('Europe/Paris')).strftime("%B")
    month = EN_to_FR(month)

    if "Cronenbourg" in buffer:
        # If the time is after 14h, the menu is for the next day
        hour = datetime.now(pytz.timezone('Europe/Paris')).strftime("%H")
        if int(hour)+delta_time >= 14:
            day_int = int(day)+1
        else:
            day_int = int(day)

        date = "%s" % day_int + " "+month
        return Cronenbourg(buffer, date)
    elif "Paul Appell" in buffer:
        # If the time is after 14h, the menu is for the next day
        hour = datetime.now(pytz.timezone('Europe/Paris')).strftime("%H")
        day_int = int(day)

        date = "%s" % day_int + " "+month
        return Paul_Appell(buffer, date)
    else:
        # If the time is after 14h, the menu is for the next day
        hour = datetime.now(pytz.timezone('Europe/Paris')).strftime("%H")
        if int(hour)+delta_time >= 14:
            day_int = int(day)+1
        else:
            day_int = int(day)

        date = "%s" % day_int + " "+month
        return Illkirch(buffer, date)


def Illkirch(buffer, date):
    # Find the html element that concern the menu of the day
    menu = buffer.find(date)
    buffer = buffer[menu:]

    # Get the menu of the lunch
    menu = buffer.find("Déjeuner")
    buffer = buffer[menu+45:]

    # Get the end of the menu
    end = buffer.find("Origin")
    buffer = buffer[:end]

    # Remove the html tags
    buffer = buffer.replace("<span class=\"name\">",
                            "")
    buffer = buffer.replace("</span>", " : \n")
    buffer = buffer.replace("<ul class=\"liste-plats\">",
                            "")
    buffer = buffer.replace("<li></li>", "")
    buffer = buffer.replace("<li>", "\t")
    buffer = buffer.replace("</li>", "\n")
    buffer = buffer.replace("</ul>", "\n")
    buffer = buffer.replace("<div>", "")
    buffer = buffer.replace("</div>", "")

    # Get only the menu concerning the students only
    buffer = buffer.split("SALLE")
    str = ""
    for i in range(0, len(buffer)):
        if buffer[i].find("ETUDIANTS") != -1:
            str += "SALLE" + buffer[i]

    # Remove the ":" in a room content
    if "chaude : " in str:
        str = str.replace("chaude : ", "chaude -> ")

    # Check if the menu is empty
    if str == "":
        str = "Pas de menu disponible pour aujourd'hui !"

    return str


def Cronenbourg(buffer, date):
    # Find the html element that concern the menu of the day
    menu = buffer.find(date)
    buffer = buffer[menu:]

    # Get the menu of the lunch
    menu = buffer.find("Déjeuner")
    buffer = buffer[menu+45:]

    # Get the end of the menu
    end = buffer.find("Origin")
    buffer = buffer[:end]

    # Remove the html tags
    buffer = buffer.replace("<span class=\"name\">",
                            "")
    buffer = buffer.replace("</span>", " : \n")
    buffer = buffer.replace("<ul class=\"liste-plats\">",
                            "")
    buffer = buffer.replace("<li></li>", "")
    buffer = buffer.replace("<li>", "\t")
    buffer = buffer.replace("</li>", "\n")
    buffer = buffer.replace("</ul>", "\n")
    buffer = buffer.replace("<div>", "")
    buffer = buffer.replace("</div>", "")

    # Get only the menu concerning the students only
    str = ""
    for i in range(0, len(buffer)):
        # Delele the é or è in the menu
        if buffer[i] == "é" or buffer[i] == "è":
            str += "e"
        else:
            str += buffer[i]

    # Check if the menu is empty
    if str == "":
        str = "Pas de menu disponible pour aujourd'hui !"

    return str


def Paul_Appell(buffer, date):
    # Copy the buffer
    buffer2 = BytesIO()
    buffer2 = buffer

    # Find the html element that concern the menu of the day
    menu = buffer.find(date)
    buffer = buffer[menu:]

    # Get the menu of the lunch
    menu = buffer.find("Déjeuner")
    buffer = buffer[menu+45:]

    # Get the end of the menu
    end = buffer.find("Origin")
    buffer = buffer[:end]

    # Remove the html tags
    buffer = buffer.replace("<span class=\"name\">",
                            "\t")
    buffer = buffer.replace("</span>", " : \n")
    buffer = buffer.replace("<ul class=\"liste-plats\">",
                            "")
    buffer = buffer.replace("<li></li>", "")
    buffer = buffer.replace("<li>", "\t\t")
    buffer = buffer.replace("</li>", "\n")
    buffer = buffer.replace("</ul>", "\n")
    buffer = buffer.replace("<div>", "")
    buffer = buffer.replace("</div>", "")

    # Get only the menu concerning the students only
    str1 = ""
    if buffer != "":
        str1 = "Midi : \n\n"
        for i in range(0, len(buffer)):
            # Delele the é or è in the menu
            if buffer[i] == "é" or buffer[i] == "è":
                str1 += "e"
            elif buffer[i] == "ô":
                str1 += "o"
            else:
                str1 += buffer[i]

        if str1[-1] == "\t":
            str1 = str1[:-1]

    # Get the menu of the dinner
    buffer = buffer2
    menu = buffer.find(date)
    buffer = buffer[menu:]
    # Get the menu of the dinner
    menu = buffer.find("Dîner")
    buffer = buffer[menu+45:]

    # Get the end of the menu
    end = buffer.find("Origin")
    buffer = buffer[:end]

    # Remove the html tags
    buffer = buffer.replace("<span class=\"name\">",
                            "\t")
    buffer = buffer.replace("</span>", " : \n")
    buffer = buffer.replace("<ul class=\"liste-plats\">",
                            "")
    buffer = buffer.replace("<li></li>", "")
    buffer = buffer.replace("<li>", "\t\t")
    buffer = buffer.replace("</li>", "\n")
    buffer = buffer.replace("</ul>", "\n")
    buffer = buffer.replace("<div>", "")
    buffer = buffer.replace("</div>", "")
    buffer = buffer.replace("an class=\"name\">", "\t")

    # Get only the menu concerning the students only
    str2 = ""
    if buffer != "":
        str2 = "Soir : \n\n"
        for i in range(0, len(buffer)):
            # Delele the é or è in the menu
            if buffer[i] == "é" or buffer[i] == "è":
                str2 += "e"
            elif buffer[i] == "ô":
                str2 += "o"
            else:
                str2 += buffer[i]

        while str2[-1] == "\t" or str2[-1] == "\n":
            str2 = str2[:-1]

    # Concatenate the two menus
    str = str1 + str2

    # Check if the menu is empty
    if str == "":
        str = "Pas de menu disponible pour aujourd'hui !"

    return str
