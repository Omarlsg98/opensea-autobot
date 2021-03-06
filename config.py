undetected_chrome = False
user_chrome_dir = "c:/temp/open_sea"
chrome_arguments = ['--start-maximized', "--lang=en"]
und_chrome_arguments = ['--start-maximized',] # "--disable-blink-features=AutomationControlled"  f'--user-data-dir={user_chrome_dir}',
                        #'--no-first-run --no-service-autorun --password-store=basic']


URL = "https://opensea.io"
INSTALLATION_DIR = "C:\\repos\\OpenSea-autobot"
DRIVER_PATH = f"{INSTALLATION_DIR}/driver/chromedriver.exe"

METAMASK_PATH = f"{INSTALLATION_DIR}/driver/10.2.0_0.crx"
METAMASK_ID = "nkbihfbeogaeaoehlefnkodbefgpgknn"

LOGIN_TIMEOUT = 140
TIMEOUT = 30  # in secs
PING = 1  # in secs

MAX_RETRIES = 3
SECS_TO_RE_CLICK = 5

SECS_RANGE_FOR_CLICKS = (0.1, 0.3)
SECS_RANGE_TO_BEHAVE_LIKE_HUMAN = (70, 120)

SECS_BEFORE_CLOSING = 5

MASTER_CONFIG = {
    "from_activity": {
        "enabled": True,
        "extract": {
            "users": {
                "enabled": True,
                "overwrite": False,
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
