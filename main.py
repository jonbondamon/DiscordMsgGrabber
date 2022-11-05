import yaml

def main():
    
    with open("settings.yml", mode="r") as yaml_file:
        settings_yaml = yaml.safe_load(yaml_file)

    print(settings_yaml['discord_token'])

if __name__ == "__main__":
    main()