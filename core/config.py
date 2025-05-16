import yaml
import sys
config = {}
def get_config():
    global config
    try:
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
            return config
    except Exception as e:
        print(f"Error loading configuration file{e}")
        sys.exit(1)
    return []
def get(key,default:any=None):
    global config
    if key in config:
        return config[key]
    else:
        print("Key {} not found in configuration".format(key))
        if default is not None:
            return default
    return None

config = get_config()
DEBUG=get("debug",False)
APP_NAME=get("app_name","we-mp-rss")


VERSION='1.2.0'
print(VERSION)