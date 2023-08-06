#!/usr/bin/python3

#     Copyright 2021. FastyBird s.r.o.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

"""
Sets of enums for application data exchange routing
"""

# Python base dependencies
from enum import unique

# Library libs
from fastybird_metadata.enum import ExtendedEnum


@unique
class RoutingKey(ExtendedEnum):
    """
    Data exchange routing key

    @package        FastyBird:Metadata!
    @module         routing

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    # GLOBAL

    CONNECTOR_ACTION: str = "fb.exchange.action.connector"
    CONNECTOR_PROPERTY_ACTION: str = "fb.exchange.action.connector.property"
    DEVICE_ACTION: str = "fb.exchange.action.device"
    DEVICE_PROPERTY_ACTION: str = "fb.exchange.action.device.property"
    CHANNEL_ACTION: str = "fb.exchange.action.channel"
    CHANNEL_PROPERTY_ACTION: str = "fb.exchange.action.channel.property"
    TRIGGER_ACTION: str = "fb.exchange.action.trigger"

    MODULE_MESSAGE: str = "fb.exchange.message.module"
    PLUGIN_MESSAGE: str = "fb.exchange.message.plugin"
    CONNECTOR_MESSAGE: str = "fb.exchange.message.connector"

    # MODULES

    # Accounts
    ACCOUNT_ENTITY_REPORTED: str = "fb.exchange.module.entity.reported.account"
    ACCOUNT_ENTITY_CREATED: str = "fb.exchange.module.entity.created.account"
    ACCOUNT_ENTITY_UPDATED: str = "fb.exchange.module.entity.updated.account"
    ACCOUNT_ENTITY_DELETED: str = "fb.exchange.module.entity.deleted.account"

    # Emails
    EMAIL_ENTITY_REPORTED: str = "fb.exchange.module.entity.reported.email"
    EMAIL_ENTITY_CREATED: str = "fb.exchange.module.entity.created.email"
    EMAIL_ENTITY_UPDATED: str = "fb.exchange.module.entity.updated.email"
    EMAIL_ENTITY_DELETED: str = "fb.exchange.module.entity.deleted.email"

    # Identities
    IDENTITY_ENTITY_REPORTED: str = "fb.exchange.module.entity.reported.identity"
    IDENTITY_ENTITY_CREATED: str = "fb.exchange.module.entity.created.identity"
    IDENTITY_ENTITY_UPDATED: str = "fb.exchange.module.entity.updated.identity"
    IDENTITY_ENTITY_DELETED: str = "fb.exchange.module.entity.deleted.identity"

    # Roles
    ROLE_ENTITY_REPORTED: str = "fb.exchange.module.entity.reported.role"
    ROLE_ENTITY_CREATED: str = "fb.exchange.module.entity.created.role"
    ROLE_ENTITY_UPDATED: str = "fb.exchange.module.entity.updated.role"
    ROLE_ENTITY_DELETED: str = "fb.exchange.module.entity.deleted.role"

    # Devices
    DEVICE_ENTITY_REPORTED: str = "fb.exchange.module.entity.reported.device"
    DEVICE_ENTITY_CREATED: str = "fb.exchange.module.entity.created.device"
    DEVICE_ENTITY_UPDATED: str = "fb.exchange.module.entity.updated.device"
    DEVICE_ENTITY_DELETED: str = "fb.exchange.module.entity.deleted.device"

    # Device's properties
    DEVICE_PROPERTY_ENTITY_REPORTED: str = "fb.exchange.module.entity.reported.device.property"
    DEVICE_PROPERTY_ENTITY_CREATED: str = "fb.exchange.module.entity.created.device.property"
    DEVICE_PROPERTY_ENTITY_UPDATED: str = "fb.exchange.module.entity.updated.device.property"
    DEVICE_PROPERTY_ENTITY_DELETED: str = "fb.exchange.module.entity.deleted.device.property"

    # Device's controls
    DEVICE_CONTROL_ENTITY_REPORTED: str = "fb.exchange.module.entity.reported.device.control"
    DEVICE_CONTROL_ENTITY_CREATED: str = "fb.exchange.module.entity.created.device.control"
    DEVICE_CONTROL_ENTITY_UPDATED: str = "fb.exchange.module.entity.updated.device.control"
    DEVICE_CONTROL_ENTITY_DELETED: str = "fb.exchange.module.entity.deleted.device.control"

    # Device's attributes
    DEVICE_ATTRIBUTE_ENTITY_REPORTED: str = "fb.exchange.module.entity.reported.device.attribute"
    DEVICE_ATTRIBUTE_ENTITY_CREATED: str = "fb.exchange.module.entity.created.device.attribute"
    DEVICE_ATTRIBUTE_ENTITY_UPDATED: str = "fb.exchange.module.entity.updated.device.attribute"
    DEVICE_ATTRIBUTE_ENTITY_DELETED: str = "fb.exchange.module.entity.deleted.device.attribute"

    # Channels
    CHANNEL_ENTITY_REPORTED: str = "fb.exchange.module.entity.reported.channel"
    CHANNEL_ENTITY_CREATED: str = "fb.exchange.module.entity.created.channel"
    CHANNEL_ENTITY_UPDATED: str = "fb.exchange.module.entity.updated.channel"
    CHANNEL_ENTITY_DELETED: str = "fb.exchange.module.entity.deleted.channel"

    # Channel's properties
    CHANNEL_PROPERTY_ENTITY_REPORTED: str = "fb.exchange.module.entity.reported.channel.property"
    CHANNEL_PROPERTY_ENTITY_CREATED: str = "fb.exchange.module.entity.created.channel.property"
    CHANNEL_PROPERTY_ENTITY_UPDATED: str = "fb.exchange.module.entity.updated.channel.property"
    CHANNEL_PROPERTY_ENTITY_DELETED: str = "fb.exchange.module.entity.deleted.channel.property"

    # Channel's controls
    CHANNEL_CONTROL_ENTITY_REPORTED: str = "fb.exchange.module.entity.reported.channel.control"
    CHANNEL_CONTROL_ENTITY_CREATED: str = "fb.exchange.module.entity.created.channel.control"
    CHANNEL_CONTROL_ENTITY_UPDATED: str = "fb.exchange.module.entity.updated.channel.control"
    CHANNEL_CONTROL_ENTITY_DELETED: str = "fb.exchange.module.entity.deleted.channel.control"

    # Connectors
    CONNECTOR_ENTITY_REPORTED: str = "fb.exchange.module.entity.reported.connector"
    CONNECTOR_ENTITY_CREATED: str = "fb.exchange.module.entity.created.connector"
    CONNECTOR_ENTITY_UPDATED: str = "fb.exchange.module.entity.updated.connector"
    CONNECTOR_ENTITY_DELETED: str = "fb.exchange.module.entity.deleted.connector"

    # Connector's properties
    CONNECTOR_PROPERTY_ENTITY_REPORTED: str = "fb.exchange.module.entity.reported.connector.property"
    CONNECTOR_PROPERTY_ENTITY_CREATED: str = "fb.exchange.module.entity.created.connector.property"
    CONNECTOR_PROPERTY_ENTITY_UPDATED: str = "fb.exchange.module.entity.updated.connector.property"
    CONNECTOR_PROPERTY_ENTITY_DELETED: str = "fb.exchange.module.entity.deleted.connector.property"

    # Connector's control
    CONNECTOR_CONTROL_ENTITY_REPORTED: str = "fb.exchange.module.entity.reported.connector.control"
    CONNECTOR_CONTROL_ENTITY_CREATED: str = "fb.exchange.module.entity.created.connector.control"
    CONNECTOR_CONTROL_ENTITY_UPDATED: str = "fb.exchange.module.entity.updated.connector.control"
    CONNECTOR_CONTROL_ENTITY_DELETED: str = "fb.exchange.module.entity.deleted.connector.control"

    # Triggers
    TRIGGER_ENTITY_REPORTED: str = "fb.exchange.module.entity.reported.trigger"
    TRIGGER_ENTITY_CREATED: str = "fb.exchange.module.entity.created.trigger"
    TRIGGER_ENTITY_UPDATED: str = "fb.exchange.module.entity.updated.trigger"
    TRIGGER_ENTITY_DELETED: str = "fb.exchange.module.entity.deleted.trigger"

    # Trigger's controls
    TRIGGER_CONTROL_ENTITY_REPORTED: str = "fb.exchange.module.entity.reported.trigger.control"
    TRIGGER_CONTROL_ENTITY_CREATED: str = "fb.exchange.module.entity.created.trigger.control"
    TRIGGER_CONTROL_ENTITY_UPDATED: str = "fb.exchange.module.entity.updated.trigger.control"
    TRIGGER_CONTROL_ENTITY_DELETED: str = "fb.exchange.module.entity.deleted.trigger.control"

    # Trigger's actions
    TRIGGER_ACTION_ENTITY_REPORTED: str = "fb.exchange.module.entity.reported.trigger.action"
    TRIGGER_ACTION_ENTITY_CREATED: str = "fb.exchange.module.entity.created.trigger.action"
    TRIGGER_ACTION_ENTITY_UPDATED: str = "fb.exchange.module.entity.updated.trigger.action"
    TRIGGER_ACTION_ENTITY_DELETED: str = "fb.exchange.module.entity.deleted.trigger.action"

    # Trigger's notifications
    TRIGGER_NOTIFICATION_ENTITY_REPORTED: str = "fb.exchange.module.entity.reported.trigger.notification"
    TRIGGER_NOTIFICATION_ENTITY_CREATED: str = "fb.exchange.module.entity.created.trigger.notification"
    TRIGGER_NOTIFICATION_ENTITY_UPDATED: str = "fb.exchange.module.entity.updated.trigger.notification"
    TRIGGER_NOTIFICATION_ENTITY_DELETED: str = "fb.exchange.module.entity.deleted.trigger.notification"

    # Trigger's conditions
    TRIGGER_CONDITION_ENTITY_REPORTED: str = "fb.exchange.module.entity.reported.trigger.condition"
    TRIGGER_CONDITION_ENTITY_CREATED: str = "fb.exchange.module.entity.created.trigger.condition"
    TRIGGER_CONDITION_ENTITY_UPDATED: str = "fb.exchange.module.entity.updated.trigger.condition"
    TRIGGER_CONDITION_ENTITY_DELETED: str = "fb.exchange.module.entity.deleted.trigger.condition"

    # -----------------------------------------------------------------------------

    def __hash__(self) -> int:
        return hash(self._name_)  # pylint: disable=no-member
