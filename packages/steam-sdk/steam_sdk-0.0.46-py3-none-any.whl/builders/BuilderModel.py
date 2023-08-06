import os
from pathlib import Path
import yaml
# import json
# import numpy as np

from data.DataModel import *
from data.DataRoxieParser import APIdata
from builders.BuilderLEDET import BuilderLEDET
from builders.BuilderSIGMA import BuilderSIGMA
from parsers.ParserLEDET import ParserLEDET
from parsers.ParserRoxie import ParserRoxie


class BuilderModel:
    """
        Class to generate STEAM models, which can be later on written to input files of supported programs
    """

    def __init__(self, file_model_data: str = None, software: List[str] = None, flag_build: bool = True,
                 flag_dump_all: bool = False, dump_all_path: str = '', output_path: str = '', verbose: bool = True):
        """
            Builder object to generate models from STEAM simulation tools specified by user

            output_path: path to the output models
            dump_all_path: path to the final yaml file
        """

        self.software: List[str] = software
        if not self.software: self.software = []  # This avoids error when None is passed to software # TODO: Verify this is sound coding
        self.file_model_data: str = file_model_data
        self.model_data: DataModel = DataModel()
        self.roxie_data: APIdata = APIdata()

        self.flag_build = flag_build
        self.flag_dump_all: bool = flag_dump_all
        self.dump_all_path: str = dump_all_path  # TODO Merge dump_all_path and output_path ?
        self.output_path: str = output_path
        self.verbose: bool = verbose

        # If flag_build set true, will build right away
        if flag_build:
            # If the output folder is not an empty string, and it does not exist, make it
            if self.output_path != '' and not os.path.isdir(self.output_path):
                print("Output folder {} does not exist. Making it now".format(self.output_path))
                os.mkdir(self.output_path)

            user_name = 'user'  # till GitLab path problem is solved
            for environ_var in ['HOMEPATH', 'SWAN_HOME']:
                if environ_var in os.environ:
                    user_name = os.path.basename(os.path.normpath(os.environ[environ_var]))

            path_sdk = Path(__file__).parent.parent.parent
            path_settings = Path.joinpath(path_sdk, "steam_models", "settings", "user_settings")
            if Path.exists(Path.joinpath(path_settings, f"settings.{user_name}.yaml")):
                with open(Path.joinpath(path_settings, f"settings.{user_name}.yaml"), 'r') as stream:
                    self.settings_dict = yaml.safe_load(stream)
            else:
                with open(Path.joinpath(Path(os.getcwd()).parent, "settings.user.yaml"), 'r') as stream:
                    self.settings_dict = yaml.safe_load(stream)
                # raise Exception('Cannot find paths without settings file')

            self.path_magnet = Path(self.file_model_data).parent

            # Load model data from the input .yaml file
            self.loadModelData()
            self.model_data.Options_LEDET.field_map_files.flag_modify_map2d_ribbon_cable

            # Load model data from the input ROXIE files
            self.loadRoxieData()

            if 'LEDET' in self.software:
                self.buildLEDET()

            if 'SIGMA' in self.software:
                self.buildSIGMA()

            if flag_dump_all:
                self.dumpAll()

    def loadModelData(self):
        """
            Loads model data from yaml file to model data object
        """
        if self.verbose:
            print('Loading .yaml file to model data object.')

        if not self.file_model_data:
            raise Exception('No .yaml path provided.')

        with open(self.file_model_data, "r") as stream:
            dictionary_yaml = yaml.safe_load(stream)
            self.model_data = DataModel(**dictionary_yaml)

    def loadRoxieData(self):
        """
            Apply roxie parser to fetch magnet information for the given magnet and stores in member variable
        """
        if not self.model_data:
            raise Exception('Model data not loaded to object.')

        if self.model_data.Sources.iron_fromROXIE:
            path_iron = Path.joinpath(self.path_magnet, self.model_data.Sources.iron_fromROXIE)
        else:
            path_iron = None
        path_data = Path.joinpath(self.path_magnet, self.model_data.Sources.coil_fromROXIE)
        if self.model_data.Sources.conductor_fromROXIE == '../roxie.cadata':
            path_cadata = Path.joinpath(self.path_magnet.parent, 'roxie.cadata')
        else:
            path_cadata = Path(self.model_data.Sources.conductor_fromROXIE)

        # TODO: add option to set a default path if no path is provided

        #######################################
        # Alternative if provided path is wrong
        if path_iron is not None and not os.path.isfile(path_iron):
            print('Cannot find {}, will attempt to proceed without file'.format(path_iron))
            path_iron = None
        if path_data is not None and not os.path.isfile(path_data):
            print('Cannot find {}, will attempt to proceed without file'.format(path_data))
            path_data = None
        if path_cadata is not None and not os.path.isfile(path_cadata):
            print('Cannot find {}, will attempt to proceed without file'.format(path_cadata))
            path_cadata = None

        ############################################################
        # Load information from ROXIE input files using ROXIE parser
        roxie_parser = ParserRoxie()
        self.roxie_data = roxie_parser.getData(dir_data=path_data, dir_cadata=path_cadata, dir_iron=path_iron)

    def buildLEDET(self):
        """
            Building a LEDET model
        """
        magnet_name = self.model_data.GeneralParameters.magnet_name
        nameFileSMIC = os.path.join(self.output_path,
                                    magnet_name + '_selfMutualInductanceMatrix.csv')  # full path of the .csv file with self-mutual inductances to write
        builder_ledet = BuilderLEDET(path_magnet=self.path_magnet, input_model_data=self.model_data,
                                     input_roxie_data=self.roxie_data, smic_write_path=nameFileSMIC,
                                     flag_build=self.flag_build, verbose=self.verbose)

        parser_ledet = ParserLEDET(builder_ledet)
        nameFileLEDET = os.path.join(self.output_path,
                                     magnet_name + '.xlsx')  # full path of the LEDET input file to write
        parser_ledet.write2Excel(nameFileLEDET=nameFileLEDET, verbose=self.verbose, SkipConsistencyCheck=True)

        # Copy the ROXIE map2d file
        # If the conducor is ribbon cable, then call the method ParserLEDET.copy_modified_map2d_ribbon_cable()
        # Else, , then call the method ParserLEDET.copy_map2d() that simply copies/pastes the existing map2d file adding a suffix
        # if self.model_data.Options_LEDET.field_map_files.flag_modify_map2d_ribbon_cable == 1:
        #     # geoArr to be calculated based on
        #     # [[...half_turn_length, Ribbon...n_strands],.....]
        #      n_strands = number of ribbon conductors in one
        #     parser_ledet.copy_modified_map2d_ribbon_cable(geoArr, verbose=self.verbose)
        # elif self.model_data.Options_LEDET.field_map_files.flag_modify_map2d_ribbon_cable == 0:
        #     parser_ledet.copy_map2d(verbose=self.verbose)

    def buildSIGMA(self):
        """
            Building a SIGMA model
        """
        BuilderSIGMA(input_model_data=self.model_data, input_roxie_data=self.roxie_data,
                     settings_dict=self.settings_dict, output_path=self.output_path,
                     flag_build=self.flag_build, verbose=self.verbose)

    def dumpAll(self):
        """
            Writes model data and data from Roxie parser in a combined .yaml file
        """
        # TODO add one more layer for model_data and roxie_data
        if self.verbose:
            print('Writing model data and data from Roxie parser in a combined .yaml file')
        # TODO: add also data from BuilderLEDET, BulderSIGMA, etc

        all_data_dict = {**self.model_data.dict(), **self.roxie_data.dict()}

        # Define output folder
        if self.dump_all_path != '':
            dump_all_path = self.dump_all_path
        elif self.output_path != '':
            dump_all_path = self.output_path
        else:
            dump_all_path = ''

        # If the output folder is not an empty string, and it does not exist, make it
        if self.dump_all_path != '' and not os.path.isdir(self.dump_all_path):
            print("Output folder {} does not exist. Making it now".format(self.dump_all_path))
            os.mkdir(self.dump_all_path)

        # Write output .yaml file
        dump_all_full_path = os.path.join(dump_all_path, self.model_data.GeneralParameters.magnet_name +
                                          '_all_data.yaml')
        with open(dump_all_full_path, 'w') as outfile:
            yaml.dump(all_data_dict, outfile, default_flow_style=False, sort_keys=False)

#         # Write output .json file
#         magnet_name = self.model_data.GeneralParameters.magnet_name
#         nameFileSMIC = os.path.join(self.output_path,
#                                     magnet_name + '_selfMutualInductanceMatrix.csv')  # full path of the .csv file with self-mutual inductances to write
#         builder_ledet = BuilderLEDET(path_magnet=self.path_magnet, input_model_data=self.model_data,
#                                      input_roxie_data=self.roxie_data, smic_write_path=nameFileSMIC,
#                                      flag_build=self.flag_build, verbose=self.verbose)
#         all_data_dict = {**self.model_data.dict(), **self.roxie_data.dict(),
#                          **builder_ledet.Inputs.__dict__,
#                          **builder_ledet.Options.__dict__,
#                          **builder_ledet.Plots.__dict__,
#                          **builder_ledet.Variables.__dict__}  # to add program-specific variables
#         dump_all_full_path_json = os.path.join(dump_all_path, self.model_data.GeneralParameters.magnet_name + '_all_data.json')
#         with open(dump_all_full_path_json, 'w') as outfile:
#             json.dump(all_data_dict, outfile, cls=NumpyEncoder)
#
# class NumpyEncoder(json.JSONEncoder):
#     '''
#     ** Helper function for dumping np.arrays in json files **
#     '''
#
#     def default(self, obj):
#         if isinstance(obj, np.ndarray):
#             return obj.tolist()
#         return json.JSONEncoder.default(self, obj)

