from homeassistant.components.sensor import SensorEntity

from homeassistant.helpers.entity import Entity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):

    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities([BatterySensor(coordinator)])


class BatterySensor(SensorEntity):

    def __init__(self, coordinator):

        self.coordinator = coordinator

        self._attr_name = "VW Battery SOC"
        self._attr_native_unit_of_measurement = "%"

    @property
    def native_value(self):
        return self.coordinator.data["soc"]

    async def async_update(self):
        await self.coordinator.async_request_refresh()
