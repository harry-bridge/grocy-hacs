[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)

---
**INFO**

**Works with Grocy version 3 and above.**

You have to have the Grocy software already installed and running, this integration only communicates with an existing installation of Grocy. You can install the software with the [Grocy add-on](https://github.com/hassio-addons/addon-grocy) or another installation method, found at [Grocy website](https://grocy.info/).

---


# Adding the integration
## <a name="addon"></a>for Grocy add-on

The configuration is slightly different for those who use the [official Grocy add-on](https://github.com/hassio-addons/addon-grocy) from the add-on store.

1. If you haven't already done so, install Grocy from the add-on store
2. In the 'Configuration' section of the add-on config, input `9192` in the host field - see [screenshot](#screenshot). Save your changes and restart the add-on.
3. Install [HACS](https://hacs.xyz/)
4. Go to Community > Store > Grocy
5. Install the Grocy integration
6. Restart Home Assistant
7. Go to Grocy > Wrench icon > Manage API keys > Add
8. Copy resulting API key
9. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Grocy"
10. Fill out the information according to [this instruction](#integration-configuration).
11. You will now have a new integration for Grocy. Some or all of the entities might be disabled from the start.


## <a name="external"></a> for existing external Grocy install

1. Install [HACS](https://hacs.xyz/)
2. Go to Community > Store > Grocy
3. Install the Grocy integration
4. Restart Home Assistant
5. Go to Grocy > Wrench icon > Manage API keys > Add
6. Copy resulting API key
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Grocy"
8. Fill out the information according to [this instruction](#integration-configuration).
9. You will now have a new integration for Grocy. Some or all of the entities might be disabled from the start.


# Entities
Some or all of the entities might be disabled from the start.
You get a sensor each for chores, meal plan, shopping list, stock and tasks.
You get a binary sensor each for expired, expiring and missing products and overdue tasks and chores.

# Translation
Translations are done via [Lokalise](https://app.lokalise.com/public/260939135f7593a05f2b79.75475372/). If you want to translate into your native language, please [join the team](https://app.lokalise.com/public/260939135f7593a05f2b79.75475372/).

# Troubleshooting

If you have problems with the integration you can add debug prints to the log.

```yaml
logger:
  default: info
  logs:
    pygrocy.grocy_api_client: debug
    custom_components.grocy: debug
```

If you are having issues and want to report a problem, always start with making sure that you're on the latest version of the integration, Grocy and Home Assistant.

You can ask for help [in the forums](https://community.home-assistant.io/t/grocy-custom-component-and-card-s/218978), or [make an issue with all of the relevant information here](https://github.com/custom-components/grocy/issues/new?assignees=&labels=&template=bug_report.md&title=).


# <a name="integration-configuration"></a>Integration configuration

The api url should be in the form below. If you use an SSL certificate you should have `https` and also check the box. Do **not** have a trailing slash at the end of the url and do not have the port in the url. It should work with for example a duck dns address as well, but you still have to access it via a port, and the above instructions for the url still apply.

**(This component will not currently work if you have an install where you don't use a port, as long as [this issue](https://github.com/SebRut/pygrocy/issues/121) is not resolved)**

![alt text](grocy-integration-config.png)

# <a name="screenshot"></a>Add-on port configuration
![alt text](grocy-addon-config.png)
