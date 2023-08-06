import unittest
import os
import shutil
from configparser import ConfigParser

from gadgethiServerUtils._configs import *
from gadgethiServerUtils.file_basics import *
from gadgethiServerUtils.scripts import generate_configs

class ScriptsTests(unittest.TestCase):
    """
    Testing Strategy:
    - generate_configs
        - partition on config file existence: config file exist, config file not exist
        - partition on credential file existence: credential file exist, credential file not exist
        - partition on database ini file existence: ini file exist, ini file not exist
        - partition on config content: config content partially meets requirement, fully meets requirement
        - partition on ini content: ini content partially meets requirement, fully meets requirement

    """

    # covers generate_configs cases
    def test_generate_configs_file(self):

        # Generate config file
        directory = "config_test"
        file = "config.yaml"
        credentials = "credentials.yaml"
        ini = "db.ini"
        fp = "/".join([directory, file])
        cp = "/".join([directory, credentials])
        ip = "/".join([directory, ini])

        generate_configs.generate_configs(fp, cp, ip)
        config_loc = os.path.abspath(
            os.path.join(default_gserver_location, fp)
        )
        credentials_loc = os.path.abspath(
            os.path.join(default_gserver_location, cp)
        )
        ini_loc = os.path.abspath(
            os.path.join(default_gserver_location, ip)
        )
        self.assertTrue(os.path.isfile(config_loc))
        self.assertTrue(os.path.isfile(credentials_loc))
        self.assertTrue(os.path.isfile(ini_loc))

        config_dict = read_config_yaml(config_loc)
        self.assertTrue(set(GServerConfigs.basic_configs.keys()).issubset(set(config_dict.keys())))
        self.assertTrue(set(GServerConfigs.aws_configs.keys()).issubset(set(config_dict.keys())))

        config = ConfigParser()
        config.read(ini_loc)
        self.assertTrue(config.has_section("gadgethi-database-001")) # assert defaults database

        # Exist case
        generate_configs.generate_configs(fp, cp, ip)

        self.assertTrue(os.path.isfile(config_loc))
        self.assertTrue(os.path.isfile(credentials_loc))
        self.assertTrue(os.path.isfile(ini_loc))

        config_dict = read_config_yaml(config_loc)
        self.assertTrue(set(GServerConfigs.basic_configs.keys()).issubset(set(config_dict.keys())))
        self.assertTrue(set(GServerConfigs.aws_configs.keys()).issubset(set(config_dict.keys())))

        config = ConfigParser()
        config.read(ini_loc)
        self.assertTrue(config.has_section("gadgethi-database-001")) # assert defaults database

        # remove config file
        shutil.rmtree(os.path.abspath(os.path.join(default_gserver_location, directory)))

        # Check no residuals
        self.assertFalse(os.path.isfile(config_loc))
        self.assertFalse(os.path.isfile(credentials_loc))
        self.assertFalse(os.path.isfile(ini_loc))

    def test_config_and_ini_content(self):
        pass


