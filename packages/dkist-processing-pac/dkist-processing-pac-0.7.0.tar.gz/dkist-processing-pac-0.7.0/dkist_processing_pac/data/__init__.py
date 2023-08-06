"""Load constants for use the rest of the package."""
import pkg_resources
import yaml

constants_file = pkg_resources.resource_filename("dkist_processing_pac", "data/constants.yml")
with open(constants_file, "rb") as f:
    CONSTANTS = yaml.safe_load(f)
