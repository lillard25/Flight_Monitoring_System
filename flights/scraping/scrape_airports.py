import requests
from bs4 import BeautifulSoup
from flights.models import Airport


def scrape_airports():
    url = "https://en.wikipedia.org/wiki/List_of_airports_in_the_United_Kingdom_and_the_British_Crown_Dependencies"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    i = 0

    tables = soup.find_all("table", class_="wikitable")
    for table in tables:
        rows = table.find_all("tr")[1:]

        for row in rows:
            columns = row.find_all("td")
            if i > 10:
                break
            if len(columns) >= 4:
                city = columns[0].text.strip()
                country = columns[1].text.strip()
                icao_code = columns[2].text.strip()
                iata_code = columns[3].text.strip()
                name = columns[4].text.strip()

                Airport.objects.update_or_create(
                    icao_code=icao_code,
                    defaults={"name": name, "iata_code": iata_code, "country": country, "city": city}
                )

                i += 1
