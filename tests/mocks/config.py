MOCK_TYPE_JSON = ".json"
MOCK_TYPE_YAML = ".yaml"
MOCK_INVALID_FILE = "invalid.test"
MOCK_JSON_FILE = "test.json"
MOCK_YAML_FILE = "test.yaml"

MOCK_CONFIGURATION = {
    "myAF": {
        "value": True,
        "description": "This is my first Air Flag",
    }
}

MOCK_CONFIG_CANARY_ROLLOUT = {
    "otherAF": {
        "value": True,
        "description": "This is other Air Flag",
        "rollout": {"strategy": "canary", "percentage": 80},
    }
}

MOCK_CONFIG_SCHEDULED_ROLLOUT = {
    "otherAF": {
        "value": True,
        "description": "This is other Air Flag",
        "rollout": {
            "strategy": "scheduled",
            "percentage": 80,
            "start_date": "2021-10-01",
            "end_date": "2021-12-01",
        },
    }
}

MOCK_CONFIG_SCHEDULED_ROLLOUT_EXPIRED = {
    "otherAF": {
        "value": True,
        "description": "This is other Air Flag",
        "rollout": {
            "strategy": "scheduled",
            "percentage": 80,
            "start_date": "2020-10-01",
            "end_date": "2020-12-01",
        },
    }
}

MOCK_CONFIG_PROGRESSIVE_ROLLOUT = {
    "otherAF": {
        "value": True,
        "description": "This is other Air Flag",
        "rollout": {"strategy": "default", "percentage": 80},
    }
}

MOCK_CONFIG_SELECTIVE_TRUE = {
    "otherAF": {
        "value": True,
        "description": "This is other Air Flag",
        "selectived": "abcd-1234",
    }
}

MOCK_CONFIG_SELECTIVE_FALSE = {
    "otherAF": {
        "value": False,
        "description": "This is other Air Flag",
        "selectived": "abcd-1234",
    }
}
