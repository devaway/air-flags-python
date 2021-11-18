from copy import deepcopy

import pytest
from pytest_mock.plugin import MockerFixture

from air_flags.config import AirFlag
from tests.mocks.config import (
    MOCK_CONFIGURATION,
    MOCK_INVALID_FILE,
    MOCK_JSON_FILE,
    MOCK_TYPE_JSON,
    MOCK_TYPE_XML,
    MOCK_TYPE_YAML,
    MOCK_YAML_FILE,
)


def test_config_invalid_type() -> None:
    with pytest.raises(ValueError) as e:
        AirFlag(
            filetype=MOCK_TYPE_XML,
            filepath=MOCK_JSON_FILE,
        )

    assert str(e.value.args[0]) == "The provided config type is not supported"


def test_config_invalid_file() -> None:
    with pytest.raises(ValueError) as e:
        AirFlag(
            filetype=MOCK_TYPE_YAML,
            filepath=MOCK_INVALID_FILE,
        )

    assert str(e.value.args[0]) == "We can't find the provided config file"


def test_config_valid_type_and_file(mocker: MockerFixture) -> None:
    mock_isfile = mocker.patch("os.path.isfile", return_value=True)
    mock_get_config = mocker.patch.object(AirFlag, "_AirFlag__get_config")
    mock_get_config.return_value = deepcopy(MOCK_CONFIGURATION)

    air_flags = AirFlag(
        filetype=MOCK_TYPE_JSON,
        filepath=MOCK_JSON_FILE,
    )

    mock_isfile.assert_called_once()
    mock_get_config.assert_called_once()
    assert air_flags.type == MOCK_TYPE_JSON
    assert air_flags.path == MOCK_JSON_FILE
    assert air_flags.config == MOCK_CONFIGURATION


def test_config_get_config_empty_json(mocker: MockerFixture) -> None:
    mock_valid_type = mocker.patch.object(AirFlag, "_AirFlag__valid_type")
    mock_valid_type.return_value = MOCK_TYPE_JSON
    mock_valid_path = mocker.patch.object(AirFlag, "_AirFlag__valid_path")
    mock_valid_path.return_value = MOCK_JSON_FILE
    mock_open_file = mocker.patch("builtins.open")
    mock_json_loads = mocker.patch("json.loads")
    mock_json_loads.return_value = {}
    mock_yaml_load = mocker.patch("yaml.load")

    with pytest.raises(Exception) as e:
        AirFlag(
            filetype=MOCK_TYPE_JSON,
            filepath=MOCK_JSON_FILE,
        )

    mock_valid_type.assert_called_once()
    mock_valid_path.assert_called_once()
    mock_open_file.assert_called_once()
    mock_json_loads.assert_called_once()
    mock_yaml_load.assert_not_called()
    assert str(e.value.args[0]) == "We can't find any air flag"


def test_config_get_config_empty_yaml(mocker: MockerFixture) -> None:
    mock_valid_type = mocker.patch.object(AirFlag, "_AirFlag__valid_type")
    mock_valid_type.return_value = MOCK_TYPE_YAML
    mock_valid_path = mocker.patch.object(AirFlag, "_AirFlag__valid_path")
    mock_valid_path.return_value = MOCK_YAML_FILE
    mock_open_file = mocker.patch("builtins.open")
    mock_json_loads = mocker.patch("json.loads")
    mock_yaml_load = mocker.patch("yaml.load")
    mock_yaml_load.return_value = {}

    with pytest.raises(Exception) as e:
        AirFlag(
            filetype=MOCK_TYPE_YAML,
            filepath=MOCK_YAML_FILE,
        )

    mock_valid_type.assert_called_once()
    mock_valid_path.assert_called_once()
    mock_open_file.assert_called_once()
    mock_json_loads.assert_not_called()
    mock_yaml_load.assert_called_once()
    assert str(e.value.args[0]) == "We can't find any air flag"


def test_config_get_config_check_attrs(mocker: MockerFixture) -> None:
    mock_valid_type = mocker.patch.object(AirFlag, "_AirFlag__valid_type")
    mock_valid_type.return_value = MOCK_TYPE_JSON
    mock_valid_path = mocker.patch.object(AirFlag, "_AirFlag__valid_path")
    mock_valid_path.return_value = MOCK_JSON_FILE
    mock_open_file = mocker.patch("builtins.open")
    mock_json_loads = mocker.patch("json.loads")
    mock_json_loads.return_value = deepcopy(MOCK_CONFIGURATION)
    mock_yaml_load = mocker.patch("yaml.load")

    flags = AirFlag(
        filetype=MOCK_TYPE_JSON,
        filepath=MOCK_JSON_FILE,
    )

    mock_valid_type.assert_called_once()
    mock_valid_path.assert_called_once()
    mock_open_file.assert_called_once()
    mock_json_loads.assert_called_once()
    mock_yaml_load.assert_not_called()
    assert flags.type == MOCK_TYPE_JSON
    assert flags.path == MOCK_JSON_FILE
    assert flags.config == MOCK_CONFIGURATION
    assert getattr(flags, list(MOCK_CONFIGURATION.keys())[0])

    with pytest.raises(Exception) as e:
        getattr(flags, "invalidAF")

    assert str(e.value.args[0]) == "We can't find the requested flag"