import os
from pathlib import Path

import numpy as np
import yaml

from steam_sdk.builders.BuilderPyBBQ import BuilderPyBBQ
from steam_sdk.data.DataPyBBQ import DataPyBBQ


class ParserPyBBQ:
    """
        Class with methods to read/write PyBBQ information from/to other programs
    """

    def __init__(self, builder_PyBBQ: BuilderPyBBQ = BuilderPyBBQ(flag_build=False)):
        """
            Initialization using a BuilderPyBBQ object containing PyBBQ parameter structure
        """

        self.builder_PyBBQ: BuilderPyBBQ = builder_PyBBQ


    def readFromYaml(self, file_name: str, verbose: bool = True):
        '''
        '''
        # TODO documentation

        # Load yaml keys into DataModelMagnet dataclass
        with open(file_name, "r") as stream:
            dictionary_yaml = yaml.safe_load(stream)
            self.builder_PyBBQ.data_PyBBQ = DataPyBBQ(**dictionary_yaml)
        if verbose: print('File {} was loaded.'.format(file_name))


    def writePyBBQ2yaml(self, full_path_file_name: str, verbose: bool = False):
        '''
        ** Writes a PyBBQ yaml input file **

        :param full_path_file_name:
        :param verbose:
        :return:
        '''

        all_data_dict = {**self.builder_PyBBQ.data_PyBBQ.dict()}

        # If the output folder is not an empty string, and it does not exist, make it
        output_path = os.path.dirname(full_path_file_name)
        if verbose: print('output_path: {}'.format(output_path))
        if output_path != '' and not os.path.isdir(output_path):
            print("Output folder {} does not exist. Making it now".format(output_path))
            Path(output_path).mkdir(parents=True)

        # Write output .yaml file
        with open(full_path_file_name, 'w') as outfile:
            yaml.dump(all_data_dict, outfile, default_flow_style=False, sort_keys=False)


# #######################  Helper functions - START  #######################
# def ComparePyBBQParameters(fileA, fileB, max_relative_error=1E-5, show_indices=0):
#     '''
#         Compare all the variables imported from two PyBBQ Excel input files
#     '''
#
#     Diff = 0
#
#     pp_a = ParserPyBBQ(BuilderPyBBQ(flag_build=False))
#     pp_a.readFromExcel(fileA, verbose=False)
#     pp_b = ParserPyBBQ(BuilderPyBBQ(flag_build=False))
#     pp_b.readFromExcel(fileB, verbose=False)
#     print("Starting Comparison of A: ({}) and B: ({})".format(fileA, fileB))
#
#     ## Check Inputs
#     for attribute in pp_a.builder_PyBBQ.Inputs.__annotations__:
#         Diff = compare_two_parameters(pp_a.builder_PyBBQ.getAttribute("Inputs", attribute),
#                                       pp_b.builder_PyBBQ.getAttribute("Inputs", attribute),
#                                       Diff, attribute, max_relative_error, show_indices)
#
#     if Diff == 0:
#         print("Files {} and {} are equal.".format(fileA, fileB))
#         return True
#     else:
#         return False
# #######################  Helper functions - END  #######################