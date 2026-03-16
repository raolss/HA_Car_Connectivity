import logging

from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from carconnectivity import CarConnectivity
import carconnectivity_connector_volkswagen

from .const import CONF_USERNAME, CONF_PASSWORD

_LOGGER = logging.getLogger(__name__)


class VWCoordinator(DataUpdateCoordinator):

    def __init__(self, hass, config):

        self.username = config[CONF_USERNAME]
        self.password = config[CONF_PASSWORD]

        self.cc = None
        self.vehicle = None

        super().__init__(
            hass,
            _LOGGER,
            name="Volkswagen coordinator",
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self):

        if self.cc is None:

            config = {
                "carConnectivity": {
                    "connectors": [
                        {
                            "type": "volkswagen",
                            "config": {
                                "username": self.username,
                                "password": self.password,
                            },
                        }
                    ]
                }
            }

            self.cc = carConnectivity(config)

            await self.cc.start()

            connector = self.cc.connectors[0]

            self.vehicle = connector.vehicles[0]

        await self.cc.update()

        return {
            "soc": self.vehicle.drivetrain.battery.level.value
        }
