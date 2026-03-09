from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from carconnectivity import CarConnectivity
import carconnectivity_connector_volkswagen

DOMAIN = "ha_car_connectivity"

_LOGGER = logging.getLogger(__name__)


STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("username"): str,
        vol.Required("password"): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect."""

    config = {
        "carConnectivity": {
            "connectors": [
                {
                    "type": "volkswagen",
                    "config": {
                        "username": data["username"],
                        "password": data["password"],
                    },
                }
            ]
        }
    }

    try:
        cc = CarConnectivity(config)

        await cc.start()

        connector = cc.connectors[0]

        vehicles = connector.vehicles

        if not vehicles:
            raise CannotConnect

    except Exception as err:
        _LOGGER.error("Login failed: %s", err)
        raise CannotConnect from err

    return {"title": "Volkswagen We Connect ID"}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Volkswagen."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None):
        """Handle the initial step."""

        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)

                await self.async_set_unique_id(user_input["username"])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=info["title"],
                    data=user_input,
                )

            except CannotConnect:
                errors["base"] = "cannot_connect"

            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )


class CannotConnect(Exception):
    """Error to indicate we cannot connect."""
