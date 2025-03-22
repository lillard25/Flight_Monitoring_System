import requests
from bs4 import BeautifulSoup
from flights.models import Airline


def scrape_airlines():
    url = "https://en.wikipedia.org/wiki/List_of_airlines_of_the_United_Kingdom"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    i = 0

    airlines = soup.find_all("tr")[1:]
    for row in airlines:
        if i > 10:
            break
        columns = row.find_all("td")
        if len(columns) >= 3:
            name = columns[0].text.strip()
            iata = columns[2].text.strip()
            icao = columns[3].text.strip()

            i += 1

            # Check if an airline with the same ICAO code already exists
            Airline.objects.get_or_create(
                icao_code=icao,
                defaults={
                    'name': name,
                    'iata_code': iata,
                    'icao_code': icao
                }
            )