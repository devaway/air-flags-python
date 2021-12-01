# Python Air Flags SDK

[![Run tests](https://github.com/devaway/air-flags-python/actions/workflows/tests.yml/badge.svg)](https://github.com/devaway/air-flags-python/actions/workflows/tests.yml)

> Feature Toggles (often also refered to as Feature Flags) are a powerful technique, allowing teams to modify system behavior without changing code. [Pete Hodgson](https://martinfowler.com/articles/feature-toggles.html)

## Air flag definitions

We allow 2 different type of configuration files for the Air flags definitions:

YAML
```yaml
flag_name:
    value: true
    description: This an amazing Air flag with scheduled rollout
    rollout:
        strategy: scheduled
        percentage: 50
        start_date: 2021-11-01
        end_date: 2021-12-01
other_flag:
    value: true
    description: This is an actived flag
```
JSON
```json
{
    "flag_name": {
        "value": true,
        "description": "This is an amazing Air flag with progressive rollout",
        "rollout": {
            "strategy": "progressive",
            "percentage": 5,
            "start_date": "2021-11-01",
            "end_date": "2021-12-01"
        }
    },
    "other_flag": {
        "value": true,
        "description": "This is other flag with a static rollout percentage",
        "rollout": {
            "strategy": "canary",
            "percentage": 50
        }
    },
    "other_one": {
        "value": false,
        "description": "This is an inactived flag"
    }
}
```
Flag:
| Field | Context | Type | Required |
| ----------- | ----------- | ----------- | ----------- |
| flag_name | The flag_name is the name of the flag | str | Yes |
| value | Status of the flag | bool | Yes |
| description | Short description of the flag | str | No |
| rollout | Custom object to set up | object | No |

Canary rollout:
| Field | Context | Type | Required |
| ----------- | ----------- | ----------- | ----------- |
| strategy | Rollout strategy 'canary' | str | Yes |
| percentage | Percent of traffic to roll the feature out [0 : 100] 'only applies to active flags' | int | Yes |
| start_date | Start date of the flag with format 'YYYY-mm-dd' | date / str | No |
| end_date | Expiration date of the flag with format 'YYYY-mm-dd' | date / str | No |

Scheduled rollout:
| Field | Context | Type | Required |
| ----------- | ----------- | ----------- | ----------- |
| strategy | Rollout strategy 'scheduled' | str | Yes |
| percentage | Percent of traffic to roll the feature out [0 : 100] 'only applies to active flags' | int | No |
| start_date | Start date of the flag with format 'YYYY-mm-dd' | date / str | Yes |
| end_date | Expiration date of the flag with format 'YYYY-mm-dd' | date / str | Yes |

Progressive rollout:
| Field | Context | Type | Required |
| ----------- | ----------- | ----------- | ----------- |
| strategy | Rollout strategy 'progressive' | str | Yes |
| percentage | Percent of traffic to start the rollout, it will increase progressively until 100 at end_date | int | Yes |
| start_date | Start date of the flag with format 'YYYY-mm-dd' | date / str | Yes |
| end_date | Expiration date of the flag with format 'YYYY-mm-dd' | date / str | Yes |

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

## Best practices
Increased technical debt is a common objection to implementing feature flags.
* Standardize naming:
  * Naming your flags to be as much descriptive as possible.
  * Use prefixes to categorize / group them.
  * Include a description with expected the behavior.
* Using `rollout` can generate different value outputs, be careful re-using the same flag in different parts of your application.

## Contributing to the SDK

Please refer to [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Licensed under the BSD license, see [LICENSE](LICENSE)
