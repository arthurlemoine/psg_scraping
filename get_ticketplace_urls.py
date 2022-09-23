import osv
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(os.path.basename(__file__))


URL = "https://billetterie.psg.fr/fr/?utm_campaign=Menu_Top_PSG&utm_medium=referral&utm_source=PSG_Site"
response = requests.get(URL)
soup = BeautifulSoup(response.content, "html.parser")

urls_ticketplace = []

matchs = soup.find("div", {"class": "nq-c-HomeMatchList-list"})
list_matchs = matchs.find_all("div", {"class": "nq-c-MatchLine"})

for match in list_matchs:
    tickets = match.find_all("a", {"class": "nq-c-Btn"})
    for ticket in tickets:
        if "Ticketplace" in ticket.text:
            urls_ticketplace.append(ticket.attrs["href"])
        else:
            pass
