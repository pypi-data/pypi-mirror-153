def get_logger(filename):
    """
    :param filename: file.txt
    :return: logger
    """
    import logging

    if not filename:
        raise Exception('require var filename: {file_path.txt} ')

    logging.basicConfig(
        filename=filename,
        format="[%(levelname)s]%(asctime)s:%(name)s:%(message)s",
        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger('main')
    logger.setLevel(logging.INFO)
    return logger
