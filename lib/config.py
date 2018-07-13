#!/usr/bin/python3

from yaml import load

# Loading the configuration
with open("/etc/zmbackup/zmbackup.yml","r") as fp:
    try:
        config = load(fp)
    except yaml.YAMLError as e:
        print("An error ocurred while trying to load the config files")
        print(e)
