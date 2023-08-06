import ruamel.yaml


def data_to_yaml(data_model, name_output_file: str, list_exceptions: list = []):
    """
        Write a data-class object to yaml with pre-set format used across STEAM yaml files.
        In particular:
        - keys order is preserved
        - lists are written in a single row

        :param data_model: Data-class object to write
        :param name_output_file: Name of the yaml file to write
        :param list_exceptions: List of strings defining keys that will not be written in a single row
    """

    #################################################################################################
    # Helper functions
    def my_represent_none(self, data):
        '''
            TODO: Add description
            TODO: Delete argument "data"
        '''
        return self.represent_scalar('tag:yaml.org,2002:null', 'null')

    def flist(x):
        '''
            Define a commented sequence to allow writing a list in a single row
        '''
        retval = ruamel.yaml.comments.CommentedSeq(x)
        retval.fa.set_flow_style()  # fa -> format attribute
        return retval

    def list_single_row_recursively(data_dict: dict, list_exceptions: list = []):
        '''
            Write lists in a single row
            :param data_dict: Dictionary to edit
            :param list_exceptions: List of strings defining keys that will not be written in a single row
            :return:
        '''
        for key, value in data_dict.items():
            if isinstance(value, list) and (not key in list_exceptions):
                data_dict[key] = flist(value)
            elif isinstance(value, dict):
                data_dict[key] = list_single_row_recursively(value, list_exceptions)
        return data_dict
    #################################################################################################


    # Set up ruamel.yaml settings
    ruamel_yaml = ruamel.yaml.YAML()
    ruamel_yaml.width = 268435456  # define the maximum number of characters in each line
    ruamel_yaml.default_flow_style = False
    ruamel_yaml.emitter.alt_null = 'Null'
    ruamel_yaml.representer.add_representer(type(None), my_represent_none)


    # Convert the DataModelMagnet object to a dictionary
    data_dict = data_model.dict()

    # Write lists in a single row
    data_dict = list_single_row_recursively(data_dict, list_exceptions=list_exceptions)

    # Write yaml file
    with open(name_output_file, 'w') as yaml_file:
        ruamel_yaml.dump(data_dict, yaml_file)
