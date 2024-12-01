# WeatherAnalyzer

## Table of Contents

1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Tech Stack](#tech-stack)
4. [Environment Variables](#environment-variables)
5. [Database Architecture](#database-architecture)
6. [Events](#events)
   - [Data Collection](#data-collection)
   - [Triggering Data Processing](#triggering-data-processing)
   - [Weekly Statistics Calculation](#weekly-statistics-calculation)
7. [Usage](#usage)
   - [Create a .env file](#create-a-env-file)
   - [Access the Application](#access-the-application)
   - [API Endpoints](#api-endpoints)
     - [List Cities](#list-cities)
     - [List Historical Data for City](#list-historical-data-for-city)
     - [List Weekly Statistics](#list-weekly-statistics)
8. [Start the Project](#start-the-project)
9. [Triggering Data Collection](#triggering-data-collection)
   - [Step 1: Access the Docker Container](#step-1-access-the-docker-container)
   - [Step 2: Trigger Data Collection](#step-2-trigger-data-collection)

## Project Overview
This project is a Django-based application. It consists of three main components:
1. **Weather API**: The central part of the system that exposes endpoints to interact with the application. It handles requests and provides responses to clients.

2. **Weather Collector Worker** (data_collector): This Celery worker performs the collection and saving of weather data from `WeatherStack API`.

3. **Weather Processor Worker** (data_processor): This Celery worker performs the calculation of the staticstics from the data provided by `data_collector` worker.

Each of these components — API and both Celery workers — can be deployed and scaled independently.

### Prerequisites

Before running the application, ensure that the following tools are installed:

- **Docker**: Docker is required to containerize the services and run them in isolated environments. You can install Docker from [here](https://docs.docker.com/get-docker/).
- **Docker Compose**: Docker Compose is used to manage multi-container Docker applications. It allows you to define and run services in a single configuration file. You can install Docker Compose from [here](https://docs.docker.com/compose/install/).

### Tech Stack

| **Technology**     | **Description**                                   |
|--------------------|---------------------------------------------------|
| **Django**         | Web framework for building the weather API.       |
| **Celery**         | Task queue for managing background workers.       |
| **Celery-beat**    | Scheduler for periodic tasks.                     |
| **Redis**          | Caching and storing Celery results.               |
| **PostgreSQL**     | Relational database for data storage.             |
| **PGBouncer**      | Connection pooling for PostgreSQL.                |
| **RabbitMQ**       | Message broker for communication between services.|
| **Docker**         | Containerized environment for deploying services. |

### Environment Variables
| **Variable**                           | **Description**                                  |
|----------------------------------------|--------------------------------------------------|
| `POSTGRES_USER`                        | PostgreSQL username.                            |
| `POSTGRES_PASSWORD`                    | PostgreSQL password.                            |
| `POSTGRES_DB`                          | PostgreSQL database name.                       |
| `SECRET_KEY`                           | Django secret key for encryption.               |
| `API_KEY`                              | API key for accessing weather data.             |
| `RABBITMQ_USER`                        | RabbitMQ username                               |
| `RABBITMQ_PASSWORD`                    | RabbitMQ password.                              |
| `POSTGRESQL_PRIMARY_REPLICATION_MODE`  | Replication mode for PostgreSQL primary.        |
| `POSTGRESQL_REPLICATION_USER`          | Replication username for PostgreSQL.            |
| `POSTGRESQL_REPLICATION_PASSWORD`      | Replication password for PostgreSQL.            |
| `POSTGRESQL_DATABASE`                  | PostgreSQL database for replication.            |
| `POSTGRESQL_EXTRA_FLAGS`               | Additional PostgreSQL flags for configuration.  |
| `POSTGRESQL_REPLICA_REPLICATION_MODE`  | Replication mode for PostgreSQL replica         |
| `POSTGRESQL_MASTER_HOST`               | Host for PostgreSQL master.                     |
| `POSTGRESQL_MASTER_PORT_NUMBER`        | Port for PostgreSQL master.                     |
| `PGBOUNCER_DATABASE`                   | Database for PGBouncer.                         |
| `PGBOUNCER_AUTH_TYPE`                  | Authentication type for PGBouncer.              |
| `PGBOUNCER_POOL_MODE`                  | Pooling mode for PGBouncer.                     |
| `PGBOUNCER_MAX_CLIENT_CONN`            | Maximum client connections for PGBouncer.       |
| `PGBOUNCER_DSN_0`                      | Data source name for PGBouncer.                 |

## Database Architecture
It uses PostgreSQL as the primary database, with replication for fault tolerance and PGbouncer for connection pooling.

#### PostgreSQL (Primary)
- **Role**: Main database instance for storing all application data.
- **Replication**: Configured as the primary instance in a replication setup.

#### PostgreSQL (Replica)
- **Role**: Replica database instance for mirroring data from the primary.
- **Replication**: Configured to act as a replica in the replication setup.

#### PGbouncer
- **Role**: Connection pooler for PostgreSQL, optimizing database connections. Routes read and write queries to the appropriate PostgreSQL instance, ensuring efficient load distribution and reducing connection overhead.

## Events
The data collection and processing flow is managed by Celery tasks, which are triggered by specific events.</br>
The sequence of events is as follows

1. Data Collection:
The `collect_weather_data_task` task is scheduled to run automatically at `00:00 every Monday`. This task fetches weather data from the `WeatherStack` API and saves it in the PostgreSQL database.

2. Triggering Data Processing:
Once the data collection is completed successfully, the `collect_weather_data_task` task sends a message to the `processor_queue` through `RabbitMQ`. This message signals that new weather data is available and ready for processing.

3. Weekly Statistics Calculation:
The `calculate_weekly_statistics_task` is triggered by the message sent by `collect_weather_data_task`. It aggregates weather data for the week and saves the statistics into the database.

This event-driven flow ensures that data is collected and processed in an automated and scalable manner.

## Usage
### Create a .env file
You ned to create a .env file in the same directory as the `Docker` and `docker-compose` file. </br>
Configure all the variables listed in the [Environment Variables](#environment-variables) section.

### Access the Application
**Weather API**: Once the services are up, the API will be available on http://localhost:8000/weather_api.
The weather data collection and processing will run in the background using Celery workers.

### API Endpoints

1. **List Cities**
   - **URL**: `/cities/`
   - **Method**: `GET`
   - **Description**: Retrieves a list of all cities with weather data.
   - **Query Parameters**:
     - `id`: Filter cities by ID.
     - `name`: Filter cities by name.
     - `country_code`: Filter cities by country code.
   - **Response**: A list of cities with basic weather information.

2. **List Historical Data for City**
   - **URL**: `/historical/`
   - **Method**: `GET`
   - **Description**: Retrieves historical weather data for a specified city.
   - **Query Parameters**:
     - `city__id`: Filter historical data by city ID.
     - `city__name`: Filter historical data by city name.
     - `date`: Filter historical data by specific date.
   - **Response**: A list of weather data records within the specified range for the given city.

3. **List Weekly Statistics**
   - **URL**: `/statistics/weekly/`
   - **Method**: `GET`
   - **Description**: Retrieves the weekly weather statistics for a city.
   - **Query Parameters**:
     - `city__id`: Filter weekly statistics by city ID.
     - `city__name`: Filter weekly statistics by city name.
     - `week_start_date`: Filter weekly statistics by start date of the week.
   - **Response**: A list of weekly weather statistics for the requested city or cities.


### Start the project
```bash
(sudo) docker-compose --env-file .env up --build
```

## Triggering Data Collection

### Step 1: Access the Docker Container

First, navigate into the `weather_api` Docker container where the Django management command will run.

```bash
sudo docker-compose exec -it weather_api bash
```

Then, this command
```bash
python manage.py trigger_data_collection
```