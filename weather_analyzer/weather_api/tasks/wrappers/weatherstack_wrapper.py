import logging
from typing import List, Optional
from datetime import datetime, timedelta

import requests

from weather_api.tasks.exceptions import WeatherStackAPIError
from weather_api.tasks.decorators import retry


logger = logging.getLogger("data_collector")


class WeatherStackWrapper:
    def __init__(self, api_key):
        self.api_key = api_key
        self._base_url = "https://api.weatherbit.io/v2.0"

    @retry(exceptions=(WeatherStackAPIError,))
    def get_last_week_weather(
        self,
        cities: Optional[List[str]] = ["New York,NY", "Los Angeles,CA"],
        date_from: datetime = datetime.today() - timedelta(days=7),
        date_to: datetime = datetime.today(),
    ):
        logger.info(f"Collection last week's weather data for:{','.join(cities)}")
        responses = []
        try:
            for city in cities:
                params = {
                    "city": city,
                    "start_date": date_from.date(),
                    "end_date": date_to.date(),
                    "key": self.api_key,
                }
                response = requests.get(
                    f"{self._base_url}/history/daily", params=params
                )

                # The API returns with 200 without api key
                if "error" in response.text:
                    raise WeatherStackAPIError(response.text)

                responses.append(response.json())

            logger.info("Done!")
            return responses
        except Exception as e:
            logger.error(f"Error occurred: {e}")
            raise e
