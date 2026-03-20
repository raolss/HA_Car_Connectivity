import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(
                title="Car Connectivity",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("username"): str,
                vol.Required("password"): str,
                vol.Optional("country", default="SE"): str,
                vol.Optional("brand", default="VW"): str,
                vol.Optional("region", default="emea"): str,

            }),
        )
