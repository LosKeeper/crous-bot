import pycurl
import certifi
from io import BytesIO
from datetime import datetime

from config import URL

def EN_to_FR(month) :

    # Convert the month from english to french
    months = {
        "January" : "janvier",
        "February" : "février",
        "March" : "mars",
        "April" : "avril",
        "May" : "mai",
        "June" : "juin",
        "July" : "juillet",
        "August" : "août",
        "September" : "septembre",
        "October" : "octobre",
        "November" : "novembre",
        "December" : "décembre"
    }

    return months[month]

def get_html() :

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


    c.setopt(c.CAINFO, certifi.where())

    # Perform a file transfer
    c.perform()

    # End curl session
    c.close()

    # Decode the buffer
    body = buffer.getvalue().decode('utf-8')

    return body

def parse_html(buffer) :

    # Get the date
    day = datetime.now().strftime("%d")
    month = datetime.now().strftime("%B")
    month = EN_to_FR(month)
    date = day + " " + month

    # Find the html element that concern the menu of the day
    menu = buffer.find(date)

    # Get the 12 lines after the date
    buffer = buffer[menu:menu+2000]

    # Get the menu
    menu = buffer.find("Déjeuner")
    buffer = buffer[menu+45:]

    # Get the end of the menu
    end = buffer.find("Origin")
    buffer = buffer[:end]

    # Remove the html tags
    buffer = buffer.replace("<span class=\"name\">", "")
    buffer = buffer.replace("</span>", "\n")
    buffer = buffer.replace("<ul class=\"liste-plats\">", "")
    buffer = buffer.replace("<li>", "\t")
    buffer = buffer.replace("</li>", "\n")
    buffer = buffer.replace("</ul>", "")
    buffer = buffer.replace("<div>", "")
    buffer = buffer.replace("</div>", "")

    print("Menu: " + buffer)

parse_html(get_html())