HEADLESS = False

URL = "https://opensea.io"
INSTALLATION_DIR = "C:\\repos\\OpenSea-autobot"

TIMEOUT = 30  # in secs
PING = 1  # in secs

MAX_RETRIES = 3
SECS_TO_RE_CLICK = 5

SECS_RANGE_FOR_CLICKS = (0.1, 0.3)
SECS_RANGE_TO_BEHAVE_LIKE_HUMAN = (70, 120)

SECS_BEFORE_CLOSING = 5

MASTER_CONFIG = {
    "from_activity": {
        "enabled": False,
        "extract": {
            "users": {
                "enabled": True,
                "overwrite": True,
                "first_n_users": 1000,
                "from/to": ["To"]
            },
        },
    },
    "from_profile": {
        "enabled": True,
        "extract": {
            "socials": {
                "enabled": True,
                "overwrite": False,
            },
        },
    },
}
