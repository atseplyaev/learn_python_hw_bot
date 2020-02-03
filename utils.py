import os
import configparser

def get_param(section, name):
    """
    Возращает значение параметра "name" из секции "section"

    Args:
        section: имя секции
        name: имя параметра

    Returns:
        значение параметра.
    """
    # TODO: Переместить функцию в глобальный файл (utils|tools).py
    path = os.path.expanduser("~/.mpython_conf")
    if not os.path.exists(path):
        print("{} not found".format(path))
        return

    config = configparser.ConfigParser()

    config.read(path)
    value = config.get(section, name)
    return value