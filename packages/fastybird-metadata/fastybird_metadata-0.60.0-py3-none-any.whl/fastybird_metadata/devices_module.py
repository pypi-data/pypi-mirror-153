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
Sets of enums for Devices Module
"""

# Python base dependencies
from enum import unique

# Library libs
from fastybird_metadata.enum import ExtendedEnum


@unique
class PropertyType(ExtendedEnum):
    """
    Property entity type

    @package        FastyBird:Metadata!
    @module         devices_module

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    DYNAMIC: str = "dynamic"
    STATIC: str = "static"
    MAPPED: str = "mapped"

    # -----------------------------------------------------------------------------

    def __hash__(self) -> int:
        return hash(self._name_)  # pylint: disable=no-member


@unique
class ConnectionState(ExtendedEnum):
    """
    Device connection state

    @package        FastyBird:Metadata!
    @module         devices_module

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    # Device is connected to gateway
    CONNECTED: str = "connected"
    # Device is disconnected from gateway
    DISCONNECTED: str = "disconnected"
    # Device is in initialization process
    INIT: str = "init"
    # Device is ready to operate
    READY: str = "ready"
    # Device is in operating mode
    RUNNING: str = "running"
    # Device is in sleep mode - support fow low power devices
    SLEEPING: str = "sleeping"
    # Device is not ready for receiving commands
    STOPPED: str = "stopped"
    # Connection with device is lost
    LOST: str = "lost"
    # Device has some error
    ALERT: str = "alert"
    # Device is in unknown state
    UNKNOWN: str = "unknown"

    # -----------------------------------------------------------------------------

    def __hash__(self) -> int:
        return hash(self._name_)  # pylint: disable=no-member


@unique
class DeviceModel(ExtendedEnum):
    """
    Device known models

    @package        FastyBird:Metadata!
    @module         devices_module

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    CUSTOM: str = "custom"

    SONOFF_BASIC: str = "sonoff_basic"
    SONOFF_RF: str = "sonoff_rf"
    SONOFF_TH: str = "sonoff_th"
    SONOFF_SV: str = "sonoff_sv"
    SONOFF_SLAMPHER: str = "sonoff_slampher"
    SONOFF_S20: str = "sonoff_s20"
    SONOFF_TOUCH: str = "sonoff_touch"
    SONOFF_POW: str = "sonoff_pow"
    SONOFF_POW_R2: str = "sonoff_pow_r2"
    SONOFF_DUAL: str = "sonoff_dual"
    SONOFF_DUAL_R2: str = "sonoff_dual_r2"
    SONOFF_4CH: str = "sonoff_4ch"
    SONOFF_4CH_PRO: str = "sonoff_4ch_pro"
    SONOFF_RF_BRIDGE: str = "sonoff_rf_bridge"
    SONOFF_B1: str = "sonoff_b1"
    SONOFF_LED: str = "sonoff_led"
    SONOFF_T1_1CH: str = "sonoff_t1_1ch"
    SONOFF_T1_2CH: str = "sonoff_t1_2ch"
    SONOFF_T1_3CH: str = "sonoff_t1_3ch"
    SONOFF_S31: str = "sonoff_s31"
    SONOFF_SC: str = "sonoff_sc"
    SONOFF_SC_PRO: str = "sonoff_sc_pro"
    SONOFF_PS_15: str = "sonoff_ps_15"

    AI_THINKER_AI_LIGHT: str = "ai_thinker_ai_light"

    FASTYBIRD_WIFI_GW: str = "fastybird_wifi_gw"
    FASTYBIRD_3CH_POWER_STRIP_R1: str = "fastybird_3ch_power_strip_r1"
    FASTYBIRD_8CH_BUTTONS: str = "8ch_buttons"
    FASTYBIRD_16CH_BUTTONS: str = "16ch_buttons"

    # -----------------------------------------------------------------------------

    def __hash__(self) -> int:
        return hash(self._name_)  # pylint: disable=no-member


@unique
class FirmwareManufacturer(ExtendedEnum):
    """
    Device firmware manufacturer

    @package        FastyBird:Metadata!
    @module         devices_module

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    GENERIC: str = "generic"
    FASTYBIRD: str = "fastybird"
    ITEAD = "itead"
    SHELLY: str = "shelly"
    TUYA: str = "tuya"
    SONOFF: str = "sonoff"

    # -----------------------------------------------------------------------------

    def __hash__(self) -> int:
        return hash(self._name_)  # pylint: disable=no-member


@unique
class HardwareManufacturer(ExtendedEnum):
    """
    Device hardware manufacturer

    @package        FastyBird:Metadata!
    @module         devices_module

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    GENERIC = "generic"
    FASTYBIRD = "fastybird"
    ITEAD = "itead"
    AI_THINKER = "ai_thinker"
    SHELLY: str = "shelly"
    TUYA: str = "tuya"
    SONOFF: str = "sonoff"

    # -----------------------------------------------------------------------------

    def __hash__(self) -> int:
        return hash(self._name_)  # pylint: disable=no-member


@unique
class DevicePropertyName(ExtendedEnum):
    """
    Device known property name

    @package        FastyBird:Metadata!
    @module         devices_module

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    STATE: str = "state"
    BATTERY: str = "battery"
    WIFI: str = "wifi"
    SIGNAL: str = "signal"
    RSSI: str = "rssi"
    SSID: str = "ssid"
    VCC: str = "vcc"
    CPU_LOAD: str = "cpu-load"
    UPTIME: str = "uptime"
    IP_ADDRESS: str = "ip-address"
    ADDRESS: str = "address"
    STATUS_LED: str = "status-led"
    FREE_HEAP: str = "free-heap"

    # -----------------------------------------------------------------------------

    def __hash__(self) -> int:
        return hash(self._name_)  # pylint: disable=no-member


@unique
class DeviceAttributeName(ExtendedEnum):
    """
    Device known attribute name

    @package        FastyBird:Metadata!
    @module         devices_module

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    HARDWARE_MANUFACTURER: str = "hardware_manufacturer"
    HARDWARE_MODEL: str = "hardware_model"
    HARDWARE_VERSION: str = "hardware_version"
    HARDWARE_MAC_ADDRESS: str = "hardware_mac_address"
    FIRMWARE_MANUFACTURER: str = "firmware_manufacturer"
    FIRMWARE_NAME: str = "firmware_name"
    FIRMWARE_VERSION: str = "firmware_version"


@unique
class ConnectorPropertyName(ExtendedEnum):
    """
    Connector known property name

    @package        FastyBird:Metadata!
    @module         devices_module

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    STATE: str = "state"
    SERVER: str = "server"
    PORT: str = "port"
    SECURED_PORT: str = "secured_port"
    BAUD_RATE: str = "baud_rate"
    INTERFACE: str = "interface"
    ADDRESS: str = "address"

    # -----------------------------------------------------------------------------

    def __hash__(self) -> int:
        return hash(self._name_)  # pylint: disable=no-member
