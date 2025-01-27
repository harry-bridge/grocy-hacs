"""Sensor platform for Grocy."""
from __future__ import annotations

import logging
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any, List

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import (
    ATTR_BATTERIES,
    ATTR_CHORES,
    ATTR_MEAL_PLAN,
    ATTR_SHOPPING_LIST,
    ATTR_ALL_LOCATIONS,
    ATTR_ALL_PRODUCTS,
    ATTR_QUANTITY_UNITS,
    ATTR_STOCK,
    ATTR_STOCK_BY_LOCATION,
    ATTR_TASKS,
    CHORES,
    DOMAIN,
    ITEMS,
    MEAL_PLANS,
    PRODUCTS,
    LOCATIONS,
    UNITS,
    TASKS,
)
from .coordinator import GrocyDataUpdateCoordinator
from .entity import GrocyEntity

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Setup sensor platform."""
    coordinator: GrocyDataUpdateCoordinator = hass.data[DOMAIN]
    entities = []
    for description in SENSORS:
        if description.exists_fn(coordinator.available_entities):
            entity = GrocySensorEntity(coordinator, description, config_entry)
            coordinator.entities.append(entity)
            entities.append(entity)
        else:
            _LOGGER.debug(
                "Entity description '%s' is not available.",
                description.key,
            )

    async_add_entities(entities, True)


@dataclass
class GrocySensorEntityDescription(SensorEntityDescription):
    """Grocy sensor entity description."""

    attributes_fn: Callable[[List[Any]], Mapping[str, Any] | None] = lambda _: None
    exists_fn: Callable[[List[str]], bool] = lambda _: True
    entity_registry_enabled_default: bool = False


SENSORS: tuple[GrocySensorEntityDescription, ...] = (
    GrocySensorEntityDescription(
        key=ATTR_CHORES,
        name="Grocy chores",
        native_unit_of_measurement=CHORES,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:broom",
        exists_fn=lambda entities: ATTR_CHORES in entities,
        attributes_fn=lambda data: {
            "chores": [x.as_dict() for x in data],
            "count": len(data),
        },
    ),
    GrocySensorEntityDescription(
        key=ATTR_MEAL_PLAN,
        name="Grocy meal plan",
        native_unit_of_measurement=MEAL_PLANS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:silverware-variant",
        exists_fn=lambda entities: ATTR_MEAL_PLAN in entities,
        attributes_fn=lambda data: {
            "meals": [x.as_dict() for x in data],
            "count": len(data),
        },
    ),
    GrocySensorEntityDescription(
        key=ATTR_SHOPPING_LIST,
        name="Grocy shopping list",
        native_unit_of_measurement=PRODUCTS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:cart-outline",
        exists_fn=lambda entities: ATTR_SHOPPING_LIST in entities,
        attributes_fn=lambda data: {
            "products": [x.as_dict() for x in data],
            "count": len(data),
        },
    ),
    GrocySensorEntityDescription(
        key=ATTR_STOCK,
        name="Grocy stock",
        native_unit_of_measurement=PRODUCTS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:fridge-outline",
        exists_fn=lambda entities: ATTR_STOCK in entities,
        attributes_fn=lambda data: {
            "products": [x.as_dict() for x in data],
            "count": len(data),
        },
    ),
    GrocySensorEntityDescription(
        key=ATTR_ALL_LOCATIONS,
        name="Grocy locations",
        native_unit_of_measurement=LOCATIONS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:fridge-outline",
        exists_fn=lambda entities: ATTR_ALL_LOCATIONS in entities,
        attributes_fn=lambda data: {
            "locations": [x for x in data],
            "count": len(data),
        },
    ),
    GrocySensorEntityDescription(
        key=ATTR_STOCK_BY_LOCATION,
        name="Grocy stock by location",
        native_unit_of_measurement=LOCATIONS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:fridge-outline",
        exists_fn=lambda entities: ATTR_STOCK_BY_LOCATION in entities,
        attributes_fn=lambda data: {
            "products": [x for x in data],
            "count": len(data),
        },
    ),
    GrocySensorEntityDescription(
        key=ATTR_ALL_PRODUCTS,
        name="Grocy products",
        native_unit_of_measurement=PRODUCTS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:fridge-outline",
        exists_fn=lambda entities: ATTR_ALL_PRODUCTS in entities,
        attributes_fn=lambda data: {
            "products": [x for x in data],
            "count": len(data),
        },
    ),
    GrocySensorEntityDescription(
        key=ATTR_QUANTITY_UNITS,
        name="Grocy quantity units",
        native_unit_of_measurement=UNITS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:fridge-outline",
        exists_fn=lambda entities: ATTR_QUANTITY_UNITS in entities,
        attributes_fn=lambda data: {
            "products": [x for x in data],
            "count": len(data),
        },
    ),
    GrocySensorEntityDescription(
        key=ATTR_TASKS,
        name="Grocy tasks",
        native_unit_of_measurement=TASKS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:checkbox-marked-circle-outline",
        exists_fn=lambda entities: ATTR_TASKS in entities,
        attributes_fn=lambda data: {
            "tasks": [x.as_dict() for x in data],
            "count": len(data),
        },
    ),
    GrocySensorEntityDescription(
        key=ATTR_BATTERIES,
        name="Grocy batteries",
        native_unit_of_measurement=ITEMS,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery",
        exists_fn=lambda entities: ATTR_BATTERIES in entities,
        attributes_fn=lambda data: {
            "batteries": [x.as_dict() for x in data],
            "count": len(data),
        },
    ),
)


class GrocySensorEntity(GrocyEntity, SensorEntity):
    """Grocy sensor entity definition."""

    @property
    def native_value(self) -> StateType:
        """Return the value reported by the sensor."""
        entity_data = self.coordinator.data.get(self.entity_description.key, None)

        return len(entity_data) if entity_data else 0
