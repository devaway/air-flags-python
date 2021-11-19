# Python Air Flags

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