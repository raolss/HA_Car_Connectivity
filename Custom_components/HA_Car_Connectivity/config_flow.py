import voluptuous as vol

from homeassistant import config_entries

from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD

STEP_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    VERSION = 1

    async def async_step_user(self, user_input=None):

        if user_input is not None:

            return self.async_create_entry(
                title="Volkswagen",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_SCHEMA,
        )
