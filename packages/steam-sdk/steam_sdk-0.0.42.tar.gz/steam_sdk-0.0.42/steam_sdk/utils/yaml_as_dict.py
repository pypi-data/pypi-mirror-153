import yaml


def yaml_as_dict(file_name: str):
    """
        Helper function to load a yaml file as a dictionary
    """
    my_dict = {}
    with open(file_name, 'r') as fp:
        docs = yaml.safe_load_all(fp)
        for doc in docs:
            for key, value in doc.items():
                my_dict[key] = value
    return my_dict