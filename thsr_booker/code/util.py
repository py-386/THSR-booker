import chromedriver_autoinstaller
import yaml


def inatall_driver():
    chromedriver_autoinstaller.install()


def read_yaml_file(file_name: str) -> dict:
    with open(file_name, "r") as file:
        data = yaml.safe_load(stream=file)
    return data
