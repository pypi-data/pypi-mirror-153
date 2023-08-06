import os
import re
import sys
import copy
from configparser import ConfigParser

from gadgethiServerUtils._configs import *
from gadgethiServerUtils.file_basics import *

def write_default_database_ini_entries(ini_cfgmanager, ini_location):
    """
    This is the helper function to help write default database
    ini entries with config parser. 
    * Input:
        - ini_cfgmanager: config parser
        - ini_location: file path to ini location
    """
    # add a new section and some values
    ini_cfgmanager.add_section('gadgethi-database-001')
    ini_cfgmanager.set('gadgethi-database-001', 'host', 'localhost')
    ini_cfgmanager.set('gadgethi-database-001', 'database', 'postgres')
    ini_cfgmanager.set('gadgethi-database-001', 'user', 'postgres')
    ini_cfgmanager.set('gadgethi-database-001', 'password', 'password')
    ini_cfgmanager.set('gadgethi-database-001', 'port', '5432')

    # save to a file
    with open(ini_location, 'w') as configfile:
        ini_cfgmanager.write(configfile)

# Autogenerate Configs
# -------------------------
def generate_configs(filepath, credentials_fp="credentials.yaml", 
    databaseini_fp="database.ini"):
    """
    This is the function to generate default 
    yaml configs and default credentials configs
    * Input
        - filepath: file path to the config file. 
        - credentials_fp: file path to the credential file.
        - databaseini_fp: file path to the database ini file.
    """
    config_loc = os.path.abspath(
        os.path.join(default_gserver_location, filepath)
    )

    credentials_loc = os.path.abspath(
        os.path.join(default_gserver_location, credentials_fp)
    )

    databaseini_loc = os.path.abspath(
        os.path.join(default_gserver_location, databaseini_fp)
    )
    
    # This checks the config file
    if os.path.isfile(config_loc):
        print("Config file existed.. Checking configurations meet reqs..")
        # If configs file existed in directory
        current_cfgs = read_config_yaml(config_loc)
        flag, modified_dict = GServerConfigs.check_current_configs_match_reqs(current_cfgs)

        if not flag:
            print("Requirements don't meet, adding defaults entries")
            write_yaml(config_loc, modified_dict)
    else:
        print("Config file not existed.. Generating default configuations")
        os.makedirs(os.path.dirname(config_loc), exist_ok=True)

        default_configs = copy.deepcopy(GServerConfigs.basic_configs)
        default_configs.update(GServerConfigs.aws_configs)
        write_yaml(config_loc, default_configs)

    # This checks the credential file
    if not os.path.isfile(credentials_loc):
        print("Credentials file not exist.. Initializing Defaults..")
        os.makedirs(os.path.dirname(credentials_loc), exist_ok=True)
        write_yaml(credentials_loc, GServerConfigs.credential_configs)

    # This checks database ini
    if not os.path.isfile(databaseini_loc):
        print("Database Ini file not exist.. Initializing Defaults")
        config = ConfigParser()
        write_default_database_ini_entries(config, databaseini_loc)
    else:
        # instantiate
        config = ConfigParser()

        # parse existing file
        config.read(databaseini_loc)

        if not config.has_section("gadgethi-database-001"):
            print("Adding testing database entry...")
            write_default_database_ini_entries(config, databaseini_loc)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Need config file yaml path. Ex. python3 generate_configs.py config.yaml')
        sys.exit()

    # make sure the arguments meet the regex
    yaml_regex = "^.+\.yaml$"

    if not bool(re.search(yaml_regex, sys.argv[1])):
        print("Args %s is not a yaml file" % sys.argv[1])
        sys.exit(-1)

    generate_configs(sys.argv[1])