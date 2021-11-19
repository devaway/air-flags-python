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
```
JSON
```json
{
    "flag_name": {
        "value": true,
        "description": "This an amazing Air flag"
    }
}
```

## Usage

```python
import air_flags

flags = air_flags.init("/path/to/af_definition.json")


if flags.flag_name:
    print("Oh yeah!")
```

## Contributing to the SDK

Please refer to [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Licensed under the BSD license, see [LICENSE](LICENSE)
