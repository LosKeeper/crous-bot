import pycurl
import certifi
from io import BytesIO
from datetime import datetime

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
    day = datetime.now().strftime("%d")

    if day[0] == "0":
        day = day[1]

    month = datetime.now().strftime("%B")
    month = EN_to_FR(month)

    # If the time is after 14h, the menu is for the next day
    hour = datetime.now().strftime("%H")
    if int(hour)+delta_time >= 14:
        day_int = int(day)+1
    else:
        day_int = int(day)

    date = "%s" % day_int + " "+month

    if "Cronenbourg" in buffer:
        return Cronenbourg(buffer, date)
    else:
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
        str += buffer[i]

    # Check if the menu is empty
    if str == "":
        str = "Pas de menu disponible pour aujourd'hui !"

    return str
