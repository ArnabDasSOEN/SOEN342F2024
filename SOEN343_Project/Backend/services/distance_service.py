"""
Distance Service
Provides functionality for calculating distances and travel times using the Google Maps API.
"""

import os
import requests


class DistanceService:
    """
    Service for interacting with the Google Maps API to calculate distances and travel times.
    """

    @staticmethod
    def calculate(pick_up_address: str, drop_off_address: str) -> float:
        """
        Calculate the distance (in kilometers) between two addresses using the Google Maps Distance Matrix API.

        Args:
            pick_up_address (str): The origin address as a string.
            drop_off_address (str): The destination address as a string.

        Returns:
            float: The distance in kilometers.
        """
        google_api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not google_api_key:
            raise ValueError(
                "Google Maps API key is missing in environment variables.")

        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": pick_up_address,
            "destinations": drop_off_address,
            "key": google_api_key,
            "units": "metric",
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "rows" in data and data["rows"][0]["elements"][0]["status"] == "OK":
                distance_meters = data["rows"][0]["elements"][0]["distance"]["value"]
                return distance_meters / 1000  # Convert meters to kilometers
            else:
                error_message = data.get(
                    "error_message", "Unknown error occurred.")
                raise ValueError(f"Google Maps API error: {error_message}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error calculating distance: {e}") from e

    @staticmethod
    def get_intermediate_locations(origin: str, destination: str) -> list:
        """
        Get intermediate locations between the origin and destination using the Google Maps Directions API.

        Args:
            origin (str): The starting address.
            destination (str): The destination address.

        Returns:
            list: A list of intermediate location coordinates (latitude and longitude).
        """
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not api_key:
            raise ValueError(
                "Google Maps API key is missing in environment variables.")

        url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "origin": origin,
            "destination": destination,
            "key": api_key,
            "mode": "driving",
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            steps = data["routes"][0]["legs"][0]["steps"]
            locations = [step["end_location"] for step in steps]
            return locations
        except (IndexError, KeyError) as exc:
            raise ValueError(
                "Invalid or incomplete Google Maps API response.") from exc
        except requests.exceptions.RequestException as e:
            raise ValueError(
                f"Error fetching intermediate locations: {e}") from e

    @staticmethod
    def calculate_route_time(origin: str, destination: str) -> float:
        """
        Calculate travel time between the origin and destination using the Google Maps Distance Matrix API.

        Args:
            origin (str): The starting address.
            destination (str): The destination address.

        Returns:
            float: The travel time in minutes.
        """
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not api_key:
            raise ValueError(
                "Google Maps API key is missing in environment variables.")

        url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        params = {
            "origins": origin,
            "destinations": destination,
            "key": api_key,
            "mode": "driving",
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data["rows"][0]["elements"][0]["status"] == "OK":
                travel_time_seconds = data["rows"][0]["elements"][0]["duration"]["value"]
                return travel_time_seconds / 60  # Convert seconds to minutes
            else:
                error_status = data["rows"][0]["elements"][0]["status"]
                raise ValueError(f"Error fetching travel time: {error_status}")
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Error calculating route time: {e}") from e
