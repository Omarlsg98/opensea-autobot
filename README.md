# OpenSea-autobot xd
A bot to extract social media links of the main buyers...
You have to make sure your NFTs are seen by the big fish. 
:p

It also **posts and lists automatically** new NFTs on OpenSea :3
>***Note:** To post you must have an account, and the secret phrase to that account*
##Install
1. You have to download the chromewebdriver that works with your 
    version of chrome and put it in the driver/ folder
   
1. Change INSTALLATION_DIR and DRIVER_PATH with your own values
   ```python
   INSTALLATION_DIR = "C:\\repos\\OpenSea-autobot"
   DRIVER_PATH = f"{INSTALLATION_DIR}/driver/chromedriver.exe"
   ```
1. Install all the requirements with 
   ```bash 
   pip -r requirements.txt
   ```
   
---
##Use
###To post and list NFT
1. Use secret_config.py.template to create secret_config.py. put there 
   your metamask credentials
   ```python
   SECRET_RECOVERY_PHRASE = "lorem ipsulum lorem etc xd here you put the words"
   NEW_PASSWORD = "thoithinkthiscouldbeanyvalue"
   ```
1. Use the data/input/to_post.csv.template to create a to_post.csv 
   with the info of the NFT you want to post and list.
   
1. Execute main.py -m post list
   >**Note:**
   > * You can just post using "-m post" or just list using "-m list"
   > * You can use -b {number of NFTs} if you just want to post that number on NFTs at the moment
1. See the results of the process in output/posted.csv and output/listed.csv
---
###To extract social media 
1. Use the data/input/activities.csv.template to create a activities.csv. 
   Here you must put a list of the activities (opensea URLs with /activity/ in it)
   that you are interested on getting info. Also put a name to the URL, just for your reference.
   
1. change MASTER_CONFIG on congfig.py as you need it:
    ```python
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
    ```
   Probably, you just want to change "first_n_users": the amount of users to check in each activity
1. Run python main.py -m scrap
1. See the results on output/users.csv 
