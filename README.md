# Python Air Flags
Air Flags also known as feature toggle, feature switch, feature flag, feature gate, feature flipper, conditional feature... is used to hide, enable or disable the feature during runtime. For example, during the development process, a developer can enable the feature for testing and disable it for other users

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

| Field | Context | Type | Required |
| ----------- | ----------- | ----------- | ----------- |
| flag_name | The flag_name is the name of the flag | str | Yes |
| value | Status of the flag | bool | Yes |
| description | Short description of the flag | str | Yes |

## Usage

```python
import air_flags

flags = air_flags.init("/path/to/af_definition.json")

# Used as boolean statement
if flags.flag_name:
    print("Oh yeah!")

# Used as decorators
@flags.is_active("flag_name")
def order_beer():
    pass
```
