import os
from pathlib import Path
import yaml

from steam_sdk.data.DataModelMagnet import *


def yaml_dump_with_lists(data_model: DataModelMagnet, dump_all_full_path: str):
    '''
    ** Dump a dictionary into a yaml file writing lists of int, str, and np.array horizontally **
    :param data_model:
    :param dump_all_full_path:
    :return:
    '''

    # If the output folder is not an empty string, and it does not exist, make it
    dump_all_path = os.path.dirname(dump_all_full_path)
    if not os.path.isdir(dump_all_path):
        print("Output folder {} does not exist. Making it now".format(dump_all_path))
        Path(dump_all_path).mkdir(parents=True)

    # Convert list entries to string
    print(data_model.GeneralParameters.magnet_inductance.fL_L)
    print(str(data_model.GeneralParameters.magnet_inductance.fL_L))
    print(type(data_model.GeneralParameters.magnet_inductance.fL_L))

    to_write = [str(x) for x in data_model.GeneralParameters.magnet_inductance.fL_L]
    print(to_write)
    to_write = ", ".join([str(i) for i in data_model.GeneralParameters.magnet_inductance.fL_L])
    to_write = '[' + to_write + ']'

    data_model.GeneralParameters.magnet_inductance.fL_L = str(data_model.GeneralParameters.magnet_inductance.fL_L)
    data_model.GeneralParameters.magnet_inductance.fL_L = str(to_write)



    # Transform in a dictionary
    data_dict = data_model.dict()

    # Write to yaml file
    with open(dump_all_full_path, 'w') as outfile:
        yaml.dump(data_dict, outfile, default_flow_style=None, sort_keys=False)
