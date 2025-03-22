## Airports and Flight Monitoring System
### Project Overview
This project provides a RESTful API for managing European airports, airlines, flights, and flight statuses using Django and Django REST Framework (DRF). The system allows users to monitor flights, track delays, and scrape data for airports and airlines.
### Features
- CRUD operations for Airports, Airlines, Flights, and Flight Statuses
- API endpoint to retrieve delayed flights
- Web scraping endpoints for airport and airline data

### Technologies Used
- Django: Backend framework
- Django REST Framework (DRF): API development
- Docker: Containerization
- PostgreSQL: Database (inside Docker)

### API Endpoints
- Scrape Airport Data: POST - /api/scrape-airports/
- Scrape Airline Data: POST - /api/scrape-airlines/
- Airports: GET - /api/airports/
- Airlines: GET - /api/airlines/
- Flights: GET- /api/flights/
- Flight Status: GET - /api/flight-status/
- Delayed Flights: GET - /api/delayed-flights/

### Installation and Setup
 Prerequisites
 - Docker
#### Clone the repository
```
git clone <repository_url>
cd <project_directory>
```
### Run the project
```
docker-compose build
docker-compose up
```

Your project is running at http://127.0.0.1:8000/
