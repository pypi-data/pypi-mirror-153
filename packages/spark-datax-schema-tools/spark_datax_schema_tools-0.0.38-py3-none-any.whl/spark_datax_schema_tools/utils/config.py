def load_config(path_name=None):
    """This method is for load configuration project
    :param path_name: String
    """
    import yaml
    if not path_name:
        raise Exception('require var path_name: {path_name} ')

    with open(path_name, "r") as _file:
        return yaml.load(_file, Loader=yaml.FullLoader)
