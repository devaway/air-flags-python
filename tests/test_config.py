from copy import deepcopy

import pytest
from pytest_mock.plugin import MockerFixture

import air_flags
from air_flags.config import AirFlag
from air_flags.validators import PathValidator, TypeValidator
from tests.mocks.config import (
    MOCK_CONFIG_SELECTIVE,
    MOCK_CONFIG_SCHEDULED_ROLLOUT_EXPIRED,
    MOCK_CONFIGURATION,
    MOCK_INVALID_FILE,
    MOCK_JSON_FILE,
    MOCK_TYPE_JSON,
    MOCK_TYPE_YAML,
    MOCK_YAML_FILE,
)


def test_config_invalid_type() -> None:
    with pytest.raises(ValueError) as e:
        AirFlag(MOCK_INVALID_FILE)

    assert str(e.value.args[0]) == "The provided config type is not supported"


def test_config_invalid_file() -> None:
    with pytest.raises(ValueError) as e:
        AirFlag(MOCK_JSON_FILE)

    assert str(e.value.args[0]) == "We can't find the provided config file"


def test_config_valid_type_and_file(mocker: MockerFixture) -> None:
    mock_isfile = mocker.patch("os.path.splitext", return_value=["json", ""])
    mock_isfile = mocker.patch("os.path.isfile", return_value=True)
    mock_get_config = mocker.patch.object(AirFlag, "_AirFlag__get_config")
    mock_get_config.return_value = deepcopy(MOCK_CONFIGURATION)

    flags = AirFlag(MOCK_JSON_FILE)

    mock_isfile.assert_called_once()
    mock_get_config.assert_called_once()
    assert flags.type == MOCK_TYPE_JSON
    assert flags.path == MOCK_JSON_FILE
    assert flags.config == MOCK_CONFIGURATION


def test_config_get_config_empty_json(mocker: MockerFixture) -> None:
    mock_valid_type = mocker.patch.object(TypeValidator, "run")
    mock_valid_type.return_value = MOCK_TYPE_JSON
    mock_valid_path = mocker.patch.object(PathValidator, "run")
    mock_valid_path.return_value = MOCK_JSON_FILE
    mock_open_file = mocker.patch("builtins.open")
    mock_json_loads = mocker.patch("json.loads")
    mock_json_loads.return_value = {}
    mock_yaml_load = mocker.patch("yaml.load")

    with pytest.raises(Exception) as e:
        AirFlag(MOCK_JSON_FILE)

    mock_valid_type.assert_called_once()
    mock_valid_path.assert_called_once()
    mock_open_file.assert_called_once()
    mock_json_loads.assert_called_once()
    mock_yaml_load.assert_not_called()
    assert str(e.value.args[0]) == "We can't find any air flag"


def test_config_get_config_empty_yaml(mocker: MockerFixture) -> None:
    mock_valid_type = mocker.patch.object(TypeValidator, "run")
    mock_valid_type.return_value = MOCK_TYPE_YAML
    mock_valid_path = mocker.patch.object(PathValidator, "run")
    mock_valid_path.return_value = MOCK_JSON_FILE
    mock_open_file = mocker.patch("builtins.open")
    mock_json_loads = mocker.patch("json.loads")
    mock_yaml_load = mocker.patch("yaml.load")
    mock_yaml_load.return_value = {}

    with pytest.raises(Exception) as e:
        AirFlag(MOCK_YAML_FILE)

    mock_valid_type.assert_called_once()
    mock_valid_path.assert_called_once()
    mock_open_file.assert_called_once()
    mock_json_loads.assert_not_called()
    mock_yaml_load.assert_called_once()
    assert str(e.value.args[0]) == "We can't find any air flag"


@pytest.mark.freeze_time("2021-11-19")
def test_config_get_config_check_attrs(mocker: MockerFixture) -> None:
    mock_valid_type = mocker.patch.object(TypeValidator, "run")
    mock_valid_type.return_value = MOCK_TYPE_JSON
    mock_valid_path = mocker.patch.object(PathValidator, "run")
    mock_valid_path.return_value = MOCK_JSON_FILE
    mock_open_file = mocker.patch("builtins.open")
    mock_json_loads = mocker.patch("json.loads")
    mock_json_loads.return_value = deepcopy(MOCK_CONFIGURATION)
    mock_yaml_load = mocker.patch("yaml.load")
    mock_val_schema = mocker.patch("jsonschema.validate", return_value=None)

    flags = AirFlag(MOCK_JSON_FILE)

    mock_val_schema.assert_called_once()
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


def test_config_init(mocker: MockerFixture) -> None:
    mock_isfile = mocker.patch("os.path.splitext", return_value=["json", ""])
    mock_isfile = mocker.patch("os.path.isfile", return_value=True)
    mock_get_config = mocker.patch.object(AirFlag, "_AirFlag__get_config")
    mock_get_config.return_value = deepcopy(MOCK_CONFIGURATION)

    flags = air_flags.init(MOCK_JSON_FILE)

    mock_isfile.assert_called_once()
    mock_get_config.assert_called_once()
    assert flags.type == MOCK_TYPE_JSON
    assert flags.path == MOCK_JSON_FILE
    assert flags.config == MOCK_CONFIGURATION


def test_config_is_active_non_existing_flag(mocker: MockerFixture) -> None:
    mocker.patch("os.path.splitext", return_value=["json", ""])
    mocker.patch("os.path.isfile", return_value=True)
    mock_get_config = mocker.patch.object(AirFlag, "_AirFlag__get_config")
    mock_get_config.return_value = deepcopy(MOCK_CONFIGURATION)

    flags = air_flags.init(MOCK_JSON_FILE)

    @flags.is_active("invalidFlag")
    def mock_func():
        pass

    with pytest.raises(Exception) as e:
        mock_func()

    assert str(e.value.args[0]) == "We can't find the requested flag"


@pytest.mark.freeze_time("2021-11-19")
def test_config_is_active_actived_flag(mocker: MockerFixture) -> None:
    mocker.patch.object(TypeValidator, "run").return_value = MOCK_TYPE_JSON
    mocker.patch.object(PathValidator, "run").return_value = MOCK_JSON_FILE
    mocker.patch("builtins.open")
    mocker.patch("json.loads").return_value = deepcopy(MOCK_CONFIGURATION)
    mocker.patch("jsonschema.validate", return_value=None)

    flags = AirFlag(MOCK_JSON_FILE)

    @flags.is_active("myAF")
    def mock_func():
        return "ok"

    assert mock_func() == "ok"


@pytest.mark.freeze_time("2021-11-19")
def test_config_is_active_expired_flag(mocker: MockerFixture) -> None:
    mocker.patch.object(TypeValidator, "run").return_value = MOCK_TYPE_JSON
    mocker.patch.object(PathValidator, "run").return_value = MOCK_JSON_FILE
    mocker.patch("builtins.open")
    mocker.patch("json.loads").return_value = deepcopy(
        MOCK_CONFIG_SCHEDULED_ROLLOUT_EXPIRED
    )
    mocker.patch("jsonschema.validate", return_value=None)

    flags = AirFlag(MOCK_JSON_FILE)

    @flags.is_active("otherAF")
    def mock_func():
        return "ok"

    assert not mock_func()


def test_config_is_active_selective_flag(mocker: MockerFixture) -> None:
    mocker.patch.object(TypeValidator, "run").return_value = MOCK_TYPE_JSON
    mocker.patch.object(PathValidator, "run").return_value = MOCK_JSON_FILE
    mocker.patch("builtins.open")
    mocker.patch("json.loads").return_value = deepcopy(MOCK_CONFIG_SELECTIVE)
    mocker.patch("jsonschema.validate", return_value=None)

    flags = AirFlag(MOCK_JSON_FILE)

    @flags.is_active("otherAF", "abcd-1234")
    def mock_func():
        return "ok"

    assert mock_func() == "ok"


def test_config_is_active_not_selective_flag(mocker: MockerFixture) -> None:
    mocker.patch.object(TypeValidator, "run").return_value = MOCK_TYPE_JSON
    mocker.patch.object(PathValidator, "run").return_value = MOCK_JSON_FILE
    mocker.patch("builtins.open")
    mocker.patch("json.loads").return_value = deepcopy(MOCK_CONFIG_SELECTIVE)
    mocker.patch("jsonschema.validate", return_value=None)

    flags = AirFlag(MOCK_JSON_FILE)

    @flags.is_active("otherAF", "invalid")
    def mock_func():
        return "ok"

    assert not mock_func()
