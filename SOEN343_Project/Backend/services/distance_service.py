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
