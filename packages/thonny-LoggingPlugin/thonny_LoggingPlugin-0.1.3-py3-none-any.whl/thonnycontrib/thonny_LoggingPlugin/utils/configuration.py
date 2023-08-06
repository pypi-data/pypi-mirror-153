import configparser
import os

def read_config(fd):
    """
    read the 'GENERAL' section of the config at localisation fd
    where all the config informations should be stored
    and return the configuration in a dict() object

    Args:
        fd (str): the file directory
    
    Returns:
        :dict:
    """
    config = configparser.ConfigParser()
    res = dict()
    config.read(fd+"/config.INI")
    
    for sec in config.sections() :
        for key in config[sec] :
            res[key] = config[sec][key]

    if len(res) == 0:
        raise FileNotFoundError

    return res

def write_config(dic,fd):
    """
    update the 'GENERAL' section of the config at localisation fd
    where all the config informations should be stored
    The blank field are not changed.
    This function assume that the config file exist in the file directory fd.

    Args:
        dic (obj:'dict'): a dictionnary wich contains some (configKey : value) to update the config
        fd (str): the file directory

    Returns:
        None

    """
    config = configparser.ConfigParser()
    config.read(fd+"/config.INI")

    for key in dic :
        if dic[key] != '':
            config['GENERAL'][key] = dic[key]

    with open(fd+"/config.INI", 'w') as configfile:
        config.write(configfile)
        
def init_config(dic,fd):
    """
    Clean and init the 'GENERAL' section of the config at localisation fd
    where all the config informations should be stored

    Args:
        dic (obj:'dict'): a dictionnary wich contains some (configKey : value) to create the config
        fd (str): the file directory

    Returns:
        None
    """
    config = configparser.ConfigParser()
    config['GENERAL'] = {}
    for key in dic :
        config['GENERAL'][key] = dic[key]

    try :
        configfile = open(fd+"/config.INI", 'w')
    except FileNotFoundError :
        os.mkdir(fd)
        configfile = open(fd+"/config.INI", 'w')
    finally :
        config.write(configfile)
        configfile.close()
