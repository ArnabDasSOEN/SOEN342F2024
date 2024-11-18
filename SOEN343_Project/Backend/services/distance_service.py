import os
import requests


class DistanceService:
    @staticmethod
    def calculate(pick_up_address: str, drop_off_address: str) -> float:
        """
        Calculate the distance (in kilometers) between two addresses using Google Maps Distance Matrix API.

        :param pick_up_address: The origin address as a string.
        :param drop_off_address: The destination address as a string.
        :return: The distance in kilometers.
        """
        # Get the Google Maps API key from environment variables
        google_api_key = os.getenv("GOOGLE_MAPS_API_KEY")

        if not google_api_key:
            raise ValueError("Google Maps API key not found in environment variables. Please set GOOGLE_MAPS_API_KEY.")

        # API endpoint
        url = "https://maps.googleapis.com/maps/api/distancematrix/json"

        # Request parameters
        params = {
            "origins": pick_up_address,
            "destinations": drop_off_address,
            "key": google_api_key,
            "units": "metric",  # Use metric units to get distances in kilometers
        }

        try:
            # Make the API call
            response = requests.get(url, params=params)
            data = response.json()

            # Validate the API response
            if response.status_code == 200 and "rows" in data:
                distance_meters = data["rows"][0]["elements"][0]["distance"]["value"]
                return distance_meters / 1000  # Convert meters to kilometers
            else:
                error_message = data.get("error_message", "Unknown error occurred.")
                raise Exception(f"Google Maps API error: {error_message}")
        except Exception as e:
            raise Exception(f"Error calculating distance: {e}")
        

    @staticmethod
    def calculate_route_time(origin_address, destination_address):
        """
        Calculate the route time between two addresses using Google Maps Distance Matrix API.

        :param origin_address: The origin address as a string.
        :param destination_address: The destination address as a string.
        :return: Estimated travel time in minutes.
        """
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not api_key:
            raise ValueError("Google Maps API key is not set in environment variables.")

        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": origin_address,
            "destinations": destination_address,
            "key": api_key,
            "mode": "driving"
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data["rows"][0]["elements"][0]["status"] == "OK":
                travel_time_seconds = data["rows"][0]["elements"][0]["duration"]["value"]
                return travel_time_seconds / 60  # Convert seconds to minutes
            else:
                raise ValueError(f"Error fetching travel time: {data['rows'][0]['elements'][0]['status']}")
        else:
            raise ValueError(f"Google Maps API request failed with status: {response.status_code}")
