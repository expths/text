import json

with open("config.json",mode='r')as config_file:
    config = json.load(config_file)

BITGET_API = config["bitget_api"]
postgreSQL = config["postgreSQL"]

if __name__ == "__main__":
    print(config)
