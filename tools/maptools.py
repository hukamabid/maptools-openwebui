import urllib.parse
from pydantic import BaseModel, Field
from typing import Optional, List


class Tools:
    # VALVE CONFIGURATION
    class Valves(BaseModel):
        GOOGLE_MAPS_API_KEY: str = Field(
            default="",
            description="The API Key from Google Cloud Console. Must have 'Static Maps API' enabled.",
        )
        IMAGE_SIZE: str = Field(
            default="600x400",
            description="Resolution of the map image (e.g., 600x400).",
        )

    def __init__(self):
        self.valves = self.Valves()
        self.base_url = "https://maps.googleapis.com/maps/api/staticmap"

    def find_places_and_map(self, query: str) -> str:
        """
        Search for a place and return a static image of the location.
        """
        if not self.valves.GOOGLE_MAPS_API_KEY:
            return "Error: Google Maps API key is missing."

        safe_query = urllib.parse.quote(query)

        # map_url for a single location with a marker
        map_url = (
            f"{self.base_url}?center={safe_query}&zoom=15&size={self.valves.IMAGE_SIZE}"
            f"&markers=color:red%7C{safe_query}&key={self.valves.GOOGLE_MAPS_API_KEY}"
        )

        external_link = f"https://www.google.com/maps/search/?api=1&query={safe_query}"

        return f"""
### 📍 Location: {query}

![Map of {query}]({map_url})

[↗ Open in Google Maps]({external_link})

"""

    def get_directions_map(self, origin: str, destination: str) -> str:
        """
        Generate a static map showing markers and a path between origin and destination.
        """
        if not self.valves.GOOGLE_MAPS_API_KEY:
            return "Error: API Key not configured."

        safe_origin = urllib.parse.quote(origin)
        safe_dest = urllib.parse.quote(destination)

        # 1. Construct Static Map URL
        # markers: Points A and B
        # path: Draws a blue line between the two addresses
        map_url = (
            f"{self.base_url}?size={self.valves.IMAGE_SIZE}"
            f"&markers=color:green%7Clabel:A%7C{safe_origin}"
            f"&markers=color:red%7Clabel:B%7C{safe_dest}"
            f"&path=color:0x0000ff|weight:5|{safe_origin}|{safe_dest}"
            f"&key={self.valves.GOOGLE_MAPS_API_KEY}"
        )

        # 2. Construct the direct Google Maps Route URL for the external link
        route_link = f"https://www.google.com/maps/dir/?api=1&origin={safe_origin}&destination={safe_dest}&travelmode=driving"

        return f"""
### 🚗 Route: {origin} to {destination}

![Route from {origin} to {destination}]({map_url})

[↗ View Step-by-Step Directions on Google Maps]({route_link})

"""
