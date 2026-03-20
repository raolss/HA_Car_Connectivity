from carconnectivity.carconnectivity import CarConnectivity
import logging

_LOGGER = logging.getLogger(__name__)

try:
    from carconnectivity_connector.volkswagen.volkswagen_connector import VolkswagenConnector
    _LOGGER.warning("VolkswagenConnector import OK")
except Exception as e:
    _LOGGER.error("Import failed: %s", e)

#from carconnectivity_connector.volkswagen.volkswagen_connector import VolkswagenConnector

class CarConnectivityAPI:
    def __init__(self, entry_data):
        # Bygg config enligt CarConnectivity-specen
        self.config = {
            "carConnectivity": {
                "connectors": [
                    {
                        "connectorId": "vw",
                        "type": "volkswagen",
                        "config": {
                            "username": entry_data["username"],
                            "password": entry_data["password"],
                            "country": entry_data.get("country", "SE"),
                            "brand": entry_data.get("brand", "VW"),
                            "region": entry_data.get("region", "emea"),
                        },
                    }
                ]
            }
        }

        # Skapa CarConnectivity-instansen
        self.cc = CarConnectivity(self.config)

        # Hämta connectorn
        self.connector = self.cc.get_connector("vw")

        self.vehicles = None

    async def get_vehicles(self):
        if self.vehicles is None:
            self.vehicles = await self.connector.get_vehicles()

        normalized = []
        for v in self.vehicles:
            normalized.append({
                "vin": v.vin,
                "name": v.nickname or v.model or v.vin,
                "brand": "Volkswagen",
                "model": v.model,
                "softwareVersion": getattr(v, "software_version", None),
                "vehicle_obj": v,
            })

        return normalized

    async def get_vehicle_status(self, vin):
        if self.vehicles is None:
            await self.get_vehicles()

        vehicle = next((v for v in self.vehicles if v.vin == vin), None)
        if vehicle is None:
            return {}

        status = await vehicle.get_status()

        result = {}

        if hasattr(status, "battery_level"):
            result["battery"] = {"level": status.battery_level}

        if hasattr(status, "range_km"):
            result["range"] = {"km": status.range_km}

        if hasattr(status, "doors_locked"):
            result["doors"] = {"locked": status.doors_locked}

        return result
