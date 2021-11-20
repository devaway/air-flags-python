# Python Air Flags SDK

[![Run tests](https://github.com/devaway/air-flags-python/actions/workflows/tests.yml/badge.svg)](https://github.com/devaway/air-flags-python/actions/workflows/tests.yml)

> Feature Toggles (often also refered to as Feature Flags) are a powerful technique, allowing teams to modify system behavior without changing code. [Pete Hodgson](https://martinfowler.com/articles/feature-toggles.html)

## Air flag definitions

We allow 2 different type of configuration files for the Air flags definitions:

YAML
```yaml
flag_name:
    value: true
    description: This an amazing Air flag
    expiration_date: 2021-11-19
```
JSON
```json
{
    "flag_name": {
        "value": true,
        "description": "This an amazing Air flag",
        "expiration_date": "2021-11-19"
    }
}
```

| Field | Context | Type | Required |
| ----------- | ----------- | ----------- | ----------- |
| flag_name | The flag_name is the name of the flag | str | Yes |
| value | Status of the flag | bool | Yes |
| description | Short description of the flag | str | No |
| expiration_date | Expiration date of the flag with format 'YYYY-mm-dd' | date / str | No |

## Usage

```python
import air_flags

flags = air_flags.init("/path/to/af_definition.json")

# Used as boolean statement
if flags.flag_name:
    print("Oh yeah!")

# Used as decorator
@flags.is_active("flag_name")
def order_beer():
    pass
```

## Contributing to the SDK

Please refer to [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Licensed under the BSD license, see [LICENSE](LICENSE)
