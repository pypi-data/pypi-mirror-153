from __future__ import annotations

import pytest

from aiolookin.protocol import LookInHttpProtocol


@pytest.fixture
def lookin_http_protocol(faker):
    def wrapper(test_client):
        return LookInHttpProtocol(
            session=test_client.session,
            api_uri=str(test_client.make_url("")),
        )

    return wrapper


@pytest.fixture
def get_info_response(faker) -> dict[str, str]:
    yield {
        "Type": "Remote",
        "MRDC": "02000105001K17E3",
        "Status": "Running",
        "ID": "98F33011",
        "Name": "living_room",
        "Time": "1634495587",
        "Timezone": "+3",
        "PowerMode": "5v",
        "CurrentVoltage": "5889",
        "Firmware": "2.38",
        "Temperature": "57",
        "HomeKit": "1",
        "EcoMode": "off",
        "SensorMode": "0",
    }


@pytest.fixture
def get_meteo_sensor_response(faker) -> dict[str, str]:
    yield {
        "Humidity": "38.6",
        "Pressure": "99649.6",
        "Temperature": "24.6",
        "Updated": "1634499757",
    }


@pytest.fixture
def get_devices_response(faker) -> dict[str, str]:
    yield [
        {"Type": "01", "UUID": "49C2", "Updated": "1630089608"},
        {"Type": "03", "UUID": "703A", "Updated": "1631862703"},
        {"Type": "06", "UUID": "AE74", "Updated": "1632039732"},
        {"Type": "07", "UUID": "1234", "Updated": "1632129287"},
        {"Type": "04", "UUID": "1235", "Updated": "1632129287"},
        {"Type": "05", "UUID": "1236", "Updated": "1632129287"},
        {"Type": "EF", "UUID": "460E", "Updated": "1634283385"},
    ]


@pytest.fixture
def get_device_response(faker) -> dict[str, str]:
    yield {
        "Type": "07",
        "Name": "Fan",
        "Updated": "1632129287",
        "Status": "1000",
        "Functions": [
            {"Name": "power", "Type": "single"},
            {"Name": "speed", "Type": "single"},
            {"Name": "swing", "Type": "single"},
        ],
    }


@pytest.fixture
def get_conditioner_response(faker) -> dict[str, str]:
    yield {
        "Type": "EF",
        "Name": "Зал",
        "Updated": "1634283385",
        "Extra": "0001",
        "Status": "3701",
        "LastStatus": "1100",
        "Functions": [],
    }
